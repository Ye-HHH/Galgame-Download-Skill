# CJK 输入协议 — 搜索输入文字出现乱码

## 问题根因

中文/日文/韩文字符在通过 bash 命令行传递时会被重新编码，造成乱码（mojibake）。

```
bash 命令 → shell 编码转换 → 传给 opencli → 浏览器收到乱码
```

这影响所有通过 bash 传递 CJK 的操作：
- `opencli browser dl type 16 "拔作岛"` → 输入框显示 `鎷斾綔宀�`
- `opencli browser dl eval "window.location.href = '/search?q=借恋'"` → URL 变成 `/search?q=鍊熸亱`
- `python idm_bridge.py ... "LAMUNATION！.7z"` → 文件名变成 `LAMUNATION锛�.7z`

## 唯一可靠的解决方案

**在浏览器 JS 引擎内部构造字符串，永远不让 CJK 经过 bash。**

核心工具：
- `String.fromCodePoint()` — 用十六进制码点构造字符，全程在浏览器 JS 中执行，不经过 bash
- `document.execCommand('insertText', false, text)` — 模拟真实键盘输入，触发 React onChange，适用于受控组件

## 流程 A：shinnku（简单 `<input>`，非 React 受控）

shinnku 的搜索框是普通 HTML input，可以直接用 URL 导航。

```
opencli browser dl eval "
window.location.href = '/search?q=' + encodeURIComponent(String.fromCodePoint(0x62D4, 0x4F5C, 0x5C9B));
'ok'
"
```

注意：不要直接在 shell 里写 `/search?q=拔作岛`——中文会乱码。必须用 `String.fromCodePoint()` 在 JS 内构造。

## 流程 B：mihoyo.ink / Alist（React 受控组件 — 必须用 execCommand）

Alist 使用 hope-ui（基于 React），搜索输入框是**受控组件**。
- `input.value = "xxx"` → **无效**，React 内部状态不会更新
- `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(input, "xxx")` → **不稳定**，有时抛 `Illegal invocation`
- `document.execCommand('insertText', false, "xxx")` → **唯一可靠方案**

### 步骤 1：打开网站并唤起搜索弹窗

```
opencli browser dl open "https://mihoyo.ink/"
sleep 2
opencli browser dl keys Control+k
sleep 1
```

### 步骤 2：确认搜索弹窗已打开

**⚠️ 必须读取完整 state，绝不能用 head/tail 截断。**

搜索弹窗是一个 React portal，渲染在 DOM 的**最末尾**（在页面 footer 之后）。
典型的 state 输出有 150-250 行，弹窗的 `<section role=dialog>` 大约在第 180-220 行。

如果用 `state | head -60`，你只会看到首页内容、目录列表和 footer——**搜索弹窗被截断了**。
然后你就会错误地认为"Ctrl+K 没起作用"。

实际上 Ctrl+K 已经成功了，只是你看不到。

**正确做法**：读完整 state，在底部寻找 `id=search-input`。

如果懒得看完整 state，用 eval 直接检测：
```
opencli browser dl eval "document.getElementById('search-input') ? 'modal OPEN' : 'modal CLOSED'"
```

如果弹窗没打开 → 重试 Ctrl+K（最多 3 次）。

### 步骤 3：用 execCommand 输入 CJK 文字

```
opencli browser dl eval "
(() => {
  const input = document.getElementById('search-input');
  input.focus();
  const q = String.fromCodePoint(0x62D4, 0x4F5C, 0x5C9B);
  document.execCommand('insertText', false, q);
  document.querySelector('button[aria-label=search]').click();
  return 'typed: ' + q + ' value: ' + input.value;
})()"
```

返回值示例：`typed: 拔作岛 value: 拔作岛`

**typed 和 value 一致 = 输入成功，无乱码。**

### 步骤 4：提取搜索结果中的 CDN 直链

搜索完成后，在结果列表中选出最佳版本，点击进入详情页，提取 CDN 直链。
**搜到一个游戏就当场提取，不要批量搜索后再回头补提。**

## ⛔ 反模式：Alist @search URL

不要用 `/@search?keyword=...` 搜索 mihoyo.ink。这会返回：
```
failed get storage: storage not found; rawPath: /@search
```

Alist 的搜索**只能通过 Ctrl+K 弹窗**进行。

## 常用码点速查

| 用途 | 字符 | 码点 |
|------|------|------|
| 拔作岛 | 拔 / 作 / 岛 | 0x62D4 / 0x4F5C / 0x5C9B |
| 变态监狱 | 变 / 态 / 监 / 狱 | 0x53D8 / 0x6001 / 0x76D1 / 0x72F1 |
| 借恋(恋爱我就借走了) | 借 / 恋 | 0x501F / 0x604B |
| 无码 | 无 / 码 | 0x65E0 / 0x7801 |
| 汉化 | 汉 / 化 | 0x6C49 / 0x5316 |
| 熟肉/生肉 | 熟 / 肉 / 生 | 0x719F / 0x8089 / 0x751F |
| 终点汉化 | 终 / 点 | 0x7EC8 / 0x70B9 |
| 缘起甜韵趣恋丛生 | 缘 / 起 / 甜 / 韵 / 趣 / 丛 / 生 | 0x7F18 / 0x8D77 / 0x751C / 0x97F5 / 0x8DA3 / 0x4E1B / 0x751F |
| ぬきたし | ぬ / き / た / し | 0x306C / 0x304D / 0x305F / 0x3057 |
| ヘンタイ・プリズン | ヘ / ン / タ / イ / ・ / プ / リ / ズ / ン | 0x30D8 / 0x30F3 / 0x30BF / 0x30A4 / 0x30FB / 0x30D7 / 0x30EA / 0x30BA / 0x30F3 |
| ラブピカルポッピー | ラ / ブ / ピ / カ / ル / ポ / ッ / ピ / ー | 0x30E9 / 0x30D6 / 0x30D4 / 0x30AB / 0x30EB / 0x30DD / 0x30C3 / 0x30D4 / 0x30FC |

## 写中文内容到文件（密码文件等）

`echo "中文" > file` 和 `python -c "print('中文')"` 都会乱码——中文经过了 bash。

使用 Python + chr()，命令行里零汉字：

```bash
python -c "text=chr(0x6587)+chr(0x4ef6)+chr(0x540d)+': file.rar\n'+chr(0x89e3)+chr(0x538b)+chr(0x5bc6)+chr(0x7801)+': pwd\n'+chr(0x4e0b)+chr(0x8f7d)+chr(0x6765)+chr(0x6e90)+': site';open('g:/output.txt','w',encoding='utf-8').write(text)"
```

常用词的 chr() 值：
- 文件名 = `chr(0x6587)+chr(0x4ef6)+chr(0x540d)`
- 解压密码 = `chr(0x89e3)+chr(0x538b)+chr(0x5bc6)+chr(0x7801)`
- 下载来源 = `chr(0x4e0b)+chr(0x8f7d)+chr(0x6765)+chr(0x6e90)`

⚠️ 文件名也必须 ASCII（`_password.txt`），中文文件名同样会乱码。

## 获取任意字符的码点

在浏览器控制台或 opencli eval 中：
```javascript
"拔作岛".codePointAt(0).toString(16)  // "62d4"
```

或一次性获取所有字符：
```javascript
"ヘンタイ・プリズン".split('').map(c => '0x' + c.codePointAt(0).toString(16).toUpperCase()).join(', ')
```
