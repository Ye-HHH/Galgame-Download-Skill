# ai2.moe — 御爱同萌 AI 去码补丁站

站点类型：**IPS 论坛 + 文件下载系统**，无需登录即可下载。

## 搜索

ai2.moe 的 AI 无码补丁集中在分类页：
- `https://www.ai2.moe/files/category/12-全游戏无码化计划（ai去码）/`

直接浏览翻页搜索，不支持 URL 搜索参数。

## 下载流程（3 层嵌套）

### 层 1：话题页 → "查看文件"

从搜索结果进入话题页（`/topic/xxxxx`），页面底部有一个大按钮：

```
[查看文件]  ← ipsButton_primary ipsButton_fullWidth
```

点击后跳转到文件详情页。

### 层 2：文件详情页 → "下载此文件"

文件详情页（`/files/file/xxxxx`）右侧边栏有下载按钮：

```javascript
// 获取下载按钮 URL（popup 之前的链接）
var btn = document.querySelector('a.ipsButton_important');
// btn.href → /files/file/xxxxx/?do=download&csrfKey=...
```

点击此按钮弹出确认弹窗。

### 层 3：弹窗 → "同意并下载" → 获取最终直链

弹窗内的同意按钮 **href 就是最终下载链接**：

```javascript
// 弹窗打开后，获取最终下载 URL
var agreeBtn = Array.from(document.querySelectorAll('a')).filter(
  b => b.textContent.includes('同意') && b.offsetParent !== null
);
// agreeBtn[0].href → /files/file/xxxxx/?do=download&confirm=1&csrfKey=...
```

## 下载策略（优先级递减）

### 根因

ai2.moe 使用 Cloudflare JS Challenge，检测 **TLS 指纹**（非 cookie）。
- Python + 完整浏览器头 → 200 OK（无 cookie 也行）
- IDM 直接请求 → 403（TLS 指纹不匹配）
- IDM + cookie → 403（cookie 对 Cloudflare 无效）

### 策略 1：浏览器点击 + IDM 扩展捕获（主力 ✅）

浏览器已通过 Cloudflare（TLS 指纹合法），IDM 扩展拦截下载请求，满速。

**步骤：**

1. 走完 3 层流程到弹窗
2. 点击 "同意并下载" → 浏览器触发下载 → IDM 扩展自动捕获
3. 下载完成后移动到目标位置：
```bash
cp "<browser_download_dir>/<auto_filename>" "<save_dir>/<filename>"
```
IDM 扩展捕获后下载目录通常是浏览器默认目录（如 `e:\All In One\Downloads\06\`）。

### 策略 2：Python 直接下载（备选，较慢）

用 Python urllib + 完整浏览器头。能过 Cloudflare 但单线程较慢：

```python
import urllib.request
url = "<agree_href>"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.ai2.moe/',
    'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin',
}
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req)
with open('<save_dir>/<filename>', 'wb') as f:
    f.write(resp.read())
```

## 文件信息提取

文件详情页包含：

```javascript
JSON.stringify({
  title: document.title,
  size: (() => {
    var m = document.body.innerText.match(/文件大小\s*([\d.]+\s*[KMGT]?B)/i);
    return m ? m[1] : 'unknown';
  })(),
  version: (() => {
    var m = document.body.innerText.match(/版本\s*([\d.]+)/);
    return m ? m[1] : null;
  })()
})
```

## 关键反模式

- **不要用 IDM 下载 csrfKey 链接但无 Referer** → 必 403
- **不要假设 csrfKey 永久有效** → 可能过期，需重新获取
- **ai2.moe 不需要登录即可下载** → 不要浪费时间尝试登录
- **话题页 URL 不是下载页** → 必须点 "查看文件" 进入文件详情页
