#!/usr/bin/env python3
"""
MORENE W4 增量圖卡生成腳本 (Wave 4, 7/19–7/25, 大暑 7/23, 31 則)
規格: Stories/Reels 1080×1920; IG 1080×1350; FB 1080×1080
樣式: Y2K 攝影主導 + 單色暖色底 + 真實琥珀瓶 + 極少字
字體: BW Gradual/英 + Noto Sans TC/中 + Outfit/小字
無 ISO/認證標章 | 身體塗抹=稀釋提醒+感受/儀式詞,無療效詞

CJK tofu 防呆: 所有含漢字之 text 必須用 FONT_ZH/FONT_ZH_BOLD
色票: 全用 MORENE VIS 官方暖色票(不用 Savor 鮮綠 #2D6A4F / 橘 #E8622A)
大暑強調色 = 陶土磚紅 #A85539 + 焦糖 #C9853E
"""

import os, sys
sys.path.insert(0, "/Users/morrislin/mw-social-assets/MORENE")
from make_covers_v2 import (
    compose_card,
    FONT_EN_BOLD, FONT_EN, FONT_ZH, FONT_ZH_BOLD,
    CREAM, BLACK, TERRA, SAGE, WHITE,
    OUT_BASE, hex2rgb, fnt, get_logo, add_contact_shadow, add_directional_shadow,
    crop_to_bottle,
)
from PIL import Image, ImageDraw

# =====================
# 色彩補充 (VIS 暖色票)
# =====================
CARAMEL   = "#C9853E"   # 焦糖
MUSTARD   = "#E8CE8C"   # 芥末黃
FOGPINK   = "#E9C5B9"   # 霧粉
WARMSAND  = "#CBA98A"   # 暖沙
FOGBLUE   = "#82A8CC"   # 霧藍
FOGSAGE   = "#8DBFBE"   # 霧藍綠 (= SAGE)
GRYBROWN  = "#8C8079"   # 灰褐
DARKBROWN = "#2A2520"   # 深暗褐

# =====================
# 路徑常數
# =====================
BASE_PROD = "/Users/morrislin/Desktop/MORENE/03_MORENE/03_Assets/A009：MORENE-產品相關/01.產品相關/01. 產品資料/05. 產品照片/素材/商品大圖/01_精油"
OUT_W4    = "/Users/morrislin/mw-social-assets/MORENE/W_increment"

# =====================
# W4 新增瓶身路徑
# =====================
BOTTLES = {
    "乳香":     f"{BASE_PROD}/5MOEO009_乳香/MORENE_精油瓶_去背_乳香.png",
    "甜橙":     f"{BASE_PROD}/甜橙/MORENE_精油瓶_去背_甜橙.png",
    "白葡萄柚": f"{BASE_PROD}/5MOEO011_白葡萄柚/MORENE_精油瓶_去背_白葡萄柚.png",
    "薄荷":     f"{BASE_PROD}/薄荷/MORENE_精油瓶_去背_薄荷.png",
    "茶樹":     f"{BASE_PROD}/茶樹/MORENE_精油瓶_去背_茶樹.png",
    "甜羅勒":   f"{BASE_PROD}/5MOEO002_甜羅勒/MORENE_精油瓶_去背_甜羅勒.png",
    "迷迭香":   f"{BASE_PROD}/桉油葉迷迭香/MORENE_精油瓶_去背_桉油葉迷迭香.png",
}

import make_covers_v2 as _m
_orig_get_bottle = _m.get_bottle
def _patched_get_bottle(name):
    if name in BOTTLES:
        return BOTTLES[name]
    return _orig_get_bottle(name)
_m.get_bottle = _patched_get_bottle

LOGO_CREAM = "/Users/morrislin/mw-social-assets/MORENE/_fonts/MORENE_logo_cream.png"
LOGO_BLACK = "/Users/morrislin/mw-social-assets/MORENE/_fonts/MORENE_logo_black.png"

# =====================
# CJK 防呆斷言
# =====================
def _has_cjk(text):
    for ch in text:
        cp = ord(ch)
        if cp == 0x00B7:
            continue
        if (0x4E00 <= cp <= 0x9FFF or 0x3400 <= cp <= 0x4DBF or
                0x3000 <= cp <= 0x303F or 0xF900 <= cp <= 0xFAFF or
                0x2E80 <= cp <= 0x2EFF or 0xFF00 <= cp <= 0xFFEF or
                0x3040 <= cp <= 0x30FF or 0xAC00 <= cp <= 0xD7AF):
            return True
    return False

def _assert_no_tofu(text_lines):
    for item in text_lines:
        text, fpath = item[0], item[1]
        if _has_cjk(text):
            assert fpath in (FONT_ZH, FONT_ZH_BOLD), (
                f"TOFU RISK: CJK text \"{text[:20]}\" uses non-ZH font {fpath}"
            )

# =====================
# 輔助: 帶 logo 的 compose_card 包裝
# =====================
def card(w, h, bg, bottle, bscale, bxf, byf, lines, out, **kwargs):
    _assert_no_tofu(lines)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    return compose_card(w, h, bg, bottle, bscale, bxf, byf, lines, out, **kwargs)

def logo_line(color_hex, xf, yf):
    """MORENE logo text_line tuple"""
    return ("MORENE", FONT_EN_BOLD, 1, color_hex, xf, yf, "tl")


# =====================
# STORIES ×14  (1080×1920)
# =====================
SW, SH = 1080, 1920

