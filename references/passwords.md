# Passwords & Format Notes

## Principle: Extract, Don't Memorize

**Forum posts (fh-xy, galgame.dev) each have their own password.** Don't hardcode — always extract the password from the page content using Phase 3's auto-extract. The password is usually right next to the download link in the post body.

## Site-wide Fixed Passwords

These sites use the same password for ALL resources:

| 站点 | 密码 | 格式 |
|------|------|------|
| **qingju.org** | `qingju` | **lz4 加密** |
| **chgal.com** | `erciyuanfengwo` | 磁力/网盘 |

## No Password

| 站点 | 格式 |
|------|------|
| shinnku.com | .7z / .rar 直接解压 |
| galzy.moe | .rar 直接解压 |
| inarigal.com | .zip 直接解压 |
| mihoyo.ink | 直链 |
| 2DFan | 各补丁独立，需从页面提取 |

## qingju lz4 Handling

1. 文件后缀 `.lz4` → 需先用 lz4 工具解密
2. 解密后再用 WinRAR/7-Zip 解压

密码文件中必须注明:
```
⚠️ 本文件使用 lz4 加密格式，需要先解密再解压
PC 解密教程：https://www.qingju.org/4344.html
手机解密教程：https://www.qingju.org/4346.html
解压密码：qingju
```

## Post-Download

**每次下载完成后创建 `解压密码.txt`**:
```
文件名: <downloaded_filename>
解压密码: <password>
下载来源: <site_url>
<额外说明: lz4格式/需要专用工具等>
```

## Suffix Repair

如果文件实际是 `.7z` 但被改成了 `.rar`（防封），用 7-Zip 检测真实格式，解压失败则提示改后缀。
