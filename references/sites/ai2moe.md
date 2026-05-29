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

### 策略：浏览器原生下载 → 轮询完成 → 移动（全自动 ✅）

1. 走完 3 层流程到弹窗
2. 点击 "同意并下载" → 浏览器原生下载（满速，通过 Cloudflare）
3. 等文件出现在浏览器下载目录后（轮询文件大小），移动到目标位置：
```bash
# 浏览器下载目录（OpenCLI 默认）
DOWN_DIR="e:/All In One/Downloads/06"
# 等文件下载完（大小不再变化）
while true; do
  f=$(ls -t "$DOWN_DIR"/*.zip 2>/dev/null | head -1)
  if [ -n "$f" ]; then
    s1=$(stat -c%s "$f" 2>/dev/null)
    sleep 5
    s2=$(stat -c%s "$f" 2>/dev/null)
    [ "$s1" = "$s2" ] && break
  fi
  sleep 5
done
cp "$f" "<save_dir>/<filename>"
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