def make_stories():
    os.makedirs(f"{OUT_W4}/Stories", exist_ok=True)

    # S1 7/19 柑橘暖身 — 焦糖底+甜橙/白葡萄柚兩瓶
    card(SW, SH, CARAMEL, "甜橙", 0.72, 0.52, 0.82, [
        logo_line(CREAM, 0.07, 0.06),
        ("07.19", FONT_EN, 36, CREAM, 0.07, 0.11, "tl"),
        ("Citrus Wake-Up", FONT_EN_BOLD, 72, CREAM, 0.07, 0.15, "tl"),
        ("柑橘,留住夏天最後的陽光", FONT_ZH_BOLD, 46, CREAM, 0.07, 0.25, "tl"),
        ("甜橙・白葡萄柚", FONT_ZH, 36, MUSTARD, 0.07, 0.33, "tl"),
        ("你今天選哪支? ↓", FONT_ZH_BOLD, 38, MUSTARD, 0.07, 0.88, "tl"),
    ], f"{OUT_W4}/Stories/MORENE_W4inc_S1.png",
    shadow_offset_x=45, shadow_opacity=0.22)
    print("S1 done")

    # S2 7/19 測驗導流 — 深暗褐底+白文
    card(SW, SH, DARKBROWN, "乳香", 0.68, 0.60, 0.85, [
        logo_line(CREAM, 0.07, 0.06),
        ("07.19", FONT_EN, 36, FOGPINK, 0.07, 0.11, "tl"),
        ("你是哪種香氣人格?", FONT_ZH_BOLD, 54, CREAM, 0.07, 0.16, "tl"),
        ("16 型香氣人格測驗", FONT_ZH, 40, FOGPINK, 0.07, 0.25, "tl"),
        ("柑橘型・木質型・花香型・大地型", FONT_ZH, 32, WARMSAND, 0.07, 0.32, "tl"),
        ("點 bio 連結立即測驗 →", FONT_ZH_BOLD, 40, MUSTARD, 0.07, 0.88, "tl"),
    ], f"{OUT_W4}/Stories/MORENE_W4inc_S2.png",
    shadow_offset_x=35, shadow_opacity=0.18)
    print("S2 done")

    # S3 7/20 廚房去味投票 — 奶油白底+薄荷/茶樹
    card(SW, SH, CREAM, "薄荷", 0.66, 0.55, 0.80, [
        logo_line(BLACK, 0.07, 0.06),
        ("07.20", FONT_EN, 36, TERRA, 0.07, 0.11, "tl"),
        ("Kitchen Fresh", FONT_EN_BOLD, 68, BLACK, 0.07, 0.15, "tl"),
        ("廚房去味,你選哪支?", FONT_ZH_BOLD, 52, BLACK, 0.07, 0.24, "tl"),
        ("A  薄荷・清涼透氣感", FONT_ZH, 42, TERRA, 0.07, 0.52, "tl"),
        ("B  茶樹・乾淨清潔感", FONT_ZH, 42, BLACK, 0.07, 0.61, "tl"),
        ("C  甜橙・果香覆蓋", FONT_ZH, 42, BLACK, 0.07, 0.70, "tl"),
        ("留言選你的答案 ↓", FONT_ZH, 34, GRYBROWN, 0.07, 0.88, "tl"),
    ], f"{OUT_W4}/Stories/MORENE_W4inc_S3.png")
    print("S3 done")

    # S4 7/20 廚房新文導流 — 暖焦糖底
    card(SW, SH, CARAMEL, "茶樹", 0.64, 0.56, 0.80, [
        logo_line(CREAM, 0.07, 0.06),
        ("07.20", FONT_EN, 36, MUSTARD, 0.07, 0.11, "tl"),
        ("Kitchen Blend", FONT_EN_BOLD, 72, CREAM, 0.07, 0.15, "tl"),
        ("廚房空間的去味配方", FONT_ZH_BOLD, 50, CREAM, 0.07, 0.25, "tl"),
        ("擴香怎麼用・效果怎麼選", FONT_ZH, 36, MUSTARD, 0.07, 0.33, "tl"),
        ("完整文章,點 bio 連結 →", FONT_ZH_BOLD, 38, MUSTARD, 0.07, 0.87, "tl"),
    ], f"{OUT_W4}/Stories/MORENE_W4inc_S4.png",
    shadow_opacity=0.20)
    print("S4 done")

    # S5 7/21 薄荷vs柑橘投票 — 霧藍綠/焦糖撞色(VIS 暖撞)
    card(SW, SH, FOGSAGE, "薄荷", 0.68, 0.54, 0.82, [
        logo_line(BLACK, 0.07, 0.06),
        ("07.21", FONT_EN, 36, BLACK, 0.07, 0.11, "tl"),
        ("薄荷 vs 柑橘", FONT_ZH_BOLD, 62, BLACK, 0.07, 0.16, "tl"),
        ("夏天最需要哪一種?", FONT_ZH, 42, BLACK, 0.07, 0.26, "tl"),
        ("薄荷", FONT_ZH_BOLD, 56, BLACK, 0.07, 0.55, "tl"),
        ("清涼・透氣・提神", FONT_ZH, 34, DARKBROWN, 0.07, 0.63, "tl"),
        ("柑橘", FONT_ZH_BOLD, 56, CARAMEL, 0.55, 0.55, "tl"),
        ("活力・陽光・溫暖感", FONT_ZH, 34, DARKBROWN, 0.55, 0.63, "tl"),
        ("留言告訴我們 →", FONT_ZH, 34, BLACK, 0.07, 0.88, "tl"),
    ], f"{OUT_W4}/Stories/MORENE_W4inc_S5.png",
    shadow_opacity=0.20)
    print("S5 done")

    # S6 7/21 薄荷後頸情境 — 冷調霧藍綠底+薄荷瓶+稀釋提醒
    card(SW, SH, FOGSAGE, "薄荷", 0.70, 0.52, 0.84, [
        logo_line(BLACK, 0.07, 0.06),
        ("07.21", FONT_EN, 36, BLACK, 0.07, 0.11, "tl"),
        ("Neck Cool-Down", FONT_EN_BOLD, 64, BLACK, 0.07, 0.15, "tl"),
        ("夏天頸側的香氣儀式", FONT_ZH_BOLD, 50, BLACK, 0.07, 0.24, "tl"),
        ("薄荷精油・後頸・手腕", FONT_ZH, 36, DARKBROWN, 0.07, 0.33, "tl"),
        ("一滴清涼,從香氣感受夏日", FONT_ZH, 34, DARKBROWN, 0.07, 0.40, "tl"),
        ("⚠ 使用前請以基底油稀釋 2-3%", FONT_ZH_BOLD, 30, TERRA, 0.07, 0.75, "tl"),
        ("敏感肌與孕婦請諮詢後使用", FONT_ZH, 26, GRYBROWN, 0.07, 0.81, "tl"),
        ("IFA 監製・學名產地透明", FONT_ZH, 26, GRYBROWN, 0.07, 0.88, "tl"),
    ], f"{OUT_W4}/Stories/MORENE_W4inc_S6.png",
    shadow_offset_x=40, shadow_opacity=0.22)
    print("S6 done")

    # S7 7/22 書房擴香問答 — 奶油白+甜羅勒瓶+暖白
    card(SW, SH, CREAM, "甜羅勒", 0.66, 0.54, 0.80, [
        logo_line(BLACK, 0.07, 0.06),
        ("07.22", FONT_EN, 36, TERRA, 0.07, 0.11, "tl"),
        ("Study Room Scent", FONT_EN_BOLD, 62, BLACK, 0.07, 0.15, "tl"),
        ("書房裡,你用哪種香氣?", FONT_ZH_BOLD, 50, BLACK, 0.07, 0.24, "tl"),
        ("A  甜羅勒・專注草本", FONT_ZH, 40, TERRA, 0.07, 0.50, "tl"),
        ("B  迷迭香・清醒提振", FONT_ZH, 40, BLACK, 0.07, 0.59, "tl"),
        ("C  薄荷・清涼降溫", FONT_ZH, 40, BLACK, 0.07, 0.68, "tl"),
        ("D  乳香・沉靜深思", FONT_ZH, 40, BLACK, 0.07, 0.77, "tl"),
        ("留言選你的書房香 ↓", FONT_ZH, 32, GRYBROWN, 0.07, 0.88, "tl"),
    ], f"{OUT_W4}/Stories/MORENE_W4inc_S7.png")
    print("S7 done")

    # S8 7/22 書房Reels預告 — 暗底+預告感
    card(SW, SH, DARKBROWN, "迷迭香", 0.66, 0.56, 0.82, [
        logo_line(CREAM, 0.07, 0.06),
        ("07.22", FONT_EN, 36, FOGPINK, 0.07, 0.11, "tl"),
        ("Coming Soon", FONT_EN_BOLD, 80, CREAM, 0.07, 0.15, "tl"),
        ("書房配香 Reels", FONT_ZH_BOLD, 54, CREAM, 0.07, 0.27, "tl"),
        ("從甜羅勒到乳香", FONT_ZH, 38, WARMSAND, 0.07, 0.36, "tl"),
        ("打造你的專注香氣空間", FONT_ZH, 36, WARMSAND, 0.07, 0.43, "tl"),
        ("明天上線,記得開通知 →", FONT_ZH_BOLD, 38, MUSTARD, 0.07, 0.87, "tl"),
    ], f"{OUT_W4}/Stories/MORENE_W4inc_S8.png",
    shadow_offset_x=40, shadow_opacity=0.22)
    print("S8 done")

    # S9 7/23 大暑漢字 — 深陶土底+大字
    card(SW, SH, TERRA, "乳香", 0.72, 0.55, 0.84, [
        logo_line(CREAM, 0.07, 0.06),
        ("07.23  大暑", FONT_ZH_BOLD, 42, MUSTARD, 0.07, 0.11, "tl"),
        ("大", FONT_ZH_BOLD, 260, CREAM, 0.04, 0.12, "tl"),
        ("暑", FONT_ZH_BOLD, 260, CREAM, 0.04, 0.38, "tl"),
        ("Da Shu", FONT_EN_BOLD, 52, FOGPINK, 0.07, 0.67, "tl"),
        ("一年最熱的節氣", FONT_ZH, 38, CREAM, 0.07, 0.74, "tl"),
        ("香氣,是夏日最好的儀式", FONT_ZH_BOLD, 38, MUSTARD, 0.07, 0.87, "tl"),
    ], f"{OUT_W4}/Stories/MORENE_W4inc_S9.png",
    shadow_offset_x=50, shadow_opacity=0.25)
    print("S9 done")

    # S10 7/23 大暑夜投票清涼/木質 — 深夜底+兩瓶對比
    card(SW, SH, DARKBROWN, "乳香", 0.64, 0.58, 0.82, [
        logo_line(CREAM, 0.07, 0.06),
        ("07.23  大暑之夜", FONT_ZH_BOLD, 38, FOGPINK, 0.07, 0.11, "tl"),
        ("大暑入夜,你選哪種香?", FONT_ZH_BOLD, 50, CREAM, 0.07, 0.17, "tl"),
        ("清涼系", FONT_ZH_BOLD, 54, FOGSAGE, 0.07, 0.55, "tl"),
        ("薄荷・白葡萄柚", FONT_ZH, 34, CREAM, 0.07, 0.63, "tl"),
        ("木質系", FONT_ZH_BOLD, 54, WARMSAND, 0.55, 0.55, "tl"),
        ("乳香・大西洋雪松", FONT_ZH, 34, CREAM, 0.55, 0.63, "tl"),
        ("你的夜晚選哪邊? ↓", FONT_ZH, 34, FOGPINK, 0.07, 0.87, "tl"),
    ], f"{OUT_W4}/Stories/MORENE_W4inc_S10.png",
    shadow_opacity=0.20)
    print("S10 done")

    # S11 7/24 收納新文導流 — 精油瓶整齊+暖木底
    card(SW, SH, WARMSAND, "甜橙", 0.64, 0.54, 0.80, [
        logo_line(BLACK, 0.07, 0.06),
        ("07.24", FONT_EN, 36, TERRA, 0.07, 0.11, "tl"),
        ("Storage Know-How", FONT_EN_BOLD, 58, BLACK, 0.07, 0.15, "tl"),
        ("精油怎麼收納最對?", FONT_ZH_BOLD, 52, BLACK, 0.07, 0.24, "tl"),
        ("避光・避熱・直立放置", FONT_ZH, 36, TERRA, 0.07, 0.33, "tl"),
        ("完整收納指南,點 bio →", FONT_ZH_BOLD, 40, TERRA, 0.07, 0.87, "tl"),
    ], f"{OUT_W4}/Stories/MORENE_W4inc_S11.png")
    print("S11 done")

    # S12 7/24 精油放哪投票 — 書桌散落+燈光感
    card(SW, SH, CREAM, "迷迭香", 0.62, 0.56, 0.78, [
        logo_line(BLACK, 0.07, 0.06),
        ("07.24", FONT_EN, 36, GRYBROWN, 0.07, 0.11, "tl"),
        ("你的精油都放哪?", FONT_ZH_BOLD, 54, BLACK, 0.07, 0.16, "tl"),
        ("A  書桌上,隨手就拿", FONT_ZH, 42, BLACK, 0.07, 0.50, "tl"),
        ("B  抽屜裡,整齊收好", FONT_ZH, 42, BLACK, 0.07, 0.59, "tl"),
        ("C  浴室架上", FONT_ZH, 42, GRYBROWN, 0.07, 0.68, "tl"),
        ("D  窗邊,喜歡有光感", FONT_ZH, 42, GRYBROWN, 0.07, 0.77, "tl"),
        ("其實 D 是錯誤答案 ↓", FONT_ZH_BOLD, 32, TERRA, 0.07, 0.88, "tl"),
    ], f"{OUT_W4}/Stories/MORENE_W4inc_S12.png")
    print("S12 done")

    # S13 7/25 香氣日記首句 — 暖米白+日記本感
    card(SW, SH, CREAM, "乳香", 0.64, 0.52, 0.78, [
        logo_line(BLACK, 0.07, 0.06),
        ("07.25", FONT_EN, 36, GRYBROWN, 0.07, 0.11, "tl"),
        ("Scent Diary", FONT_EN_BOLD, 80, BLACK, 0.07, 0.15, "tl"),
        ("香氣日記", FONT_ZH_BOLD, 64, BLACK, 0.07, 0.27, "tl"),
        ("今天,你用的是哪支精油?", FONT_ZH, 40, GRYBROWN, 0.07, 0.36, "tl"),
        ("寫下你的香氣記憶 ↓", FONT_ZH_BOLD, 38, TERRA, 0.07, 0.87, "tl"),
    ], f"{OUT_W4}/Stories/MORENE_W4inc_S13.png")
    print("S13 done")

    # S14 7/25 夏天值得入手問答 — 甜橙+焦糖鮮底
    card(SW, SH, CARAMEL, "甜橙", 0.70, 0.52, 0.84, [
        logo_line(CREAM, 0.07, 0.06),
        ("07.25", FONT_EN, 36, CREAM, 0.07, 0.11, "tl"),
        ("Summer Must-Have", FONT_EN_BOLD, 64, CREAM, 0.07, 0.15, "tl"),
        ("夏天最值得入手的精油", FONT_ZH_BOLD, 50, CREAM, 0.07, 0.25, "tl"),
        ("你選哪支?", FONT_ZH, 42, MUSTARD, 0.07, 0.33, "tl"),
        ("A  甜橙・早晨活力", FONT_ZH, 40, CREAM, 0.07, 0.50, "tl"),
        ("B  薄荷・清涼提神", FONT_ZH, 40, CREAM, 0.07, 0.59, "tl"),
        ("C  白葡萄柚・輕盈", FONT_ZH, 40, CREAM, 0.07, 0.68, "tl"),
        ("D  乳香・大暑沉靜", FONT_ZH, 40, MUSTARD, 0.07, 0.77, "tl"),
        ("留言告訴我們 ↓", FONT_ZH, 32, CREAM, 0.07, 0.89, "tl"),
    ], f"{OUT_W4}/Stories/MORENE_W4inc_S14.png",
    shadow_offset_x=45, shadow_opacity=0.22)
    print("S14 done")


