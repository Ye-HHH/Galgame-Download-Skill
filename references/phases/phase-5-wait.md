# Phase 5: Wait & Complete

**Entry**: Phase 4 submitted all downloads.

**Exit**: All files on disk, sizes verified. → Phase 6.

---

## 5.0 Quick Check — Did Download Start?

30 seconds after IDM submit, check:

```bash
ls -la "<save_dir>/<filename>"
```

- File exists + size > 0 → download started, proceed to 5.1
- File does NOT exist → IDM 说 OK 但文件没出现 = 403 Forbidden。**→ Read `references/403-forbidden.md`，按流程修复后回到 Phase 4 重发**

## 5.0.5 Active Re-Check ⛔

**Do NOT rely on memory or notifications to check if downloads finished.** While doing other work (Phase 6 extraction, searching for other games), periodically re-check the download directory:

```bash
ls -lh "g:/压缩文件/"
```

- If a file's size matches expected → it's done, proceed to Phase 6 for that game
- If the file appeared but is still growing → still downloading, check again later
- **Never assume a file "will finish eventually" and forget about it.** A finished download sitting idle wastes time.

## 5.1 Poll for Completion

```bash
cd <skill_dir>
python references/wait_download.py "<save_dir>\\<filename>" "<expected_size>" --interval=30 --timeout=7200
```

- `expected_size`: bytes or human-readable ("3.5 GB")
- Polls every 30s, 2 hour timeout
- Exit 0 = done, exit 1 = timeout

Run multiple instances in parallel via `run_in_background`. When done → ✅, on timeout → ⚠️ tell user.
