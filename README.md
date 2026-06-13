🎮 GalGame Download · AI 驱动的 Galgame 下载助手

🤖 **AI 对话驱动** | 🚀 **IDM 满速直链** | 🎮 **17+ 站点聚合** | 🔑 **密码自动收集** | 📦 **智能解压整理**

[skill 源码] • [更新日志] • [问题反馈]

---

## 📸 它能干什么

你只需要跟 Claude 说一句人话：

> "帮我把 CLOCKUP 钟表社的 euphoria、Erewhon、Maggot baits 下了，汉化优先，下完自动整理"

然后它会自动完成：搜索 → 筛选 → 下载 → 解压 → 扁平化 → 整理入库。全程你只需点几下确认。

---

## 🎯 核心功能

| 特性 | 说明 |
|------|------|
| 🧠 **AI 对话驱动** | 不写命令、不记站点，用自然语言描述需求即可 |
| 🔍 **17 站并行搜索** | shinnku / mihoyo.ink / inarigal / galzy / fh-xy / qingju / kungal 等 |
| 📎 **IDM 直链下载** | 自动提取 CDN 直链，通过 IDM COM Bridge 提交下载 |
| 🔑 **密码自动收集** | Phase 3 强制收集解压密码，不遗漏 |
| 📦 **智能解压整理** | 三层目录（压缩文件→预整理→会社名），自动扁平化嵌套 |
| 🗜️ **递归解包** | 嵌套 rar / ISO / MDF 逐层解压，直到见 .exe |
| 🀄 **补丁自动覆盖** | 翻译补丁多层解包后按文档覆盖到游戏目录 |
| 🧹 **拒绝脏目录** | 修改解压前恢复原文件夹名。永不自动删文件，需用户确认 |

---

## 🗺️ 收录的下载站

### 🟢 IDM 直链

