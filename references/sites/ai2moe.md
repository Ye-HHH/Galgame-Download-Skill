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

ai2.moe 使用 Cloudflare JS Challenge。Cloudflare 检查浏览器 session cookie（`document.cookie`）。IDM 不带 cookie → 403。带 cookie → 满速。

### 策略 1：IDM + 浏览器 Cookie（主力 ✅）

浏览器已访问 ai2.moe 并解决 Cloudflare 挑战后，提取 cookie 传给 IDM：

**步骤：**

1. 在 OpenCLI 浏览器中打开 ai2.moe 任意页面（确保 Cloudflare 挑战已过）
2. 提取 cookies：
```bash
opencli browser dl eval "document.cookie"
```
3. 走完 3 层下载流程，获取 "同意并下载" href
4. IDM 带 cookie 下载：
```bash
python idm_bridge.py "<agree_href>" "https://www.ai2.moe/" "<save_dir>\\" "<ascii_filename>" --cookie="<cookies>" --silent
```
5. 10 秒后检查文件是否出现：
```bash
ls -la "<save_dir>/<filename>"
```
6. 文件不在 → cookie 过期，刷新页面重新获取 cookie 重试

### 策略 2：Python 直接下载（备选）

提取 "同意并下载" href，用 Python urllib + 完整浏览器头。已验证可行（`idm_bridge.py` `--cookie` 更简单）：

```python
import urllib.request
url = "<agree_href>"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.ai2.moe/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
}
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req)
with open('<save_dir>/<filename>', 'wb') as f:
    f.write(resp.read())
```

### 策略 3：浏览器下载（最后手段）

直接在浏览器中点击 "同意并下载"，下载完成后移动到目标目录：
```bash
mv "/c/Users/adminn/Downloads/<filename>" "<save_dir>/<filename>"
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
