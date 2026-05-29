---
name: galgame-download
description: GalGame 下载助手 — 搜索、筛选、下载 galgame 资源。支持全系列下载、模糊推荐、社团补完。TRIGGER: 用户想下载/找 galgame/视觉小说/ADV，提到游戏名/系列/社团（如"对魔忍""柚子社""白色相簿"），或要求找汉化补丁。全语言触发（中日英）。
---

# GalGame 下载助手

## Architecture

```
User request → Claude + OpenCLI browser → search sites → filter versions
    → IDM bridge (直链) / bdpan (百度盘) / 展示链接 (其他)
```

## Config

Session-persistent settings stored in `references/config.json`:

```json
{
  "save_directory": "e:\\AllinOne"
}
```

- **Read** at start of every session (Phase 0)
- **Write** when user changes save directory: `"以后都下到 F:\\Games"`
- Path format: Windows backslash, double-escaped in JSON. No trailing backslash.
- User can override per-session: `"这次下到 D:\\Temp"` → use for this session only, don't update config

---

## Phase 0: Dependency Check

Before doing anything, verify these are available. If missing, fix or skip the related download mode.

| Dependency | Check command | Used for | Required? |
|-----------|---------------|----------|-----------|
| Config | `cat references/config.json` | Save directory | **Yes** |
| OpenCLI | `opencli doctor` | Browser search on all sites | **Yes** |
| IDM bridge | `ls idm_bridge.py` in skill dir | Direct link downloads | For IDM mode |
| IDM TempPath | `reg query HKCU\Software\DownloadManager /v TempPath` | 下载缓存目录 | **Must be on same drive as save path** |
| Baidu client | `ls "D:/APP/BaiduNetdisk/BaiduNetdisk.exe"` | 百度盘 (auto-capture) | For 百度 mode |
| BaiduPCS-Go | `which BaiduPCS-Go` | 百度盘 CLI (fast) | Optional, better than bdpan |
| bdpan CLI | `bdpan whoami` | 百度盘 fallback | Deprecated |
| 7z | `ls "/c/Program Files/NVIDIA Corporation/NVIDIA app/7z.exe"` | Archive extraction | Nice to have |

Report what's available, including the current `save_directory` from config.

If IDM TempPath is on C: drive but save path is on another drive, fix it:
```
cmd.exe /c "reg add HKCU\Software\DownloadManager /v TempPath /t REG_SZ /d G:\IDM\Temp\ /f"
mkdir -p "G:/IDM/Temp"
```

Before starting any download work, ensure these permissions are in `.claude/settings.local.json` to avoid constant prompts: `Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, `Skill`, `Agent`. If missing, add them with Python.

---

## Phase 1: Pre-download

Ask these every session:

1. **PC or mobile?** (exe / apk / krkr / ons)
2. **Download mode?** Normal / Silent / Silent+Notify (飞书)

**Save directory** is read from `references/config.json` in Phase 0. If user says `"这次下到 D:\\Temp"` or `"以后都下到 F:\\Games"`:
- "这次" / "这次下载" → session-only override, don't touch config
- "以后" / "默认" / "改到" → update `references/config.json`, persists across sessions
- No mention of path → use config value silently, don't ask

---

## Phase 2: Understand the Request

**Web research FIRST** via WebSearch/Exa before touching any download site.

### Match the scenario:

| User says | Action |
|-----------|--------|
| Game/series name | Research → present overview → ask which entries |
| Vague description ("催泪的") | Research → shortlist 3-5 titles with ratings → let user pick |
| Developer name ("柚子社") | Research → catalog their works → ask which |
| "Patch" / "补丁" for a game | Go to patch flow |

### For series: present ALL entries with story synopses + tags. Ask "all or pick?"

Use WebSearch to gather from VNDB/Bangumi/2DFan, then present:

```
作品系列 | 开发商 | 年份范围

