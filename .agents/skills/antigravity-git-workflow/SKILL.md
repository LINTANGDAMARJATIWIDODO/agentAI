---
name: antigravity-git-workflow
description: Enforce Conventional Commits specification, semantic versioning (SemVer), feature branch naming conventions, and pull request hygiene in Antigravity agent workspaces. Use when committing code or managing git branches.
---

# SKILL: Antigravity Git Workflow & Release Engineering

> **Origin Repository:** https://github.com/LichAmnesia/awesome-antigravity-skills  
> **Source License:** CC0 1.0 Universal (Public Domain)  
> **Attribution:** Adapted from `awesome-antigravity-skills` (LichAmnesia) standard developer templates.  
> **Target Owner:** Shared (All Agents: ARKA, NAYA, RAKA, SEKAR, DIMAS)

---

## 1. PURPOSE & OBJECTIVE
To guarantee an immaculate, automated, and traceable version control history across all multi-agent codebases, documentation, and configuration files using Conventional Commits and Semantic Versioning.

## 2. SCOPE
- Git branch naming (`feature/`, `bugfix/`, `chore/`, `docs/`), commit message anatomy, pull request templates, and semantic tagging (`v1.0.0`).

## 3. CONVENTIONAL COMMITS SPECIFICATION
Commit messages must follow the standard structure:
```
<type>(<optional-scope>): <imperative-description>

[optional body explaining motivation and trade-offs]

[optional footer(s) e.g. Closes #123, BREAKING CHANGE: ...]
```

### Approved Commit Types:
- `feat`: A new feature or capability.
- `fix`: A bug fix or patch.
- `docs`: Documentation changes only.
- `style`: Formatting, missing semicolons, no code change.
- `refactor`: Code restructuring without bug fix or feature addition.
- `perf`: Code change that improves performance.
- `test`: Adding missing tests or correcting existing tests.
- `chore`: Build process, dependencies, auxiliary tooling updates.

## 4. BRANCHING STRATEGY (TRUNK-BASED / SHORT-LIVED FEATURE BRANCHES)
- `main`: Always deployable production-grade state.
- `feature/<agent>-<short-description>`: Bounded branch for agent development (e.g. `feature/raka-api-gateway`).
- Clean squashed merge commits to keep the main branch history readable.

## 5. QUALITY STANDARDS & ACCEPTANCE CRITERIA
- Commit messages must be in the present imperative tense ("add feature", not "added feature").
- Never bundle unrelated changes into a single monolithic commit.

## 6. CONSTRAINTS
- Never force push (`git push -f`) to protected branches (`main`, `master`, `release/*`).
- Never commit binary artifacts, build caches, or credentials.
