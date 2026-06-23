#!/usr/bin/env python3
"""
MORENE W38 常態週(8/27–9/2)圖卡生成腳本
主題: 初秋 · 九月開學季
策略: 攝影主導 + 單色暖底 + 真實琥珀瓶 + 極少字 + Y2K 克制版

SKU 逐日:
  8/27 初秋夜晚 → 乳香(深可可/暗夜底,沉靜)
  8/28 聚光單方 → 玫瑰天竺葵(霧粉/奶油底,花系,學名 Pelargonium graveolens)
  8/29 UGC 九月香氣計畫 → 多瓶概念·甜橙代表(暖白底)
  8/30 文學(梭羅《湖濱散記》) → 乳香+木質 書本道具(米白底,引言印卡)
  8/31 九月晨間儀式 → 甜橙(焦糖/暖橘底)
  9/1  開學通勤輕香 → 苦橙葉(奶油白,極簡)
  9/2  前中後調科普 → 三層色塊圖表(暖色系,代表精油)

命名規則:
  Stories: MORENE_W38_S01 ~ S14
  IG:      MORENE_W38_IG1 ~ IG7
  FB:      MORENE_W38_FB1 ~ FB7
  Reels:   MORENE_W38_R1_f1~f6 / R2_f1~f6 / R3_f1~f6

⚠️ 不放 ISO/GMP/認證標章
⚠️ 不寫療效詞(助眠/修復/治療)
⚠️ CJK tofu 防呆: 含 CJK 字元必用 FONT_ZH / FONT_ZH_BOLD
⚠️ 信任點: IFA 國際芳療師監製 · 學名產地透明 · INCI 公開
"""

import os
import sys
import shutil
sys.path.insert(0, "/Users/morrislin/mw-social-assets/MORENE")

from make_covers_v2 import (
    compose_card,
    FONT_EN_BOLD, FONT_EN, FONT_ZH, FONT_ZH_BOLD,
    CREAM, BLACK, TERRA, MUSTARD, SAGE, WHITE,
    OUT_BASE,
    get_bottle,
)
import make_covers_v2 as _m

# =====================
# W38 色彩補充(VIS 暖色票)
# =====================
WARMSAND   = "#CBA98A"   # 暖沙
CARAMEL    = "#C9853E"   # 焦糖
FOGPINK    = "#E9C5B9"   # 霧粉
FOGBLUE    = "#82A8CC"   # 霧藍
TEAL       = "#8DBFBE"   # 霧藍綠
GREYBROWN  = "#8C8079"   # 灰褐
WARMCREAM  = "#EDE7DC"   # 奶油
GOLDYELLOW = "#E8CE8C"   # 芥末淡
DARKBROWN  = "#3D2B1F"   # 暖棕深(夜晚/沉靜)
WARMWHITE  = "#F5F0E8"   # 暖白
COCOA      = "#2A1A10"   # 深可可(8/27 乳香夜晚底)
DUSTYROSE  = "#D4A49A"   # 深霧粉(玫瑰天竺葵中調底)

# =====================
# 路徑
# =====================
BASE_PROD = "/Users/morrislin/Desktop/MORENE/03_MORENE/03_Assets/A009：MORENE-產品相關/01.產品相關/01. 產品資料/05. 產品照片/素材/商品大圖/01_精油"
DESK_ASSETS = "/Users/morrislin/Desktop/MORENE/MORENE_社群營運_Social/03_圖卡_Assets"

# W38 瓶子路徑
EXTRA_BOTTLES = {
    "乳香":       f"{BASE_PROD}/5MOEO009_乳香/MORENE_精油瓶_去背_乳香.png",
    "玫瑰天竺葵": f"{BASE_PROD}/5MOEO025_玫瑰天竺葵/MORENE_精油瓶_去背_玫瑰天竺葵.png",
    "甜橙":       f"{BASE_PROD}/甜橙/MORENE_精油瓶_去背_甜橙.png",
    "苦橙葉":     f"{BASE_PROD}/苦橙葉/MORENE_精油瓶_去背_苦橙葉.png",
    "真正薰衣草": f"{BASE_PROD}/5MOEO015_真正薰衣草/MORENE_精油瓶_去背_真正薰衣草.png",
    "大西洋雪松": f"{BASE_PROD}/5MOEO005_大西洋雪松/MORENE_精油瓶_去背_大西洋雪松.png",
}

_orig_get_bottle = _m.get_bottle
def _patched_get_bottle(name):
    if name in EXTRA_BOTTLES:
        return EXTRA_BOTTLES[name]
    return _orig_get_bottle(name)
_m.get_bottle = _patched_get_bottle

# =====================
# CJK tofu 防呆
# =====================
def _has_cjk(text):
    for ch in text:
        cp = ord(ch)
        if cp == 0x00B7:
            continue
        if (0x4E00 <= cp <= 0x9FFF or
                0x3400 <= cp <= 0x4DBF or
                0x3000 <= cp <= 0x303F or
                0xF900 <= cp <= 0xFAFF or
                0x2E80 <= cp <= 0x2EFF or
                0xFF00 <= cp <= 0xFFEF or
                0x3040 <= cp <= 0x30FF or
                0xFE30 <= cp <= 0xFE4F):
            return True
    return False

_ZH_FONTS = {FONT_ZH, FONT_ZH_BOLD}

def assert_no_cjk_tofu(text_lines, card_name=""):
    for (text, fpath, fsize, color, xf, yf, anc) in text_lines:
        if text == "MORENE":
            continue
        if _has_cjk(text) and fpath not in _ZH_FONTS:
            raise ValueError(
                f"[tofu guard] {card_name}: CJK text '{text}' "
                f"uses non-ZH font {os.path.basename(fpath)}. "
                f"Must use FONT_ZH or FONT_ZH_BOLD."
            )

# =====================
# 雙寫輔助
# =====================
def dual_save(week: str, channel: str, filename: str, src_path: str):
    if not filename.startswith("MORENE_"):
        raise ValueError(f"Filename must start with MORENE_: {filename}")
    desk_dir = f"{DESK_ASSETS}/{week}/{channel}"
    os.makedirs(desk_dir, exist_ok=True)
    desk_path = f"{desk_dir}/{filename}"
    shutil.copy2(src_path, desk_path)
    print(f"  dual-write -> {desk_path}")

