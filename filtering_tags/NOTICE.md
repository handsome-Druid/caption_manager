# 第三方数据来源说明

本目录下的标签过滤数据文件并非本项目原创，而是来自第三方开源项目，经复制（vendoring）后纳入本仓库，以保证可复现性与离线可用。

## 来源

- 上游项目：[cyber-meow/anime_screenshot_pipeline](https://github.com/cyber-meow/anime_screenshot_pipeline)
- 来源目录：[configs/tag_filtering](https://github.com/cyber-meow/anime_screenshot_pipeline/tree/main/configs/tag_filtering)
- 许可证：MIT License，Copyright (c) 2022 CyberMeow
- 许可证全文见同目录下的 [`THIRD_PARTY_LICENSE`](./THIRD_PARTY_LICENSE)

## 包含的文件

| 文件 | 说明 |
| --- | --- |
| `blacklist_tags.txt` | 黑名单标签 |
| `character_tags.json` | 角色标签 |
| `overlap_tags.json` | 重叠/冗余标签映射 |
| `overlap_tags_simplified.json` | 简化版重叠标签映射 |

> 提示：如需追踪上游更新，建议在同步时记录所采用的上游 commit hash，以便审计具体版本。
