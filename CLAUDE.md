# CLAUDE.md

This file provides guidance to Claude Code when working with this galgame-download skill.

## Overview

This is a Claude Code skill that automates galgame (visual novel) searching and downloading. The skill drives an OpenCLI-controlled browser to search across ~17 galgame download sites, extracts CDN/cloud drive links, and feeds them to IDM (Internet Download Manager) for downloading.

## Architecture

```
User request → SKILL.md Phase 0-6 workflow
  → OpenCLI browser (opencli browser dl <cmd>) for site interaction
  → idm_bridge.py (Python COM bridge) for sending links to IDM
  → wait_download.py (poll file size until complete)
  → extract_and_clean.py (extract, delete archive, clean junk)
```

The skill is NOT a standalone program — it's a workflow executed by Claude using OpenCLI browser commands and Python scripts.

## File Structure & When to Read

```
SKILL.md                         ← READ FIRST. Workflow router (~74 lines). Each phase
                                    points to its detail file in references/phases/.
idm_bridge.py                    ← IDM COM API bridge. Read if modifying download behavior.
references/
  phases/
    phase-0-check.md             ← Toolchain dependency check
    phase-1-setup.md             ← Config, save dir, TempPath, preferences
    phase-2-research.md          ← Game research, name table, series presentation
    phase-3-search.md            ← Search sites, extract links, 3.4 extract, 3.5 verify
    phase-4-download.md          ← IDM/Baidu/other download execution
    phase-5-wait.md              ← 403 check, file size polling
    phase-6-extract.md           ← Extract, organize, clean, password files
  sites.md                       ← Quick reference for all 17 sites.
  sites/mihoyo.md                ← MANDATORY before mihoyo.ink. Ctrl+K, React, CDN, anti-patterns.
  sites/ai2moe.md                ← MANDATORY before ai2.moe. 3-layer flow, browser download (Cloudflare TLS).
  cjk-input.md                   ← CJK input. execCommand('insertText') + String.fromCodePoint().
  cdn.md                         ← shinnku CDN URL patterns and IDM usage.
  passwords.md                   ← Site-wide passwords, lz4 format handling.
  config.json                    ← Persistent save_directory setting.
  wait_download.py               ← Poll file size vs expected until download complete.
  extract_and_clean.py           ← Extract archive, delete on success, clean junk.
  403-forbidden.md               ← Download fails to start → Cloudflare detection, cookie bypass.
```

**Key rule**: SKILL.md Phase 3 directs you to read `references/sites/mihoyo.md` before touching mihoyo.ink. Follow that directive every time — do not rely on memory.

## Critical Rules (learned from real failures)

### CJK Input
- Chinese/Japanese/Korean characters **WILL** corrupt when passed through bash.
- Use `document.execCommand('insertText', false, String.fromCodePoint(...))` inside browser eval.
- Use `String.fromCodePoint()` (hex code points) — they're pure ASCII, never corrupt.
- See `references/cjk-input.md` for the full protocol and code point table.

### State Output
- **NEVER pipe `opencli browser dl state` through `head`/`tail`/`grep -v`**.
- The Ctrl+K search modal on mihoyo.ink renders at the VERY END of DOM output (~line 180+).
- Verify modal is open with: `document.getElementById('search-input') ? 'OPEN' : 'CLOSED'`

### IDM Path
- Use Windows backslash from config: `save_directory` in `references/config.json`. Forward slash produces invalid `g:/\filename`.
- **Preserve original filename from CDN. Do NOT rename files.** The original name contains game title, version, patch type.
- If filename has CJK chars that corrupt through bash → use Python to construct the path and call idm_bridge.py, or download via browser click instead.
- IDM TempPath must be on the same drive as downloads. Check via `reg query HKCU\Software\DownloadManager /v TempPath`.

### Cloudflare / 403
- Cloudflare detects **TLS fingerprint**, not cookies. IDM can't pass → 403 even with cookies.
- For Cloudflare sites (ai2.moe): browser click download → poll completion (30s stable) → cp to save dir.
- Python urllib + full browser headers works as fallback (single-threaded, slower).
- See `references/403-forbidden.md` for full detection and resolution flow.

### No Automation Scripts ⛔
- **NEVER write Python/shell scripts to automate cleanup, deletion, or batch operations.**
- All procedures must be natural language instructions in reference docs.
- Scripts hide failure modes (silent errors, permission issues, partial completions) and cause irreversible damage.
- The only allowed scripts are `idm_bridge.py` (IDM download submission) and `wait_download.py` (poll completion) — these have been battle-tested and do NOT modify/delete files.

### Delete Requires User Permission ⛔
- **NEVER delete archive files (.rar/.7z/.zip) without explicit user confirmation.**
- Deletion is the LAST step: extract → verify completeness (file count, sizes) → organize → THEN ask: "解压完成，确认删除压缩包？"
- If extraction fails or is incomplete: keep archive, report failure.
- If unsure about anything: keep archive, ask user.

### No Silent Rerouting ⛔ (TOP-LEVEL RULE)
- ⛔ **When ANY step fails, hits friction, or the documented procedure doesn't work — STOP and tell the user before changing anything.**
- This covers EVERYTHING: search sites, download sources, CDN, file operations, folder naming, game selection.
- Report: (1) what step failed, (2) what error you got, (3) what options you see.
- Let the user decide the path forward. They know the sites better than you do.
- **Specific examples of what requires user approval BEFORE acting:**
  - Search modal won't open → don't switch to directory browsing
  - One site's CDN is broken → don't silently use another site
  - A game version is missing → don't skip it without asking
  - Moving files between directories → user confirms first
  - Deleting any file → user confirms first
  - Renaming folders → user confirms first
  - ISO/MDF detected → tell user, don't silently leave it
  - Multiple game editions found → ask which to keep
