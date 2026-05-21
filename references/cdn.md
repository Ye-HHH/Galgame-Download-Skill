# shinnku CDN & IDM Download

## CDN Architecture

**生肉和熟肉使用不同的 CDN — 不要猜 URL，必须从详情页提取！**

| Category | File Path Pattern | CDN Domain |
|----------|------------------|------------|
| 熟肉（新win） | `/files/shinnku/zd/XXX.rar` | `https://zd.shinnku.top/file/shinnku/zd/...` |
| 熟肉（前win） | `/files/shinnku/0/win/XXX.7z` | `https://zd.shinnku.top/file/shinnku/0/win/...` |
| 生肉（合集） | `/files/galgame0/...` | `https://galgamedownload.date/合集系列/浮士德galgame游戏合集/...` |

## Getting the Real CDN URL

1. Navigate to file detail page: `https://www.shinnku.com/files/shinnku/zd/...`
2. Extract the URL from the "点击此处下载" link
3. Use `browser_evaluate` to get the href:
   ```js
   () => document.querySelector('a[href*="shinnku.top"], a[href*="galgamedownload"]').href
   ```
4. Referer is always `https://www.shinnku.com/`

## IDM Bridge Usage

**Never use `idman /d` CLI** — it cannot pass Referer headers.

The bridge script: `idm_bridge.py`

```bash
# Normal (shows IDM window)
python idm_bridge.py "<url>" "<referer>" "<save_path>" "<filename>"

# Silent (background)
python idm_bridge.py "<url>" "<referer>" "<save_path>" "<filename>" --silent
```

## inarigal.com Direct Links

inarigal uses API-backed downloads with time-limited authorization tokens:
1. Click "下载资源" → site shows countdown → download triggered
2. Capture real URL from `browser_network_requests`
3. URL pattern: `https://annnnnnn.soraflie.top/upfiles/...?Authorization=...`
4. Token expires quickly — call IDM immediately
5. Referer: `https://inarigal.com/`
