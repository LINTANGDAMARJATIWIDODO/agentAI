"""
NEXUS AI ENTERPRISE — CORE ENGINE 2: FILESYSTEM ENGINE
Modeled after Cursor, Claude Code (View, Edit, Glob, Grep), and Google Antigravity.
Provides structured, safe, surgical file reading, writing, editing, code search, and traversal.
"""

import os
import glob
import re
from typing import Dict, List, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FilesystemEngine:
    """
    High-precision Filesystem engine for autonomous coding agents.
    Supports surgical edits, windowed line reading, fast grep, and glob search.
    """

    def __init__(self, workspace_dir: Optional[str] = None):
        self.workspace_dir = os.path.abspath(workspace_dir or BASE_DIR)

    def _resolve_path(self, relative_path: str) -> str:
        """Resolves relative paths safely within the workspace boundary."""
        clean = relative_path.strip().lstrip("/\\")
        full = os.path.abspath(os.path.join(self.workspace_dir, clean))
        # Enforce workspace boundary
        if not full.startswith(self.workspace_dir):
            raise PermissionError(f"Akses di luar workspace ditolak: {relative_path}")
        return full

    def read_file(
        self,
        path: str,
        start_line: int = 1,
        end_line: Optional[int] = None,
        max_bytes: int = 100000
    ) -> Dict[str, Any]:
        """
        Reads lines from a text file within a specific range.
        """
        try:
            full_path = self._resolve_path(path)
            if not os.path.exists(full_path):
                return {"status": "ERROR", "message": f"File tidak ditemukan: {path}"}
            if os.path.isdir(full_path):
                return {"status": "ERROR", "message": f"Path adalah direktori, bukan berkas: {path}"}

            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()

            total_lines = len(lines)
            s_idx = max(0, start_line - 1)
            e_idx = min(total_lines, end_line) if end_line is not None else total_lines

            selected_lines = lines[s_idx:e_idx]
            content = "".join(selected_lines)

            # Cap byte limit
            if len(content.encode("utf-8")) > max_bytes:
                content = content[:max_bytes] + "\n... [TRUNCATED DUE TO SIZE LIMIT]"

            return {
                "status": "SUCCESS",
                "path": path,
                "total_lines": total_lines,
                "start_line": start_line,
                "end_line": e_idx,
                "lines_returned": len(selected_lines),
                "content": content
            }
        except Exception as e:
            return {"status": "ERROR", "message": str(e), "path": path}

    def write_file(self, path: str, content: str, overwrite: bool = True) -> Dict[str, Any]:
        """
        Creates or overwrites a file, creating parent directories automatically.
        """
        try:
            full_path = self._resolve_path(path)
            if os.path.exists(full_path) and not overwrite:
                return {"status": "ERROR", "message": f"File sudah ada dan overwrite=False: {path}"}

            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

            return {
                "status": "SUCCESS",
                "path": path,
                "bytes_written": len(content.encode("utf-8")),
                "lines_count": len(content.splitlines()),
                "message": f"Berkas berhasil ditulis: {path}"
            }
        except Exception as e:
            return {"status": "ERROR", "message": str(e), "path": path}

    def edit_file(self, path: str, target: str, replacement: str) -> Dict[str, Any]:
        """
        Surgically replaces a specific substring or code block inside an existing file.
        Exact character match required (including whitespace).
        """
        try:
            full_path = self._resolve_path(path)
            if not os.path.exists(full_path):
                return {"status": "ERROR", "message": f"File tidak ditemukan untuk diedit: {path}"}

            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

            if target not in content:
                return {
                    "status": "ERROR",
                    "message": f"Target string tidak ditemukan di dalam {path}. Pastikan spasi dan baris persis sama."
                }

            occurrences = content.count(target)
            new_content = content.replace(target, replacement)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            return {
                "status": "SUCCESS",
                "path": path,
                "replacements_made": occurrences,
                "message": f"Berhasil mengganti {occurrences} kemunculan target di {path}."
            }
        except Exception as e:
            return {"status": "ERROR", "message": str(e), "path": path}

    def list_directory(self, path: str = "", recursive: bool = False, max_depth: int = 2) -> Dict[str, Any]:
        """
        Lists files and subdirectories with sizes and types.
        """
        try:
            full_path = self._resolve_path(path)
            if not os.path.exists(full_path):
                return {"status": "ERROR", "message": f"Direktori tidak ditemukan: {path}"}
            if not os.path.isdir(full_path):
                return {"status": "ERROR", "message": f"Path bukan direktori: {path}"}

            items = []
            if not recursive:
                for entry in os.scandir(full_path):
                    items.append({
                        "name": entry.name,
                        "is_dir": entry.is_dir(),
                        "size": entry.stat().st_size if entry.is_file() else 0,
                        "path": os.path.relpath(entry.path, self.workspace_dir).replace("\\", "/")
                    })
            else:
                for root, dirs, files in os.walk(full_path):
                    # Compute current depth
                    rel_root = os.path.relpath(root, full_path)
                    depth = 0 if rel_root == "." else len(rel_root.split(os.sep))
                    if depth > max_depth:
                        continue
                    for d in dirs:
                        p = os.path.relpath(os.path.join(root, d), self.workspace_dir).replace("\\", "/")
                        items.append({"name": d, "is_dir": True, "size": 0, "path": p})
                    for f_name in files:
                        fp = os.path.join(root, f_name)
                        p = os.path.relpath(fp, self.workspace_dir).replace("\\", "/")
                        items.append({"name": f_name, "is_dir": False, "size": os.path.getsize(fp), "path": p})

            # Sort: directories first, then alphabetically
            items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
            return {"status": "SUCCESS", "base_path": path, "total_items": len(items), "items": items}
        except Exception as e:
            return {"status": "ERROR", "message": str(e), "path": path}

    def glob_search(self, pattern: str, base_path: str = "") -> Dict[str, Any]:
        """
        Searches for files matching a wildcard pattern (e.g. '**/*.py', 'public/**/*.html').
        """
        try:
            full_base = self._resolve_path(base_path)
            search_pattern = os.path.join(full_base, pattern)
            matches = glob.glob(search_pattern, recursive=True)
            rel_matches = [
                os.path.relpath(m, self.workspace_dir).replace("\\", "/")
                for m in matches if os.path.isfile(m)
            ]
            return {
                "status": "SUCCESS",
                "pattern": pattern,
                "total_matches": len(rel_matches),
                "matches": rel_matches[:100]
            }
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def grep_search(
        self,
        query: str,
        base_path: str = "",
        file_pattern: str = "*.*",
        max_results: int = 50
    ) -> Dict[str, Any]:
        """
        Scans files in workspace for occurrences of a search string or regex.
        Returns filename, line number, and line content.
        """
        try:
            full_base = self._resolve_path(base_path)
            results = []
            regex = re.compile(query, re.IGNORECASE)

            for root, _, files in os.walk(full_base):
                # Skip hidden and cache folders relative to workspace
                rel_from_ws = os.path.relpath(root, self.workspace_dir)
                if rel_from_ws != "." and any(part.startswith(".") or part in ["__pycache__", "node_modules"] for part in rel_from_ws.split(os.sep)):
                    continue
                for fname in files:
                    if not glob.fnmatch.fnmatch(fname, file_pattern):
                        continue
                    fpath = os.path.join(root, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                            for idx, line in enumerate(f, start=1):
                                if regex.search(line):
                                    rel_p = os.path.relpath(fpath, self.workspace_dir).replace("\\", "/")
                                    results.append({
                                        "file": rel_p,
                                        "line": idx,
                                        "text": line.strip()[:200]
                                    })
                                    if len(results) >= max_results:
                                        break
                    except Exception:
                        continue
                if len(results) >= max_results:
                    break

            return {
                "status": "SUCCESS",
                "query": query,
                "total_found": len(results),
                "matches": results
            }
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def file_info(self, path: str) -> Dict[str, Any]:
        """
        Retrieves file metadata.
        """
        try:
            full_path = self._resolve_path(path)
            if not os.path.exists(full_path):
                return {"status": "ERROR", "message": f"Berkas tidak ditemukan: {path}"}

            stat = os.stat(full_path)
            is_dir = os.path.isdir(full_path)
            lines_cnt = 0
            if not is_dir and stat.st_size < 5000000:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines_cnt = sum(1 for _ in f)

            return {
                "status": "SUCCESS",
                "path": path,
                "is_dir": is_dir,
                "size_bytes": stat.st_size,
                "line_count": lines_cnt,
                "extension": os.path.splitext(full_path)[1].lower(),
                "last_modified": stat.st_mtime
            }
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}


# Global singleton
filesystem_engine = FilesystemEngine()
