# mihoyo.ink — 柚哩遊戲分享站 完整指南

站点类型：**Alist（React + hope-ui）**，直接 CDN 下载，无需登录。

---

## 🛑 唯一搜索方式：Ctrl+K 弹窗

> ⛔ **搜索 mihoyo.ink 只有一条路：Ctrl+K 打开搜索弹窗 → 输入关键词 → 搜索。**
>
> **绝对禁止的操作：**
> - ❌ 进目录手动翻找 — 目录层级极深，翻半天找不到，纯浪费时间
> - ❌ `/@search?keyword=` URL 搜索 — Alist 不支持，会报错
> - ❌ 搜不到就换站 — 先确认步骤正确、重试 Ctrl+K（最多 3 次）、确认无结果再说
>
> **如果 Ctrl+K 弹窗打不开：**
> 1. 确认已 `sleep 2` 等页面加载完
> 2. 重试 `opencli browser dl keys Control+k`（最多 3 次）
> 3. 还是打不开 → **停下来，告诉用户，问怎么办。不准换方案。**

---

## 目录结构概览（仅供参考，不要手动翻）

```
/
├── 柚哩Gal/
│   ├── GAL仓库1/          ← 汉化游戏月份合集，终点汉化重整
│   └── GAL仓库2（更新中）/ ← 较新的汉化作品
├── 梓澪の妙妙屋(第三方)/
│   ├── `【合集系列】/     ← 浮士德合集、汉化galgame合集、终点汉化合集 等
│   ├── `【补 丁】/        ← 汉化补丁归档、AI翻译补丁合集
│   └── `【归 档】/        ← Tyranor合集等
├── 南+合集/
│   └── SP后端1[GalGame分区]/ ← 离散分发的汉化/生肉
├── 相关工具下载/
└── free clash sub/
```

游戏本体主要在：
- `柚哩Gal/GAL仓库1/汉化游戏月份合集/` — 按年/月/新汉化作品 排列
- `柚哩Gal/GAL仓库2/汉化游戏月份合集/` — 同上，较新
- `梓澪の妙妙屋/\`【合集系列】/汉化galgame合集/` — 按年/月/ADV 排列，单文件
- `梓澪の妙妙屋/\`【合集系列】/终点汉化合集/` — 终点汉化组的作品
- `南+合集/SP后端1[GalGame分区]/汉化游戏月份合集-离散/` — 离散分发，镜像内容

## 搜索流程（完整步骤）

### ⚠️ 搜索前必读

mihoyo.ink 使用 React (hope-ui) 构建。搜索输入框是 React 受控组件，普通的 `.value = "xxx"` 赋值**无效**。

另外，中文/日文通过 bash 命令行传递会乱码。**完整的 CJK 输入协议见 `references/cjk-input.md`。**

### 步骤 1：进入首页并打开搜索弹窗

```
opencli browser dl open "https://mihoyo.ink/"
sleep 2
opencli browser dl keys Control+k
sleep 2
```

### 步骤 2：确认弹窗已打开（这是踩过的大坑）

**搜索弹窗是一个 React portal，渲染在 DOM 的最末尾。** 页面 state 输出通常有 150-250 行，弹窗的 `<section role=dialog>` 大约在第 180-220 行。

如果使用 `state | head -60`，弹窗内容会被**完全截断**。你会看到首页 → 目录列表 → footer → 以为没有弹窗。

**正确验证方法：**

```
opencli browser dl eval "document.getElementById('search-input') ? 'modal OPEN' : 'modal CLOSED'"
```

返回 `modal OPEN` = 弹窗已打开。返回 `modal CLOSED` = 重试 Ctrl+K（最多 3 次）。

### 步骤 3：输入搜索关键词

```
opencli browser dl eval "
(() => {
  const input = document.getElementById('search-input');
  input.focus();
  const q = String.fromCodePoint(0x62D4, 0x4F5C, 0x5C9B);  // 拔作岛
  document.execCommand('insertText', false, q);
  document.querySelector('button[aria-label=search]').click();
  return 'typed: ' + q + ' value: ' + input.value;
})()"
```

返回值示例：`typed: 拔作岛 value: 拔作岛` — typed 和 value 一致 = 无乱码，输入成功。

