# Phase 6: Extract & Organize

**Entry**: Phase 5 complete, all files on disk.

**Exit**: Archives extracted, junk cleaned, password files created. Done.

---

## 6.1 Determine Output Directory

```
Single game:  <save_dir>/
Series:       <save_dir>/ENGLISH_SERIES_NAME/
```

- Archive internal folder name preserved as-is
- Series name: ASCII only (e.g. "Taimanin", "Amakano")
- Unsure if series → ask: "这是系列吗？如果是，用哪个英文名？"

## 6.2 Extract

```bash
cd <skill_dir>
python references/extract_and_clean.py "<save_dir>\\<filename>" "<output_dir>" --password "<pwd>"
```

- `--password` only if archive has one (from Phase 3)
- `--keep` to skip deletion (default: deletes archive on success)
- Handles: .7z, .rar, .zip, .lz4, .tar.gz, multipart (.7z.001)
- On success: deletes archive, cleans junk (.url, 广告, Thumbs.db, __MACOSX)
- On failure: keeps archive, reports error

## 6.3 Password File

If archive had a password, create `_password.txt` in extracted game folder:

```bash
python -c "text=chr(0x6587)+chr(0x4ef6)+chr(0x540d)+': <ascii_filename>\n'+chr(0x89e3)+chr(0x538b)+chr(0x5bc6)+chr(0x7801)+': <password>\n'+chr(0x4e0b)+chr(0x8f7d)+chr(0x6765)+chr(0x6e90)+': <site>';open('<output_dir>/<ascii_basename>_password.txt','w',encoding='utf-8').write(text)"
```

chr() values: 文件名 = 0x6587+0x4ef6+0x540d, 解压密码 = 0x89e3+0x538b+0x5bc6+0x7801, 下载来源 = 0x4e0b+0x8f7d+0x6765+0x6e90.

⚠️ Filename must be ASCII. Content is Chinese via chr(), never through bash.

## 6.4 Report

```
📦 解压完成
| # | 作品 | 解压到 | 大小 | 状态 |
|---|------|--------|------|------|
| 1 | XXX | g:\XXX_汉化版 | 3.5 GB | ✅ |
```

## Example: Series

"对魔忍全系列" → `g:\Taimanin\`:

```
g:\Taimanin\
├── 対魔忍アサギ_完全版\
├── 対魔忍アサギ2_謀略の奴隷\
└── 対魔忍ユキカゼ\
```