# =====================
# IG ×7  (1080×1350)
# =====================
IW, IH = 1080, 1350

def make_ig():
    os.makedirs(f"{OUT_W4}/IG", exist_ok=True)

    # IG1 7/19 大暑前柑橘留住夏天 — 焦糖暖橘底+甜橙
    card(IW, IH, CARAMEL, "甜橙", 0.72, 0.57, 0.84, [
        logo_line(CREAM, 0.07, 0.055),
        ("07.19", FONT_EN, 32, CREAM, 0.07, 0.10, "tl"),
        ("Before Da Shu", FONT_EN_BOLD, 72, CREAM, 0.07, 0.14, "tl"),
        ("大暑前,留住夏天的陽光感", FONT_ZH_BOLD, 46, CREAM, 0.07, 0.24, "tl"),
        ("甜橙", FONT_ZH_BOLD, 56, MUSTARD, 0.07, 0.33, "tl"),
        ("Citrus sinensis · 巴西 · 冷壓萃取", FONT_ZH, 28, CREAM, 0.07, 0.41, "tl"),
        ("白葡萄柚", FONT_ZH_BOLD, 56, MUSTARD, 0.07, 0.49, "tl"),
        ("Citrus paradisi · 以色列 · 冷壓萃取", FONT_ZH, 28, CREAM, 0.07, 0.57, "tl"),
        ("MORENE · IFA 監製 · 學名產地透明", FONT_ZH, 26, FOGPINK, 0.07, 0.89, "tl"),
    ], f"{OUT_W4}/IG/MORENE_W4inc_IG1.png",
    shadow_offset_x=50, shadow_opacity=0.24)
    print("IG1 done")

    # IG2 7/20 廚房去味科普 — 奶油白+茶樹薄荷+暖白
    card(IW, IH, CREAM, "茶樹", 0.66, 0.57, 0.82, [
        logo_line(BLACK, 0.07, 0.055),
        ("07.20", FONT_EN, 32, TERRA, 0.07, 0.10, "tl"),
        ("Kitchen Fresh", FONT_EN_BOLD, 72, BLACK, 0.07, 0.14, "tl"),
        ("廚房去除異味", FONT_ZH_BOLD, 56, BLACK, 0.07, 0.24, "tl"),
        ("茶樹・薄荷・甜橙", FONT_ZH_BOLD, 40, TERRA, 0.07, 0.33, "tl"),
        ("擴香 30 分鐘,空間感受煥新", FONT_ZH, 34, GRYBROWN, 0.07, 0.41, "tl"),
        ("茶樹 Melaleuca alternifolia · 澳洲", FONT_ZH, 26, GRYBROWN, 0.07, 0.51, "tl"),
        ("薄荷 Mentha × piperita · 美國", FONT_ZH, 26, GRYBROWN, 0.07, 0.57, "tl"),
        ("IFA 監製 · 完整 INCI 公開 · morene.com.tw", FONT_ZH, 24, GRYBROWN, 0.07, 0.89, "tl"),
    ], f"{OUT_W4}/IG/MORENE_W4inc_IG2.png")
    print("IG2 done")

    # IG3 7/21 薄荷聚光 — 霧藍綠底+薄荷瓶大圖+強投影
    card(IW, IH, FOGSAGE, "薄荷", 0.78, 0.55, 0.86, [
        logo_line(BLACK, 0.07, 0.055),
        ("07.21", FONT_EN, 32, BLACK, 0.07, 0.10, "tl"),
        ("Peppermint", FONT_EN_BOLD, 96, BLACK, 0.07, 0.14, "tl"),
        ("薄荷", FONT_ZH_BOLD, 76, BLACK, 0.07, 0.26, "tl"),
        ("Mentha × piperita", FONT_EN, 32, DARKBROWN, 0.07, 0.36, "tl"),
        ("美國 · 蒸氣蒸餾", FONT_ZH, 30, DARKBROWN, 0.07, 0.43, "tl"),
        ("使用前以 2-3% 稀釋 · 避免幼兒使用", FONT_ZH_BOLD, 28, TERRA, 0.07, 0.52, "tl"),
        ("IFA 監製 · 學名產地透明 · INCI 公開", FONT_ZH, 24, DARKBROWN, 0.07, 0.89, "tl"),
    ], f"{OUT_W4}/IG/MORENE_W4inc_IG3.png",
    shadow_offset_x=70, shadow_blur=55, shadow_opacity=0.32)
    print("IG3 done")

    # IG4 7/22 書房草本配香 — 草本奶油底+甜羅勒迷迭香
    card(IW, IH, CREAM, "甜羅勒", 0.68, 0.56, 0.83, [
        logo_line(BLACK, 0.07, 0.055),
        ("07.22", FONT_EN, 32, FOGSAGE, 0.07, 0.10, "tl"),
        ("Study Blend", FONT_EN_BOLD, 76, BLACK, 0.07, 0.14, "tl"),
        ("書房配香,兩支草本", FONT_ZH_BOLD, 52, BLACK, 0.07, 0.24, "tl"),
        ("甜羅勒", FONT_ZH_BOLD, 44, FOGSAGE, 0.07, 0.33, "tl"),
        ("Ocimum basilicum · 草本清新 · 幫助專注感", FONT_ZH, 28, GRYBROWN, 0.07, 0.40, "tl"),
        ("桉油葉迷迭香", FONT_ZH_BOLD, 44, FOGSAGE, 0.07, 0.48, "tl"),
        ("Rosmarinus officinalis ct. camphor · 清醒感", FONT_ZH, 28, GRYBROWN, 0.07, 0.55, "tl"),
        ("擴香使用 · 無需稀釋", FONT_ZH, 30, TERRA, 0.07, 0.63, "tl"),
        ("IFA 監製 · 完整 INCI 公開", FONT_ZH, 24, GRYBROWN, 0.07, 0.89, "tl"),
    ], f"{OUT_W4}/IG/MORENE_W4inc_IG4.png")
    print("IG4 done")

    # IG5 7/23 大暑乳香單方 — 深陶土底+乳香瓶+樹脂道具感
    card(IW, IH, TERRA, "乳香", 0.74, 0.56, 0.86, [
        logo_line(CREAM, 0.07, 0.055),
        ("07.23  大暑", FONT_ZH_BOLD, 36, MUSTARD, 0.07, 0.10, "tl"),
        ("Frankincense", FONT_EN_BOLD, 72, CREAM, 0.07, 0.14, "tl"),
        ("乳香", FONT_ZH_BOLD, 76, CREAM, 0.07, 0.24, "tl"),
        ("Boswellia carterii", FONT_EN, 30, FOGPINK, 0.07, 0.34, "tl"),
        ("印度 · 蒸氣蒸餾", FONT_ZH, 30, FOGPINK, 0.07, 0.41, "tl"),
        ("大暑最適合的沉靜香氣", FONT_ZH, 36, WARMSAND, 0.07, 0.49, "tl"),
        ("IFA 監製 · 學名產地透明 · INCI 公開", FONT_ZH, 24, FOGPINK, 0.07, 0.89, "tl"),
    ], f"{OUT_W4}/IG/MORENE_W4inc_IG5.png",
    shadow_offset_x=55, shadow_blur=45, shadow_opacity=0.28)
    print("IG5 done")

    # IG6 7/24 精油收納科普 — 暖木底+多瓶俯拍感
    card(IW, IH, WARMSAND, "甜橙", 0.62, 0.57, 0.80, [
        logo_line(BLACK, 0.07, 0.055),
        ("07.24", FONT_EN, 32, TERRA, 0.07, 0.10, "tl"),
        ("Storage Guide", FONT_EN_BOLD, 74, BLACK, 0.07, 0.14, "tl"),
        ("精油收納的三個鐵則", FONT_ZH_BOLD, 54, BLACK, 0.07, 0.24, "tl"),
        ("1  避光・不放窗邊或燈光下", FONT_ZH, 34, TERRA, 0.07, 0.34, "tl"),
        ("2  避熱・遠離廚房熱源", FONT_ZH, 34, BLACK, 0.07, 0.42, "tl"),
        ("3  直立放置・蓋緊瓶蓋", FONT_ZH, 34, BLACK, 0.07, 0.50, "tl"),
        ("柑橘類 6 個月 · 樹脂類 2 年以上", FONT_ZH_BOLD, 30, TERRA, 0.07, 0.60, "tl"),
        ("IFA 監製 · 完整 INCI 公開 · morene.com.tw", FONT_ZH, 24, GRYBROWN, 0.07, 0.88, "tl"),
    ], f"{OUT_W4}/IG/MORENE_W4inc_IG6.png")
    print("IG6 done")

    # IG7 7/25 香氣日記 — 暖米白+日記本+乳香瓶
    card(IW, IH, CREAM, "乳香", 0.66, 0.54, 0.82, [
        logo_line(BLACK, 0.07, 0.055),
        ("07.25", FONT_EN, 32, GRYBROWN, 0.07, 0.10, "tl"),
        ("Scent Diary", FONT_EN_BOLD, 82, BLACK, 0.07, 0.14, "tl"),
        ("香氣日記", FONT_ZH_BOLD, 64, BLACK, 0.07, 0.25, "tl"),
        ("夏天,用一支精油記錄情緒", FONT_ZH, 38, GRYBROWN, 0.07, 0.35, "tl"),
        ("你的香氣日記,從今天開始", FONT_ZH, 34, GRYBROWN, 0.07, 0.43, "tl"),
        ("morene.com.tw · IFA 監製 · 學名產地透明", FONT_ZH, 24, GRYBROWN, 0.07, 0.88, "tl"),
    ], f"{OUT_W4}/IG/MORENE_W4inc_IG7.png")
    print("IG7 done")


