#!/usr/bin/env python3
"""
MORENE W35–W36 七夕「送一支懂她的香氣」圖卡生成腳本
基於 make_w31_w34.py 視覺系統(Y2K 攝影 + 單色飽和底 + 真實瓶身主角 + 官方 logo + 規範字體)

重要前提:
- 無禮盒/無折扣/無包裝/無包裝卡片/無優惠
- 核心 = 「送一支懂她的香氣」,單支瓶,不用多瓶組
- CTA 導向 morene.com.tw/pages/scent-personality
- W36 引用秦觀《鵲橋仙》逐字,中文署名一律 FONT_ZH

CJK tofu 防呆:
- 含 CJK 字元之 text_line 必須使用 FONT_ZH / FONT_ZH_BOLD
- 此腳本在文字渲染前做自動斷言
"""

import os, sys, shutil
sys.path.insert(0, "/Users/morrislin/mw-social-assets/MORENE")
from make_covers_v2 import (
    compose_card,
    FONT_EN_BOLD, FONT_EN, FONT_ZH, FONT_ZH_BOLD,
    CREAM, BLACK, TERRA, MUSTARD, SAGE, ORANGE, WHITE,
    OUT_BASE,
)

# =====================
# 色彩補充(七夕暖色)
# =====================
FOGPINK   = "#E9C5B9"   # 霧粉(花香情境)
WARMSAND  = "#CBA98A"   # 暖沙
CARAMEL   = "#C9853E"   # 焦糖(七夕暖色)
FOGBLUE   = "#82A8CC"   # 霧藍

# =====================
# 路徑常數
# =====================
BASE_PROD = "/Users/morrislin/Desktop/MORENE/03_MORENE/03_Assets/A009：MORENE-產品相關/01.產品相關/01. 產品資料/05. 產品照片/素材/商品大圖/01_精油"
DESK_ASSETS = "/Users/morrislin/Desktop/MORENE/MORENE_社群營運_Social/03_圖卡_Assets"
LOGO_CREAM = "/Users/morrislin/mw-social-assets/MORENE/_fonts/MORENE_logo_cream.png"
LOGO_BLACK = "/Users/morrislin/mw-social-assets/MORENE/_fonts/MORENE_logo_black.png"

# W35-W36 瓶身路徑(補 make_covers_v2 沒有的)
EXTRA_BOTTLES = {
    "岩蘭草":       f"{BASE_PROD}/岩蘭草/MORENE_精油瓶_去背_岩蘭草.png",
    "白葡萄柚":     f"{BASE_PROD}/5MOEO011_白葡萄柚/MORENE_精油瓶_去背_白葡萄柚.png",
    "迷迭香":       f"{BASE_PROD}/桉油葉迷迭香/MORENE_精油瓶_去背_桉油葉迷迭香.png",
    "真正薰衣草":   f"{BASE_PROD}/5MOEO015_真正薰衣草/MORENE_精油瓶_去背_真正薰衣草.png",
    "乳香":         f"{BASE_PROD}/5MOEO009_乳香/MORENE_精油瓶_去背_乳香.png",
    "甜橙":         f"{BASE_PROD}/甜橙/MORENE_精油瓶_去背_甜橙.png",
    "玫瑰天竺葵":   f"{BASE_PROD}/5MOEO025_玫瑰天竺葵/MORENE_精油瓶_去背_玫瑰天竺葵.png",
    "大西洋雪松":   f"{BASE_PROD}/5MOEO005_大西洋雪松/MORENE_精油瓶_去背_大西洋雪松.png",
}

# Monkey-patch get_bottle to include extra bottles
import make_covers_v2 as _m
_orig_get_bottle = _m.get_bottle
def _patched_get_bottle(name):
    if name in EXTRA_BOTTLES:
        return EXTRA_BOTTLES[name]
    return _orig_get_bottle(name)
_m.get_bottle = _patched_get_bottle

