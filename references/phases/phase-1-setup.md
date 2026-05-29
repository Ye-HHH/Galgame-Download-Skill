# Phase 1: Setup

**Entry**: Phase 0 complete, tools verified.

**Exit**: Save directory confirmed + exists, IDM TempPath corrected, preferences set. → Phase 2.

---

## 1.1 Load Config

Read `references/config.json`:

```json
{ "save_directory": "e:\\AllinOne" }
```

Report the current value. Path format: Windows backslash, double-escaped in JSON, no trailing backslash.

## 1.2 Save Directory

Check if `save_directory` exists on disk. Report:

```
💾 保存路径: g:\  ✅ (已存在)
```

If NOT exists:
1. ⚠️ `"下载目录 X 不存在，需要创建或换个目录？"`
2. "创建" → `mkdir -p "<save_directory>"`
3. New path → update config + `mkdir -p`
4. "以后都下到 X" → update config + `mkdir -p`

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
