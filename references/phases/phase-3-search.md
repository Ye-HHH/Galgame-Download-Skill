# Phase 3: Search Sites

**Entry**: Phase 2 complete, name table ready, user confirmed which games.

**Exit**: All games found, download links + sizes + passwords extracted, summary table presented, user confirmed. → Phase 4.

---

## Before Searching

- **Use OpenCLI browser** (`opencli browser dl <cmd>`). Never WebSearch/WebFetch for site searching.
- **Read reference docs first:**
  - `references/sites/mihoyo.md` — mihoyo.ink (mandatory)
  - `references/sites.md` — all other sites
  - `references/cjk-input.md` — CJK input protocol

## CJK Input

Chinese/Japanese/Korean text corrupts through bash. → Read `references/cjk-input.md`.

Quick summary:
- **shinnku**: eval with `encodeURIComponent(String.fromCodePoint(...))`
- **mihoyo.ink / Alist**: `document.execCommand('insertText', false, String.fromCodePoint(...))`
- ⛔ NEVER `/@search?keyword=` URL on mihoyo.ink
- ⛔ NEVER truncate state with head/tail — search modal at VERY END of DOM

## Search Workflow

**Find → Extract → Next.** Never batch-search then backtrack.

1. Search all name variants (CN/JP/EN from Phase 2)
2. Click best result → detail page → extract CDN immediately
3. Record CDN + password + size
4. Move to next game

## Path Decision

```
Found 熟肉? → PATH A: Direct download (Phase 4)
No 熟肉?   → PATH B: 生肉 + Patch (two downloads, then Phase 4)
```

For PATH B: both parts mandatory. Track status: [生肉✅/❌] [补丁✅/❌].

## Search Order

OpenCLI controls one browser. Use tabs (`tab new` / `tab select`) for fast serial searching. ~30s per site.

### Game Bodies (熟肉 / 生肉)

1. **shinnku.com** — IDM direct. 熟肉 (`zd/`, `0/win/`), 生肉 (`galgame0/`)
2. **mihoyo.ink** — Ctrl+K search. 柚哩Gal/GAL仓库*, 梓澪妙妙屋/合集系列/, 南+合集/
3. **inarigal.com** — direct, AI汉化 tag
4. **galzy.moe** — direct (must use searchbox, URL params invalid)
5. **fh-xy.net** — 百度/夸克 (click 🔍 to search)
6. **qingju.org** — 百度盘, lz4 encrypted
7. **kungal.com / touchgal.ink** — fallback

### Patches (PATH B only)

1. **mihoyo.ink** — `梓澪の妙妙屋/补丁/汉化补丁归档/`
2. **2dfan.com** — patches (may need login)
3. **ai2.moe** — AI 去码补丁 → `references/sites/ai2moe.md`
4. **moyu.moe** — patch archive

## Auto-Extract Info

Use `opencli browser dl eval` to extract programmatically:
- **Links**: `document.querySelectorAll('a[href*="pan.baidu.com"], a[href*="pan.quark.cn"], a[href*="shinnku.top"], ...')`
- **提取码**: regex `提取码[：:]\s*([a-zA-Z0-9]+)`
- **解压密码**: regex `(解压密码|密码)[：:]\s*(.+?)(?:\s|$|\))`
- **File sizes**: `大小[：:]\s*([\d.]+ ?[GM]B)` or `([\d.]+ ?[GM]B)` near filename

## Version Selection

Priority: 熟肉 > 生肉, 汉化/官中 > 机翻, non-Steam > Steam, 无码 > 有码(if available), single file > split, smaller > larger, exclude apk/krkr/ons unless mobile.

## Multi-Keyword Search

Pass 1 — Full names (JP + CN). Pass 2 — Partial terms fallback. JP → CN → EN → partial → series.

---

# Phase 3.4: Extract Download Links

→ See `references/sites.md` for per-site instructions.

**Universal flow:**
- **Step A**: Read `opencli browser dl state` of detail page. Look for buttons ("复制链接", "下载", "点击此处下载") and <a> links with cloud URLs.
- **Step B**: Extract real URL. Page URL itself is rarely the download link.
- **Step C**: Feed to IDM bridge. Never paste into IDM manually.

**Path/filename rules:**
- Path: Windows backslash from config → `save_directory`.
- Filename: ASCII ONLY. ✅ `NUKITASHI1.rar` ❌ `LAMUNATION！.7z`

```bash
python idm_bridge.py "<cdn_url>" "<referer>" "<save_dir>\\" "<ascii_filename>" --silent
```

**Referer mapping:**
- shinnku → `"https://www.shinnku.com/"`
- mihoyo.ink / galgamedownload.date / ali-cdn.mihoyo.fans → `"https://mihoyo.ink/"`

**Per-site quick reference:**
- **shinnku**: detail page → "点击此处下载" <a> href = CDN URL
- **mihoyo.ink / Alist**: Search → file detail → "复制链接" button → intercept clipboard
- **inarigal**: "下载资源" → countdown → `opencli browser dl network` capture
- **fh-xy / galgame.dev**: links in post body, regex passwords
- **qingju**: blog post body → 百度 links + 提取码, lz4 + password `qingju`
- **kungal**: "获取链接" button → extract href
- **ai2.moe**: 3-layer flow → `references/sites/ai2moe.md`. IDM + cookie, Python fallback.

---

# Phase 3.5: Verify & Present

### Verify Links

Open multiple OpenCLI tabs to verify each link is alive. Dead link → check backups from same post.

### Present Summary

```
=== IDM 直链 (首选) ===
| # | 作品 | 来源 | 大小 |
|---|------|------|------|

=== 百度盘 (bdpan) ===
| # | 作品 | 链接 | 提取码 |
|---|------|------|--------|

=== 其他网盘 (手动) ===
| # | 作品 | 链接 | 密码 |
|---|------|------|------|
```

### HARD BOUNDARY

⛔ **Do NOT start any download before user explicitly confirms.**
- STOP after presenting the table
- Wait for: "下吧", "全下", "挑这几部下"
- If accidentally started a download during search, tell user immediately
- Only after confirmation → Phase 4

### Fallback

If nothing usable found:
1. Tell user which sites searched + what was found
2. Ask: "要不要添加其他站点？还是 WebSearch 全网搜索？"
3. New site URLs → add to search list, re-run Phase 3