- The procedure docs (mihoyo.md, sites.md, etc.) are the playbook. Follow them exactly. If they don't work, report — don't improvise.

### Workflow
- Phase 3 → Find game → click result → extract CDN + size + password → next game. **Never batch-search then backtrack.**
- Phase 3.5 is a HARD BOUNDARY. Present full summary table → wait for explicit confirmation → then download.
- Do NOT start any download before user confirms.
- Phase 4: Send downloads + track expected_size for each file.
- Phase 5: Poll each file with `wait_download.py` until size >= expected. Run in parallel.
- Phase 6: Extract → check archive structure → extract to `g:\预整理\` → flatten nesting (remove duplicate wrapper folders) → **check for ISO/MDF/nested rars and extract those too** → verify exe exists → place patches → move to `g:\<指定的文件夹名>\` → **ONLY delete archives after user permission**. Archive folder name is the archive's own top-level folder name (Principle 1), never renamed.
- ⛔ **ISO/MDF detection is mandatory.** If after extraction you see .iso/.mdf/.mds files instead of .exe → TELL THE USER immediately. Don't silently leave an unplayable game folder. The archive filename itself often contains `iso+mds` or `mdf+mds` — check BEFORE extracting.
- ⛔ **Recursive extraction required.** If the extracted folder contains more .rar files → extract those too. Repeat until you see actual game files.
- ⛔ **NEVER delete a rar unless the extraction produced >2 top-level items AND total extracted bytes >= 30% of archive size.** If output dir is empty, or has only 1-2 shell items, or extracted data is too small — KEEP the archive and report failure.

### mihoyo.ink Anti-Patterns
- `/@search?keyword=` URL does NOT work. Use Ctrl+K modal only.
- `input.value = "xxx"` does NOT work on React controlled inputs. Use `execCommand('insertText')`.
- Do not browse directories manually — search is always faster on this site.

### Background Process Cleanup ⛔

- `TaskStop` kills the bash wrapper, **NOT** child processes (7z, python, IDM).
- After stopping a background task, always kill orphans:
  ```bash
  cmd.exe /c "taskkill /f /im 7z.exe"     # Kill extraction zombies
  cmd.exe /c "taskkill /f /im python.exe"  # Kill script zombies
  ```
- Zombie processes hold file locks → "Device or resource busy" on mv/rm.
- Never submit long-running extractions as background tasks without a cleanup plan.

### Multi-Agent Browser Strategy (OpenCLI Profiles)

⛔ **Do NOT launch multiple agents sharing one OpenCLI browser.** The browser is a singleton resource — agents will race for the page, causing context corruption and deadlocks.

**The fix: OpenCLI profiles.** Each profile gets its own Chrome instance. Agents can run in parallel if each uses a different profile.

```bash
# Create and bind profiles (one-time setup)
opencli profile create galgame-dl-1
opencli profile create galgame-dl-2
opencli profile create galgame-dl-3

# Each agent uses a different profile
opencli --profile galgame-dl-1 browser dl open "https://mihoyo.ink/"
opencli --profile galgame-dl-2 browser dl open "https://mihoyo.ink/"
opencli --profile galgame-dl-3 browser dl open "https://mihoyo.ink/"
```

**Known issue:** OpenCLI has a Chrome process cleanup bug ([#10299](https://github.com/openclaw/openclaw/issues/10299)) where old processes accumulate. After parallel work, run:
```bash
opencli daemon restart  # Cleans up stale Chrome processes
```

**When to use multi-agent:** Only for independent download tasks (each agent handles one game end-to-end). Do NOT use for tasks that need coordination across agents.

## Key Commands

```bash
# IDM download (run from skill directory)
cd E:/.../skills/galgame-download
python idm_bridge.py "<url>" "<referer>" "<save_dir>\\" "<filename>" --silent

# IDM with cookies (for non-Cloudflare sites that need auth)
python idm_bridge.py "<url>" "<referer>" "<save_dir>\\" "<filename>" --cookie="<cookies>" --silent

# Wait for download to complete
python references/wait_download.py "<save_dir>\\<filename>" "3.5 GB" --interval=30

# Extract, delete archive, clean junk
python references/extract_and_clean.py "<save_dir>\\<filename>" "<output_dir>" --password "<pwd>"

# Cloudflare sites (ai2.moe): browser download + poll + move
# 1. Click 同意并下载 in browser -> downloads to DOWN_DIR
# 2. Poll until file size stable for 30s
# 3. cp "$DOWN_DIR/$f" "<save_dir>/<filename>"

# OpenCLI browser search (run from any directory)
opencli browser dl open "https://mihoyo.ink/"
opencli browser dl keys Control+k
opencli browser dl eval "..."  # Use String.fromCodePoint() for CJK

# Fix IDM temp directory if on wrong drive
cmd.exe /c "reg add HKCU\Software\DownloadManager /v TempPath /t REG_SZ /d G:\IDM\Temp\ /f"
```

## Dependencies

- Windows + Internet Download Manager (IDM)
- **Python 3** + `comtypes` (`pip install comtypes`) — needed for idm_bridge.py, wait_download.py, extract_and_clean.py
- OpenCLI (`npm install -g @jackwener/opencli`) + Chrome extension — browser automation
- BaiduPCS-Go / bdpan (optional, for Baidu cloud downloads)
- 7z — archive extraction (nice to have)

## Modifying the Skill

1. Edit `SKILL.md` or reference files directly
2. No build step — skills are read at runtime by Claude Code
3. Test by triggering the skill with a real download request
4. Keep SKILL.md under ~500 lines; push detailed procedures into `references/`
5. Per-site guides go in `references/sites/<site-name>.md`
