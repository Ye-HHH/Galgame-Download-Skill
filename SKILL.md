---
name: galgame-download
description: GalGame 下载助手 — 搜索、筛选、下载 galgame 资源。支持全系列下载、模糊推荐、社团补完。TRIGGER: 用户想下载/找 galgame/视觉小说/ADV，提到游戏名/系列/社团（如"对魔忍""柚子社""白色相簿"），或要求找汉化补丁。全语言触发（中日英）。
---

# GalGame 下载助手

## Architecture

```
User request → Claude + Playwright MCP → search sites → filter versions
    → IDM bridge (直链) / bdpan (百度盘) / 展示链接 (其他)
```

---

## Phase 0: Dependency Check

Before doing anything, verify these are available. If missing, fix or skip the related download mode.

| Dependency | Check command | Used for | Required? |
|-----------|---------------|----------|-----------|
| Playwright MCP | Check available tools for `mcp__plugin_playwright_playwright__browser_*` | Browser search on all sites | **Yes** |
| IDM bridge | `ls idm_bridge.py` in skill dir | Direct link downloads | For IDM mode |
| Baidu client | `ls "D:/APP/BaiduNetdisk/BaiduNetdisk.exe"` | 百度盘 (auto-capture) | For 百度 mode |
| BaiduPCS-Go | `which BaiduPCS-Go` | 百度盘 CLI (fast) | Optional, better than bdpan |
| bdpan CLI | `bdpan whoami` | 百度盘 fallback | Deprecated |
| 7z | `ls "/c/Program Files/NVIDIA Corporation/NVIDIA app/7z.exe"` | Archive extraction | Nice to have |

Report what's available. If IDM is missing, skip Mode A (direct links become manual). If bdpan is missing or not logged in, skip Mode B or ask user to login.

---

## Phase 1: Pre-download

First session questions (once answered, reuse for the session):

1. **PC or mobile?** (exe / apk / krkr / ons)
2. **Save directory?** (default: `e:\AllinOne`)
3. **Download mode?** Normal / Silent / Silent+Notify (飞书)

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

---

## Phase 3: Search Sites

**ALWAYS use Playwright MCP (`mcp__plugin_playwright_playwright__browser_*`). Never use WebSearch/WebFetch for site searching — they can't interact with search boxes, handle login walls, or execute JavaScript.**

### Search Discovery Protocol (for ANY site)

Every site is different. Before searching, figure out how it works:

1. **Navigate** to the site homepage
2. **Snapshot** (`browser_snapshot`) — look for:
   - `<textbox>` or `<searchbox>` elements → try typing + Enter
   - 🔍 / magnifying glass icons → click to open search
   - `Ctrl+K` hints (Alist sites)
   - URL structure: try `/?s=keyword` or `/?search=keyword` or `/search?q=keyword`
3. **If URL params don't work** (page shows home, not results) → the site requires interactive search. Use the searchbox or icon found in step 2.
4. **If snapshot is too large** (>1000 lines) → use `browser_evaluate` to extract only links/text matching the game name
5. **Discuz! forums** (powered by Discuz) — URL params rarely work, always click 🔍 icon
6. **Alist sites** (show `Ctrl K` at top) — press `Control+k` to open search modal

**Common failure patterns to avoid:**
- ❌ Assuming `?s=` works everywhere → always test
- ❌ Taking snapshot without first interacting with search → snapshot shows home page
- ❌ Using WebSearch as shortcut → doesn't work for these sites

Cached search methods for known sites → `references/sites.md`

### Path Decision (per game)

```
Found 熟肉? → PATH A: Direct download (go to Phase 4)
No 熟肉?   → PATH B: 生肉 + Patch (two downloads, then go to Phase 4)
```

**For PATH B: both parts are mandatory.** Don't stop after finding 生肉 — must also find a matching patch. Track each game's status as [生肉✅/❌] [补丁✅/❌].

### Search order (by download quality):

**Search in fast serial** — Playwright MCP can only control one page at a time. Use `browser_tabs` to open multiple sites, then switch tabs quickly: fill search → Enter → snapshot → next tab. Each site should take ~30 seconds max.

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

After getting search results, use `browser_evaluate` to automatically extract:
- **Download links**: `document.querySelectorAll('a[href*="pan.baidu.com"], a[href*="pan.quark.cn"], a[href*="drive.uc.cn"], a[href*="shinnku.top"], a[href*="galgamedownload.date"]')`
- **提取码**: regex `提取码[：:]\s*([a-zA-Z0-9]+)` on page text
- **解压密码**: regex `(解压密码|密码)[：:]\s*(.+?)(?:\s|$|\))` on page text
- **File sizes**: look for patterns like `大小[：:]\s*([\d.]+ ?[GM]B)` or `([\d.]+ ?[GM]B)` near the file name

Don't manually copy-paste links — extract programmatically.