| # | 作品 | 年份 | 简介 | 亮点 | 标签 |
|---|------|------|------|------|------|
| 1 | 対魔忍アサギ | 2005 | 近未来日本，对魔忍井河アサギ与朧率领的魔界势力对抗，被宿敌盯上后陷入凌辱陷阱。妹妹さくら也被卷入了这场战斗 | 系列开山作，累计销量35万，动态CG | ADV/调教/触手/凌辱 |
| 2 | アマカノ | 2014 | 主人公搬到雪国温泉小镇帮祖父母铲雪，与神社巫女高社紗雪、神秘学姐上林聖、甜品店学妹星川こはる相恋 | 纯爱标杆，冬雪氛围感极强 | 纯爱/学园/冬日 |
| ... |
```

**各列要求:**
- **简介**: 故事设定+主要人物，2-3句，从VNDB/Bangumi/2DFan提炼，讲清楚这游戏"发生了什么"
- **亮点**: 为什么值得玩——评分、特色系统、系列地位、奖项等
- **标签**: 尽可能全（ADV/纯爱/NTR/调教/触手/学园/拔作/剧情/等等）

Then ask which to download.

### Mandatory Name Research (BEFORE Phase 3)

For EVERY game the user wants, compile a name table BEFORE touching any download site. Use WebSearch to find all variants:

```
| Language | Name |
|----------|------|
| 日文原名 | ラブピカルポッピー！ |
| 中文译名 | 缘起甜韵趣恋丛生！ |
| 英文译名 | LOVEPICAL-POPPY! |
| 简称/别名 | ラブピカ |
```

This is critical because:
- mihoyo.ink uploaders mostly use Chinese filenames — 中文名命中率最高
- shinnku raw files (galgame0/) use Japanese filenames — 日文名命中率最高
- English names work as fallback on both sites

Search each site with ALL name variants (Pass 1), then partial terms (Pass 2). Don't search with only one language and give up.

---

## Phase 3: Search Sites

**ALWAYS use OpenCLI browser commands (`opencli browser dl <command>`). Never use WebSearch/WebFetch for site searching — they can't interact with search boxes, handle login walls, or execute JavaScript.**

**Before searching any site, read its reference doc:**
- `references/sites/mihoyo.md` — mihoyo.ink (mandatory: CJK input, Ctrl+K modal, CDN extraction)
- `references/sites.md` — all other sites (shinnku, inarigal, galzy, fh-xy, etc.)
- `references/cjk-input.md` — CJK input protocol and code point reference

### ⚠️ CJK Input — Read This Before Searching

Chinese/Japanese/Korean text gets corrupted when passed through bash. This breaks ALL search attempts on mihoyo.ink and any site with React-controlled inputs.

**→ Read `references/cjk-input.md` for the full protocol and code point reference.**

Quick summary:
- **shinnku**: Navigate via eval with `encodeURIComponent(String.fromCodePoint(...))`
- **mihoyo.ink / Alist**: MUST use `document.execCommand('insertText', false, String.fromCodePoint(...))` — React controlled inputs reject direct `.value =` assignment
- **⛔ NEVER use `/@search?keyword=` URL on mihoyo.ink** — returns "failed get storage"
- **⛔ NEVER truncate state with head/tail** — the Ctrl+K search modal renders at the VERY END of DOM output

### Search Workflow: Find → Extract → Next

**Do NOT batch-search all games then backtrack to extract links.** For each game:
1. Search all name variants (CN/JP/EN from Phase 2)
2. Click best result → detail page → extract CDN immediately
3. Record CDN + password + size
4. Move to next game

This avoids re-searching and re-finding games you already located.

### Path Decision (per game)

```
Found 熟肉? → PATH A: Direct download (go to Phase 4)
No 熟肉?   → PATH B: 生肉 + Patch (two downloads, then go to Phase 4)
```

**For PATH B: both parts are mandatory.** Don't stop after finding 生肉 — must also find a matching patch. Track each game's status as [生肉✅/❌] [补丁✅/❌].

### Search order (by download quality):

**Search in fast serial** — OpenCLI controls one browser. Use `opencli browser dl tab new` to open multiple sites in tabs, then switch tabs (`opencli browser dl tab select <id>`) to search each: fill search → Enter → state → next tab. Each site should take ~30 seconds max.

**For 熟肉 / 生肉 (game bodies):**
1. **shinnku.com** — direct links, IDM. 熟肉 (`zd/`, `0/win/`), 生肉 (`galgame0/`)
2. **mihoyo.ink** — Ctrl+K search, direct links. Game bodies in `柚哩Gal/GAL仓库*`, `梓澪の妙妙屋/合集系列/`. Also check `南+合集/`
3. **inarigal.com** — direct links, has AI汉化
4. **galzy.moe** — direct links (must use searchbox, not URL params)
5. **fh-xy.net** — 百度/夸克 (must click 🔍 to search, links in post body)
6. **qingju.org** — 百度盘, lz4 encrypted
7. **kungal.com / touchgal.ink** — fallback disks

**For Patches (PATH B only):**
1. **mihoyo.ink** — `梓澪の妙妙屋/补丁/汉化补丁归档/2dfan AI翻译补丁合集/`
2. **2dfan.com** — patches (may need login)
3. **moyu.moe** — patch archive
4. **ai2.moe** — fallback

### Auto-Extract Download Info

After getting search results, use `opencli browser dl eval` to automatically extract:
- **Download links**: `document.querySelectorAll('a[href*="pan.baidu.com"], a[href*="pan.quark.cn"], a[href*="drive.uc.cn"], a[href*="shinnku.top"], a[href*="galgamedownload.date"]')`
- **提取码**: regex `提取码[：:]\s*([a-zA-Z0-9]+)` on page text
- **解压密码**: regex `(解压密码|密码)[：:]\s*(.+?)(?:\s|$|\))` on page text
- **File sizes**: look for patterns like `大小[：:]\s*([\d.]+ ?[GM]B)` or `([\d.]+ ?[GM]B)` near the file name

Don't manually copy-paste links — extract programmatically.

### Version selection
When comparing download options, prefer in this order:
1. 熟肉 (Chinese translation) over 生肉 (Japanese only)
2. 汉化硬盘版 / 官中 over 机翻 (machine translation) — users explicitly reject 机翻
3. Non-Steam repacks over Steam versions (user preference)
4. 无码 (uncensored) over 有码 if available — but don't reject a version solely for lacking 无码
5. Single file over split parts (`.7z.001/.002/.003...` — extra reassembly steps)
6. Smaller file size when versions are equivalent
7. Exclude apk/krkr/ons unless mobile requested

### Multi-keyword search (two passes):

**Pass 1 — Full names first.** Search each site with BOTH the full Japanese name AND full Chinese name (most uploaders are Chinese, so files often get Chinese filenames). Don't settle for one — run both.

**Pass 2 — Fallback only if Pass 1 empty.** Combine Chinese/Japanese/English keywords with partial terms. JP name → Chinese name → English → partial → series name.

---

## Phase 3.4: Extract Download Links

### Universal Link Sniffing

**Step A: Read the visual page first.** Take `opencli browser dl state` of the detail/post page. LOOK for:
- Buttons labeled "复制链接", "下载", "获取链接", "点击此处下载"
- `<a>` links containing `pan.baidu.com`, `pan.quark.cn`, `drive.uc.cn`, `shinnku.top`, `galgamedownload.date`
- Text patterns: `提取码`, `解压密码`, `密码`

**Step B: Extract the real URL.** The page URL itself is rarely the download link. Find the link source:
- If there's a "复制链接" / "点击下载" button → intercept clipboard or click to trigger download
- If there are `<a>` tags with cloud URLs → extract href directly via `opencli browser dl eval`
- If the link is hidden (kungal) → click "获取链接" button first

**Step C: Feed to IDM bridge.** Never paste into IDM manually.

⚠️ **Path and filename rules:**
- **Path**: Use Windows backslash from `references/config.json` → `save_directory`, escaped for bash. Forward slash produces `g:/\filename` — NOT a valid Windows path (IDM silently falls back to its default directory, usually C: drive).
- **Filename**: ASCII ONLY. No CJK, no full-width punctuation (！？～ etc.). CJK characters corrupt when passed through bash and the file ends up with a garbled name like `LAMUNATION锛�.7z`.
  - ✅ `NUKITASHI1.rar`, `HENPRI.rar`, `Karikoi.rar`
  - ❌ `LAMUNATION！.7z`, `抜きゲー...rar`

```bash
python idm_bridge.py "<cdn_url>" "<referer>" "<save_dir>\\" "<ascii_filename>" --silent
```

Where `<save_dir>` is the value from `references/config.json` (e.g. `e:\\AllinOne`).

Referer mapping:
- shinnku → `"https://www.shinnku.com/"`
- mihoyo.ink / galgamedownload.date / ali-cdn.mihoyo.fans / alist-public.imoutoheaven.org → `"https://mihoyo.ink/"`

### Per-Site Instructions

**shinnku:** Navigate to file detail page → the "点击此处下载" `<a>` tag href IS the CDN URL. Extract with `opencli browser dl eval` → IDM. Referer: `https://www.shinnku.com/`

