import os
import json
import re

BASE_DIR = r"C:\Users\LENOVO\.gemini\antigravity\scratch\NEXUS-AI-ENTERPRISE"
skills_dir = os.path.join(BASE_DIR, ".agents", "skills")

skills_list = []
for entry in sorted(os.listdir(skills_dir)):
    skill_path = os.path.join(skills_dir, entry)
    if os.path.isdir(skill_path):
        md_file = os.path.join(skill_path, "SKILL.md")
        desc = ""
        name = entry
        if os.path.exists(md_file):
            try:
                with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
                    txt = f.read(1500)
                m = re.search(r'^---\s*\n(.*?)\n---', txt, re.DOTALL)
                if m:
                    front = m.group(1)
                    m_name = re.search(r'name:\s*["\']?([^"\'\n]+)', front)
                    if m_name:
                        name = m_name.group(1).strip()
                    m_desc = re.search(r'description:\s*["\']?([^"\'\n]+)', front)
                    if m_desc:
                        desc = m_desc.group(1).strip()
            except Exception as e:
                pass
        
        # Categorize
        cat = "Engineering & Development"
        if any(w in entry for w in ["finance", "fraud", "procurement"]):
            cat = "Finance & Risk"
        elif any(w in entry for w in ["cyber", "security", "guardian"]):
            cat = "Cybersecurity & Governance"
        elif any(w in entry for w in ["market", "growth", "brand", "seo"]):
            cat = "Marketing & Growth"
        elif any(w in entry for w in ["data", "etl", "mlops"]):
            cat = "Data & AI"
        elif any(w in entry for w in ["strategic", "decision", "corporate", "agile", "project"]):
            cat = "Executive & Strategy"
        elif any(w in entry for w in ["qa", "test", "debug"]):
            cat = "Quality Assurance"

        skills_list.append({
            "id": entry,
            "name": name,
            "description": desc or f"Enterprise skill for {name}",
            "category": cat,
            "assigned_agents": ["RAKA", "ARKA"] if "fullstack" in entry else ["ARKA"]
        })

output_data = {
    "total_skills": len(skills_list),
    "skills": skills_list
}

out_file = os.path.join(BASE_DIR, "config", "skills_registry.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"Generated {out_file} with {len(skills_list)} skills successfully!")