def save_and_dual(week: str, channel: str, filename: str, **compose_kwargs):
    if not filename.startswith("MORENE_"):
        raise ValueError(f"Filename must start with MORENE_: {filename}")
    assert_no_cjk_tofu(compose_kwargs.get("text_lines", []), card_name=filename)
    nas_dir = f"{OUT_BASE}/{week}/{channel}"
    os.makedirs(nas_dir, exist_ok=True)
    nas_path = f"{nas_dir}/{filename}"
    compose_card(out_path=nas_path, **compose_kwargs)
    dual_save(week, channel, filename, nas_path)
    return nas_path


# =====================================================================
# STORIES ×14  (1080×1920)
# 命名: MORENE_W38_S01 ~ MORENE_W38_S14
# 每日 2 則:類型輪替 互動/情境/預告導流
# 8/27 S01-02 / 8/28 S03-04 / 8/29 S05-06
# 8/30 S07-08 / 8/31 S09-10 / 9/1 S11-12 / 9/2 S13-14
# =====================================================================
def make_stories():
    print("\n=== W38 Stories S01–S14 ===")

    # S01 8/27 初秋夜晚投票 — 深可可底 + 乳香 (互動)
    print("S01 8/27 初秋夜晚投票...")
    save_and_dual(
        "W38", "Stories", "MORENE_W38_S01.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=COCOA,
        bottle_name="乳香",
        bottle_scale=0.50,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.76,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=36, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("W38 · 8/27", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("初秋夜晚", FONT_ZH, 90, WARMCREAM, 0.055, 0.130, "tl"),
            ("你的晚間香氣是什麼?", FONT_ZH, 40, GOLDYELLOW, 0.055, 0.288, "tl"),
            ("投票告訴我們 ↓", FONT_ZH, 30, WARMCREAM, 0.055, 0.360, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S02 8/27 乳香導流 — 深可可底 + 乳香 (預告)
    print("S02 8/27 乳香導流...")
    save_and_dual(
        "W38", "Stories", "MORENE_W38_S02.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=DARKBROWN,
        bottle_name="乳香",
        bottle_scale=0.52,
        bottle_x_frac=0.66,
        bottle_bottom_frac=0.76,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=36, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("W38 · 8/27", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("乳香", FONT_ZH, 100, WARMCREAM, 0.055, 0.130, "tl"),
            ("初秋夜晚的沉靜", FONT_ZH, 44, GOLDYELLOW, 0.055, 0.270, "tl"),
            ("主頁看圖文 →", FONT_ZH, 30, WARMCREAM, 0.055, 0.354, "tl"),
            ("Boswellia carterii", FONT_EN, 22, GREYBROWN, 0.055, 0.412, "tl"),
            ("印度 · 樹脂 · 木質溫暖", FONT_ZH, 26, GREYBROWN, 0.055, 0.462, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S03 8/28 玫瑰天竺葵問答 — 霧粉底 + 玫瑰天竺葵 (互動)
    print("S03 8/28 玫瑰天竺葵問答...")
    save_and_dual(
        "W38", "Stories", "MORENE_W38_S03.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=FOGPINK,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W38 · 8/28", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("你聞過", FONT_ZH, 80, BLACK, 0.055, 0.130, "tl"),
            ("玫瑰天竺葵嗎?", FONT_ZH, 58, TERRA, 0.055, 0.254, "tl"),
            ("留言告訴我們你的感受", FONT_ZH, 30, BLACK, 0.055, 0.364, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S04 8/28 玫瑰天竺葵導流 — 奶油底 + 玫瑰天竺葵 (預告)
    print("S04 8/28 玫瑰天竺葵導流...")
    save_and_dual(
        "W38", "Stories", "MORENE_W38_S04.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMCREAM,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.54,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W38 · 8/28", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("玫瑰天竺葵", FONT_ZH, 72, BLACK, 0.055, 0.130, "tl"),
            ("Pelargonium graveolens", FONT_EN, 24, TERRA, 0.055, 0.256, "tl"),
            ("法國 · 花香 · 蒸氣蒸餾", FONT_ZH, 28, BLACK, 0.055, 0.316, "tl"),
            ("主頁看全文 →", FONT_ZH, 32, TERRA, 0.055, 0.378, "tl"),
            ("IFA 國際芳療師監製 · 學名產地透明", FONT_ZH, 20, GREYBROWN, 0.055, 0.438, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S05 8/29 UGC 九月香氣計畫 — 暖白底 + 甜橙 (互動)
    print("S05 8/29 UGC 互動...")
    save_and_dual(
        "W38", "Stories", "MORENE_W38_S05.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMWHITE,
        bottle_name="甜橙",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=34, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W38 · 8/29", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("九月", FONT_ZH, 110, BLACK, 0.055, 0.130, "tl"),
            ("香氣計畫", FONT_ZH, 68, TERRA, 0.055, 0.298, "tl"),
            ("你這個月用什麼精油?", FONT_ZH, 32, BLACK, 0.055, 0.402, "tl"),
            ("標記 @morene_organic", FONT_ZH, 26, GREYBROWN, 0.055, 0.458, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S06 8/29 UGC 導流 — 暖白底 + 甜橙 (預告)
    print("S06 8/29 UGC 導流...")
    save_and_dual(
        "W38", "Stories", "MORENE_W38_S06.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMWHITE,
        bottle_name="甜橙",
        bottle_scale=0.52,
        bottle_x_frac=0.66,
        bottle_bottom_frac=0.78,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=36, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W38 · 8/29", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("分享你的", FONT_ZH, 76, BLACK, 0.055, 0.130, "tl"),
            ("九月精油", FONT_ZH, 76, CARAMEL, 0.055, 0.248, "tl"),
            ("主頁看大家的分享 →", FONT_ZH, 30, BLACK, 0.055, 0.362, "tl"),
            ("甜橙 · Citrus sinensis", FONT_ZH, 24, GREYBROWN, 0.055, 0.418, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S07 8/30 文學引言卡 — 米白底 + 乳香 (情境)
    print("S07 8/30 文學引言...")
    save_and_dual(
        "W38", "Stories", "MORENE_W38_S07.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMWHITE,
        bottle_name="乳香",
        bottle_scale=0.48,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.76,
        shadow_offset_x=44, shadow_offset_y=18,
        shadow_blur=34, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("文學 × 芳療", FONT_ZH, 20, GREYBROWN, 0.055, 0.092, "tl"),
            ("我步入叢林", FONT_ZH, 58, BLACK, 0.055, 0.130, "tl"),
            ("是因為我想從容地生活", FONT_ZH, 38, BLACK, 0.055, 0.218, "tl"),
            ("只面對生活中真正重要的事", FONT_ZH, 38, BLACK, 0.055, 0.282, "tl"),
            ("—— 梭羅《湖濱散記》", FONT_ZH, 22, GREYBROWN, 0.055, 0.350, "tl"),
            ("Walden, Henry David Thoreau, 1854", FONT_EN, 18, GREYBROWN, 0.055, 0.394, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S08 8/30 文學導流 — 米白底 + 乳香 (預告)
    print("S08 8/30 文學導流...")
    save_and_dual(
        "W38", "Stories", "MORENE_W38_S08.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMSAND,
        bottle_name="乳香",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W38 · 8/30", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("梭羅與香氣", FONT_ZH, 68, BLACK, 0.055, 0.130, "tl"),
            ("主頁看芳療誌 →", FONT_ZH, 46, TERRA, 0.055, 0.246, "tl"),
            ("從容生活的香氣哲學", FONT_ZH, 30, BLACK, 0.055, 0.342, "tl"),
            ("Boswellia carterii · 印度", FONT_ZH, 20, GREYBROWN, 0.055, 0.400, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S09 8/31 晨間儀式問答 — 焦糖底 + 甜橙 (互動)
    print("S09 8/31 晨間儀式問答...")
    save_and_dual(
        "W38", "Stories", "MORENE_W38_S09.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=CARAMEL,
        bottle_name="甜橙",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W38 · 8/31", FONT_EN, 14, DARKBROWN, 0.055, 0.092, "tl"),
            ("你的晨間", FONT_ZH, 80, BLACK, 0.055, 0.130, "tl"),
            ("第一件事是什麼?", FONT_ZH, 48, DARKBROWN, 0.055, 0.254, "tl"),
            ("投票 ↓", FONT_ZH, 40, BLACK, 0.055, 0.358, "tl"),
            ("A  聞精油(香氣啟動)", FONT_ZH, 28, BLACK, 0.055, 0.440, "tl"),
            ("B  泡咖啡(氣味同感)", FONT_ZH, 28, BLACK, 0.055, 0.494, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, DARKBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S10 8/31 甜橙導流 — 焦糖底 + 甜橙 (預告)
    print("S10 8/31 甜橙導流...")
    save_and_dual(
        "W38", "Stories", "MORENE_W38_S10.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMCREAM,
        bottle_name="甜橙",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W38 · 8/31", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("晨間精選", FONT_ZH, 76, BLACK, 0.055, 0.130, "tl"),
            ("甜橙 · 九月的早晨", FONT_ZH, 44, CARAMEL, 0.055, 0.254, "tl"),
            ("主頁看圖文 →", FONT_ZH, 32, BLACK, 0.055, 0.346, "tl"),
            ("Citrus sinensis", FONT_EN, 22, GREYBROWN, 0.055, 0.406, "tl"),
            ("澳洲 · 柑橘 · 冷壓萃取", FONT_ZH, 26, BLACK, 0.055, 0.456, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S11 9/1 通勤輕香問答 — 奶油白底 + 苦橙葉 (互動)
    print("S11 9/1 通勤問答...")
    save_and_dual(
        "W38", "Stories", "MORENE_W38_S11.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMCREAM,
        bottle_name="苦橙葉",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=34, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W38 · 9/1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("通勤香氣", FONT_ZH, 80, BLACK, 0.055, 0.130, "tl"),
            ("你選哪種輕薄感?", FONT_ZH, 48, TERRA, 0.055, 0.262, "tl"),
            ("投票 ↓", FONT_ZH, 36, BLACK, 0.055, 0.362, "tl"),
            ("A  苦橙葉(輕木質·沉穩)", FONT_ZH, 26, BLACK, 0.055, 0.430, "tl"),
            ("B  佛手柑(柑橘·明亮)", FONT_ZH, 26, BLACK, 0.055, 0.480, "tl"),
            ("情境使用非療效 · 趣味體驗非診斷 · MORENE", FONT_ZH, 15, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S12 9/1 苦橙葉導流 — 奶油白底 + 苦橙葉 (預告)
    print("S12 9/1 苦橙葉導流...")
    save_and_dual(
        "W38", "Stories", "MORENE_W38_S12.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMCREAM,
        bottle_name="苦橙葉",
        bottle_scale=0.54,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W38 · 9/1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("苦橙葉", FONT_ZH, 84, BLACK, 0.055, 0.130, "tl"),
            ("Petitgrain bigarade", FONT_EN, 26, TERRA, 0.055, 0.254, "tl"),
            ("巴拉圭 · 葉片 · 蒸氣蒸餾", FONT_ZH, 28, BLACK, 0.055, 0.318, "tl"),
            ("通勤最適合的輕薄香調", FONT_ZH, 26, GREYBROWN, 0.055, 0.372, "tl"),
            ("主頁看全文 →", FONT_ZH, 32, TERRA, 0.055, 0.432, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S13 9/2 前中後調投票 — 暖白底 + 乳香 (互動)
    print("S13 9/2 前中後調投票...")
    save_and_dual(
        "W38", "Stories", "MORENE_W38_S13.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMWHITE,
        bottle_name="乳香",
        bottle_scale=0.50,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.76,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=34, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W38 · 9/2", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("你最常聞到", FONT_ZH, 68, BLACK, 0.055, 0.130, "tl"),
            ("哪個香調?", FONT_ZH, 68, TERRA, 0.055, 0.236, "tl"),
            ("前調  柑橘 · 草本(前15分鐘)", FONT_ZH, 26, BLACK, 0.055, 0.352, "tl"),
            ("中調  花香 · 辛香(20–60分鐘)", FONT_ZH, 26, BLACK, 0.055, 0.406, "tl"),
            ("後調  木質 · 樹脂(1小時後)", FONT_ZH, 26, BLACK, 0.055, 0.460, "tl"),
            ("情境使用 · 趣味體驗非診斷 · MORENE", FONT_ZH, 15, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S14 9/2 前中後調導流 — 暖沙底 + 甜橙(前調) (預告)
    print("S14 9/2 前中後調導流...")
    save_and_dual(
        "W38", "Stories", "MORENE_W38_S14.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMSAND,
        bottle_name="甜橙",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W38 · 9/2", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("前中後調全解析", FONT_ZH, 62, BLACK, 0.055, 0.130, "tl"),
            ("主頁看圖解 →", FONT_ZH, 44, TERRA, 0.055, 0.242, "tl"),
            ("懂了層次 · 聞香更有感", FONT_ZH, 30, BLACK, 0.055, 0.340, "tl"),
            ("SCENT NOTES · ACCORDS · MORENE.COM.TW", FONT_EN, 18, GREYBROWN, 0.055, 0.402, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    print("W38 Stories 完成。")


# =====================================================================
# IG ×7 (1080×1350) + FB ×7 (1080×1080) 同主題雙出
# 命名: MORENE_W38_IG1~IG7 / MORENE_W38_FB1~FB7
# =====================================================================
def make_ig_fb():
    print("\n=== W38 IG+FB ===")

    # --------------------------------------------------
    # IG1/FB1 8/27 初秋夜晚乳香 — 深可可底
    # --------------------------------------------------
    print("IG1 8/27 初秋夜晚乳香...")
    save_and_dual(
        "W38", "IG", "MORENE_W38_IG1.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=COCOA,
        bottle_name="乳香",
        bottle_scale=0.62,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.88,
        shadow_offset_x=58, shadow_offset_y=26,
        shadow_blur=42, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, WARMCREAM, 0.055, 0.048, "tl"),
            ("01 / 07", FONT_EN, 14, GREYBROWN, 0.870, 0.048, "tl"),
            ("初秋夜晚", FONT_ZH, 96, WARMCREAM, 0.055, 0.094, "tl"),
            ("沉靜一下", FONT_ZH, 64, GOLDYELLOW, 0.055, 0.268, "tl"),
            ("乳香 · Boswellia carterii", FONT_ZH, 28, GREYBROWN, 0.055, 0.376, "tl"),
            ("印度 · 樹脂 · 木質溫暖", FONT_ZH, 24, GREYBROWN, 0.055, 0.422, "tl"),
            ("初秋情境 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ],
    )

    print("FB1 8/27 初秋夜晚乳香...")
    save_and_dual(
        "W38", "FB", "MORENE_W38_FB1.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=COCOA,
        bottle_name="乳香",
        bottle_scale=0.68,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.92,
        shadow_offset_x=62, shadow_offset_y=28,
        shadow_blur=44, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, WARMCREAM, 0.055, 0.048, "tl"),
            ("初秋夜晚", FONT_ZH, 84, WARMCREAM, 0.055, 0.100, "tl"),
            ("沉靜一下", FONT_ZH, 56, GOLDYELLOW, 0.055, 0.260, "tl"),
            ("乳香 · Boswellia carterii", FONT_ZH, 26, GREYBROWN, 0.055, 0.362, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG2/FB2 8/28 玫瑰天竺葵單方 — 霧粉/奶油底
    # --------------------------------------------------
    print("IG2 8/28 玫瑰天竺葵...")
    save_and_dual(
        "W38", "IG", "MORENE_W38_IG2.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=FOGPINK,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.64,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.88,
        shadow_offset_x=60, shadow_offset_y=26,
        shadow_blur=42, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("02 / 07", FONT_EN, 14, GREYBROWN, 0.870, 0.048, "tl"),
            ("玫瑰天竺葵", FONT_ZH, 68, BLACK, 0.055, 0.094, "tl"),
            ("Pelargonium graveolens", FONT_EN, 26, TERRA, 0.055, 0.218, "tl"),
            ("法國 · 花香 · 蒸氣蒸餾", FONT_ZH, 28, BLACK, 0.055, 0.282, "tl"),
            ("初秋的第一支花香系精油", FONT_ZH, 26, GREYBROWN, 0.055, 0.340, "tl"),
            ("IFA 國際芳療師監製 · 學名產地透明", FONT_ZH, 20, GREYBROWN, 0.055, 0.400, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ],
    )

    print("FB2 8/28 玫瑰天竺葵...")
    save_and_dual(
        "W38", "FB", "MORENE_W38_FB2.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=FOGPINK,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.70,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.92,
        shadow_offset_x=62, shadow_offset_y=28,
        shadow_blur=44, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("玫瑰天竺葵", FONT_ZH, 60, BLACK, 0.055, 0.100, "tl"),
            ("Pelargonium graveolens", FONT_EN, 22, TERRA, 0.055, 0.214, "tl"),
            ("法國 · 花香 · 蒸氣蒸餾", FONT_ZH, 26, BLACK, 0.055, 0.276, "tl"),
            ("IFA 國際芳療師監製 · 學名產地透明", FONT_ZH, 18, GREYBROWN, 0.055, 0.334, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG3/FB3 8/29 UGC 九月香氣計畫 — 暖白底 + 甜橙
    # --------------------------------------------------
    print("IG3 8/29 UGC...")
    save_and_dual(
        "W38", "IG", "MORENE_W38_IG3.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=WARMWHITE,
        bottle_name="甜橙",
        bottle_scale=0.62,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.88,
        shadow_offset_x=58, shadow_offset_y=25,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("03 / 07", FONT_EN, 14, GREYBROWN, 0.870, 0.048, "tl"),
            ("九月香氣計畫", FONT_ZH, 58, BLACK, 0.055, 0.094, "tl"),
            ("你這個月用什麼精油?", FONT_ZH, 40, TERRA, 0.055, 0.216, "tl"),
            ("分享你的九月香氣", FONT_ZH, 32, BLACK, 0.055, 0.306, "tl"),
            ("留言 or 標記 @morene_organic", FONT_ZH, 26, BLACK, 0.055, 0.360, "tl"),
            ("我們會轉發分享", FONT_ZH, 24, GREYBROWN, 0.055, 0.414, "tl"),
            ("UGC · 情境使用非療效 · MORENE.COM.TW", FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ],
    )

    print("FB3 8/29 UGC...")
    save_and_dual(
        "W38", "FB", "MORENE_W38_FB3.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=WARMWHITE,
        bottle_name="甜橙",
        bottle_scale=0.68,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.92,
        shadow_offset_x=60, shadow_offset_y=26,
        shadow_blur=42, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("九月香氣計畫", FONT_ZH, 52, BLACK, 0.055, 0.100, "tl"),
            ("你這個月用什麼精油?", FONT_ZH, 36, TERRA, 0.055, 0.214, "tl"),
            ("標記 @morene_organic", FONT_ZH, 24, BLACK, 0.055, 0.306, "tl"),
            ("情境使用非療效 · MORENE.COM.TW", FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG4/FB4 8/30 梭羅《湖濱散記》文學 — 米白底 + 乳香
    # --------------------------------------------------
    print("IG4 8/30 梭羅文學...")
    save_and_dual(
        "W38", "IG", "MORENE_W38_IG4.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=WARMWHITE,
        bottle_name="乳香",
        bottle_scale=0.60,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.88,
        shadow_offset_x=56, shadow_offset_y=24,
        shadow_blur=42, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("04 / 07", FONT_EN, 14, GREYBROWN, 0.870, 0.048, "tl"),
            ("我步入叢林", FONT_ZH, 62, BLACK, 0.055, 0.094, "tl"),
            ("是因為我想從容地生活", FONT_ZH, 36, BLACK, 0.055, 0.198, "tl"),
            ("只面對生活中真正重要的事", FONT_ZH, 36, BLACK, 0.055, 0.254, "tl"),
            ("—— 梭羅《湖濱散記》1854", FONT_ZH, 22, GREYBROWN, 0.055, 0.318, "tl"),
            ("乳香 · Boswellia carterii · 印度", FONT_ZH, 24, TERRA, 0.055, 0.382, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ],
    )

    print("FB4 8/30 梭羅文學...")
    save_and_dual(
        "W38", "FB", "MORENE_W38_FB4.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=WARMWHITE,
        bottle_name="乳香",
        bottle_scale=0.66,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.92,
        shadow_offset_x=58, shadow_offset_y=26,
        shadow_blur=42, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("我步入叢林", FONT_ZH, 56, BLACK, 0.055, 0.100, "tl"),
            ("是因為我想從容地生活", FONT_ZH, 32, BLACK, 0.055, 0.196, "tl"),
            ("只面對生活中真正重要的事", FONT_ZH, 32, BLACK, 0.055, 0.250, "tl"),
            ("—— 梭羅《湖濱散記》", FONT_ZH, 20, GREYBROWN, 0.055, 0.308, "tl"),
            ("乳香 · Boswellia carterii", FONT_ZH, 22, TERRA, 0.055, 0.368, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG5/FB5 8/31 九月晨間甜橙 — 焦糖/暖橘底
    # --------------------------------------------------
    print("IG5 8/31 晨間甜橙...")
    save_and_dual(
        "W38", "IG", "MORENE_W38_IG5.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=CARAMEL,
        bottle_name="甜橙",
        bottle_scale=0.64,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.88,
        shadow_offset_x=60, shadow_offset_y=26,
        shadow_blur=42, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("05 / 07", FONT_EN, 14, DARKBROWN, 0.870, 0.048, "tl"),
            ("九月晨間", FONT_ZH, 88, BLACK, 0.055, 0.094, "tl"),
            ("甜橙 · 光的味道", FONT_ZH, 44, DARKBROWN, 0.055, 0.260, "tl"),
            ("Citrus sinensis", FONT_EN, 24, DARKBROWN, 0.055, 0.340, "tl"),
            ("澳洲 · 柑橘 · 冷壓萃取", FONT_ZH, 26, DARKBROWN, 0.055, 0.396, "tl"),
            ("IFA 國際芳療師監製 · 學名產地透明", FONT_ZH, 20, DARKBROWN, 0.055, 0.448, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 15, DARKBROWN, 0.055, 0.946, "tl"),
        ],
    )

    print("FB5 8/31 晨間甜橙...")
    save_and_dual(
        "W38", "FB", "MORENE_W38_FB5.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=CARAMEL,
        bottle_name="甜橙",
        bottle_scale=0.70,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.92,
        shadow_offset_x=62, shadow_offset_y=28,
        shadow_blur=44, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("九月晨間", FONT_ZH, 76, BLACK, 0.055, 0.100, "tl"),
            ("甜橙 · 光的味道", FONT_ZH, 40, DARKBROWN, 0.055, 0.250, "tl"),
            ("Citrus sinensis · 澳洲 · 冷壓", FONT_ZH, 22, DARKBROWN, 0.055, 0.336, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 14, DARKBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG6/FB6 9/1 開學通勤苦橙葉 — 奶油白底 · 極簡
    # --------------------------------------------------
    print("IG6 9/1 通勤苦橙葉...")
    save_and_dual(
        "W38", "IG", "MORENE_W38_IG6.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=WARMCREAM,
        bottle_name="苦橙葉",
        bottle_scale=0.64,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.88,
        shadow_offset_x=58, shadow_offset_y=25,
        shadow_blur=40, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("06 / 07", FONT_EN, 14, GREYBROWN, 0.870, 0.048, "tl"),
            ("苦橙葉", FONT_ZH, 90, BLACK, 0.055, 0.094, "tl"),
            ("Petitgrain bigarade", FONT_EN, 28, TERRA, 0.055, 0.262, "tl"),
            ("巴拉圭 · 葉片 · 蒸氣蒸餾", FONT_ZH, 26, BLACK, 0.055, 0.328, "tl"),
            ("開學通勤的輕薄香氣", FONT_ZH, 26, GREYBROWN, 0.055, 0.380, "tl"),
            ("IFA 國際芳療師監製 · 學名產地透明", FONT_ZH, 20, GREYBROWN, 0.055, 0.432, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ],
    )

    print("FB6 9/1 通勤苦橙葉...")
    save_and_dual(
        "W38", "FB", "MORENE_W38_FB6.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=WARMCREAM,
        bottle_name="苦橙葉",
        bottle_scale=0.70,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.92,
        shadow_offset_x=60, shadow_offset_y=26,
        shadow_blur=42, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("苦橙葉", FONT_ZH, 78, BLACK, 0.055, 0.100, "tl"),
            ("Petitgrain bigarade", FONT_EN, 24, TERRA, 0.055, 0.240, "tl"),
            ("巴拉圭 · 葉片 · 蒸氣蒸餾", FONT_ZH, 24, BLACK, 0.055, 0.300, "tl"),
            ("開學通勤的輕薄香氣", FONT_ZH, 22, GREYBROWN, 0.055, 0.354, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG7/FB7 9/2 前中後調圖表 — 三層暖色 + 乳香(後調代表)
    # --------------------------------------------------
    print("IG7 9/2 前中後調圖表...")
    save_and_dual(
        "W38", "IG", "MORENE_W38_IG7.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=WARMSAND,
        bottle_name="乳香",
        bottle_scale=0.60,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.88,
        shadow_offset_x=56, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("07 / 07", FONT_EN, 14, GREYBROWN, 0.870, 0.048, "tl"),
            ("前調", FONT_ZH, 60, CARAMEL, 0.055, 0.094, "tl"),
            ("柑橘 · 草本 · 前15分鐘 · 甜橙/苦橙葉", FONT_ZH, 24, BLACK, 0.055, 0.172, "tl"),
            ("中調", FONT_ZH, 60, TERRA, 0.055, 0.234, "tl"),
            ("花香 · 辛香 · 20–60分鐘 · 玫瑰天竺葵", FONT_ZH, 24, BLACK, 0.055, 0.314, "tl"),
            ("後調", FONT_ZH, 60, DARKBROWN, 0.055, 0.374, "tl"),
            ("木質 · 樹脂 · 1小時後 · 乳香/大西洋雪松", FONT_ZH, 24, BLACK, 0.055, 0.454, "tl"),
            ("換季搭配全解析 · MORENE 芳療誌", FONT_ZH, 22, GREYBROWN, 0.055, 0.524, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ],
    )

    print("FB7 9/2 前中後調圖表...")
    save_and_dual(
        "W38", "FB", "MORENE_W38_FB7.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=WARMSAND,
        bottle_name="乳香",
        bottle_scale=0.66,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.92,
        shadow_offset_x=58, shadow_offset_y=26,
        shadow_blur=42, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("前調 · 中調 · 後調", FONT_ZH, 48, BLACK, 0.055, 0.100, "tl"),
            ("前調  甜橙/苦橙葉(前15分鐘)", FONT_ZH, 24, CARAMEL, 0.055, 0.212, "tl"),
            ("中調  玫瑰天竺葵(20–60分鐘)", FONT_ZH, 24, TERRA, 0.055, 0.264, "tl"),
            ("後調  乳香/大西洋雪松(1小時後)", FONT_ZH, 24, DARKBROWN, 0.055, 0.316, "tl"),
            ("換季搭配 · 芳療誌全解析", FONT_ZH, 22, GREYBROWN, 0.055, 0.378, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    print("W38 IG+FB 完成。")


# =====================================================================
# REELS ×3 各6幀 (1080×1920)
# R1: 8/27 初秋夜晚沉靜儀式 (乳香)
# R2: 8/30 梭羅×香氣(湖濱散記減法)
# R3: 9/2 前中後調換季搭配
# =====================================================================
def make_reels():
    print("\n=== W38 Reels ===")

    # ----------------------------------------------------------------
    # R1: 8/27 初秋夜晚沉靜儀式(乳香)
    # ----------------------------------------------------------------
    print("--- R1 初秋夜晚儀式 ---")

    # R1-f1 開場:深夜場景/標題 — 深可可底
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R1_f1.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=COCOA,
        bottle_name="乳香",
        bottle_scale=0.56,
        bottle_x_frac=0.64,
        bottle_bottom_frac=0.78,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=38, shadow_opacity=0.08,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("初秋夜晚", FONT_ZH, 96, WARMCREAM, 0.055, 0.130, "tl"),
            ("沉靜儀式", FONT_ZH, 68, GOLDYELLOW, 0.055, 0.296, "tl"),
            ("乳香 · 深可可夜底", FONT_ZH, 28, GREYBROWN, 0.055, 0.388, "tl"),
        ],
    )

    # R1-f2 乳香介紹 — 暖棕底
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R1_f2.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=DARKBROWN,
        bottle_name="乳香",
        bottle_scale=0.58,
        bottle_x_frac=0.64,
        bottle_bottom_frac=0.80,
        shadow_offset_x=52, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("乳香", FONT_ZH, 110, WARMCREAM, 0.055, 0.130, "tl"),
            ("Boswellia carterii", FONT_EN, 26, GREYBROWN, 0.055, 0.304, "tl"),
            ("印度 · 樹脂 · 木質溫暖", FONT_ZH, 28, GREYBROWN, 0.055, 0.362, "tl"),
        ],
    )

    # R1-f3 情境:夜晚書桌 — 暗夜奶油底
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R1_f3.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=COCOA,
        bottle_name="乳香",
        bottle_scale=0.55,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22,
        shadow_blur=38, shadow_opacity=0.08,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("夜晚的書桌", FONT_ZH, 72, WARMCREAM, 0.055, 0.130, "tl"),
            ("需要一點木質的重量", FONT_ZH, 36, GOLDYELLOW, 0.055, 0.256, "tl"),
            ("乳香最適合這個時刻", FONT_ZH, 28, GREYBROWN, 0.055, 0.324, "tl"),
            ("情境使用 · 非療效宣稱", FONT_ZH, 18, GREYBROWN, 0.055, 0.380, "tl"),
        ],
    )

    # R1-f4 學名透明 — 暖沙底
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R1_f4.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMSAND,
        bottle_name="乳香",
        bottle_scale=0.58,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.80,
        shadow_offset_x=52, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("看得見的信任", FONT_ZH, 72, BLACK, 0.055, 0.130, "tl"),
            ("學名 · Boswellia carterii", FONT_ZH, 28, BLACK, 0.055, 0.250, "tl"),
            ("產地 · 印度", FONT_ZH, 28, BLACK, 0.055, 0.302, "tl"),
            ("IFA 國際芳療師監製", FONT_ZH, 28, TERRA, 0.055, 0.356, "tl"),
        ],
    )

    # R1-f5 儀式感 — 深可可底
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R1_f5.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=COCOA,
        bottle_name="乳香",
        bottle_scale=0.55,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=20,
        shadow_blur=36, shadow_opacity=0.08,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("晚間儀式", FONT_ZH, 88, WARMCREAM, 0.055, 0.130, "tl"),
            ("從聞一支油開始", FONT_ZH, 44, GOLDYELLOW, 0.055, 0.278, "tl"),
            ("不需要很多,只要真實", FONT_ZH, 30, GREYBROWN, 0.055, 0.364, "tl"),
            ("情境使用 · 非療效宣稱", FONT_ZH, 18, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # R1-f6 CTA — 奶油底
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R1_f6.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMCREAM,
        bottle_name="乳香",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22,
        shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("初秋夜晚", FONT_ZH, 72, BLACK, 0.055, 0.130, "tl"),
            ("你的沉靜儀式", FONT_ZH, 52, TERRA, 0.055, 0.252, "tl"),
            ("MORENE.COM.TW", FONT_EN, 28, TERRA, 0.055, 0.368, "tl"),
            ("個人簡介連結 ↑", FONT_ZH, 26, BLACK, 0.055, 0.426, "tl"),
            ("情境使用 · 非療效宣稱", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    print("R1 完成。")

    # ----------------------------------------------------------------
    # R2: 8/30 梭羅×香氣(湖濱散記減法)
    # ----------------------------------------------------------------
    print("--- R2 梭羅×香氣 ---")

    # R2-f1 開場引言 — 米白底
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R2_f1.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMWHITE,
        bottle_name="乳香",
        bottle_scale=0.50,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.76,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=36, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R2", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("梭羅說", FONT_ZH, 90, BLACK, 0.055, 0.130, "tl"),
            ("我步入叢林", FONT_ZH, 52, BLACK, 0.055, 0.284, "tl"),
            ("是因為我想從容地生活", FONT_ZH, 38, BLACK, 0.055, 0.354, "tl"),
            ("—— 《湖濱散記》1854", FONT_ZH, 22, GREYBROWN, 0.055, 0.422, "tl"),
        ],
    )

    # R2-f2 文學脈絡 — 暖白底
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R2_f2.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMWHITE,
        bottle_name="乳香",
        bottle_scale=0.52,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22,
        shadow_blur=38, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R2", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("減法", FONT_ZH, 110, BLACK, 0.055, 0.130, "tl"),
            ("不是擁有更多", FONT_ZH, 46, BLACK, 0.055, 0.310, "tl"),
            ("而是更少但更深", FONT_ZH, 42, TERRA, 0.055, 0.382, "tl"),
            ("香氣也是", FONT_ZH, 36, GREYBROWN, 0.055, 0.458, "tl"),
        ],
    )

    # R2-f3 乳香主角 — 暖沙底
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R2_f3.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMSAND,
        bottle_name="乳香",
        bottle_scale=0.58,
        bottle_x_frac=0.64,
        bottle_bottom_frac=0.80,
        shadow_offset_x=52, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R2", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("一支就夠", FONT_ZH, 86, BLACK, 0.055, 0.130, "tl"),
            ("乳香 · Boswellia carterii", FONT_ZH, 30, TERRA, 0.055, 0.280, "tl"),
            ("印度 · 樹脂 · 木質溫暖", FONT_ZH, 26, BLACK, 0.055, 0.336, "tl"),
            ("情境使用 · 非療效宣稱", FONT_ZH, 18, GREYBROWN, 0.055, 0.400, "tl"),
        ],
    )

    # R2-f4 《湖濱散記》第二段引言 — 米白底
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R2_f4.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMWHITE,
        bottle_name="乳香",
        bottle_scale=0.50,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.78,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=36, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R2", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("只面對生活中", FONT_ZH, 56, BLACK, 0.055, 0.130, "tl"),
            ("真正重要的事", FONT_ZH, 56, BLACK, 0.055, 0.218, "tl"),
            ("—— 梭羅", FONT_ZH, 28, GREYBROWN, 0.055, 0.308, "tl"),
            ("香氣是一個選擇", FONT_ZH, 36, TERRA, 0.055, 0.380, "tl"),
            ("選擇讓自己慢下來", FONT_ZH, 32, BLACK, 0.055, 0.442, "tl"),
        ],
    )

    # R2-f5 換季搭配建議 — 暖沙底 + 乳香
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R2_f5.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMSAND,
        bottle_name="乳香",
        bottle_scale=0.55,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.80,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R2", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("梭羅的香氣", FONT_ZH, 72, BLACK, 0.055, 0.130, "tl"),
            ("如果他選一支精油", FONT_ZH, 38, BLACK, 0.055, 0.248, "tl"),
            ("一定是乳香", FONT_ZH, 50, TERRA, 0.055, 0.316, "tl"),
            ("木質 · 樹脂 · 返回本質", FONT_ZH, 26, GREYBROWN, 0.055, 0.396, "tl"),
        ],
    )

    # R2-f6 CTA — 奶油底
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R2_f6.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMCREAM,
        bottle_name="乳香",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22,
        shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R2", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("梭羅×香氣", FONT_ZH, 68, BLACK, 0.055, 0.130, "tl"),
            ("芳療誌全文", FONT_ZH, 52, TERRA, 0.055, 0.240, "tl"),
            ("MORENE.COM.TW", FONT_EN, 28, TERRA, 0.055, 0.356, "tl"),
            ("個人簡介連結 ↑", FONT_ZH, 26, BLACK, 0.055, 0.416, "tl"),
            ("情境使用 · 非療效宣稱", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    print("R2 完成。")

    # ----------------------------------------------------------------
    # R3: 9/2 前中後調換季搭配
    # ----------------------------------------------------------------
    print("--- R3 前中後調換季搭配 ---")

    # R3-f1 開場 — 暖沙底 + 甜橙(前調)
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R3_f1.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMSAND,
        bottle_name="甜橙",
        bottle_scale=0.58,
        bottle_x_frac=0.64,
        bottle_bottom_frac=0.80,
        shadow_offset_x=52, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("換季搭配", FONT_ZH, 88, BLACK, 0.055, 0.130, "tl"),
            ("前中後調全解析", FONT_ZH, 44, TERRA, 0.055, 0.282, "tl"),
            ("W38 · 初秋×開學季", FONT_ZH, 26, GREYBROWN, 0.055, 0.360, "tl"),
        ],
    )

    # R3-f2 前調 — 焦糖底 + 甜橙
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R3_f2.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=CARAMEL,
        bottle_name="甜橙",
        bottle_scale=0.60,
        bottle_x_frac=0.62,
        bottle_bottom_frac=0.80,
        shadow_offset_x=54, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, DARKBROWN, 0.055, 0.092, "tl"),
            ("前調", FONT_ZH, 100, BLACK, 0.055, 0.130, "tl"),
            ("柑橘 · 草本", FONT_ZH, 48, DARKBROWN, 0.055, 0.290, "tl"),
            ("前15分鐘 · 甜橙 · 苦橙葉", FONT_ZH, 26, DARKBROWN, 0.055, 0.376, "tl"),
            ("Citrus sinensis · Petitgrain bigarade", FONT_EN, 20, DARKBROWN, 0.055, 0.424, "tl"),
        ],
    )

    # R3-f3 中調 — 霧粉底 + 玫瑰天竺葵
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R3_f3.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=FOGPINK,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.60,
        bottle_x_frac=0.62,
        bottle_bottom_frac=0.80,
        shadow_offset_x=54, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("中調", FONT_ZH, 100, TERRA, 0.055, 0.130, "tl"),
            ("花香 · 辛香", FONT_ZH, 48, BLACK, 0.055, 0.290, "tl"),
            ("20–60分鐘 · 玫瑰天竺葵", FONT_ZH, 26, GREYBROWN, 0.055, 0.376, "tl"),
            ("Pelargonium graveolens", FONT_EN, 22, GREYBROWN, 0.055, 0.424, "tl"),
        ],
    )

    # R3-f4 後調 — 深可可底 + 乳香
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R3_f4.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=COCOA,
        bottle_name="乳香",
        bottle_scale=0.60,
        bottle_x_frac=0.62,
        bottle_bottom_frac=0.80,
        shadow_offset_x=54, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.08,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("後調", FONT_ZH, 100, GOLDYELLOW, 0.055, 0.130, "tl"),
            ("木質 · 樹脂", FONT_ZH, 48, WARMCREAM, 0.055, 0.290, "tl"),
            ("1小時後 · 乳香 · 大西洋雪松", FONT_ZH, 26, GREYBROWN, 0.055, 0.376, "tl"),
            ("Boswellia carterii", FONT_EN, 22, GREYBROWN, 0.055, 0.424, "tl"),
        ],
    )

    # R3-f5 換季搭配建議 — 暖沙底 + 苦橙葉
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R3_f5.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMSAND,
        bottle_name="苦橙葉",
        bottle_scale=0.58,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.80,
        shadow_offset_x=52, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("W38 換季首選", FONT_ZH, 64, BLACK, 0.055, 0.130, "tl"),
            ("甜橙(前)+玫瑰天竺葵(中)", FONT_ZH, 30, TERRA, 0.055, 0.238, "tl"),
            ("+乳香(後)", FONT_ZH, 44, TERRA, 0.055, 0.300, "tl"),
            ("苦橙葉加進前調更輕薄", FONT_ZH, 26, BLACK, 0.055, 0.374, "tl"),
            ("Petitgrain bigarade · 巴拉圭", FONT_ZH, 22, GREYBROWN, 0.055, 0.428, "tl"),
        ],
    )

    # R3-f6 CTA — 奶油底
    save_and_dual(
        "W38", "Reels", "MORENE_W38_R3_f6.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMCREAM,
        bottle_name="乳香",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22,
        shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("前中後調全解析", FONT_ZH, 60, BLACK, 0.055, 0.130, "tl"),
            ("MORENE.COM.TW", FONT_EN, 30, TERRA, 0.055, 0.244, "tl"),
            ("個人簡介連結 ↑", FONT_ZH, 28, BLACK, 0.055, 0.308, "tl"),
            ("情境使用 · 非療效宣稱", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    print("R3 完成。")
    print("W38 Reels 全部完成。")


# =====================================================================
# MAIN — 分批執行
# =====================================================================
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MORENE W38 圖卡生成")
    parser.add_argument("--batch", choices=["stories", "ig_fb", "reels", "all"],
                        default="all", help="指定生成批次")
    args = parser.parse_args()

    print("MORENE W38 常態週(初秋·九月開學季)圖卡生成開始...")

    if args.batch in ("stories", "all"):
        print("\n=== 批次 1: Stories ===")
        make_stories()

    if args.batch in ("ig_fb", "all"):
        print("\n=== 批次 2: IG + FB ===")
        make_ig_fb()

    if args.batch in ("reels", "all"):
        print("\n=== 批次 3: Reels ===")
        make_reels()

    total = {"stories": 14, "ig_fb": 14, "reels": 18, "all": 46}
    print(f"\n完成。W38 {total.get(args.batch, 46)} 張圖卡生成完畢。")
    print(f"NAS 路徑:  /Users/morrislin/mw-social-assets/MORENE/W38/")
    print(f"Desktop:   /Users/morrislin/Desktop/MORENE/MORENE_社群營運_Social/03_圖卡_Assets/W38/")
