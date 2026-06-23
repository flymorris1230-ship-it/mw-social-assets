#!/usr/bin/env python3
"""
MORENE W37 常態化樣板週(8/20–8/26)圖卡生成腳本
策略: 攝影主導 + 單色暖底 + 真實琥珀瓶 + 極少字 + Y2K 克制版
節氣: 處暑(8/23) · 換季 · 書房 · 前中後調 · 學名信任

⚠️ CJK tofu 防呆:含 CJK 字元必用 FONT_ZH / FONT_ZH_BOLD
⚠️ 不放 ISO/GMP/認證標章;不寫療效詞(助眠/修復/治療)
⚠️ 信任點:IFA 國際芳療師監製 · 學名產地透明 · INCI 公開
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
# W37 色彩補充(VIS 暖色票)
# =====================
WARMSAND  = "#CBA98A"   # 暖沙
CARAMEL   = "#C9853E"   # 焦糖
FOGPINK   = "#E9C5B9"   # 霧粉
FOGBLUE   = "#82A8CC"   # 霧藍
TEAL      = "#8DBFBE"   # 霧藍綠(SAGE alias)
GREYBROWN = "#8C8079"   # 灰褐
WARMCREAM = "#EDE7DC"   # 奶油(= CREAM)
GOLDYELLOW= "#E8CE8C"   # 芥末淡(比 MUSTARD 柔)
DARKBROWN = "#3D2B1F"   # 暖棕深(木紋感)
WARMWHITE = "#F5F0E8"   # 暖白

# =====================
# 路徑
# =====================
BASE_PROD = "/Users/morrislin/Desktop/MORENE/03_MORENE/03_Assets/A009：MORENE-產品相關/01.產品相關/01. 產品資料/05. 產品照片/素材/商品大圖/01_精油"
DESK_ASSETS = "/Users/morrislin/Desktop/MORENE/MORENE_社群營運_Social/03_圖卡_Assets"
LOGO_CREAM = "/Users/morrislin/mw-social-assets/MORENE/_fonts/MORENE_logo_cream.png"
LOGO_BLACK = "/Users/morrislin/mw-social-assets/MORENE/_fonts/MORENE_logo_black.png"

# W37 需要的瓶子路徑補丁
EXTRA_BOTTLES = {
    "大西洋雪松": f"{BASE_PROD}/5MOEO005_大西洋雪松/MORENE_精油瓶_去背_大西洋雪松.png",
    "乳香":       f"{BASE_PROD}/5MOEO009_乳香/MORENE_精油瓶_去背_乳香.png",
    "真正薰衣草": f"{BASE_PROD}/5MOEO015_真正薰衣草/MORENE_精油瓶_去背_真正薰衣草.png",
    "迷迭香":     f"{BASE_PROD}/桉油葉迷迭香/MORENE_精油瓶_去背_桉油葉迷迭香.png",
    "廣藿香":     f"{BASE_PROD}/廣藿香/MORENE_精油瓶_去背_廣藿香.png",
    "甜橙":       f"{BASE_PROD}/甜橙/MORENE_精油瓶_去背_甜橙.png",
    "白葡萄柚":   f"{BASE_PROD}/5MOEO011_白葡萄柚/MORENE_精油瓶_去背_白葡萄柚.png",
    "玫瑰天竺葵": f"{BASE_PROD}/5MOEO025_玫瑰天竺葵/MORENE_精油瓶_去背_玫瑰天竺葵.png",
    "岩蘭草":     f"{BASE_PROD}/岩蘭草/MORENE_精油瓶_去背_岩蘭草.png",
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
# 命名: MORENE_W37_S01 ~ MORENE_W37_S14
# =====================================================================
def make_stories():
    print("\n=== W37 Stories S01–S14 ===")

    # S01 8/20 晨換季投票 — 暖棕底 + 深色乳香瓶
    print("S01 8/20 晨換季投票...")
    save_and_dual(
        "W37", "Stories", "MORENE_W37_S01.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=DARKBROWN,
        bottle_name="乳香",
        bottle_scale=0.50,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.76,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=36, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("W37 · 8/20", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("換季了", FONT_ZH, 90, WARMCREAM, 0.055, 0.130, "tl"),
            ("你換香氣了嗎?", FONT_ZH, 48, GOLDYELLOW, 0.055, 0.272, "tl"),
            ("投票告訴我們 ↓", FONT_ZH, 30, WARMCREAM, 0.055, 0.358, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S02 8/20 換季導流 — 暖棕底 + 大西洋雪松(縮圖預告)
    print("S02 8/20 換季導流...")
    save_and_dual(
        "W37", "Stories", "MORENE_W37_S02.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMSAND,
        bottle_name="大西洋雪松",
        bottle_scale=0.52,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.76,
        shadow_offset_x=48, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W37 · 8/20", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("換季精選", FONT_ZH, 76, BLACK, 0.055, 0.130, "tl"),
            ("大西洋雪松 + 乳香", FONT_ZH, 40, TERRA, 0.055, 0.262, "tl"),
            ("主頁看全文 →", FONT_ZH, 28, BLACK, 0.055, 0.344, "tl"),
            ("Cedrus atlantica · Boswellia carterii", FONT_EN, 20, GREYBROWN, 0.055, 0.406, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S03 8/21 靜下來問答 — 深棕底 + 開蓋乳香
    print("S03 8/21 靜下來問答...")
    save_and_dual(
        "W37", "Stories", "MORENE_W37_S03.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=DARKBROWN,
        bottle_name="乳香",
        bottle_scale=0.50,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.76,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=34, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("W37 · 8/21", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("靜下來", FONT_ZH, 90, WARMCREAM, 0.055, 0.130, "tl"),
            ("問答時間", FONT_ZH, 60, GOLDYELLOW, 0.055, 0.262, "tl"),
            ("留言問精油任何事", FONT_ZH, 32, WARMCREAM, 0.055, 0.362, "tl"),
            ("我們都在", FONT_ZH, 28, WARMCREAM, 0.055, 0.418, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S04 8/21 雪松預告 — 暖木紋(暖沙) + 大西洋雪松
    print("S04 8/21 雪松預告...")
    save_and_dual(
        "W37", "Stories", "MORENE_W37_S04.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMSAND,
        bottle_name="大西洋雪松",
        bottle_scale=0.54,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W37 · 8/21", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("明天登場", FONT_ZH, 68, BLACK, 0.055, 0.130, "tl"),
            ("大西洋雪松", FONT_ZH, 54, TERRA, 0.055, 0.234, "tl"),
            ("Cedrus atlantica", FONT_EN, 22, GREYBROWN, 0.055, 0.320, "tl"),
            ("摩洛哥 · 木質 · 秋天的開始", FONT_ZH, 28, BLACK, 0.055, 0.374, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S05 8/22 換季靠哪支投票 — 秋色三選一(焦糖底)
    print("S05 8/22 換季靠哪支投票...")
    save_and_dual(
        "W37", "Stories", "MORENE_W37_S05.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=CARAMEL,
        bottle_name="乳香",
        bottle_scale=0.50,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.78,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W37 · 8/22", FONT_EN, 14, DARKBROWN, 0.055, 0.092, "tl"),
            ("換季靠哪支?", FONT_ZH, 72, BLACK, 0.055, 0.130, "tl"),
            ("投票 ↓", FONT_ZH, 48, DARKBROWN, 0.055, 0.248, "tl"),
            ("A  大西洋雪松(木質)", FONT_ZH, 28, BLACK, 0.055, 0.342, "tl"),
            ("B  乳香(樹脂溫暖)", FONT_ZH, 28, BLACK, 0.055, 0.396, "tl"),
            ("C  迷迭香(草本清醒)", FONT_ZH, 28, BLACK, 0.055, 0.450, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, DARKBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S06 8/22 投票延伸(結果風) — 暖沙底 + 大西洋雪松
    print("S06 8/22 投票延伸...")
    save_and_dual(
        "W37", "Stories", "MORENE_W37_S06.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMSAND,
        bottle_name="大西洋雪松",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.76,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=36, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W37 · 8/22", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("換季首選", FONT_ZH, 76, BLACK, 0.055, 0.130, "tl"),
            ("大西洋雪松勝出", FONT_ZH, 48, TERRA, 0.055, 0.252, "tl"),
            ("木質 · 穩定 · 轉季最常提", FONT_ZH, 30, BLACK, 0.055, 0.354, "tl"),
            ("主頁了解更多 →", FONT_ZH, 28, BLACK, 0.055, 0.416, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S07 8/23 處暑漢字 — 金棕書法風(GOLDYELLOW)
    print("S07 8/23 處暑漢字...")
    save_and_dual(
        "W37", "Stories", "MORENE_W37_S07.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=DARKBROWN,
        bottle_name="乳香",
        bottle_scale=0.48,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.76,
        shadow_offset_x=44, shadow_offset_y=18,
        shadow_blur=34, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("節氣 · 二十四節氣第十四", FONT_ZH, 18, GREYBROWN, 0.055, 0.092, "tl"),
            ("處", FONT_ZH_BOLD, 200, GOLDYELLOW, 0.055, 0.120, "tl"),
            ("暑", FONT_ZH_BOLD, 200, GOLDYELLOW, 0.055, 0.350, "tl"),
            ("8月23日", FONT_ZH, 36, WARMCREAM, 0.055, 0.580, "tl"),
            ("暑氣漸退 · 秋意初現", FONT_ZH, 28, WARMCREAM, 0.055, 0.648, "tl"),
            ("換一支秋天的香氣吧", FONT_ZH, 24, GOLDYELLOW, 0.055, 0.706, "tl"),
            ("MORENE · 芳療誌 · 情境使用非療效", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S08 8/23 處暑導流 — 暖沙底 + 乳香縮圖
    print("S08 8/23 處暑導流...")
    save_and_dual(
        "W37", "Stories", "MORENE_W37_S08.png",
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
            ("處暑 · 8/23", FONT_ZH, 32, TERRA, 0.055, 0.092, "tl"),
            ("乳香圖文看主頁 →", FONT_ZH, 48, BLACK, 0.055, 0.152, "tl"),
            ("Boswellia carterii", FONT_EN, 22, GREYBROWN, 0.055, 0.248, "tl"),
            ("印度 · 樹脂 · 木質溫暖", FONT_ZH, 28, BLACK, 0.055, 0.302, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S09 8/24 開學書房投票 — 暖米白(奶油) + 迷迭香
    print("S09 8/24 開學書房投票...")
    save_and_dual(
        "W37", "Stories", "MORENE_W37_S09.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMCREAM,
        bottle_name="迷迭香",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=34, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W37 · 8/24", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("書房香氣", FONT_ZH, 80, BLACK, 0.055, 0.130, "tl"),
            ("你選哪支?", FONT_ZH, 56, TERRA, 0.055, 0.258, "tl"),
            ("投票 ↓", FONT_ZH, 36, BLACK, 0.055, 0.354, "tl"),
            ("A  迷迭香(草本醒腦)", FONT_ZH, 26, BLACK, 0.055, 0.420, "tl"),
            ("B  薄荷(清涼專注)", FONT_ZH, 26, BLACK, 0.055, 0.470, "tl"),
            ("情境使用非療效 · 趣味體驗非診斷 · MORENE", FONT_ZH, 15, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S10 8/24 書房導流 — 暖沙底 + 迷迭香
    print("S10 8/24 書房導流...")
    save_and_dual(
        "W37", "Stories", "MORENE_W37_S10.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMSAND,
        bottle_name="迷迭香",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=36, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W37 · 8/24", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("書房精選", FONT_ZH, 76, BLACK, 0.055, 0.130, "tl"),
            ("主頁看圖文 →", FONT_ZH, 44, TERRA, 0.055, 0.258, "tl"),
            ("迷迭香 × 薄荷", FONT_ZH, 32, BLACK, 0.055, 0.352, "tl"),
            ("Rosmarinus officinalis", FONT_EN, 20, GREYBROWN, 0.055, 0.410, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S11 8/25 學名標籤(瓶標特寫) — 暖白底 + 真正薰衣草
    print("S11 8/25 學名標籤...")
    save_and_dual(
        "W37", "Stories", "MORENE_W37_S11.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMWHITE,
        bottle_name="真正薰衣草",
        bottle_scale=0.55,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.78,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=38, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W37 · 8/25", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("看得見學名", FONT_ZH, 68, BLACK, 0.055, 0.130, "tl"),
            ("才是真的透明", FONT_ZH, 52, TERRA, 0.055, 0.246, "tl"),
            ("Lavandula angustifolia", FONT_EN, 28, BLACK, 0.055, 0.362, "tl"),
            ("法國普羅旺斯 · 花香 · 植物性萃取", FONT_ZH, 24, GREYBROWN, 0.055, 0.418, "tl"),
            ("IFA 國際芳療師監製 · INCI 公開", FONT_ZH, 20, GREYBROWN, 0.055, 0.476, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S12 8/25 信任導流 — 奶油底 + 真正薰衣草
    print("S12 8/25 信任導流...")
    save_and_dual(
        "W37", "Stories", "MORENE_W37_S12.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMCREAM,
        bottle_name="真正薰衣草",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W37 · 8/25", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("品牌信任", FONT_ZH, 76, BLACK, 0.055, 0.130, "tl"),
            ("主頁看全文 →", FONT_ZH, 44, TERRA, 0.055, 0.258, "tl"),
            ("學名 · 產地 · IFA 監製", FONT_ZH, 30, BLACK, 0.055, 0.350, "tl"),
            ("用看得見的,取代你的信任", FONT_ZH, 24, GREYBROWN, 0.055, 0.408, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S13 8/26 前中後調投票 — 暖白 + 三層字
    print("S13 8/26 前中後調投票...")
    save_and_dual(
        "W37", "Stories", "MORENE_W37_S13.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMWHITE,
        bottle_name="大西洋雪松",
        bottle_scale=0.50,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.76,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=34, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("W37 · 8/26", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("前調 · 中調 · 後調", FONT_ZH, 54, BLACK, 0.055, 0.130, "tl"),
            ("你最常聞到哪層?", FONT_ZH, 44, TERRA, 0.055, 0.228, "tl"),
            ("前調  柑橘 · 草本(前15分鐘)", FONT_ZH, 26, BLACK, 0.055, 0.336, "tl"),
            ("中調  花香 · 辛香(20–60分鐘)", FONT_ZH, 26, BLACK, 0.055, 0.390, "tl"),
            ("後調  木質 · 樹脂(1小時後)", FONT_ZH, 26, BLACK, 0.055, 0.444, "tl"),
            ("情境使用 · 趣味體驗非診斷 · MORENE", FONT_ZH, 15, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # S14 8/26 科普導流 — 暖沙底 + 乳香
    print("S14 8/26 科普導流...")
    save_and_dual(
        "W37", "Stories", "MORENE_W37_S14.png",
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
            ("W37 · 8/26", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("前中後調科普", FONT_ZH, 68, BLACK, 0.055, 0.130, "tl"),
            ("主頁看圖解 →", FONT_ZH, 44, TERRA, 0.055, 0.248, "tl"),
            ("懂了層次 · 聞香更有感", FONT_ZH, 28, BLACK, 0.055, 0.344, "tl"),
            ("SCENT NOTES · ACCORDS · MORENE.COM.TW", FONT_EN, 18, GREYBROWN, 0.055, 0.406, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    print("W37 Stories 完成。")


# =====================================================================
# IG ×7 (1080×1350) + FB ×7 (1080×1080) 同主題雙出
# 命名: MORENE_W37_IG1 ~ MORENE_W37_IG7 / MORENE_W37_FB1 ~ MORENE_W37_FB7
# =====================================================================
def make_ig_fb():
    print("\n=== W37 IG+FB ===")

    # --------------------------------------------------
    # IG1/FB1 8/20 換季 — 暖棕底 + 大西洋雪松+乳香並排
    # IG: 1080×1350 / FB: 1080×1080 (使用 compose_card 單瓶,標文字說明並排概念)
    # --------------------------------------------------
    print("IG1 8/20 換季...")
    save_and_dual(
        "W37", "IG", "MORENE_W37_IG1.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=DARKBROWN,
        bottle_name="大西洋雪松",
        bottle_scale=0.62,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.88,
        shadow_offset_x=58, shadow_offset_y=26,
        shadow_blur=42, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, WARMCREAM, 0.055, 0.048, "tl"),
            ("01 / 07", FONT_EN, 14, GREYBROWN, 0.870, 0.048, "tl"),
            ("換季", FONT_ZH, 100, WARMCREAM, 0.055, 0.094, "tl"),
            ("你的香氣跟上了嗎", FONT_ZH, 42, GOLDYELLOW, 0.055, 0.258, "tl"),
            ("大西洋雪松 · 乳香", FONT_ZH, 30, WARMCREAM, 0.055, 0.340, "tl"),
            ("Cedrus atlantica · Boswellia carterii", FONT_EN, 19, GREYBROWN, 0.055, 0.394, "tl"),
            ("換季推薦 · 情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ],
    )

    # FB1 (1080×1080)
    print("FB1 8/20 換季...")
    save_and_dual(
        "W37", "FB", "MORENE_W37_FB1.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=DARKBROWN,
        bottle_name="大西洋雪松",
        bottle_scale=0.68,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.92,
        shadow_offset_x=62, shadow_offset_y=28,
        shadow_blur=44, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, WARMCREAM, 0.055, 0.048, "tl"),
            ("換季", FONT_ZH, 90, WARMCREAM, 0.055, 0.100, "tl"),
            ("你的香氣跟上了嗎", FONT_ZH, 38, GOLDYELLOW, 0.055, 0.248, "tl"),
            ("大西洋雪松 · 乳香", FONT_ZH, 28, WARMCREAM, 0.055, 0.318, "tl"),
            ("Cedrus atlantica · Boswellia carterii", FONT_EN, 17, GREYBROWN, 0.055, 0.368, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG2/FB2 8/21 大西洋雪松單方 — 暖木紋底
    # --------------------------------------------------
    print("IG2 8/21 大西洋雪松...")
    save_and_dual(
        "W37", "IG", "MORENE_W37_IG2.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=WARMSAND,
        bottle_name="大西洋雪松",
        bottle_scale=0.64,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.88,
        shadow_offset_x=60, shadow_offset_y=26,
        shadow_blur=42, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("02 / 07", FONT_EN, 14, GREYBROWN, 0.870, 0.048, "tl"),
            ("大西洋雪松", FONT_ZH, 72, BLACK, 0.055, 0.094, "tl"),
            ("Cedrus atlantica", FONT_EN, 26, TERRA, 0.055, 0.222, "tl"),
            ("摩洛哥 · 蒸氣蒸餾 · 木質針葉", FONT_ZH, 28, BLACK, 0.055, 0.286, "tl"),
            ("秋天開始前 · 從木質系開始換季", FONT_ZH, 26, GREYBROWN, 0.055, 0.348, "tl"),
            ("IFA 國際芳療師監製 · 學名產地透明", FONT_ZH, 20, GREYBROWN, 0.055, 0.402, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ],
    )

    print("FB2 8/21 大西洋雪松...")
    save_and_dual(
        "W37", "FB", "MORENE_W37_FB2.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=WARMSAND,
        bottle_name="大西洋雪松",
        bottle_scale=0.70,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.92,
        shadow_offset_x=62, shadow_offset_y=28,
        shadow_blur=44, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("大西洋雪松", FONT_ZH, 64, BLACK, 0.055, 0.100, "tl"),
            ("Cedrus atlantica", FONT_EN, 24, TERRA, 0.055, 0.220, "tl"),
            ("摩洛哥 · 蒸氣蒸餾 · 木質針葉", FONT_ZH, 26, BLACK, 0.055, 0.280, "tl"),
            ("IFA 國際芳療師監製 · 學名產地透明", FONT_ZH, 18, GREYBROWN, 0.055, 0.340, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG3/FB3 8/22 UGC — 暖白底 + 多瓶(乳香代表)
    # --------------------------------------------------
    print("IG3 8/22 UGC...")
    save_and_dual(
        "W37", "IG", "MORENE_W37_IG3.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=WARMWHITE,
        bottle_name="乳香",
        bottle_scale=0.62,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.88,
        shadow_offset_x=58, shadow_offset_y=25,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("03 / 07", FONT_EN, 14, GREYBROWN, 0.870, 0.048, "tl"),
            ("你換季用哪支?", FONT_ZH, 62, BLACK, 0.055, 0.094, "tl"),
            ("分享你的換季香氣", FONT_ZH, 42, TERRA, 0.055, 0.214, "tl"),
            ("留言 or 標記 @morene_organic", FONT_ZH, 26, BLACK, 0.055, 0.310, "tl"),
            ("我們會轉發分享", FONT_ZH, 24, GREYBROWN, 0.055, 0.364, "tl"),
            ("UGC · 情境使用非療效 · MORENE.COM.TW", FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ],
    )

    print("FB3 8/22 UGC...")
    save_and_dual(
        "W37", "FB", "MORENE_W37_FB3.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=WARMWHITE,
        bottle_name="乳香",
        bottle_scale=0.68,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.92,
        shadow_offset_x=60, shadow_offset_y=26,
        shadow_blur=42, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("你換季用哪支?", FONT_ZH, 56, BLACK, 0.055, 0.100, "tl"),
            ("分享你的換季香氣", FONT_ZH, 38, TERRA, 0.055, 0.212, "tl"),
            ("標記 @morene_organic", FONT_ZH, 24, BLACK, 0.055, 0.306, "tl"),
            ("情境使用非療效 · MORENE.COM.TW", FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG4/FB4 8/23 處暑 — 金秋底 + 乳香 + 漢字
    # --------------------------------------------------
    print("IG4 8/23 處暑...")
    save_and_dual(
        "W37", "IG", "MORENE_W37_IG4.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=CARAMEL,
        bottle_name="乳香",
        bottle_scale=0.62,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.88,
        shadow_offset_x=58, shadow_offset_y=25,
        shadow_blur=42, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("04 / 07", FONT_EN, 14, DARKBROWN, 0.870, 0.048, "tl"),
            ("處暑", FONT_ZH_BOLD, 130, BLACK, 0.055, 0.092, "tl"),
            ("8月23日 · 二十四節氣", FONT_ZH, 26, DARKBROWN, 0.055, 0.286, "tl"),
            ("暑氣漸退 · 秋意初現", FONT_ZH, 36, BLACK, 0.055, 0.342, "tl"),
            ("乳香 · Boswellia carterii", FONT_ZH, 26, DARKBROWN, 0.055, 0.416, "tl"),
            ("印度 · 樹脂 · 溫暖木質", FONT_ZH, 22, DARKBROWN, 0.055, 0.462, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 15, DARKBROWN, 0.055, 0.946, "tl"),
        ],
    )

    print("FB4 8/23 處暑...")
    save_and_dual(
        "W37", "FB", "MORENE_W37_FB4.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=CARAMEL,
        bottle_name="乳香",
        bottle_scale=0.68,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.92,
        shadow_offset_x=62, shadow_offset_y=28,
        shadow_blur=44, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("處暑", FONT_ZH_BOLD, 110, BLACK, 0.055, 0.096, "tl"),
            ("8月23日 · 二十四節氣", FONT_ZH, 24, DARKBROWN, 0.055, 0.274, "tl"),
            ("暑氣漸退 · 秋意初現", FONT_ZH, 32, BLACK, 0.055, 0.330, "tl"),
            ("乳香 · Boswellia carterii", FONT_ZH, 24, DARKBROWN, 0.055, 0.402, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 14, DARKBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG5/FB5 8/24 書房 — 暖米白 + 迷迭香
    # --------------------------------------------------
    print("IG5 8/24 書房...")
    save_and_dual(
        "W37", "IG", "MORENE_W37_IG5.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=WARMCREAM,
        bottle_name="迷迭香",
        bottle_scale=0.62,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.88,
        shadow_offset_x=58, shadow_offset_y=25,
        shadow_blur=40, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("05 / 07", FONT_EN, 14, GREYBROWN, 0.870, 0.048, "tl"),
            ("書房香氣", FONT_ZH, 88, BLACK, 0.055, 0.094, "tl"),
            ("迷迭香 × 薄荷", FONT_ZH, 48, TERRA, 0.055, 0.248, "tl"),
            ("Rosmarinus officinalis", FONT_EN, 22, GREYBROWN, 0.055, 0.336, "tl"),
            ("西班牙 · 草本 · 蒸氣蒸餾", FONT_ZH, 24, BLACK, 0.055, 0.390, "tl"),
            ("開學了 · 書房的香氣也換一換", FONT_ZH, 24, GREYBROWN, 0.055, 0.440, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ],
    )

    print("FB5 8/24 書房...")
    save_and_dual(
        "W37", "FB", "MORENE_W37_FB5.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=WARMCREAM,
        bottle_name="迷迭香",
        bottle_scale=0.68,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.92,
        shadow_offset_x=60, shadow_offset_y=26,
        shadow_blur=42, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("書房香氣", FONT_ZH, 78, BLACK, 0.055, 0.100, "tl"),
            ("迷迭香 × 薄荷", FONT_ZH, 44, TERRA, 0.055, 0.240, "tl"),
            ("Rosmarinus officinalis", FONT_EN, 20, GREYBROWN, 0.055, 0.320, "tl"),
            ("開學了 · 書房的香氣也換一換", FONT_ZH, 22, GREYBROWN, 0.055, 0.372, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG6/FB6 8/25 品牌信任 — 暖白 + 真正薰衣草 + 學名三點
    # --------------------------------------------------
    print("IG6 8/25 品牌信任...")
    save_and_dual(
        "W37", "IG", "MORENE_W37_IG6.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=WARMWHITE,
        bottle_name="真正薰衣草",
        bottle_scale=0.62,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.88,
        shadow_offset_x=56, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("06 / 07", FONT_EN, 14, GREYBROWN, 0.870, 0.048, "tl"),
            ("看得見", FONT_ZH, 88, BLACK, 0.055, 0.094, "tl"),
            ("才是真的", FONT_ZH, 64, TERRA, 0.055, 0.244, "tl"),
            ("學名 · Lavandula angustifolia", FONT_ZH, 26, BLACK, 0.055, 0.366, "tl"),
            ("產地 · 法國普羅旺斯", FONT_ZH, 26, BLACK, 0.055, 0.416, "tl"),
            ("IFA 國際芳療師監製", FONT_ZH, 26, BLACK, 0.055, 0.466, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ],
    )

    print("FB6 8/25 品牌信任...")
    save_and_dual(
        "W37", "FB", "MORENE_W37_FB6.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=WARMWHITE,
        bottle_name="真正薰衣草",
        bottle_scale=0.68,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.92,
        shadow_offset_x=58, shadow_offset_y=26,
        shadow_blur=42, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("看得見 · 才是真的", FONT_ZH, 54, BLACK, 0.055, 0.100, "tl"),
            ("學名 · Lavandula angustifolia", FONT_ZH, 24, BLACK, 0.055, 0.226, "tl"),
            ("產地 · 法國普羅旺斯", FONT_ZH, 24, BLACK, 0.055, 0.278, "tl"),
            ("IFA 國際芳療師監製", FONT_ZH, 24, BLACK, 0.055, 0.330, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG7/FB7 8/26 前中後調圖表 — 三層色塊暖色系 + 乳香代表後調
    # --------------------------------------------------
    print("IG7 8/26 前中後調圖表...")
    save_and_dual(
        "W37", "IG", "MORENE_W37_IG7.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=WARMCREAM,
        bottle_name="乳香",
        bottle_scale=0.58,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.88,
        shadow_offset_x=54, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("07 / 07", FONT_EN, 14, GREYBROWN, 0.870, 0.048, "tl"),
            ("前調", FONT_ZH, 52, "#E8622A", 0.055, 0.094, "tl"),
            ("柑橘 · 草本  開場白", FONT_ZH, 28, BLACK, 0.055, 0.168, "tl"),
            ("中調", FONT_ZH, 52, TERRA, 0.055, 0.228, "tl"),
            ("花香 · 辛香  主角登場", FONT_ZH, 28, BLACK, 0.055, 0.302, "tl"),
            ("後調", FONT_ZH, 52, DARKBROWN, 0.055, 0.362, "tl"),
            ("木質 · 樹脂  留香最久", FONT_ZH, 28, BLACK, 0.055, 0.436, "tl"),
            ("乳香 · 大西洋雪松 → 後調代表", FONT_ZH, 24, GREYBROWN, 0.055, 0.510, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ],
    )

    print("FB7 8/26 前中後調圖表...")
    save_and_dual(
        "W37", "FB", "MORENE_W37_FB7.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=WARMCREAM,
        bottle_name="乳香",
        bottle_scale=0.65,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.92,
        shadow_offset_x=58, shadow_offset_y=26,
        shadow_blur=42, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("前調  柑橘 · 草本", FONT_ZH, 32, "#E8622A", 0.055, 0.104, "tl"),
            ("中調  花香 · 辛香", FONT_ZH, 32, TERRA, 0.055, 0.176, "tl"),
            ("後調  木質 · 樹脂", FONT_ZH, 32, DARKBROWN, 0.055, 0.248, "tl"),
            ("乳香 · 大西洋雪松 → 後調代表", FONT_ZH, 22, GREYBROWN, 0.055, 0.322, "tl"),
            ("情境使用 · 非療效宣稱 · MORENE.COM.TW", FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    print("W37 IG+FB 完成。")


# =====================================================================
# REELS 分鏡 ×3 (1080×1920)  各6幀
# R1 8/20 換季過渡 · R2 8/23 處暑 · R3 8/26 前中後調
# 命名: MORENE_W37_R1_f1 ~ f6 / R2_f1~f6 / R3_f1~f6
# =====================================================================
def make_reels():
    print("\n=== W37 Reels R1–R3 ===")

    # ──────────────────────────────────────────────
    # R1 8/20 換季過渡 (6幀)
    # f1 夏瓶登場 / f2 蓋緊收季 / f3 雪松入鏡 / f4 擴香滴入 / f5 桌面橫移 / f6 Logo CTA
    # ──────────────────────────────────────────────
    print("R1 換季過渡...")

    # R1-f1 夏瓶登場 — 暖白底 + 甜橙(夏季代表)
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R1_f1.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMWHITE,
        bottle_name="甜橙",
        bottle_scale=0.62,
        bottle_x_frac=0.60,
        bottle_bottom_frac=0.80,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("夏天最後一滴", FONT_ZH, 56, BLACK, 0.055, 0.130, "tl"),
            ("甜橙 · Citrus sinensis", FONT_ZH, 28, TERRA, 0.055, 0.232, "tl"),
        ],
    )

    # R1-f2 蓋緊收季 — 奶油底 + 甜橙
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R1_f2.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMCREAM,
        bottle_name="甜橙",
        bottle_scale=0.58,
        bottle_x_frac=0.58,
        bottle_bottom_frac=0.78,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=38, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("蓋緊 · 收好", FONT_ZH, 64, BLACK, 0.055, 0.130, "tl"),
            ("夏天的香氣謝幕了", FONT_ZH, 34, GREYBROWN, 0.055, 0.242, "tl"),
        ],
    )

    # R1-f3 雪松入鏡 — 暖沙底 + 大西洋雪松
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R1_f3.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMSAND,
        bottle_name="大西洋雪松",
        bottle_scale=0.62,
        bottle_x_frac=0.62,
        bottle_bottom_frac=0.80,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("換季入場", FONT_ZH, 72, BLACK, 0.055, 0.130, "tl"),
            ("大西洋雪松", FONT_ZH, 46, TERRA, 0.055, 0.258, "tl"),
            ("Cedrus atlantica", FONT_EN, 22, GREYBROWN, 0.055, 0.326, "tl"),
        ],
    )

    # R1-f4 擴香滴入 — 焦糖底 + 乳香
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R1_f4.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=CARAMEL,
        bottle_name="乳香",
        bottle_scale=0.60,
        bottle_x_frac=0.60,
        bottle_bottom_frac=0.80,
        shadow_offset_x=53, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, DARKBROWN, 0.055, 0.092, "tl"),
            ("擴香滴入", FONT_ZH, 68, BLACK, 0.055, 0.130, "tl"),
            ("乳香 + 大西洋雪松", FONT_ZH, 36, DARKBROWN, 0.055, 0.248, "tl"),
            ("秋天換季配方", FONT_ZH, 28, BLACK, 0.055, 0.314, "tl"),
        ],
    )

    # R1-f5 桌面橫移 — 暗棕底 + 大西洋雪松
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R1_f5.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=DARKBROWN,
        bottle_name="大西洋雪松",
        bottle_scale=0.58,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.78,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=38, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("換季桌面", FONT_ZH, 68, WARMCREAM, 0.055, 0.130, "tl"),
            ("秋天的開始從一支香氣", FONT_ZH, 34, GOLDYELLOW, 0.055, 0.248, "tl"),
        ],
    )

    # R1-f6 Logo CTA — 奶油底
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R1_f6.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMCREAM,
        bottle_name="大西洋雪松",
        bottle_scale=0.55,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.80,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("換季精選", FONT_ZH, 68, BLACK, 0.055, 0.130, "tl"),
            ("MORENE.COM.TW", FONT_EN, 30, TERRA, 0.055, 0.244, "tl"),
            ("個人簡介連結 ↑", FONT_ZH, 28, BLACK, 0.055, 0.304, "tl"),
            ("情境使用 · 非療效宣稱", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    print("R1 完成。")

    # ──────────────────────────────────────────────
    # R2 8/23 處暑 (6幀)
    # f1 日曆8/23 / f2 乳香開蓋 / f3 乳香+廣藿香並排 / f4 擴香 / f5 桌面橫移 / f6 Logo CTA
    # ──────────────────────────────────────────────
    print("R2 處暑...")

    # R2-f1 日曆8/23 — 暗棕底
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R2_f1.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=DARKBROWN,
        bottle_name="乳香",
        bottle_scale=0.50,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=34, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R2", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("8 / 23", FONT_EN_BOLD, 130, GOLDYELLOW, 0.055, 0.130, "tl"),
            ("處暑", FONT_ZH_BOLD, 90, WARMCREAM, 0.055, 0.330, "tl"),
            ("二十四節氣 · 暑氣漸退", FONT_ZH, 28, GREYBROWN, 0.055, 0.454, "tl"),
        ],
    )

    # R2-f2 乳香開蓋 — 焦糖底
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R2_f2.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=CARAMEL,
        bottle_name="乳香",
        bottle_scale=0.62,
        bottle_x_frac=0.60,
        bottle_bottom_frac=0.80,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R2", FONT_EN, 14, DARKBROWN, 0.055, 0.092, "tl"),
            ("乳香", FONT_ZH, 90, BLACK, 0.055, 0.130, "tl"),
            ("Boswellia carterii", FONT_EN, 28, DARKBROWN, 0.055, 0.258, "tl"),
            ("印度 · 樹脂 · 溫暖木質", FONT_ZH, 28, BLACK, 0.055, 0.322, "tl"),
        ],
    )

    # R2-f3 乳香+廣藿香並排 — 暖沙底
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R2_f3.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMSAND,
        bottle_name="廣藿香",
        bottle_scale=0.60,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.80,
        shadow_offset_x=53, shadow_offset_y=22,
        shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R2", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("乳香 + 廣藿香", FONT_ZH, 60, BLACK, 0.055, 0.130, "tl"),
            ("處暑換季配方", FONT_ZH, 42, TERRA, 0.055, 0.230, "tl"),
            ("Boswellia · Pogostemon cablin", FONT_EN, 20, GREYBROWN, 0.055, 0.312, "tl"),
        ],
    )

    # R2-f4 擴香 — 奶油底 + 乳香
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R2_f4.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMCREAM,
        bottle_name="乳香",
        bottle_scale=0.60,
        bottle_x_frac=0.60,
        bottle_bottom_frac=0.80,
        shadow_offset_x=53, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R2", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("擴香 · 三滴", FONT_ZH, 66, BLACK, 0.055, 0.130, "tl"),
            ("乳香 + 廣藿香", FONT_ZH, 40, TERRA, 0.055, 0.244, "tl"),
            ("處暑節氣香氣儀式", FONT_ZH, 28, GREYBROWN, 0.055, 0.322, "tl"),
        ],
    )

    # R2-f5 桌面橫移 — 暗棕底
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R2_f5.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=DARKBROWN,
        bottle_name="乳香",
        bottle_scale=0.56,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.78,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R2", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("處暑", FONT_ZH_BOLD, 110, GOLDYELLOW, 0.055, 0.130, "tl"),
            ("秋天的前奏已經開始", FONT_ZH, 34, WARMCREAM, 0.055, 0.340, "tl"),
        ],
    )

    # R2-f6 Logo CTA — 焦糖底
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R2_f6.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=CARAMEL,
        bottle_name="乳香",
        bottle_scale=0.55,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.80,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R2", FONT_EN, 14, DARKBROWN, 0.055, 0.092, "tl"),
            ("處暑精選", FONT_ZH, 68, BLACK, 0.055, 0.130, "tl"),
            ("MORENE.COM.TW", FONT_EN, 30, DARKBROWN, 0.055, 0.244, "tl"),
            ("個人簡介連結 ↑", FONT_ZH, 28, BLACK, 0.055, 0.304, "tl"),
            ("情境使用 · 非療效宣稱", FONT_ZH, 16, DARKBROWN, 0.055, 0.944, "tl"),
        ],
    )

    print("R2 完成。")

    # ──────────────────────────────────────────────
    # R3 8/26 前中後調 (6幀)
    # f1 三杯排列 / f2 前調滴入 / f3 中調瓶 / f4 後調並排 / f5 換季構圖 / f6 Logo CTA
    # ──────────────────────────────────────────────
    print("R3 前中後調...")

    # R3-f1 三杯排列 — 暖白底 + 白葡萄柚(前調代表)
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R3_f1.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMWHITE,
        bottle_name="白葡萄柚",
        bottle_scale=0.60,
        bottle_x_frac=0.60,
        bottle_bottom_frac=0.80,
        shadow_offset_x=53, shadow_offset_y=24,
        shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("前調 · 中調 · 後調", FONT_ZH, 54, BLACK, 0.055, 0.130, "tl"),
            ("三層都認識了嗎?", FONT_ZH, 36, TERRA, 0.055, 0.226, "tl"),
            ("SCENT NOTES · TOP · HEART · BASE", FONT_EN, 20, GREYBROWN, 0.055, 0.310, "tl"),
        ],
    )

    # R3-f2 前調滴入 — 暖白底 + 白葡萄柚
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R3_f2.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMWHITE,
        bottle_name="白葡萄柚",
        bottle_scale=0.62,
        bottle_x_frac=0.62,
        bottle_bottom_frac=0.80,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("前調", FONT_ZH, 100, "#E8622A", 0.055, 0.130, "tl"),
            ("柑橘 · 草本", FONT_ZH, 46, BLACK, 0.055, 0.282, "tl"),
            ("前15分鐘 · 白葡萄柚 · 甜橙", FONT_ZH, 26, GREYBROWN, 0.055, 0.364, "tl"),
            ("Citrus paradisi", FONT_EN, 22, GREYBROWN, 0.055, 0.416, "tl"),
        ],
    )

    # R3-f3 中調瓶 — 霧粉底 + 真正薰衣草
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R3_f3.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=FOGPINK,
        bottle_name="真正薰衣草",
        bottle_scale=0.62,
        bottle_x_frac=0.62,
        bottle_bottom_frac=0.80,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("中調", FONT_ZH, 100, TERRA, 0.055, 0.130, "tl"),
            ("花香 · 辛香", FONT_ZH, 46, BLACK, 0.055, 0.282, "tl"),
            ("20–60分鐘 · 薰衣草 · 玫瑰天竺葵", FONT_ZH, 24, GREYBROWN, 0.055, 0.364, "tl"),
            ("Lavandula angustifolia", FONT_EN, 22, GREYBROWN, 0.055, 0.414, "tl"),
        ],
    )

    # R3-f4 後調並排 — 暗棕底 + 乳香
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R3_f4.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=DARKBROWN,
        bottle_name="乳香",
        bottle_scale=0.62,
        bottle_x_frac=0.62,
        bottle_bottom_frac=0.80,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("後調", FONT_ZH, 100, GOLDYELLOW, 0.055, 0.130, "tl"),
            ("木質 · 樹脂", FONT_ZH, 46, WARMCREAM, 0.055, 0.282, "tl"),
            ("1小時後 · 乳香 · 大西洋雪松", FONT_ZH, 24, GREYBROWN, 0.055, 0.364, "tl"),
            ("Boswellia carterii", FONT_EN, 22, GREYBROWN, 0.055, 0.414, "tl"),
        ],
    )

    # R3-f5 換季構圖 — 焦糖底 + 大西洋雪松
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R3_f5.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=CARAMEL,
        bottle_name="大西洋雪松",
        bottle_scale=0.62,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.80,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, DARKBROWN, 0.055, 0.092, "tl"),
            ("換季首選", FONT_ZH, 72, BLACK, 0.055, 0.130, "tl"),
            ("後調木質最適合秋天", FONT_ZH, 38, DARKBROWN, 0.055, 0.252, "tl"),
            ("大西洋雪松 · 乳香 · 廣藿香", FONT_ZH, 26, BLACK, 0.055, 0.338, "tl"),
        ],
    )

    # R3-f6 Logo CTA — 奶油底
    save_and_dual(
        "W37", "Reels", "MORENE_W37_R3_f6.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMCREAM,
        bottle_name="乳香",
        bottle_scale=0.55,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.80,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("前中後調全解析", FONT_ZH, 60, BLACK, 0.055, 0.130, "tl"),
            ("MORENE.COM.TW", FONT_EN, 30, TERRA, 0.055, 0.240, "tl"),
            ("個人簡介連結 ↑", FONT_ZH, 28, BLACK, 0.055, 0.300, "tl"),
            ("情境使用 · 非療效宣稱", FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ],
    )

    print("R3 完成。")
    print("W37 Reels 全部完成。")


# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    print("MORENE W37 常態化樣板週 圖卡生成開始...")
    print("=== 批次 1: Stories ===")
    make_stories()
    print("\n=== 批次 2: IG + FB ===")
    make_ig_fb()
    print("\n=== 批次 3: Reels ===")
    make_reels()
    print("\n全部完成。W37 46 張圖卡生成完畢。")
    print("路徑: /Users/morrislin/mw-social-assets/MORENE/W37/")
    print("雙寫: /Users/morrislin/Desktop/MORENE/MORENE_社群營運_Social/03_圖卡_Assets/W37/")