### Version selection:
- Prefer 熟肉 over 生肉
- Prefer 整合版 over split parts
- Exclude apk/krkr/ons unless mobile requested

### Multi-keyword search (two passes):

**Pass 1 — Full names first.** Search each site with BOTH the full Japanese name AND full Chinese name (most uploaders are Chinese, so files often get Chinese filenames). Don't settle for one — run both.

**Pass 2 — Fallback only if Pass 1 empty.** Combine Chinese/Japanese/English keywords with partial terms. JP name → Chinese name → English → partial → series name.

---

## Phase 3.4: Extract Download Links

### Universal Link Sniffing

**Step A: Read the visual page first.** Take `browser_snapshot` of the detail/post page. LOOK for:
- Buttons labeled "复制链接", "下载", "获取链接", "点击此处下载"
- `<a>` links containing `pan.baidu.com`, `pan.quark.cn`, `drive.uc.cn`, `shinnku.top`, `galgamedownload.date`
- Text patterns: `提取码`, `解压密码`, `密码`

**Step B: Extract the real URL.** The page URL itself is rarely the download link. Find the link source:
- If there's a "复制链接" / "点击下载" button → intercept clipboard or click to trigger download
- If there are `<a>` tags with cloud URLs → extract href directly via `browser_evaluate`
- If the link is hidden (kungal) → click "获取链接" button first

**Step C: Feed to IDM bridge.** Never paste into IDM manually. Use:
```bash
python idm_bridge.py "<real_download_url>" "<referer>" "g:/" "<filename>" --silent
```

### Per-Site Instructions

**shinnku:** Navigate to file detail page → the "点击此处下载" `<a>` tag href IS the CDN URL. Extract with `browser_evaluate` → IDM. Referer: `https://www.shinnku.com/`

**mihoyo.ink / Alist:** Search → click file → detail page has "复制链接" button. Intercept `navigator.clipboard.writeText()` + `document.execCommand('copy')`, click button, captured URL is `/d/...` which IS the direct download. Feed to IDM. Referer: `https://mihoyo.ink/`. Password on same page.

**inarigal:** Click "下载资源" → wait countdown → capture URL from `browser_network_requests`. Token expires fast — IDM immediately. Referer: `https://inarigal.com/`

**fh-xy / galgame.dev (Discuz! forums):** Links + passwords are plain text in post body. `browser_evaluate` to extract `pan.baidu.com` / `pan.quark.cn` hrefs. Passwords regex from text.

**qingju:** Blog post body → extract `pan.baidu.com` links + `提取码` from text. lz4格式 + 密码 `qingju`.

**kungal:** Click "获取链接" button → reveals hidden link → extract href. Usually 夸克/和彩云.

## Phase 3.5: Verify & Present

### Step 1: Parallel link verification

**Spawn agents in parallel** — one agent per link to verify it's alive. Each agent:
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

**Ask user: "全下还是挑几部？"** Only after user confirms, proceed to Phase 4. **Never switch files on your own — user chose this, download exactly this.**

### Step 3: Fallback when nothing found

**If all sites searched and nothing usable found:**
1. Tell user which sites were searched and what (if anything) was found
2. Ask: *"要不要我自行添加其他有效站点继续搜？还是启用 WebSearch 全网搜索？"*
3. If user provides new site URLs, add them to the search list and re-run Phase 3
4. If user chooses WebSearch, use it to discover new sites/links, then verify with Playwright

---

## Phase 4: Execute Download

### Mode A: IDM 直链 (shinnku, galzy, inarigal, mihoyo)

**shinnku: must visit detail page to get real CDN URL** (生肉/熟肉 use different CDN). See `references/cdn.md`.

```bash
python idm_bridge.py "<cdn_url>" "<referer>" "<save_path>" "<filename>" --silent
```

### Mode B: 百度网盘

**Strategy (try in order):**

**1. Playwright browser (most reliable)** — navigate to share link, fill code, Baidu client auto-captures:
- Open `https://pan.baidu.com/s/1xxxxx?pwd=abcd` in Playwright
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

**Simultaneously with download**, create a `<filename>_解压密码.txt` in the same directory:
```
文件名: <filename>
解压密码: <password>
下载来源: <site>
```
Extract the password from the same page where you found the download link. Don't guess — it's on the same page.

---

## Key Rules

- Never use `idman /d` CLI — no Referer support; use `idm_bridge.py`
- Never guess shinnku CDN URLs — visit detail page to extract real CDN link
- Each site has a different search method — check `references/sites.md`, don't assume URL params work
- `bdpan download` for 百度 share links, use `run_in_background` for >50MB files
- bdpan error -7 = Baidu API rate limit; file is already in cloud, suggest manual browser download
- For qingju: lz4 encryption, must note in password file with tutorial links
- For Alist sites (mihoyo.ink): Ctrl+K search, explore subdirectories
- fh-xy search: click 🔍 icon first, URL params don't work
- Inarigal downloads have time-limited tokens — capture from network requests and IDM immediately