**mihoyo.ink / Alist:** Search → click file → detail page has "复制链接" button. Use `opencli browser dl eval` to intercept `navigator.clipboard.writeText()` + `document.execCommand('copy')`, click button, captured URL is `/d/...` which IS the direct download. Feed to IDM. Referer: `https://mihoyo.ink/`. Password on same page.

**inarigal:** Click "下载资源" → wait countdown → capture URL from `opencli browser dl network`. Token expires fast — IDM immediately. Referer: `https://inarigal.com/`

**fh-xy / galgame.dev (Discuz! forums):** Links + passwords are plain text in post body. `opencli browser dl eval` to extract `pan.baidu.com` / `pan.quark.cn` hrefs. Passwords regex from text.

**qingju:** Blog post body → extract `pan.baidu.com` links + `提取码` from text. lz4格式 + 密码 `qingju`.

**kungal:** Click "获取链接" button → reveals hidden link → extract href. Usually 夸克/和彩云.

## Phase 3.5: Verify & Present

### Step 1: Parallel link verification

**Open multiple tabs in OpenCLI** — one tab per link to verify it's alive. In each tab:
- IDM直链: navigate to the detail page, confirm download link exists
- 百度盘: navigate to share link, check it doesn't show "已失效"/"不存在"
- 夸克/UC: navigate to confirm the page loads (not 404/deleted)