# =====================
# FB ×7  (1080×1080)
# =====================
FW, FH = 1080, 1080

def make_fb():
    os.makedirs(f"{OUT_W4}/FB", exist_ok=True)

    _fb_specs = [
        # FB1 7/19 柑橘留住夏天
        ("甜橙", 0.65, 0.58, 0.82, CARAMEL, [
            logo_line(CREAM, 0.07, 0.07),
            ("07.19", FONT_EN, 30, CREAM, 0.07, 0.13, "tl"),
            ("大暑前的柑橘香", FONT_ZH_BOLD, 58, CREAM, 0.07, 0.18, "tl"),
            ("甜橙・白葡萄柚,留住夏天", FONT_ZH, 36, MUSTARD, 0.07, 0.28, "tl"),
            ("IFA 監製 · 學名產地透明", FONT_ZH, 24, FOGPINK, 0.07, 0.87, "tl"),
        ], "FB1"),
        # FB2 7/20 廚房去味
        ("茶樹", 0.60, 0.57, 0.80, CREAM, [
            logo_line(BLACK, 0.07, 0.07),
            ("07.20", FONT_EN, 30, TERRA, 0.07, 0.13, "tl"),
            ("廚房去味配方", FONT_ZH_BOLD, 56, BLACK, 0.07, 0.18, "tl"),
            ("茶樹・薄荷・甜橙", FONT_ZH, 36, TERRA, 0.07, 0.28, "tl"),
            ("擴香 30 分鐘,空間感受煥新", FONT_ZH, 30, GRYBROWN, 0.07, 0.36, "tl"),
            ("IFA 監製 · INCI 公開", FONT_ZH, 24, GRYBROWN, 0.07, 0.87, "tl"),
        ], "FB2"),
        # FB3 7/21 薄荷聚光
        ("薄荷", 0.65, 0.56, 0.82, FOGSAGE, [
            logo_line(BLACK, 0.07, 0.07),
            ("07.21", FONT_EN, 30, BLACK, 0.07, 0.13, "tl"),
            ("Peppermint / 薄荷", FONT_ZH_BOLD, 54, BLACK, 0.07, 0.18, "tl"),
            ("Mentha × piperita · 美國", FONT_ZH, 30, DARKBROWN, 0.07, 0.28, "tl"),
            ("稀釋 2-3% · 避免幼兒使用", FONT_ZH_BOLD, 28, TERRA, 0.07, 0.36, "tl"),
            ("IFA 監製 · 學名產地透明", FONT_ZH, 24, DARKBROWN, 0.07, 0.87, "tl"),
        ], "FB3"),
        # FB4 7/22 書房配香
        ("甜羅勒", 0.62, 0.56, 0.80, CREAM, [
            logo_line(BLACK, 0.07, 0.07),
            ("07.22", FONT_EN, 30, FOGSAGE, 0.07, 0.13, "tl"),
            ("書房配香兩支草本", FONT_ZH_BOLD, 54, BLACK, 0.07, 0.18, "tl"),
            ("甜羅勒 + 迷迭香", FONT_ZH_BOLD, 40, FOGSAGE, 0.07, 0.28, "tl"),
            ("擴香使用,感受專注草本氛圍", FONT_ZH, 30, GRYBROWN, 0.07, 0.36, "tl"),
            ("IFA 監製 · INCI 公開", FONT_ZH, 24, GRYBROWN, 0.07, 0.87, "tl"),
        ], "FB4"),
        # FB5 7/23 大暑乳香
        ("乳香", 0.64, 0.56, 0.82, TERRA, [
            logo_line(CREAM, 0.07, 0.07),
            ("07.23  大暑", FONT_ZH_BOLD, 32, MUSTARD, 0.07, 0.13, "tl"),
            ("大暑・乳香", FONT_ZH_BOLD, 62, CREAM, 0.07, 0.18, "tl"),
            ("印度 · Boswellia carterii", FONT_ZH, 28, FOGPINK, 0.07, 0.28, "tl"),
            ("一年最熱的節氣,最沉靜的香氣", FONT_ZH, 30, WARMSAND, 0.07, 0.36, "tl"),
            ("IFA 監製 · 學名產地透明", FONT_ZH, 24, FOGPINK, 0.07, 0.87, "tl"),
        ], "FB5"),
        # FB6 7/24 精油收納
        ("甜橙", 0.58, 0.56, 0.78, WARMSAND, [
            logo_line(BLACK, 0.07, 0.07),
            ("07.24", FONT_EN, 30, TERRA, 0.07, 0.13, "tl"),
            ("精油收納三個鐵則", FONT_ZH_BOLD, 52, BLACK, 0.07, 0.18, "tl"),
            ("避光・避熱・直立放置", FONT_ZH, 36, TERRA, 0.07, 0.28, "tl"),
            ("柑橘 6 個月・樹脂 2 年以上", FONT_ZH_BOLD, 30, TERRA, 0.07, 0.36, "tl"),
            ("morene.com.tw", FONT_EN, 26, GRYBROWN, 0.07, 0.87, "tl"),
        ], "FB6"),
        # FB7 7/25 香氣日記
        ("乳香", 0.60, 0.54, 0.78, CREAM, [
            logo_line(BLACK, 0.07, 0.07),
            ("07.25", FONT_EN, 30, GRYBROWN, 0.07, 0.13, "tl"),
            ("香氣日記", FONT_ZH_BOLD, 60, BLACK, 0.07, 0.18, "tl"),
            ("夏天,用一支精油記錄情緒", FONT_ZH, 34, GRYBROWN, 0.07, 0.28, "tl"),
            ("你的香氣日記,從今天開始", FONT_ZH_BOLD, 30, TERRA, 0.07, 0.36, "tl"),
            ("morene.com.tw", FONT_EN, 26, GRYBROWN, 0.07, 0.87, "tl"),
        ], "FB7"),
    ]

    for (bottle, scale, xf, yf, bg, lines, suffix) in _fb_specs:
        card(FW, FH, bg, bottle, scale, xf, yf, lines,
             f"{OUT_W4}/FB/MORENE_W4inc_{suffix}.png")
        print(f"{suffix} done")


