# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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
- Filenames: ASCII ONLY. CJK chars corrupt in bash → garbled filenames like `LAMUNATION锛�.7z`.
- IDM TempPath must be on the same drive as downloads. Check via `reg query HKCU\Software\DownloadManager /v TempPath`.

### Cloudflare / 403
- Cloudflare detects **TLS fingerprint**, not cookies. IDM can't pass → 403 even with cookies.
- For Cloudflare sites (ai2.moe): browser click download → poll completion (30s stable) → cp to save dir.
- Python urllib + full browser headers works as fallback (single-threaded, slower).
- See `references/403-forbidden.md` for full detection and resolution flow.

### Workflow
- Phase 3 → Find game → click result → extract CDN + size + password → next game. **Never batch-search then backtrack.**
- Phase 3.5 is a HARD BOUNDARY. Present full summary table → wait for explicit confirmation → then download.
- Do NOT start any download before user confirms.
- Phase 4: Send downloads + track expected_size for each file.
- Phase 5: Poll each file with `wait_download.py` until size >= expected. Run in parallel.
- Phase 6: Extract → delete archive → clean junk → password file. Single game in save root, series in `SERIES_NAME/`.

### mihoyo.ink Anti-Patterns
- `/@search?keyword=` URL does NOT work. Use Ctrl+K modal only.
- `input.value = "xxx"` does NOT work on React controlled inputs. Use `execCommand('insertText')`.
- Do not browse directories manually — search is always faster on this site.

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