If a link is dead, the agent checks backup links from the same post. Only working links make it to the summary.

### Step 2: Present organized by priority

```
=== IDM 直链 (首选) ===
| # | 作品 | 来源 | 大小 |
|---|------|------|------|
| 1 | XXX | shinnku | X GB |

=== 百度盘 (bdpan) ===
| # | 作品 | 链接 | 提取码 |
|---|------|------|--------|
| 2 | YYY | pan.baidu... | xxxx |

=== 其他网盘 (手动) ===
| # | 作品 | 链接 | 密码 |
|---|------|------|------|
| 3 | ZZZ | pan.quark... | xxx |
```

**Ask user: "全下还是挑几部？"**

⛔ **This is a HARD BOUNDARY. Do NOT start any download before user explicitly confirms.**
- STOP all action after presenting the table
- Wait for explicit user confirmation ("下吧", "全下", "挑这几部下")
- If you accidentally started a download during Phase 3, TELL the user immediately
- Only AFTER confirmation, proceed to Phase 4

### Step 3: Fallback when nothing found

**If all sites searched and nothing usable found:**
1. Tell user which sites were searched and what (if anything) was found
2. Ask: *"要不要我自行添加其他有效站点继续搜？还是启用 WebSearch 全网搜索？"*
3. If user provides new site URLs, add them to the search list and re-run Phase 3
4. If user chooses WebSearch, use it to discover new sites/links, then verify with OpenCLI

---

## Phase 4: Execute Download

### Mode A: IDM 直链 (shinnku, galzy, inarigal, mihoyo)

**shinnku: must visit detail page to get real CDN URL** (生肉/熟肉 use different CDN). See `references/cdn.md`.

```bash
python idm_bridge.py "<cdn_url>" "<referer>" "<save_path>" "<filename>" --silent
```

### Mode B: 百度网盘

**Strategy (try in order):**

**1. OpenCLI browser (most reliable)** — navigate to share link, fill code, Baidu client auto-captures:
- `opencli browser dl open "https://pan.baidu.com/s/1xxxxx?pwd=abcd"`
- Baidu client at `D:/APP/BaiduNetdisk/BaiduNetdisk.exe` will auto-launch and handle download