# =====================
# REELS 分鏡 ×3×6  (1080×1920)
# =====================
def make_reels():
    os.makedirs(f"{OUT_W4}/Reels", exist_ok=True)

    # R1: 7/19 大暑身體儀式 (6 幀)
    r1_frames = [
        # f1 封面
        (CARAMEL, "甜橙", 0.72, 0.55, 0.84, [
            logo_line(CREAM, 0.07, 0.06),
            ("大暑身體儀式", FONT_ZH_BOLD, 56, CREAM, 0.07, 0.14, "tl"),
            ("Summer Body Ritual", FONT_EN_BOLD, 52, MUSTARD, 0.07, 0.23, "tl"),
            ("三支精油,三個節點", FONT_ZH, 38, CREAM, 0.07, 0.31, "tl"),
        ]),
        # f2 甜橙早晨
        (CREAM, "甜橙", 0.66, 0.52, 0.80, [
            logo_line(BLACK, 0.07, 0.06),
            ("Morning", FONT_EN_BOLD, 80, BLACK, 0.07, 0.14, "tl"),
            ("甜橙・早晨活力", FONT_ZH_BOLD, 54, BLACK, 0.07, 0.25, "tl"),
            ("稀釋後塗手腕,感受陽光感", FONT_ZH, 36, GRYBROWN, 0.07, 0.34, "tl"),
            ("使用前請稀釋 2-3% 基底油", FONT_ZH, 26, TERRA, 0.07, 0.88, "tl"),
        ]),
        # f3 薄荷沐浴後
        (FOGSAGE, "薄荷", 0.68, 0.54, 0.82, [
            logo_line(BLACK, 0.07, 0.06),
            ("After Shower", FONT_EN_BOLD, 72, BLACK, 0.07, 0.14, "tl"),
            ("薄荷・沐浴後清涼感", FONT_ZH_BOLD, 52, BLACK, 0.07, 0.25, "tl"),
            ("頸側・後頸,夏日必備香氣儀式", FONT_ZH, 34, DARKBROWN, 0.07, 0.34, "tl"),
            ("使用前請稀釋 2-3% 基底油", FONT_ZH, 26, TERRA, 0.07, 0.88, "tl"),
        ]),
        # f4 乳香入夜
        (DARKBROWN, "乳香", 0.68, 0.56, 0.83, [
            logo_line(CREAM, 0.07, 0.06),
            ("Night", FONT_EN_BOLD, 96, CREAM, 0.07, 0.14, "tl"),
            ("乳香・入夜沉靜", FONT_ZH_BOLD, 54, CREAM, 0.07, 0.26, "tl"),
            ("擴香或稀釋塗胸口,大暑夜的儀式", FONT_ZH, 34, WARMSAND, 0.07, 0.35, "tl"),
        ]),
        # f5 三瓶集合
        (CREAM, "甜橙", 0.60, 0.52, 0.78, [
            logo_line(BLACK, 0.07, 0.06),
            ("甜橙・薄荷・乳香", FONT_ZH_BOLD, 50, BLACK, 0.07, 0.14, "tl"),
            ("大暑三段式身體儀式", FONT_ZH, 38, GRYBROWN, 0.07, 0.23, "tl"),
            ("早晨 / 午後 / 入夜", FONT_ZH_BOLD, 42, TERRA, 0.07, 0.31, "tl"),
            ("MORENE · 學名產地透明 · IFA 監製", FONT_ZH, 28, GRYBROWN, 0.07, 0.88, "tl"),
        ]),
        # f6 CTA 測驗
        (TERRA, "乳香", 0.62, 0.55, 0.80, [
            logo_line(CREAM, 0.07, 0.06),
            ("你是哪種香氣人格?", FONT_ZH_BOLD, 54, CREAM, 0.07, 0.14, "tl"),
            ("morene.com.tw/pages/scent-personality", FONT_EN, 22, FOGPINK, 0.07, 0.24, "tl"),
            ("點 bio 連結立即測驗 →", FONT_ZH_BOLD, 44, MUSTARD, 0.07, 0.31, "tl"),
        ]),
    ]
    for fi, (bg, bottle, scale, xf, yf, lines) in enumerate(r1_frames, 1):
        _assert_no_tofu(lines)
        card(SW, SH, bg, bottle, scale, xf, yf, lines,
             f"{OUT_W4}/Reels/MORENE_W4inc_R1_f{fi}.png")
        print(f"R1_f{fi} done")

    # R2: 7/22 書房配香 (6 幀)
    r2_frames = [
        # f1 封面
        (CREAM, "甜羅勒", 0.72, 0.54, 0.84, [
            logo_line(BLACK, 0.07, 0.06),
            ("Study Room", FONT_EN_BOLD, 82, BLACK, 0.07, 0.14, "tl"),
            ("書房配香指南", FONT_ZH_BOLD, 56, BLACK, 0.07, 0.27, "tl"),
            ("兩支草本,一個專注空間", FONT_ZH, 38, FOGSAGE, 0.07, 0.36, "tl"),
        ]),
        # f2 甜羅勒介紹
        (CREAM, "甜羅勒", 0.66, 0.54, 0.80, [
            logo_line(BLACK, 0.07, 0.06),
            ("Sweet Basil", FONT_EN_BOLD, 76, BLACK, 0.07, 0.14, "tl"),
            ("甜羅勒", FONT_ZH_BOLD, 62, FOGSAGE, 0.07, 0.25, "tl"),
            ("Ocimum basilicum · 草本清新", FONT_ZH, 30, GRYBROWN, 0.07, 0.34, "tl"),
            ("學名透明 · 產地標示 · IFA 監製", FONT_ZH, 28, GRYBROWN, 0.07, 0.42, "tl"),
        ]),
        # f3 薄荷+迷迭香
        (FOGSAGE, "迷迭香", 0.68, 0.54, 0.82, [
            logo_line(BLACK, 0.07, 0.06),
            ("Rosemary", FONT_EN_BOLD, 80, BLACK, 0.07, 0.14, "tl"),
            ("桉油葉迷迭香", FONT_ZH_BOLD, 54, BLACK, 0.07, 0.25, "tl"),
            ("Rosmarinus officinalis ct. camphor", FONT_EN, 26, DARKBROWN, 0.07, 0.34, "tl"),
            ("清醒感・閱讀時的好搭檔", FONT_ZH, 36, DARKBROWN, 0.07, 0.41, "tl"),
        ]),
        # f4 擴香畫面
        (CREAM, "甜羅勒", 0.60, 0.52, 0.78, [
            logo_line(BLACK, 0.07, 0.06),
            ("Diffuse", FONT_EN_BOLD, 88, BLACK, 0.07, 0.14, "tl"),
            ("擴香使用方式", FONT_ZH_BOLD, 54, BLACK, 0.07, 0.26, "tl"),
            ("水 100ml + 精油 4-6 滴", FONT_ZH, 38, TERRA, 0.07, 0.35, "tl"),
            ("擴香 30-60 分鐘後通風換氣", FONT_ZH, 34, GRYBROWN, 0.07, 0.43, "tl"),
        ]),
        # f5 讀書情境
        (DARKBROWN, "迷迭香", 0.64, 0.55, 0.80, [
            logo_line(CREAM, 0.07, 0.06),
            ("Deep Focus", FONT_EN_BOLD, 76, CREAM, 0.07, 0.14, "tl"),
            ("一本書・一杯茶・一支草本精油", FONT_ZH_BOLD, 46, CREAM, 0.07, 0.25, "tl"),
            ("這是你的書房儀式", FONT_ZH, 40, WARMSAND, 0.07, 0.34, "tl"),
        ]),
        # f6 CTA
        (CREAM, "甜羅勒", 0.62, 0.54, 0.80, [
            logo_line(BLACK, 0.07, 0.06),
            ("morene.com.tw", FONT_EN_BOLD, 52, BLACK, 0.07, 0.14, "tl"),
            ("完整了解草本精油", FONT_ZH_BOLD, 54, TERRA, 0.07, 0.24, "tl"),
            ("點選 bio 連結 →", FONT_ZH, 40, BLACK, 0.07, 0.33, "tl"),
        ]),
    ]
    for fi, (bg, bottle, scale, xf, yf, lines) in enumerate(r2_frames, 1):
        _assert_no_tofu(lines)
        card(SW, SH, bg, bottle, scale, xf, yf, lines,
             f"{OUT_W4}/Reels/MORENE_W4inc_R2_f{fi}.png")
        print(f"R2_f{fi} done")

    # R3: 7/24 精油保存指南 (6 幀)
    r3_frames = [
        # f1 封面
        (WARMSAND, "甜橙", 0.70, 0.54, 0.84, [
            logo_line(BLACK, 0.07, 0.06),
            ("Storage Guide", FONT_EN_BOLD, 68, BLACK, 0.07, 0.14, "tl"),
            ("精油保存三個鐵則", FONT_ZH_BOLD, 54, BLACK, 0.07, 0.25, "tl"),
            ("你存對了嗎?", FONT_ZH, 44, TERRA, 0.07, 0.34, "tl"),
        ]),
        # f2 窗邊打叉(錯誤示範)
        (CREAM, "甜橙", 0.60, 0.52, 0.76, [
            logo_line(BLACK, 0.07, 0.06),
            ("✗ 窗邊", FONT_ZH_BOLD, 72, TERRA, 0.07, 0.14, "tl"),
            ("陽光和紫外線會加速氧化", FONT_ZH, 38, GRYBROWN, 0.07, 0.25, "tl"),
            ("柑橘類精油尤其敏感", FONT_ZH, 34, GRYBROWN, 0.07, 0.32, "tl"),
            ("效期縮短・香氣變質", FONT_ZH_BOLD, 36, TERRA, 0.07, 0.40, "tl"),
        ]),
        # f3 陰涼抽屜(正確)
        (DARKBROWN, "乳香", 0.66, 0.55, 0.82, [
            logo_line(CREAM, 0.07, 0.06),
            ("✓ 陰涼抽屜", FONT_ZH_BOLD, 64, MUSTARD, 0.07, 0.14, "tl"),
            ("避光・恆溫・直立放置", FONT_ZH_BOLD, 46, CREAM, 0.07, 0.25, "tl"),
            ("最理想的保存環境", FONT_ZH, 36, WARMSAND, 0.07, 0.34, "tl"),
            ("室溫 15-25°C 最佳", FONT_ZH, 34, WARMSAND, 0.07, 0.41, "tl"),
        ]),
        # f4 柑橘半年保存
        (CARAMEL, "甜橙", 0.65, 0.54, 0.82, [
            logo_line(CREAM, 0.07, 0.06),
            ("柑橘類", FONT_ZH_BOLD, 66, CREAM, 0.07, 0.14, "tl"),
            ("開封後 6 個月內使用", FONT_ZH_BOLD, 50, MUSTARD, 0.07, 0.24, "tl"),
            ("甜橙・白葡萄柚・薄荷", FONT_ZH, 34, CREAM, 0.07, 0.33, "tl"),
            ("前調揮發快,請儘早享用", FONT_ZH, 32, CREAM, 0.07, 0.41, "tl"),
        ]),
        # f5 樹脂類耐放
        (TERRA, "乳香", 0.68, 0.56, 0.83, [
            logo_line(CREAM, 0.07, 0.06),
            ("樹脂類", FONT_ZH_BOLD, 66, CREAM, 0.07, 0.14, "tl"),
            ("開封後 2 年以上", FONT_ZH_BOLD, 50, MUSTARD, 0.07, 0.24, "tl"),
            ("乳香・大西洋雪松・廣藿香", FONT_ZH, 34, FOGPINK, 0.07, 0.33, "tl"),
            ("適當保存香氣更有深度", FONT_ZH, 32, WARMSAND, 0.07, 0.41, "tl"),
        ]),
        # f6 CTA
        (CREAM, "甜橙", 0.62, 0.52, 0.78, [
            logo_line(BLACK, 0.07, 0.06),
            ("morene.com.tw", FONT_EN_BOLD, 52, BLACK, 0.07, 0.14, "tl"),
            ("完整收納指南", FONT_ZH_BOLD, 60, TERRA, 0.07, 0.24, "tl"),
            ("點選 bio 連結 →", FONT_ZH, 40, BLACK, 0.07, 0.33, "tl"),
        ]),
    ]
    for fi, (bg, bottle, scale, xf, yf, lines) in enumerate(r3_frames, 1):
        _assert_no_tofu(lines)
        card(SW, SH, bg, bottle, scale, xf, yf, lines,
             f"{OUT_W4}/Reels/MORENE_W4inc_R3_f{fi}.png")
        print(f"R3_f{fi} done")


# =====================
# MAIN
# =====================
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--batch", choices=["stories", "ig_fb", "reels", "all"], default="all")
    args = p.parse_args()

    if args.batch in ("stories", "all"):
        print("=== BATCH 1: Stories ===")
        make_stories()
        print("Stories batch done.\n")

    if args.batch in ("ig_fb", "all"):
        print("=== BATCH 2: IG + FB ===")
        make_ig()
        make_fb()
        print("IG+FB batch done.\n")

    if args.batch in ("reels", "all"):
        print("=== BATCH 3: Reels ===")
        make_reels()
        print("Reels batch done.\n")
