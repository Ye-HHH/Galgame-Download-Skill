# Site Reference — Galgame Download Sources

## Priority Order

**直链(IDM) → 百度盘(bdpan) → 生肉+补丁兜底。不在一个站纠结！**

## Download Sites (ranked)

| # | Site | Type | Login | Download | Search Method | Notes |
|---|------|------|-------|----------|---------------|-------|
| 1 | **shinnku.com** | 直链 | No | CDN | URL `/?search=` or searchbox "Search" | 主力，IDM高速。熟肉 zd/ + 0/win/，生肉 galgame0/ |
| 2 | **mihoyo.ink** | Alist | No | 直链 | **Ctrl+K** opens search modal | 柚哩GAL仓库1-3 + 梓澪妙妙屋合集，大量熟肉+无码+补丁归档 |
| 3 | **inarigal.com** | 直链 | No | 直链/网盘 | Searchbox "搜索游戏，L:会社，T:标签" | AI汉化标签 |
| 4 | **galzy.moe** | 直链 | No | 直链 | **Must use searchbox** "标题、标签、回车，喵喵喵～🐾" | URL `?s=` invalid! |
| 5 | **fh-xy.net** | 论坛 | No | 百度/夸克/UC | **Click 🔍 → searchbox** "请输入搜索内容" | URL `?s=` invalid! Password: 上老王论坛当老王 |
| 6 | **qingju.org** | 博客 | No | 百度盘 | URL `/?s=` or searchbox | **lz4加密**，密码 qingju |
| 7 | **kungal.com** | 聚合 | No | 跳转网盘 | URL `/search?q=` or searchbox | VNDB评分/标签/系列 |
| 8 | **touchgal.ink** | 聚合 | No | 跳转 | Search unreliable | 游戏会社/标签分类 |
| 9 | **nysoure.com** | 分享 | No | 重定向网盘 | URL or search | 930资源，标签分类 |
| 10 | **acgngames.net** | 列表 | No | 跳转网盘 | — | 备选，覆盖少 |
| 11 | **acggw.me** | 博客 | No | 跳转网盘 | URL or search | RPG/SLG偏多 |
| 12 | **chgal.com** | 博客 | **Login** | 磁力/网盘 | — | 密码 erciyuanfengwo，SSL过期 |
| 13 | **jiuliacg.com** | 博客 | **Login+Comment** | 隐藏链接 | — | 玖黎ACG |
| 14 | **galgame.dev** | 论坛 | No | 飞猫→百度 | Forum search | 真红论坛，Discuz! |
| 15 | **vikacg.com** | 论坛 | Google | OD/度云 | — | 维咔V站 |
| 16 | **2dfan.com** | 补丁站 | Google | 直链/网盘 | URL or search | 汉化补丁/存档 |
| 17 | **gameshare.cc** | 社区 | No | 直链 | — | **非gal站**，普通游戏 |

## Link Discovery Tips

- fh-xy / galgame.dev: 百度链接+提取码直接写在帖子正文里，不是附件
- vikacg / jiuliacg / chgal: 需登录才能看下载内容
- 搜索策略: 先读快照全文，搜 `pan.baidu.com` / `提取码` / `解压`

## Information & Patches

| Site | URL | Use |
|------|-----|-----|
| 2DFan | `https://2dfan.com/` | 汉化补丁、免验证补丁、攻略 |
| VNDB | `https://vndb.org/` | 评分、发售日期、系列关系 |
| Bangumi | `https://bgm.tv/` | 中文评价、讨论 |
| ai2.moe | `https://www.ai2.moe/files/category/12-全游戏无码化计划（ai去码）/` | AI 去码补丁，免登录，3 层下载流程 → `references/sites/ai2moe.md` |
| moyu.moe | `https://www.moyu.moe/` | 汉化补丁归档 |
| mihoyo.ink 补丁 | `梓澪の妙妙屋/补丁/汉化补丁归档/2dfan AI翻译补丁合集/` | 免登录补丁镜像 |

## mihoyo.ink (Alist) Specifics

**⚠️ 搜索前必须阅读：`references/sites/mihoyo.md` — 包含完整搜索流程、CJK输入、CDN提取、已知反模式和密码表。**

简要备忘：
- **Search**: Ctrl+K → `execCommand('insertText')` 输入 CJK → 弹窗在 DOM 最末尾，不能截断 state
- **No `@search` URL**: 不支持，必须用 Ctrl+K 弹窗
- **CDN**: `ali-cdn.mihoyo.fans`, `galgamedownload.date`, `alist-public.imoutoheaven.org`
- **密码**: 柚哩Gal = `south-plus`，终点汉化 = 文件名括号内标注

## Multi-Keyword Search Strategy

逐级降级: Full JP name → Chinese name → English/romaji → Partial keyword → Series name

Common conversions: `ママは`↔`妈妈`/`Mama wa`, `アサギ`↔`阿莎姬`/`Asagi`, `ZERO`↔`零`/`Zero`, `紅`↔`红`/`Kurenai`

## Known Dead / Excluded

nysoure.com, acgngames.net — connection failed. acgbox.link, moeyg.top, ourmoe.me, clfans.club, rosmontis.com, xiayuge.top, lzacg.org, ymgal.games, acgndog.com, steamgalgame.com, tianshie.com, 忧郁的弟弟, 梦灵神社, 灵梦御所, eohut.com — all dead or irrelevant.