![shinnku](https://img.shields.io/badge/shinnku-CD%E7%9B%B4%E9%93%BE-brightgreen)
![mihoyo.ink](https://img.shields.io/badge/mihoyo.ink-3%E4%BB%93%E5%BA%93%2B%E8%A1%A5%E4%B8%81-brightgreen)
![inarigal](https://img.shields.io/badge/inarigal-AI%E6%B1%89%E5%8C%96%E6%A0%87%E7%AD%BE-brightgreen)
![galzy](https://img.shields.io/badge/galzy-1966%E6%9D%A1%E7%9B%AE-brightgreen)

### ⚪ 需登录/特殊条件

![fh-xy](https://img.shields.io/badge/fh--xy-%E7%99%BE%E5%BA%A6%2F%E5%A4%B8%E5%85%8B-lightgrey)
![qingju](https://img.shields.io/badge/qingju-lz4%E5%8A%A0%E5%AF%86-lightgrey)
![kungal](https://img.shields.io/badge/kungal-%E8%AF%84%E5%88%86%E6%9C%80%E5%85%A8-lightgrey)
![touchgal](https://img.shields.io/badge/touchgal-%E9%B2%B2%E5%AE%B6%E4%BA%8C%E5%BC%9F-lightgrey)

### 🟡 需魔法访问

![acggw](https://img.shields.io/badge/acggw-ACG%E6%B8%AF%E6%B9%BE-yellow)
![chgal](https://img.shields.io/badge/chgal-%E7%A3%81%E5%8A%9B%2F%E7%BD%91%E7%9B%98-yellow)
![galgame.dev](https://img.shields.io/badge/galgame.dev-%E7%9C%9F%E7%BA%A2%E8%AE%BA%E5%9D%9B-yellow)

### 🧩 补丁站点

![2dfan](https://img.shields.io/badge/2dfan-%E8%A1%A5%E4%B8%81%E4%B9%8B%E7%8E%8B-blue)
![ai2.moe](https://img.shields.io/badge/ai2.moe-AI%E7%BF%BB%E8%AF%91%E8%A1%A5%E4%B8%81-blue)
![moyu.moe](https://img.shields.io/badge/moyu.moe-%E5%AF%B9%E8%B1%A1%E5%AD%98%E5%82%A8-blue)

---

## 🔑 站点固定密码速查

| 站点 | 密码 | 备注 |
|------|------|------|
| 柚哩 GAL 仓库 | `south-plus` | |
| 南+合集 | `south-plus` | |
| 梓澪の妙妙屋（浮士德） | 无密码 | 生肉区 |
| 梓澪の妙妙屋（补丁） | 无密码 | 补丁区 |
| qingju.org | `qingju` | lz4 加密 |
| chgal.com | `erciyuanfengwo` | |

---

## 📦 工作流管线

```
你: "帮我把时钟社的游戏下了"
              │
              ▼
┌──────────────────────────────────────┐
│ Phase 0-1   工具链检查 + 下载目录配置  │
│ opencli / IDM / Python / 7z / g:\压缩文件\ │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│ Phase 2     游戏研究                  │
│ 中/日/英全名搜索，系列梳理，确认清单   │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│ Phase 3     站点搜索 + 密码收集       │
│ OpenCLI 浏览器驱动，中/日双名搜索     │
│ 提取 CDN + 密码 + 大小，汇总确认      │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│ Phase 4     IDM 直链下载             │
│ python idm_bridge.py 提交到 g:\压缩文件\│
│ 保留服务器原始文件名，不改名          │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│ Phase 5     轮询完成 + 主动复查       │
│ 不在依赖记忆，定期检查下载目录        │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│ Phase 6     解压 + 整理              │
│ g:\压缩文件\ → g:\预整理\ → g:\会社名\│
│ 三原则：尊重原名 / 无顶自建 / 最短路径│
│ 递归解包 ISO/MDF，补丁覆盖，用户确认  │
└──────────────────────────────────────┘
```

---

## 🗂️ 文件整理原则

| 原则 | 说明 |
|------|------|
| 📁 **三层目录分离** | `压缩文件` → `预整理` → `会社名`，永不混杂 |
| 🏷️ **尊重原始文件夹名** | 压缩包里顶层文件夹叫什么就是什么，不重命名不精简标签 |
| 📏 **无顶自建** | 压缩包没有顶层文件夹才自己建一个 |
| 🪜 **最短路径** | exe 必须在根或最多一层深，拒绝 `EUPHORIA HD/EUPHORIA HD/` |
| 🔁 **递归解包** | .rar→.rar→ISO→解到见 .exe 为止 |
| 🀄 **补丁覆盖** | 多层解包后按文档覆盖到游戏目录 |
| 🗑️ **永不自动删文件** | 任何删除需用户确认，完整体验后才清压缩包 |
| ⚠️ **ISO/MDF 即刻告知** | 解出光盘镜像第一时间告知用户 |

---

## 📂 项目结构

```
galgame-download/
├── CLAUDE.md                     全局规则 + 16条避坑指南
├── SKILL.md                      工作流路由（Phase 0-6）
├── idm_bridge.py                 IDM COM 下载桥接
├── references/
│   ├── config.json               持久化配置（下载目录等）
│   ├── cjk-input.md              CJK 输入协议（防乱码）
│   ├── phases/
│   │   ├── phase-0-check.md      工具链检查
│   │   ├── phase-1-setup.md      目录配置 + 盘符检测
│   │   ├── phase-2-research.md   游戏名称研究
│   │   ├── phase-3-search.md     站点搜索 + 密码收集
│   │   ├── phase-4-download.md   IDM 下载（保留原名）
│   │   ├── phase-5-wait.md       轮询 + 主动复查
│   │   └── phase-6-extract.md    解压整理三原则
│   ├── sites/
│   │   ├── mihoyo.md             mihoyo.ink 完整指南
│   │   └── ai2moe.md             ai2.moe 下载指南
│   └── wait_download.py          下载完成轮询脚本
└── README.md
```

---

## 📢 注意事项

> **✉️ 写给站长**：本 skill 通过浏览器自动化模拟正常用户操作，单个游戏通常只下载 1 次，不会对服务器造成爬虫级负载。如果你的站点不希望被包含，欢迎联系移除。

> **🔐 安全声明**：所有下载行为由用户主动触发并确认。本 skill 不会自动批量下载、不会分发下载链接、不会绕过付费验证。

> **🤖 AI 驱动说明**：这是一个 Claude Code skill，依赖 OpenCLI 浏览器自动化 + IDM。需要在 Windows 环境下运行，Python 3 + IDM + OpenCLI 为必需依赖。

---

> *"安装 Galgame 最难的从来不是下载，而是翻山越岭下载好之后，就再也没打开过。"* —— 某不知名旮旯糕手