# =====================
# CJK tofu 防呆斷言
# =====================
def _has_cjk(text):
    """Return True if text contains CJK characters needing ZH font.
    U+00B7 middle dot is explicitly excluded (safe in Outfit)."""
    for ch in text:
        cp = ord(ch)
        if cp == 0x00B7:  # middle dot · safe in Outfit/Latin fonts
            continue
        if (0x4E00 <= cp <= 0x9FFF or   # CJK Unified Ideographs
                0x3400 <= cp <= 0x4DBF or   # Extension A
                0x3000 <= cp <= 0x303F or   # CJK Symbols & Punctuation (《》「」…)
                0xF900 <= cp <= 0xFAFF or   # Compatibility Ideographs
                0x2E80 <= cp <= 0x2EFF or   # CJK Radicals Supplement
                0x2F00 <= cp <= 0x2FDF or   # Kangxi Radicals
                0xFF00 <= cp <= 0xFFEF or   # Fullwidth Forms
                0x3040 <= cp <= 0x30FF or   # Hiragana + Katakana
                0xFE30 <= cp <= 0xFE4F):    # CJK Compatibility Forms
            return True
    return False
_ZH_FONTS = {FONT_ZH, FONT_ZH_BOLD}

def assert_no_cjk_tofu(text_lines, card_name=""):
    """任何含 CJK 字元的行若用非 ZH 字型就 raise。"""
    for (text, fpath, fsize, color, xf, yf, anc) in text_lines:
        if text == "MORENE":
            continue  # logo 由圖像處理
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
    # tofu 防呆
    assert_no_cjk_tofu(compose_kwargs.get("text_lines", []), card_name=filename)
    nas_dir = f"{OUT_BASE}/{week}/{channel}"
    os.makedirs(nas_dir, exist_ok=True)
    nas_path = f"{nas_dir}/{filename}"
    compose_card(out_path=nas_path, **compose_kwargs)
    dual_save(week, channel, filename, nas_path)
    return nas_path


