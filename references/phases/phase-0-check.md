# Phase 0: Dependency Check

**Entry**: User triggers the skill.

**Exit**: All required deps verified (or missing ones noted). → Phase 1.

## Reuse Rule

⛔ **Do NOT re-run the full check if this project has passed Phase 0 in a prior session.**
- Check project memory/CLAUDE.md for recorded toolchain status.
- If all tools were previously verified, skip to Phase 1 with a one-line confirmation.
- Only run individual checks for tools that may have changed (e.g., extension disconnected).

---

## Toolchain

| Dependency | Check command | Used for | Required? |
|-----------|---------------|----------|-----------|
| OpenCLI | `opencli doctor` | Browser search on all sites | **Yes** |
| IDM bridge | `ls idm_bridge.py` in skill dir | Direct link downloads | For IDM mode |
| Baidu client | `ls "D:/APP/BaiduNetdisk/BaiduNetdisk.exe"` | 百度盘 (auto-capture) | For 百度 mode |
| BaiduPCS-Go | `which BaiduPCS-Go` | 百度盘 CLI (fast) | Optional |
| bdpan CLI | `bdpan whoami` | 百度盘 fallback | Deprecated |
| Python | `python --version` or `"/c/Program Files/Python312/python.exe" --version` | idm_bridge.py, wait_download.py, extract_and_clean.py | **Yes** |
| 7z | `ls "/c/Program Files/NVIDIA Corporation/NVIDIA app/7z.exe"` | Archive extraction | Nice to have |

Report what's available. If OpenCLI or Python is missing, stop — everything depends on them. Other missing deps → note which download modes will be unavailable.

## Permissions

Before any download work, ensure these are in `.claude/settings.local.json`:

`Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, `Skill`, `Agent`

If missing, add them with Python.
