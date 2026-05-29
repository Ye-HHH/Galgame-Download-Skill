# Phase 4: Execute Download

**Entry**: Phase 3.5 confirmed. All games identified with download links, sizes, passwords.

**Exit**: All downloads submitted to IDM / Baidu. Queue reported. → Phase 5.

---

Track for each download: `filename`, `save_dir`, `expected_size`, `password` (if any).

## Mode A: IDM 直链 (shinnku, galzy, inarigal, mihoyo)

```bash
cd <skill_dir>
python idm_bridge.py "<url>" "<referer>" "<save_dir>\\" "<ascii_filename>" --silent
```

For ai2.moe: add `--cookie="<cookies>"` (see `references/sites/ai2moe.md`).

For shinnku: must visit detail page to get real CDN URL. See `references/cdn.md`.

## Mode B: 百度网盘

Try in order:

1. **OpenCLI browser** (most reliable):
   ```bash
   opencli browser dl open "https://pan.baidu.com/s/1xxxxx?pwd=abcd"
   ```
   Baidu client at `D:/APP/BaiduNetdisk/BaiduNetdisk.exe` auto-launches.

2. **BaiduPCS-Go** (fast, multi-threaded):
   ```bash
   BaiduPCS-Go transfer <share_link> -p <password>
   BaiduPCS-Go download <remote_path> <local_path>
   ```

3. **bdpan** (deprecated): `bdpan download ...` — error -7 = API rate limit, switch to #1.

## Mode C: Other disks (夸克/和彩云/阿里)

Show links to user. Suggest switching to shinnku/galzy. No auto-extract.

## Download Queue

After all sent, present:

```
📥 下载队列
| # | 作品 | 文件名 | 预期大小 | 状态 |
|---|------|--------|----------|------|
| 1 | XXX | FILE.rar | 3.5 GB | ⏳ 下载中 |
```

Then proceed to Phase 5 immediately — don't wait for user.
