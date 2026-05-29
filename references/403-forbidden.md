# 403 Forbidden — IDM 下载被拒处理指南

当 IDM 提交下载后文件长时间不出现（Phase 5 检查失败），最常见的原因就是 403 Forbidden。

## 检测流程

Phase 4 提交 IDM → 等待 30 秒 → 检查文件：

```bash
ls -la "<save_dir>/<filename>"
```

- 文件存在且大小 > 0 → 正常，进入 Phase 5
- 文件不存在 → 可能 403，按下面流程排查

## 快速排查

### 1. 确认 IDM 是否真的收到了 403

打开 IDM 主窗口，查看下载队列中的状态：
- "已停止" / "错误" → 看详情里的 HTTP 状态码
- 403 → 确认是被服务器拒绝

### 2. 检查是否是 Cloudflare 保护

很多下载站（ai2.moe、部分网盘站）使用 Cloudflare。测试方法：

```bash
"/c/Program Files/Python312/python.exe" -c "
import urllib.request, urllib.error
url = '<download_url>'
try:
    resp = urllib.request.urlopen(url)
    print(f'Status: {resp.status}')
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}')
    body = e.read()[:500]
    if b'cloudflare' in body.lower() or b'challenge' in body.lower():
        print('-> Cloudflare JS Challenge detected!')
    else:
        print(f'Body: {body[:200]}')
"
```

如果输出 `Cloudflare JS Challenge detected!` → 进入「Cloudflare 解决方案」。

### 3. 其他常见 403 原因

| 原因 | 症状 | 解决 |
|------|------|------|
| Referer 缺失 | 403 但浏览器能下 | 确认 `idm_bridge.py` 传了正确的 Referer |
| Cookie/登录态 | 需登录的站点 | OpenCLI 浏览器先登录，提取 cookie |
| 链接过期 | 临时令牌超时 | 重新进入详情页获取新链接 |
| User-Agent 被拒 | IDM 默认 UA 被挡 | 用 `idm_bridge.py` 的 `--cookie=` 传浏览器 cookie |

## Cloudflare 解决方案

Cloudflare JS Challenge 检测 **TLS 指纹**（非 cookie）。浏览器 TLS 指纹合法 → 通过；IDM TLS 指纹不同 → 403。

### 策略 1：浏览器点击 + IDM 扩展捕获（主力）

1. 在 OpenCLI 浏览器中触发下载（点击下载按钮）
2. IDM 浏览器扩展自动拦截下载请求
3. 通过浏览器网络栈（Cloudflare 认可 TLS 指纹）→ IDM 满速下载
4. 下载完成后 `cp` 到目标目录

### 策略 2：Python 直接下载（备选，较慢）

用 Python urllib + 完整浏览器头。能过 Cloudflare（urllib TLS 库 + 头伪装得像 Chrome）但单线程：

```python
import urllib.request
url = "<download_url>"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': '<referer_url>',
    'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin',
}
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req)
with open('<save_dir>/<filename>', 'wb') as f:
    f.write(resp.read())
```

### 为什么 IDM 直接下载不行

Cloudflare 检测 TLS 握手指纹（JA3 指纹）。Chrome 和 IDM 的 TLS 库不同，指纹不同。即使传了浏览器 cookie，Cloudflare 也不认可——它看的是 TLS 层，不是应用层。

### 站点特殊说明

- **ai2.moe**：已验证。详情 → `references/sites/ai2moe.md`

## Python 兜底下载

如果 IDM + cookie 也失败，用 Python urllib + 完整浏览器头直接下载：

```python
import urllib.request
url = "<download_url>"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': '<referer_url>',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
}
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req)
with open('<save_dir>/<filename>', 'wb') as f:
    f.write(resp.read())
```

## 浏览器兜底下载

最后手段：在 OpenCLI 浏览器中直接触发下载，然后移动到目标目录：

```bash
mv "/c/Users/adminn/Downloads/<filename>" "<save_dir>/<filename>"
```