**搜索范围下拉框**：默认是「全部」，无需修改。

### 步骤 4：评估搜索结果

搜索结果中每条记录的格式：
```
[文件名]  [大小]  [路径]
```

选版本时按以下优先级：
1. 熟肉/汉化 > 生肉
2. 官中/汉化硬盘版 > 机翻
3. 无码 > 有码（有最好，没有不硬求）
4. 单文件 > 分卷（`.7z.001/.002` 需要额外合成）
5. 同版本选体积小的

**注意区分游戏本体和补丁/CG包**：
- 游戏本体：通常 3-15 GB，路径在 `汉化galgame合集`、`终点汉化合集`、`汉化游戏月份合集`
- 补丁：通常 50-500 MB，路径在 `补丁`、`汉化补丁归档`
- CG/英译包：通常 50 MB-2 GB，路径在 `生肉`、`EX ENG/JAP GameCG Collection`
- AI生成内容：通常 <200 MB，文件名含 `AI Generated` → 跳过

### 步骤 5：进入详情页，提取 CDN 直链

点击搜索结果中的文件名，进入文件详情页。详情页显示：
- 文件名 + 大小
- **「复制链接」按钮**
- **「下载」按钮**（直接 CDN 链接）
- 可能的解压密码

**提取 CDN 直链的方式：**

方式 A — 直接从下载按钮的 href 提取：
```
opencli browser dl eval "
(() => {
  const links = [];
  document.querySelectorAll('a').forEach(a => {
    const h = a.href || '';
    if (h.includes('cdn') || h.includes('galgamedownload') || h.includes('alist-public') || h.includes('ali-cdn')) {
      links.push(h);
    }
  });
  return JSON.stringify(links);
})()"
```

方式 B — 如果没有直接 CDN 链接，点击「复制链接」按钮获取 `/d/...` 路径。

**mihoyo.ink 常见的 CDN 域名：**
- `ali-cdn.mihoyo.fans` — 阿里云 CDN
- `galgamedownload.date` — 备用 CDN
- `alist-public.imoutoheaven.org` — 公共 Alist 节点（南+合集的文件）

### 步骤 6：提取解压密码

密码通常在详情页的 footer 区域或文件描述中。常见密码：

| 来源目录 | 常见密码 |
|----------|----------|
| Gal仓库 / 柚哩Gal | `south-plus` |
| 终点汉化 / 次元终点 | 终点自定义密码（文件名括号内标注） |
| 梓澪の妙妙屋 | 看文件名括号内容 |
| 南+合集 | `south-plus` |

用 regex 从页面提取：
```javascript
// 匹配 "解压密码: xxx" 或 "密码：xxx"
document.body.textContent.match(/密码[：:]\s*(.+?)(?:\s|$)/)
```

## ⛔ 已知反模式（不要做的事）

### 1. 不要用 @search URL
`https://mihoyo.ink/@search?keyword=xxx` 会返回 `"failed get storage: storage not found"`。Alist 的搜索只能通过 Ctrl+K 弹窗。

### 2. 不要用 input.value = xxx
React 受控组件不会响应直接赋值。必须用 `execCommand('insertText')`。

### 3. 不要截断 state 输出
弹窗在 DOM 最末尾，截断就看不见。

### 4. 不要进目录手动翻找
mihoyo.ink 的目录层级深（柚哩Gal → GAL仓库1 → 汉化游戏月份合集 → 2024 → 02 → 新汉化作品 → ...），手动翻找极其低效。**始终用搜索。**

### 5. 不要忽略「复制链接」按钮
如果详情页的下载 `<a>` 标签的 href 是相对路径或目录路径（不以 `http` 开头），点击「复制链接」按钮会把完整直链写入剪贴板。此时用 eval 读取：
```javascript
// 先拦截 clipboard API，再点击按钮
navigator.clipboard.readText().then(t => console.log(t))
```

## CDN URL 的 sign 参数

mihoyo.ink 的 CDN 链接包含 `?sign=...` 参数，这是临时的签名令牌，有时效性。提取后尽快传给 IDM。
如果 sign 过期（下载失败），重新从详情页提取新的 CDN 链接。
