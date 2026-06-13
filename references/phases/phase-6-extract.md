# Phase 6: Extract & Organize

**Entry**: Phase 5 complete, all files on disk.

**Exit**: Archives extracted and organized, game folders ready to play. Done.

---

## 6.1 Three Directories — Never Mix Them

```
g:\压缩文件\           ← downloaded .rar/.7z files (from IDM)
g:\预整理\             ← temp workspace: extract here, flatten nesting, clean up
g:\<指定的文件夹名>\           ← final output, organized by game company (from Phase 2)
```

`<指定的文件夹名>` is whatever the user requested during Phase 2. Examples: `CLOCKUP` (by developer), `Taimanin` (by series), `2024年下载` (by year).

## 6.2 Three Principles — Never Violate Them

### Principle 1: Respect the Archive's Top-Level Folder Name ⛔

The archive creator named the root folder for a reason. **Use it exactly as-is.**

- If `7z l` shows all files inside `[CLOCKUP] euphoria HD 乐园高清版[萌你妹汉化组]/` → that IS the folder name
- Do NOT rename to `euphoria`, do NOT strip `[CLOCKUP]`, do NOT "clean it up"
- The folder name under `g:\CLOCKUP\` will be: `[CLOCKUP] euphoria HD 乐园高清版汉化硬盘版[萌你妹汉化组]`

### Principle 2: No Top-Level Folder → Create One

If `7z l` shows scattered files with NO common parent folder (e.g. `setup.exe` and `data/` directly at archive root):
- Create a folder named after the archive file itself (without .rar extension)
- Extract into that folder
- This is the ONLY time you create a folder name

### Principle 3: Flatten Everything — Shortest Path to Game Files ⛔

After extraction, the game files must be as close to the root folder as possible.

- ❌ `EUPHORIA HD/EUPHORIA HD/乐园/` → 3 levels of nothing
- ✅ Move game files up, delete empty intermediate folders
- ❌ `game/`, `extracted/` subfolders you created → delete them, move contents up
- Goal: the .exe should be directly inside the archive's root folder (or at most 1 level deep)

**Multi-edition archives:** If the game contains multiple versions (e.g. `18/` + `全年龄/`, or `JP/` + `CN/`):
1. Stop and tell the user: "这个游戏有多个版本，你要哪个？"
2. Delete the rejected version(s)
3. **After deletion, check again: does the remaining version still have a nested subfolder (like `18/SACRIFICE VILLAINS_R18/`)?** If so, flatten it — move contents up, delete the now-unnecessary edition wrapper

**After every cleanup action, re-check: can I flatten more?**

---

## 6.3 Workflow (executed in `g:\预整理\`)

### Step 1: Check archive structure

```bash
"/c/Program Files/NVIDIA Corporation/NVIDIA app/7z.exe" l "g:\压缩文件\<archive>" -p"<password>"
```
- Has a single root folder? → extract directly to `g:\预整理\`
- No root folder? → `mkdir "g:\预整理\<archive_basename>"` then extract into it

### Step 2: Extract to 预整理

```bash
"/c/Program Files/NVIDIA Corporation/NVIDIA app/7z.exe" x "g:\压缩文件\<archive>" -o"g:\预整理" -p"<password>" -y
```

### Step 3: Flatten nesting recursively

- If you see `<RootFolder>/<SameNameAgain>/` → move inner contents up, delete duplicate
- If you see `<RootFolder>/game/` or `<RootFolder>/extracted/` → move contents up, delete
- Keep doing this until the .exe is reachable at `<RootFolder>/` or `<RootFolder>/one_subdir/`

### Step 4: Check for nested archives / ISO / Patch

- .rar/.7z inside → go back to Step 1 for each
- .iso/.mdf/.mds → tell user, ask whether to extract with 7z or mount
- Patch archives (.7z/.rar) → extract to temp, read documentation, follow instructions
- ⛔ **NEVER batch-delete all .rar files.** Some are patches that need extraction. Check each one individually.

### Step 4.5: Apply Patches

If translation patches exist alongside the game:
1. Extract the patch archive to a temp folder (e.g. `g:\预整理\patch_temp\`)
2. Patches are often double-wrapped (.7z containing .rar) — unpack all layers
3. Look for readme documents (`.txt`, `readme*`)
4. **Follow the patch author's instructions** — typically copy/overwrite files into the game folder
5. Remove temp folder when done

### Step 5: Verify

Game .exe reachable at reasonable depth. Reasonable file count and size.

### Step 6: Present to User for Approval ⛔

**STOP HERE. Do NOT move anything to `<指定的文件夹名>` yet.**

Show the user what you have:
```
📦 预整理完成，请确认后移动：
g:\预整理\[CLOCKUP] euphoria HD 乐园高清版[萌你妹汉化组]\
  ├── EUPHORIA HD/
  │   ├── euphoriaHD.exe
  │   ├── data/
  │   └── ...
  └── patch/
```
Wait for explicit confirmation before proceeding.

### Step 7: Move to target (ONLY after user confirms)

```bash
mv "g:\预整理\<RootFolder>" "g:\<指定的文件夹名>\"
```

### Step 7: Delete archive (user permission ONLY)

Ask user before deleting anything from `g:\压缩文件\`.

---

## 6.3 Delete Archives — Last Step, User Permission Required

⛔ **NEVER delete any archive file until:**
1. All extractions (including nested rars and ISO) are complete
2. You've verified the game has proper files (exes, data folders)
3. You've ASKED the user and received explicit confirmation

```
"以下压缩包已解压完成并验证，可以删除吗？
 - euphoria HD cn.rar (3.1GB)
 - Erewhon cn.rar (3.3GB)"
```

**Auto-deletion is FORBIDDEN. No exceptions.**

---

## 6.4 Common Problems and How to Handle Them

| Problem | Cause | Fix |
|---------|-------|-----|
| Files scattered in save_dir root | Archive had no root folder, extracted to parent dir | Move files into a game folder, delete from root |
| `GameName/GameName/GameName/` | Multiple wrapper folders | Flatten: move contents up, delete wrappers |
| Only 1-3 files after extraction | Archive was ISO/MDF, needs further extraction | Extract the ISO with 7z |
| `failed get parent list` on mihoyo | Alist deep path bug | Use galgamedownload.date CDN instead |
| CJK filenames show as garbled in bash | Git Bash GBK encoding | Python os.listdir() to see real names |

---

## 6.5 Report

When all done:

```
📦 解压完成
| # | 作品 | 路径 | 大小 | 状态 |
|---|------|------|------|------|
| 1 | euphoria | g:\CLOCKUP\[CLOCKUP] euphoria HD... | 6.56 GB | ✅ |
| 2 | Erewhon | g:\CLOCKUP\[CLOCKUP] Erewhon... | 4.64 GB | ✅ |
```
