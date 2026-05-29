# Phase 2: Understand the Request

**Entry**: Phase 1 complete, config loaded.

**Exit**: User confirms which games to download. Name table compiled. → Phase 3.

---

## Research

**Web research FIRST** via WebSearch before touching any download site.

### Match the scenario

| User says | Action |
|-----------|--------|
| Game/series name | Research → present overview → ask which entries |
| Vague description ("催泪的") | Research → shortlist 3-5 titles with ratings → let user pick |
| Developer name ("柚子社") | Research → catalog their works → ask which |
| "Patch" / "补丁" for a game | Go to patch flow |

## Series Presentation

For series, present ALL entries with story synopses + tags. Use WebSearch to gather from VNDB/Bangumi/2DFan:

```
作品系列 | 开发商 | 年份范围

| # | 作品 | 年份 | 简介 | 亮点 | 标签 |
|---|------|------|------|------|------|
| 1 | 対魔忍アサギ | 2005 | 近未来日本... | 系列开山作，累计销量35万，动态CG | ADV/调教/触手/凌辱 |
| 2 | アマカノ | 2014 | 主人公搬到雪国温泉小镇... | 纯爱标杆，冬雪氛围感极强 | 纯爱/学园/冬日 |
```

**简介**: 故事设定+主要人物，2-3句，从VNDB/Bangumi/2DFan提炼。
**亮点**: 为什么值得玩——评分、特色、系列地位、奖项。
**标签**: 尽可能全（ADV/纯爱/NTR/调教/触手/学园/拔作/剧情/等等）。

Then ask: "全下还是挑几部？"

## Mandatory Name Research

For EVERY game, compile name variants BEFORE Phase 3:

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
- English names work as fallback

Search each site with ALL name variants (Pass 1), then partial terms (Pass 2).