**2. BaiduPCS-Go CLI (fast, multi-threaded)** — if installed:
```bash
# Transfer share → your cloud → download
BaiduPCS-Go transfer <share_link> -p <password>
BaiduPCS-Go download <remote_path> <local_path>
```

**3. bdpan (deprecated, unreliable)** — only as last resort:
```bash
bdpan download "https://pan.baidu.com/s/1xxxxx?pwd=abcd" <save_path>/
```
- error -7 = API rate limit, abandon immediately and switch to #1 or #2

### Mode C: Other disks (夸克/和彩云/阿里)

Show links to user. Suggest switching to shinnku/galzy.

---

## Phase 5: Post-Download

See `references/passwords.md` for site passwords and format handling.

**For resources with passwords**, create a password file in the same save directory.

⚠️ **echo and python -c "中文" both garble Chinese text through bash.** Use Python with chr() code points:

```bash
python -c "text=chr(0x6587)+chr(0x4ef6)+chr(0x540d)+': <ascii_filename>\n'+chr(0x89e3)+chr(0x538b)+chr(0x5bc6)+chr(0x7801)+': <password>\n'+chr(0x4e0b)+chr(0x8f7d)+chr(0x6765)+chr(0x6e90)+': <site>';open('<save_dir>/${ascii_basename}_password.txt','w',encoding='utf-8').write(text)"
```

Common chr() values:
- 文件名 = chr(0x6587)+chr(0x4ef6)+chr(0x540d)
- 解压密码 = chr(0x89e3)+chr(0x538b)+chr(0x5bc6)+chr(0x7801)
- 下载来源 = chr(0x4e0b)+chr(0x8f7d)+chr(0x6765)+chr(0x6e90)

⚠️ **Filename must be ASCII** (`_password.txt`) — CJK in filenames also corrupts.
**Content is Chinese** — constructed safely inside Python via chr(), never passing through bash.

Extract the password from the file detail page — it's usually written near the download button or in the page footer. Don't guess. If the page has no password, skip this step.

---

## Key Rules

### Search
- **Phase 2 is mandatory** — research CN/JP/EN names for EVERY game before Phase 3
- **Phase 3 workflow**: Find game → click best result → extract CDN → next game. Never batch-search then backtrack
- **CJK input** → `references/cjk-input.md`. `execCommand('insertText')` + `String.fromCodePoint()` ONLY
- **⛔ NEVER truncate state** with head/tail — the Ctrl+K search modal renders at the VERY END of DOM
- **⛔ NEVER use `/@search?keyword=` URL** on mihoyo.ink — doesn't work, use Ctrl+K modal
- **Ctrl+K**: if modal not visible, retry up to 3 times before assuming it failed. Use `document.getElementById('search-input') ? 'OPEN' : 'CLOSED'` to verify
- **`input.value = q` does NOT work** on React controlled inputs (mihoyo.ink) — use `execCommand('insertText')`

### Download
- **IDM path**: from `references/config.json` → `save_directory` (Windows backslash, escaped for bash). `g:/` produces `g:/\filename` — invalid path
- **IDM filename**: ASCII only. No CJK, no full-width punctuation
- **IDM TempPath**: must be on same drive as download destination — check in Phase 0
- **Never use `idman /d` CLI** — no Referer support; use `idm_bridge.py`
- **Never guess shinnku CDN URLs** — visit detail page to extract real CDN link
- **Inarigal**: time-limited tokens — capture from network requests and IDM immediately
- **bdpan error -7**: Baidu API rate limit; suggest manual browser download

### Workflow
- **Phase 3.5 is HARD BOUNDARY** — confirm full list with user BEFORE any download
- **If a download starts accidentally** during search, tell user immediately
- **Version preference**: 熟肉 > 生肉, 汉化/官中 > 机翻, 无码 > 有码(if available), non-Steam > Steam, single file > split

### Site-specific
- **fh-xy**: click 🔍 icon first, URL params don't work (Discuz! forum)
- **qingju**: lz4 encryption + password `qingju`
- **Each site has different search method** — check `references/sites.md`
- **Passwords**: extract from file detail page, create `_解压密码.txt` with ASCII basename