# =====================
# W35 ── 七夕前導(送一支懂她的香氣)
# 排程: FB 8/11(二)19:30 / IG 8/12(三)12:30 / Reels 8/13(四)20:00 / Stories 8/11(二)21:00
# =====================
def make_w35():
    print("\n=== W35 七夕前導:送一支懂她的香氣 ===")

    # --------------------------------------------------
    # FB hero 1080x1080 — 霧粉底 + 玫瑰天竺葵
    # --------------------------------------------------
    print("W35 FB hero...")
    save_and_dual(
        "W35", "FB", "MORENE_W35_FB_hero.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=FOGPINK,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.72,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.95,
        shadow_offset_x=68, shadow_offset_y=30,
        shadow_blur=46, shadow_opacity=0.18,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("七夕,送一支", FONT_ZH, 62, BLACK, 0.055, 0.108, "tl"),
            ("懂她的香氣", FONT_ZH, 62, TERRA, 0.055, 0.200, "tl"),
            ("與其送貴的,不如送對的。", FONT_ZH, 26, BLACK, 0.055, 0.306, "tl"),
            ("先測香氣人格,再選命定的那支。", FONT_ZH, 22, "#8C8079", 0.055, 0.350, "tl"),
            ("QIXI GIFT · MORENE.COM.TW", FONT_EN, 18, BLACK, 0.055, 0.944, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG p1 封面 1080x1350 — 陶土底 + 玫瑰天竺葵
    # --------------------------------------------------
    print("W35 IG p1 封面...")
    save_and_dual(
        "W35", "IG", "MORENE_W35_p1.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=TERRA,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.73,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.93,
        shadow_offset_x=68, shadow_offset_y=30,
        shadow_blur=46, shadow_opacity=0.20,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            ("七夕", FONT_ZH, 100, CREAM, 0.055, 0.095, "tl"),
            ("送一支", FONT_ZH, 100, MUSTARD, 0.055, 0.230, "tl"),
            ("懂她的香氣", FONT_ZH, 60, CREAM, 0.055, 0.365, "tl"),
            ("QIXI · SINGLE OIL GIFT · W35", FONT_EN, 18, CREAM, 0.055, 0.946, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG p2 為什麼送香氣 1080x1350 — 奶油底
    # --------------------------------------------------
    print("W35 IG p2 為什麼送香氣...")
    save_and_dual(
        "W35", "IG", "MORENE_W35_p2.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=CREAM,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.58,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.88,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("02 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("為什麼", FONT_ZH, 88, TERRA, 0.055, 0.095, "tl"),
            ("送香氣?", FONT_ZH, 72, BLACK, 0.055, 0.240, "tl"),
            ("香氣說出一個人的樣子。", FONT_ZH, 32, BLACK, 0.055, 0.366, "tl"),
            ("一支對的精油,比什麼都貼心。", FONT_ZH, 28, "#8C8079", 0.055, 0.420, "tl"),
            ("趣味體驗非診斷 · 情境使用", FONT_ZH, 15, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG p3 先測香氣人格 1080x1350 — 芥末底
    # --------------------------------------------------
    print("W35 IG p3 先測香氣人格...")
    save_and_dual(
        "W35", "IG", "MORENE_W35_p3.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=MUSTARD,
        bottle_name="甜橙",
        bottle_scale=0.60,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.88,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=38, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("03 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("先測", FONT_ZH, 100, BLACK, 0.055, 0.095, "tl"),
            ("香氣人格", FONT_ZH, 72, TERRA, 0.055, 0.250, "tl"),
            ("再選命定的那支", FONT_ZH, 36, BLACK, 0.055, 0.370, "tl"),
            ("8 題直覺作答 → 個人簡介連結", FONT_ZH, 24, BLACK, 0.055, 0.436, "tl"),
            ("morene.com.tw/pages/scent-personality", FONT_EN, 17, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG p4 依關係選:花香·柑橘·木質 1080x1350 — 深墨底
    # --------------------------------------------------
    print("W35 IG p4 依關係選...")
    save_and_dual(
        "W35", "IG", "MORENE_W35_p4.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=BLACK,
        bottle_name="乳香",
        bottle_scale=0.55,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.85,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            ("04 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("三種關係", FONT_ZH, 72, MUSTARD, 0.055, 0.095, "tl"),
            ("三支對的香氣", FONT_ZH, 48, CREAM, 0.055, 0.235, "tl"),
            ("送她  花香系 · 玫瑰天竺葵", FONT_ZH, 28, CREAM, 0.055, 0.338, "tl"),
            ("送閨蜜  柑橘系 · 甜橙/白葡萄柚", FONT_ZH, 28, CREAM, 0.055, 0.396, "tl"),
            ("送自己  木質系 · 乳香/大西洋雪松", FONT_ZH, 28, CREAM, 0.055, 0.454, "tl"),
            ("情境使用,不宣稱功效 · 趣味體驗非診斷", FONT_ZH, 15, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG p5 單支瓶示意 1080x1350 — 霧粉底 + 玫瑰天竺葵大圖
    # --------------------------------------------------
    print("W35 IG p5 單支瓶示意...")
    save_and_dual(
        "W35", "IG", "MORENE_W35_p5.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=FOGPINK,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.78,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.96,
        shadow_offset_x=72, shadow_offset_y=32,
        shadow_blur=50, shadow_opacity=0.18,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("05 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("一支瓶,", FONT_ZH, 62, BLACK, 0.055, 0.095, "tl"),
            ("剛剛好的心意。", FONT_ZH, 50, TERRA, 0.055, 0.190, "tl"),
            ("玫瑰天竺葵 · 花香系", FONT_ZH, 26, BLACK, 0.055, 0.300, "tl"),
            ("Rose Geranium · 10ml · NT$880", FONT_EN, 20, "#8C8079", 0.055, 0.340, "tl"),
            ("單支精油 · 非診斷 · 純情境使用", FONT_ZH, 15, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG p6 送禮對象 1080x1350 — 暖沙底
    # --------------------------------------------------
    print("W35 IG p6 送禮對象...")
    save_and_dual(
        "W35", "IG", "MORENE_W35_p6.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=WARMSAND,
        bottle_name="甜橙",
        bottle_scale=0.60,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.88,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("06 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("妳想送給誰?", FONT_ZH, 58, BLACK, 0.055, 0.095, "tl"),
            ("留言告訴我她是哪種香氣型", FONT_ZH, 30, BLACK, 0.055, 0.225, "tl"),
            ("花香 / 柑橘 / 木質 / 還沒測", FONT_ZH, 26, TERRA, 0.055, 0.284, "tl"),
            ("SINGLE OIL GIFT · 香氣人格選禮 W35", FONT_ZH, 17, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG p7 CTA 1080x1350 — 深墨底
    # --------------------------------------------------
    print("W35 IG p7 CTA...")
    save_and_dual(
        "W35", "IG", "MORENE_W35_p7.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=BLACK,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.55,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.85,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            ("07 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("先測妳的", FONT_ZH, 56, CREAM, 0.055, 0.100, "tl"),
            ("香氣人格", FONT_ZH, 56, MUSTARD, 0.055, 0.185, "tl"),
            ("再決定送她哪一支", FONT_ZH, 34, CREAM, 0.055, 0.278, "tl"),
            ("個人簡介連結 · 8 題直覺作答", FONT_ZH, 24, CREAM, 0.055, 0.338, "tl"),
            ("morene.com.tw/pages/scent-personality", FONT_EN, 17, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # --------------------------------------------------
    # Reels 封面 1080x1920 — 陶土底 + 玫瑰天竺葵
    # --------------------------------------------------
    print("W35 Reels cover...")
    save_and_dual(
        "W35", "Reels", "MORENE_W35_Reels_cover.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=TERRA,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.68,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.88,
        shadow_offset_x=72, shadow_offset_y=32,
        shadow_blur=50, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, CREAM, 0.055, 0.040, "tl"),
            ("七夕送什麼?", FONT_ZH, 90, CREAM, 0.055, 0.076, "tl"),
            ("送一支", FONT_ZH, 90, MUSTARD, 0.055, 0.198, "tl"),
            ("只屬於她的香氣", FONT_ZH, 54, CREAM, 0.055, 0.320, "tl"),
            ("測香氣人格 → 選命定那支", FONT_ZH, 28, CREAM, 0.055, 0.400, "tl"),
            ("QIXI GIFT · SINGLE OIL · W35", FONT_EN, 22, CREAM, 0.055, 0.944, "tl"),
        ],
    )

    # --------------------------------------------------
    # Stories x3 — 1080x1920
    # --------------------------------------------------
    # S1: 投票「送她 vs 送自己」— 霧粉底
    print("W35 Stories S1...")
    save_and_dual(
        "W35", "Stories", "MORENE_W35_S1.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=FOGPINK,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=20,
        shadow_blur=34, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("STORIES · W35", FONT_EN, 14, "#8C8079", 0.055, 0.092, "tl"),
            ("七夕妳會怎麼選?", FONT_ZH, 52, BLACK, 0.055, 0.130, "tl"),
            ("送她一支懂她的香氣", FONT_ZH, 36, TERRA, 0.055, 0.228, "tl"),
            ("vs", FONT_EN_BOLD, 36, BLACK, 0.055, 0.304, "tl"),
            ("送自己一支命定香氣", FONT_ZH, 36, BLACK, 0.055, 0.356, "tl"),
            ("留言告訴我 👇", FONT_ZH, 30, BLACK, 0.055, 0.436, "tl"),
            ("香氣人格測驗 · 個人簡介連結", FONT_ZH, 18, "#8C8079", 0.055, 0.944, "tl"),
        ],
    )

    # S2: 怎麼挑(先測香氣人格)— 芥末底
    print("W35 Stories S2...")
    save_and_dual(
        "W35", "Stories", "MORENE_W35_S2.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=MUSTARD,
        bottle_name="甜橙",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=34, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("送對了,", FONT_ZH, 62, BLACK, 0.055, 0.130, "tl"),
            ("比送貴的更難忘", FONT_ZH, 46, TERRA, 0.055, 0.222, "tl"),
            ("Step 1 請她測香氣人格", FONT_ZH, 30, BLACK, 0.055, 0.334, "tl"),
            ("Step 2 對應花香/柑橘/木質", FONT_ZH, 30, BLACK, 0.055, 0.390, "tl"),
            ("Step 3 選那支命定單方精油", FONT_ZH, 30, BLACK, 0.055, 0.446, "tl"),
            ("趣味體驗非診斷 · MORENE.COM.TW", FONT_ZH, 18, BLACK, 0.055, 0.944, "tl"),
        ],
    )

    # S3: 測驗連結導流 — 奶油底
    print("W35 Stories S3...")
    save_and_dual(
        "W35", "Stories", "MORENE_W35_S3.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=CREAM,
        bottle_name="乳香",
        bottle_scale=0.50,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.75,
        shadow_offset_x=44, shadow_offset_y=18,
        shadow_blur=32, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("她是哪種香氣型?", FONT_ZH, 52, BLACK, 0.055, 0.130, "tl"),
            ("花香 · 柑橘 · 木質", FONT_ZH, 40, TERRA, 0.055, 0.230, "tl"),
            ("8 題直覺作答", FONT_ZH, 36, BLACK, 0.055, 0.318, "tl"),
            ("個人簡介連結 ↑", FONT_ZH, 34, TERRA, 0.055, 0.400, "tl"),
            ("morene.com.tw/pages/scent-personality", FONT_EN, 18, "#8C8079", 0.055, 0.944, "tl"),
        ],
    )

    print("W35 完成。")


# =====================
# W36 ── 七夕檔(8/19)
# 排程: FB 8/18(二)19:30 / IG 8/17(一)12:30 / Reels 8/19(三)20:00 / Stories 8/18(二)21:00
# =====================
def make_w36():
    print("\n=== W36 七夕檔(8/19):三種情境三支香氣 ===")

    # --------------------------------------------------
    # FB 1080x1080 — 深墨底 + 引用秦觀《鵲橋仙》
    # ⚠️ 秦觀署名一律 FONT_ZH
    # --------------------------------------------------
    print("W36 FB 秦觀詞...")
    save_and_dual(
        "W36", "FB", "MORENE_W36_FB_qiqiao.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=BLACK,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.68,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.95,
        shadow_offset_x=65, shadow_offset_y=28,
        shadow_blur=44, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            # 秦觀《鵲橋仙》逐字 — 必須 FONT_ZH
            ("兩情若是久長時,", FONT_ZH, 42, CREAM, 0.055, 0.130, "tl"),
            ("又豈在朝朝暮暮。", FONT_ZH, 42, MUSTARD, 0.055, 0.202, "tl"),
            ("— 秦觀《鵲橋仙·纖雲弄巧》", FONT_ZH, 21, WARMSAND, 0.055, 0.282, "tl"),
            ("這週下單,剛剛好趕在七夕(8/19)。", FONT_ZH, 26, CREAM, 0.055, 0.376, "tl"),
            ("送一支對的精油,一支剛剛好的心意。", FONT_ZH, 24, CREAM, 0.055, 0.428, "tl"),
            ("情境使用,不宣稱功效 · MORENE.COM.TW", FONT_ZH, 14, "#8C8079", 0.055, 0.944, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG p1 封面 1080x1350 — 霧粉底 + 玫瑰天竺葵
    # --------------------------------------------------
    print("W36 IG p1 封面...")
    save_and_dual(
        "W36", "IG", "MORENE_W36_p1.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=FOGPINK,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.73,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.93,
        shadow_offset_x=68, shadow_offset_y=30,
        shadow_blur=46, shadow_opacity=0.18,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("七夕 8/19", FONT_ZH, 72, BLACK, 0.055, 0.095, "tl"),
            ("送她,送閨蜜", FONT_ZH, 52, TERRA, 0.055, 0.222, "tl"),
            ("還是送自己?", FONT_ZH, 52, BLACK, 0.055, 0.302, "tl"),
            ("QIXI · THREE SCENTS · THREE BONDS · W36", FONT_EN, 17, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG p2 送她 — 花香系 1080x1350 — 霧粉底 + 玫瑰天竺葵
    # --------------------------------------------------
    print("W36 IG p2 送她(花香)...")
    save_and_dual(
        "W36", "IG", "MORENE_W36_p2.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=FOGPINK,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.70,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.93,
        shadow_offset_x=65, shadow_offset_y=28,
        shadow_blur=44, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("02 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("送她", FONT_ZH, 110, TERRA, 0.055, 0.095, "tl"),
            ("花香系", FONT_ZH, 60, BLACK, 0.055, 0.290, "tl"),
            ("玫瑰天竺葵", FONT_ZH, 40, BLACK, 0.055, 0.380, "tl"),
            ("Rose Geranium · NT$880", FONT_EN, 22, "#8C8079", 0.055, 0.448, "tl"),
            ("像她的輕盈,像愛的溫度。", FONT_ZH, 26, BLACK, 0.055, 0.510, "tl"),
            ("單方精油 · 情境使用 · 非療效宣稱", FONT_ZH, 15, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG p3 送閨蜜 — 柑橘系 1080x1350 — 芥末底 + 甜橙
    # --------------------------------------------------
    print("W36 IG p3 送閨蜜(柑橘)...")
    save_and_dual(
        "W36", "IG", "MORENE_W36_p3.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=MUSTARD,
        bottle_name="甜橙",
        bottle_scale=0.70,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.93,
        shadow_offset_x=65, shadow_offset_y=28,
        shadow_blur=44, shadow_opacity=0.18,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("03 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("送閨蜜", FONT_ZH, 90, BLACK, 0.055, 0.095, "tl"),
            ("柑橘系", FONT_ZH, 60, TERRA, 0.055, 0.268, "tl"),
            ("甜橙 / 白葡萄柚", FONT_ZH, 40, BLACK, 0.055, 0.360, "tl"),
            ("Sweet Orange · White Grapefruit", FONT_EN, 20, "#8C8079", 0.055, 0.420, "tl"),
            ("那個一起笑到肚子痛的人。", FONT_ZH, 26, BLACK, 0.055, 0.480, "tl"),
            ("單方精油 · 情境使用 · 非療效宣稱", FONT_ZH, 15, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG p4 送自己 — 木質系 1080x1350 — 深墨底 + 大西洋雪松
    # --------------------------------------------------
    print("W36 IG p4 送自己(木質)...")
    save_and_dual(
        "W36", "IG", "MORENE_W36_p4.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=BLACK,
        bottle_name="大西洋雪松",
        bottle_scale=0.70,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.93,
        shadow_offset_x=65, shadow_offset_y=28,
        shadow_blur=44, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            ("04 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("送自己", FONT_ZH, 90, CREAM, 0.055, 0.095, "tl"),
            ("木質系", FONT_ZH, 60, MUSTARD, 0.055, 0.268, "tl"),
            ("乳香 / 大西洋雪松", FONT_ZH, 40, CREAM, 0.055, 0.360, "tl"),
            ("Frankincense · Atlas Cedar", FONT_EN, 20, "#8C8079", 0.055, 0.420, "tl"),
            ("七夕也可以是給自己的儀式。", FONT_ZH, 26, CREAM, 0.055, 0.480, "tl"),
            ("單方精油 · 情境使用 · 非療效宣稱", FONT_ZH, 15, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG p5 香氣人格截圖說明 1080x1350 — 暖沙底
    # --------------------------------------------------
    print("W36 IG p5 香氣人格截圖...")
    save_and_dual(
        "W36", "IG", "MORENE_W36_p5.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=WARMSAND,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.58,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.86,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("05 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("附上她的", FONT_ZH, 68, BLACK, 0.055, 0.095, "tl"),
            ("香氣人格截圖", FONT_ZH, 54, TERRA, 0.055, 0.218, "tl"),
            ("免費的個人化心意。", FONT_ZH, 34, BLACK, 0.055, 0.330, "tl"),
            ("讓她知道妳選的那支", FONT_ZH, 26, BLACK, 0.055, 0.398, "tl"),
            ("是為她量身對應的。", FONT_ZH, 26, BLACK, 0.055, 0.448, "tl"),
            ("測驗 · morene.com.tw/pages/scent-personality", FONT_ZH, 17, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG p6 秦觀詩引 1080x1350 — 奶油底
    # ⚠️ 秦觀中文著作署名一律 FONT_ZH
    # --------------------------------------------------
    print("W36 IG p6 秦觀詩引...")
    save_and_dual(
        "W36", "IG", "MORENE_W36_p6.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=CREAM,
        bottle_name="乳香",
        bottle_scale=0.62,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.90,
        shadow_offset_x=58, shadow_offset_y=26,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("06 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("兩情若是久長時,", FONT_ZH, 40, BLACK, 0.055, 0.110, "tl"),
            ("又豈在朝朝暮暮。", FONT_ZH, 40, TERRA, 0.055, 0.184, "tl"),
            ("— 秦觀《鵲橋仙·纖雲弄巧》", FONT_ZH, 21, "#8C8079", 0.055, 0.266, "tl"),
            ("這個七夕,不用說很多。", FONT_ZH, 30, BLACK, 0.055, 0.354, "tl"),
            ("一支對的香氣,已經說完了。", FONT_ZH, 30, BLACK, 0.055, 0.410, "tl"),
            ("情境使用 · 非療效宣稱 · 趣味體驗非診斷", FONT_ZH, 15, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # --------------------------------------------------
    # IG p7 CTA 1080x1350 — 深墨底
    # --------------------------------------------------
    print("W36 IG p7 CTA...")
    save_and_dual(
        "W36", "IG", "MORENE_W36_p7.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=BLACK,
        bottle_name="大西洋雪松",
        bottle_scale=0.55,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.85,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            ("07 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("七夕(8/19)", FONT_ZH, 58, CREAM, 0.055, 0.100, "tl"),
            ("本週下單剛剛好", FONT_ZH, 50, MUSTARD, 0.055, 0.188, "tl"),
            ("測驗 → 選香氣 → 送出去", FONT_ZH, 30, CREAM, 0.055, 0.300, "tl"),
            ("個人簡介連結 · morene.com.tw", FONT_ZH, 24, CREAM, 0.055, 0.366, "tl"),
            ("配送時間請以官網實際為準 · 情境使用非療效", FONT_ZH, 14, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # --------------------------------------------------
    # Reels 封面 1080x1920 — 焦糖底 + 玫瑰天竺葵
    # --------------------------------------------------
    print("W36 Reels cover...")
    save_and_dual(
        "W36", "Reels", "MORENE_W36_Reels_cover.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=CARAMEL,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.68,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.88,
        shadow_offset_x=72, shadow_offset_y=32,
        shadow_blur=50, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("七夕快選", FONT_ZH, 100, BLACK, 0.055, 0.076, "tl"),
            ("三種人", FONT_ZH, 80, CREAM, 0.055, 0.210, "tl"),
            ("三支對的香氣", FONT_ZH, 56, BLACK, 0.055, 0.316, "tl"),
            ("花香 · 柑橘 · 木質", FONT_ZH, 34, BLACK, 0.055, 0.402, "tl"),
            ("QIXI GIFT · MORENE · W36", FONT_EN, 22, BLACK, 0.055, 0.944, "tl"),
        ],
    )

    # --------------------------------------------------
    # Stories x3 — 1080x1920
    # --------------------------------------------------
    # S1: 七夕倒數 — 深墨底
    print("W36 Stories S1...")
    save_and_dual(
        "W36", "Stories", "MORENE_W36_S1.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=BLACK,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=20,
        shadow_blur=34, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, CREAM, 0.055, 0.040, "tl"),
            ("STORIES · W36", FONT_EN, 14, "#8C8079", 0.055, 0.092, "tl"),
            ("七夕 8/19", FONT_ZH, 72, MUSTARD, 0.055, 0.130, "tl"),
            ("倒數不到一週", FONT_ZH, 48, CREAM, 0.055, 0.252, "tl"),
            ("送一支懂她的香氣", FONT_ZH, 36, CREAM, 0.055, 0.340, "tl"),
            ("現在測香氣人格 → 個人簡介連結", FONT_ZH, 24, WARMSAND, 0.055, 0.416, "tl"),
            ("QIXI GIFT · 情境使用非療效 · MORENE.COM.TW", FONT_ZH, 17, CREAM, 0.055, 0.944, "tl"),
        ],
    )

    # S2: 三情境快選 — 暖沙底
    print("W36 Stories S2...")
    save_and_dual(
        "W36", "Stories", "MORENE_W36_S2.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=WARMSAND,
        bottle_name="甜橙",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=34, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("三種關係", FONT_ZH, 68, BLACK, 0.055, 0.130, "tl"),
            ("快選一支", FONT_ZH, 52, TERRA, 0.055, 0.218, "tl"),
            ("花香  送她 → 玫瑰天竺葵", FONT_ZH, 30, BLACK, 0.055, 0.322, "tl"),
            ("柑橘  送閨蜜 → 甜橙/白葡萄柚", FONT_ZH, 30, BLACK, 0.055, 0.384, "tl"),
            ("木質  送自己 → 乳香/大西洋雪松", FONT_ZH, 30, BLACK, 0.055, 0.446, "tl"),
            ("情境使用非療效 · 趣味體驗非診斷 · MORENE", FONT_ZH, 16, "#8C8079", 0.055, 0.944, "tl"),
        ],
    )

    # S3: 最後下單提醒 — 霧粉底
    print("W36 Stories S3...")
    save_and_dual(
        "W36", "Stories", "MORENE_W36_S3.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=FOGPINK,
        bottle_name="大西洋雪松",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=34, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("本週下單", FONT_ZH, 72, BLACK, 0.055, 0.130, "tl"),
            ("剛剛好", FONT_ZH, 72, TERRA, 0.055, 0.252, "tl"),
            ("七夕(8/19)前送達", FONT_ZH, 40, BLACK, 0.055, 0.368, "tl"),
            ("配送時間請以官網實際為準", FONT_ZH, 22, "#8C8079", 0.055, 0.440, "tl"),
            ("個人簡介連結 ↑", FONT_ZH, 32, TERRA, 0.055, 0.510, "tl"),
            ("MORENE.COM.TW · 情境使用非療效", FONT_ZH, 17, BLACK, 0.055, 0.944, "tl"),
        ],
    )

    print("W36 完成。")


# =====================
# 主程式
# =====================
if __name__ == "__main__":
    print("MORENE W35–W36 七夕圖卡生成開始...")
    make_w35()
    make_w36()
    print("\n全部完成。")
