# Galgame Download Skill

Claude Code skill for searching and downloading galgame/visual novel resources.

## Features

- Multi-site parallel search (17+ download sites)
- IDM direct download + Baidu Netdisk + BaiduPCS-Go
- Raw + patch strategy when no translated version available
- Auto-extract download links, extraction codes, and passwords
- Post-download password file generation

## Installation

```bash
cp -r galgame-download/ ~/.claude/skills/
```

Requires: Playwright MCP, IDM, Python (comtypes)

## Architecture

```
SKILL.md                Main workflow (5 phases)
references/sites.md     17 sites + search methods
references/passwords.md  Password table
references/cdn.md        CDN details + IDM usage
idm_bridge.py            IDM COM bridge
```
