我要成为旮旯Game糕手🦐

# GalGame 下载助手

> 一个由 AI 驱动的 Galgame 下载工作流——你只需要说"我想玩 XXX"，剩下的交给它。
> 支持 17 个下载站、IDM 高速直链、百度网盘多种下载方式、飞书通知，还能自动帮你写解压密码.txt。

---

## 🎮 它能干什么

你对着 Claude 说一句人话，比如：

> "帮我把对魔忍全系列下了，PC 熟肉，静默下载"

然后它就会：

1. 去网上查这个系列有哪些作品、评分、年代
2. 列出来让你挑（"你要哪几部？"）
3. 在 17 个站点里搜下载链接，优先找 IDM 直链和百度盘
4. 搜不到熟肉？自动找生肉 + 汉化补丁
5. 验证链接是否有效，按优先级汇总给你确认
6. 用 IDM / 百度网盘 / BaiduPCS-Go 直接下载
7. 自动在同目录创建 `解压密码.txt`

你全程只需要点几下确认。

---

## 🔧 实现管线

```
你: "下个甜蜜女友2"
        │
        ▼
┌──────────────────────────────────────┐
│  ① WebSearch                         │
│  查系列信息、评分、年代、VNDB 数据     │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│  ② 多站点并行搜索 (OpenCLI Browser)    │
│  shinnku → mihoyo → inarigal → galzy│
│  → fh-xy → qingju → kungal ...      │
│  每个站自动发现搜索方式，中/日双名搜    │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│  ③ 版本筛选 + 路径判断              │
│  熟肉? → PATH A: 直接下载           │
│  生肉? → PATH B: 生肉 + 汉化补丁    │
│  整合版 > 分卷    大文件 > 小文件    │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│  ④ 链接嗅探 + 验证                  │
│  每个站不一样的提取方式:             │
│  - 读页面找"复制链接"/"下载"按钮     │
│  - 提取云盘 <a> 标签 + 正则          │
│  - 验证链接存活后再展示              │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│  ⑤ 下载引擎                         │
│  IDM COM Bridge (CDN 直链)           │
│  OpenCLI 浏览器 (百度盘)             │
│  BaiduPCS-Go CLI (百度盘高速)        │
│  bdpan (百度盘备选)                  │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│  ⑥ 后处理                           │
│  → 创建 解压密码.txt                 │
│  → lz4 加密格式注明解密教程          │
│  → 飞书 bot 通知下载完成              │
└──────────────────────────────────────┘
```

---

## 🗺️ 收录的下载站（17 个）

| # | 站点 | 下载方式 | 搜索方式 | 一句话点评 |
|---|------|----------|----------|------|
| 1 | **shinnku.com** | CDN 直链 | 搜索框/URL | 全站最全，IDM 满速，熟肉生肉分开 CDN |
| 2 | **mihoyo.ink** | 直链 | Ctrl+K 搜索 | 柚哩，3 个 GAL 仓库 + 补丁归档，宝藏 |
| 3 | **inarigal.com** | 直链 | 搜索框 | 稻荷 GAL，有 AI 汉化标签 |
| 4 | **galzy.moe** | 直链 | 搜索框(URL 无效) | 紫缘社，1966 条目，IDM 友好 |
| 5 | **fh-xy.net** | 百度/夸克/UC | 点🔍图标搜索 | 风花雪月，论坛型，密码各帖子不同 |
| 6 | **qingju.org** | 百度网盘 | 搜索框/URL | 青桔网，lz4 加密，密码统一 qingju |
| 7 | **kungal.com** | 跳转网盘 | 搜索框/URL | 鲲 Galgame，资料最全，评分标签应有尽有 |
| 8 | **touchgal.ink** | 跳转 | 搜索不稳定 | 鲲家二弟，界面现代 |
| 9 | ~~nysoure.com~~ | 重定向网盘 | — | ❌ 已死，无法连接 |
| 10 | ~~acgngames.net~~ | 跳转网盘 | — | ❌ 已死，无法连接 |
| 11 | **acggw.me** | 跳转网盘 | 搜索框 | ACG 港湾，RPG/SLG/gal 大乱炖 |
| 12 | **chgal.com** | 磁力/网盘 | — | 绅仕天堂，密码 erciyuanfengwo，SSL 过期 |
| 13 | **jiuliacg.com** | 隐藏链接 | — | 玖黎 ACG，需登录+评论 |
| 14 | **galgame.dev** | 飞猫/百度 | 论坛搜索 | 真红论坛，shinnku 的好基友 |
| 15 | **vikacg.com** | OD/度云 | — | 维咔 V 站，谷歌一键即可 |
| 16 | **2dfan.com** | 直链/网盘 | 搜索框 | 补丁之王，免验证/CG 存档/攻略 |
| 17 | **gameshare.cc** | 直链 | — | 泛游戏站，非 gal 专站 |

---

## 🔑 站点固定密码速查

仅记录全站统一密码。论坛帖子密码各不相同，需从页面提取。

| 站点 | 密码 | 备注 |
|------|------|------|
| qingju.org | `qingju` | lz4 加密，先解密再解压 |
| chgal.com | `erciyuanfengwo` | |
| 柚哩 GAL 仓库 | `south-plus` | |
| 梓澪の妙妙屋 | `终点` | |
| 猫猫网盘 | `south-plus` | |

---

## 📦 文件结构

```
galgame-download/
├── SKILL.md              Phase 0-5 完整工作流
├── idm_bridge.py         IDM COM 桥接脚本
├── references/
│   ├── config.json       下载目录等持久化配置
│   ├── sites.md          17 站点 + 搜索方式 + 常见失败模式
│   ├── sites/mihoyo.md   mihoyo.ink 完整指南
│   ├── passwords.md      密码处理 + lz4 教程
│   ├── cjk-input.md      CJK 输入协议
│   └── cdn.md            shinnku CDN 细节 + IDM 用法
└── README.md
```

---

## 📋 使用

```bash
# IDM 直链（shinnku/galzy/mihoyo 等）
python idm_bridge.py "<url>" "<referer>" "<save_dir>" "<filename>" --silent

# 百度网盘（OpenCLI 浏览器方式，最可靠）
# 直接在 OpenCLI 中打开分享链接，客户端自动接管

# BaiduPCS-Go CLI（高速多线程）
BaiduPCS-Go transfer <share_link> -p <pwd>
BaiduPCS-Go download <remote_path> <local_path>
```

整个流程由 Claude Code + OpenCLI 浏览器驱动。
你只需要说出你想玩什么游戏，AI 会帮你找到它、验证链接、下载它、告诉你密码。

---

> *"安装 Galgame 最难的从来不是下载，而是翻山越岭下载好之后，再也没打开过。" —— 某不知名旮旯糕手*

## 依赖

- Windows + IDM（Internet Download Manager）
- Python 3 + comtypes（IDM COM 桥接）
- bdpan / BaiduPCS-Go（百度网盘 CLI，可选）
- Claude Code + OpenCLI
