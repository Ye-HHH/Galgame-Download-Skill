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

### 策略 1：IDM 直链（首选）

提取 "同意并下载" 的 href，直接发送给 IDM：

```bash
python idm_bridge.py "<agree_href>" "https://www.ai2.moe/" "<save_dir>\\" "<ascii_filename>" --silent
```

- Referer: `https://www.ai2.moe/`
- 文件名：ASCII，从文件详情页提取（通常在 title 或 h1 中）

### 策略 1.1：检查 IDM 是否成功

IDM 提交后，等 10 秒检查文件是否开始下载：

```bash
ls -la "<save_dir>/<filename>" 2>&1
```

- 文件存在且大小 > 0 → IDM 成功，进入 Phase 5 等待完成
- 文件不存在 → IDM 可能被拒绝（403），进入策略 1.2

### 策略 1.2：刷新链接重试

ai2.moe 的 csrfKey 有时效性。如果 IDM 失败（403 Forbidden）：

1. 重新打开文件详情页 → 重新点击 "下载此文件" → 重新获取 "同意并下载" href
2. 用新的 csrfKey 再次提交 IDM
3. 再次检查

如果仍失败 → 进入策略 2。

### 策略 2：Python 直接下载（备选）

ai2.moe 的链接用 Python urllib + 正确 headers 可以直接下载（不需要 cookie）：

```python
import urllib.request
url = "<agree_href>"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.ai2.moe/'
}
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req)
with open('<save_dir>/<filename>', 'wb') as f:
    f.write(resp.read())
```

**下载完成后将文件移动到目标目录：**

```bash
mv "/c/Users/adminn/Downloads/<downloaded_file>" "<save_dir>/<filename>"
```

### 策略 3：浏览器下载（最后手段）

如果 Python 下载也失败，直接在浏览器中点击 "同意并下载"，让 Chrome 原生下载处理。

**浏览器下载完成后移动到目标目录：**
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
