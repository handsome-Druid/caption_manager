"""一次性分析脚本：对比当前角色.txt 的过滤效果，找出
1) 当前过滤命中的 tag
2) 剩余 caption_set 里疑似角色特征的 tag（推荐补充过滤词）
不动业务代码。"""
import asyncio
from pathlib import Path

from caption_manager.adapters.outbound import CaptionReaderImpl, FlagReaderImpl

# 候选"疑似角色特征"关键词（用 substring 匹配剩余 caption_set，给用户参考）
SUSPECT_KEYWORDS = [
    # 身体部位 / 体型
    "feet", "legs", "toes", "soles", "thigh", "shoulder", "armpit",
    "navel", "stomach", "midriff", "back", "neck", "chest",
    "lips", "eyebrow", "eyelash", "freckle",
    "small breasts", "medium breasts", "large breasts", "flat chest",
    # 五官 / 面部
    "fang", "teeth", "tongue", "mouth", "tooth",
    "blush", "tear", "sweat", "drool",
    # 发型 / 发色（兜底——以防"hair"漏过）
    "hair", "bangs", "braid", "ponytail", "twintail", "sidelock", "ahoge", "bun",
    "blonde", "brunette", "redhead",
    # 瞳色（兜底）
    "eyes", "pupil", "iris", "heterochromia",
    # 角色身份 / 年龄
    "child", "loli", "shota", "aged", "young", "old",
    # 兽耳/尾巴等
    "ears", "tail", "horn", "wing", "halo", "fang",
    # 肤色
    "skin", "dark-skinned", "pale skin", "tan",
    # 表情
    "smile", "grin", "frown", "expression",
]

async def main() -> None:
    reader = CaptionReaderImpl()
    flag_reader = FlagReaderImpl()

    captions = await reader.read_folder("data/ksm copy")
    all_tags: set[str] = captions.caption_set
    flags: list[str] = flag_reader.read("角色")

    # 1) 当前角色.txt 过滤实际命中的 tag（精准匹配，与业务代码一致）
    flag_set = set(flags)
    removed = all_tags & flag_set
    not_hit_flags = [f for f in flags if f not in all_tags]

    print("=== 实际被移除的 tag ===")
    for t in sorted(removed):
        print(f"  - {t}")
    print(f"\n=== 角色.txt 中在本数据集未命中的过滤词 ({len(not_hit_flags)}) ===")
    for f in not_hit_flags:
        print(f"  - {f}")

    remaining = all_tags - removed
    print(f"\n总 tag 数: {len(all_tags)}")
    print(f"将被移除: {len(removed)}")
    print(f"剩余: {len(remaining)}")

    # 2) 在剩余 tag 中扫描"疑似角色特征"（仍用 substring 帮你发现漏网）
    print("\n=== 剩余 tag 中疑似角色特征 substring 命中（供参考，需手动甄别） ===")
    suspect_hit: dict[str, list[str]] = {}
    for kw in SUSPECT_KEYWORDS:
        matched = sorted(t for t in remaining if kw in t)
        if matched:
            suspect_hit[kw] = matched
    for kw, tags in suspect_hit.items():
        print(f"\n[{kw!r}] ({len(tags)})")
        for t in tags:
            print(f"    - {t}")

if __name__ == "__main__":
    asyncio.run(main())
