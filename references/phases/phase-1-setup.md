# Phase 1: Setup

**Entry**: Phase 0 complete, tools verified.

**Exit**: Save directory confirmed + exists, IDM TempPath corrected, preferences set. → Phase 2.

## Reuse Rule

⛔ **Do NOT re-verify everything if this project was previously configured.**
- If config.json has a valid `save_directory` and the drive exists → confirm with one line, move on.
- If `save_directory` exists in config but the drive/folder is missing → that is the ONLY thing to surface. Don't re-ask preferences, don't re-check TempPath unless the drive changed.
- Only run 1.1-1.4 in full for a brand-new project or when the user asks to change config.

---

## 1.1 Load Config

Read `references/config.json`:

```json
{ "save_directory": "e:\\AllinOne" }
```

Report the current value. Path format: Windows backslash, double-escaped in JSON, no trailing backslash.

## 1.2 Save Directory

Check if `save_directory` exists on disk. This is where ALL downloaded archives live.

```
📦 压缩包存放: g:\压缩文件\  ✅ (已存在)
```

The save directory holds archives ONLY. Extracted game data goes to a separate location (e.g. `g:\CLOCKUP\`). Never extract into the archive directory.

If NOT exists:
1. ⚠️ **HARD STOP — MUST ASK USER before any action.** List available drives with free space.
2. ⛔ **NEVER auto-switch** to a different drive without asking. The user may have the drive temporarily disconnected, or may want to choose a specific alternative.
3. Present options: "创建" if only the folder is missing; "换盘" if the drive letter itself doesn't exist.
4. "创建" → `mkdir -p "<save_directory>"`
5. New path → update config + `mkdir -p`
6. "以后都下到 X" → update config + `mkdir -p`

**Persist vs session override:**
- "这次下到 D:\Temp" → session-only, don't touch config
- "以后都下到 F:\Games" → update config, persists across sessions

## 1.3 IDM TempPath (only if IDM bridge available)

```bash
cmd.exe /c "reg query HKCU\Software\DownloadManager /v TempPath"
```

Must be on same drive as `save_directory`. If wrong drive:

```bash
cmd.exe /c "reg add HKCU\Software\DownloadManager /v TempPath /t REG_SZ /d <drive>:\IDM\Temp\ /f"
mkdir -p "<drive>:/IDM/Temp"
```

## 1.4 Preferences

Ask:
1. **PC or mobile?** (exe / apk / krkr / ons)
2. **Download mode?** Normal / Silent / Silent+Notify (飞书)
