#!/usr/bin/env python3
"""
MORENE W3 增量圖卡生成腳本 (Wave 3, 7/12–7/18, 31 則)
規格: Stories/Reels 1080×1920; IG 1080×1350; FB 1080×1080
樣式: Y2K 攝影主導 + 單色飽和底 + 真實琥珀瓶 + 極少字
字體: BW Gradual/英 + Noto Sans TC/中 + Outfit/小字
無 ISO/認證標章 | 光敏說明=使用注意不含療效詞

CJK tofu 防呆: 所有含漢字之 text 必須用 FONT_ZH/FONT_ZH_BOLD
"""

import os, sys
sys.path.insert(0, "/Users/morrislin/mw-social-assets/MORENE")
from make_covers_v2 import (
    compose_card,
    FONT_EN_BOLD, FONT_EN, FONT_ZH, FONT_ZH_BOLD,
    CREAM, BLACK, TERRA, MUSTARD, SAGE, ORANGE, WHITE,
    OUT_BASE, hex2rgb, fnt, get_logo, add_contact_shadow, add_directional_shadow,
    crop_to_bottle,
)
from PIL import Image, ImageDraw

# =====================
# 色彩補充
# =====================
FOGPINK   = "#E9C5B9"
WARMSAND  = "#CBA98A"
CARAMEL   = "#C9853E"
FOGBLUE   = "#82A8CC"
NAVY      = "#1C2C4A"
GRASSGRN  = "#4A7C59"
AMBER_YLW = "#E8CE8C"
DARK_GY   = "#2A2520"

# =====================
# 路徑常數
# =====================
BASE_PROD = "/Users/morrislin/Desktop/MORENE/03_MORENE/03_Assets/A009：MORENE-產品相關/01.產品相關/01. 產品資料/05. 產品照片/素材/商品大圖/01_精油"
OUT_W3    = "/Users/morrislin/mw-social-assets/MORENE/W_increment"

# =====================
# 瓶身路徑
# =====================
BOTTLES = {
    "乳香":       f"{BASE_PROD}/5MOEO009_乳香/MORENE_精油瓶_去背_乳香.png",
    "甜橙":       f"{BASE_PROD}/甜橙/MORENE_精油瓶_去背_甜橙.png",
    "佛手柑":     f"{BASE_PROD}/5MOEO003_佛手柑/MORENE_精油瓶_去背_佛手柑.png",
    "真正薰衣草": f"{BASE_PROD}/5MOEO015_真正薰衣草/MORENE_精油瓶_去背_真正薰衣草.png",
    "大西洋雪松": f"{BASE_PROD}/5MOEO005_大西洋雪松/MORENE_精油瓶_去背_大西洋雪松.png",
    "岩蘭草":     f"{BASE_PROD}/岩蘭草/MORENE_精油瓶_去背_岩蘭草.png",
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
    for (text, fpath, *_) in text_lines:
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
    """Return a MORENE logo text_line tuple (compose_card handles 'MORENE' as logo)"""
    return ("MORENE", FONT_EN_BOLD, 1, color_hex, xf, yf, "tl")

# =====================
# STORIES ×14  (1080×1920)
# =====================
SW, SH = 1080, 1920

def make_stories():
    os.makedirs(f"{OUT_W3}/Stories", exist_ok=True)

    # S1 7/12 晨光自拍 — 奶油白底+晨光橘暈
    card(SW, SH, CREAM, "甜橙", 0.72, 0.52, 0.82, [
        logo_line(BLACK, 0.07, 0.06),
        ("07.12", FONT_EN, 36, "#C9853E", 0.07, 0.11, "tl"),
        ("Morning Ritual", FONT_EN_BOLD, 78, BLACK, 0.07, 0.14, "tl"),
        ("晨光裡,一滴甜橙", FONT_ZH_BOLD, 52, BLACK, 0.07, 0.23, "tl"),
        ("讓今天從香氣開始", FONT_ZH, 40, "#8C8079", 0.07, 0.31, "tl"),
        ("swipe up →", FONT_EN, 28, "#8C8079", 0.07, 0.90, "tl"),
    ], f"{OUT_W3}/Stories/MORENE_W3inc_S1.png",
    shadow_offset_x=45, shadow_opacity=0.22)
    print("S1 done")

    # S2 7/12 老子投票 — 深藍底+引言
    card(SW, SH, NAVY, "乳香", 0.68, 0.60, 0.85, [
        logo_line(CREAM, 0.07, 0.06),
        ("07.12", FONT_EN, 36, FOGBLUE, 0.07, 0.11, "tl"),
        ('“知人者智,', FONT_ZH_BOLD, 64, CREAM, 0.07, 0.16, "tl"),
        ('自知者明。”', FONT_ZH_BOLD, 64, CREAM, 0.07, 0.24, "tl"),
        ('—— 老子《道德經》', FONT_ZH, 34, "#82A8CC", 0.07, 0.33, "tl"),
        ('選香,也是認識自己的一刻', FONT_ZH, 38, "#CBA98A", 0.07, 0.40, "tl"),
        ('你平時選精油看重什麼?', FONT_ZH_BOLD, 42, CREAM, 0.07, 0.88, "tl"),
        ('留言告訴我們 ↓', FONT_ZH, 32, FOGBLUE, 0.07, 0.93, "tl"),
    ], f"{OUT_W3}/Stories/MORENE_W3inc_S2.png",
    shadow_offset_x=35, shadow_opacity=0.18)
    print("S2 done")

    # S3 7/13 塗抹位置預告 — 奶油白+說明文字
    card(SW, SH, CREAM, "甜橙", 0.65, 0.55, 0.75, [
        logo_line(BLACK, 0.07, 0.06),
        ("07.13", FONT_EN, 36, TERRA, 0.07, 0.11, "tl"),
        ("Where to apply?", FONT_EN_BOLD, 72, BLACK, 0.07, 0.15, "tl"),
        ("精油要塗哪裡?", FONT_ZH_BOLD, 58, BLACK, 0.07, 0.24, "tl"),
        ("手腕・頸側・腳底・胸口", FONT_ZH, 38, TERRA, 0.07, 0.33, "tl"),
        ("各有不同吸收速度和效果", FONT_ZH, 34, "#8C8079", 0.07, 0.40, "tl"),
        ("明天帶你完整看一遍 →", FONT_ZH_BOLD, 38, TERRA, 0.07, 0.88, "tl"),
    ], f"{OUT_W3}/Stories/MORENE_W3inc_S3.png")
    print("S3 done")

    # S4 7/13 稀釋投票 — 草綠底
    card(SW, SH, GRASSGRN, "甜橙", 0.64, 0.58, 0.82, [
        logo_line(CREAM, 0.07, 0.06),
        ("07.13", FONT_EN, 36, AMBER_YLW, 0.07, 0.11, "tl"),
        ("Dilute or not?", FONT_EN_BOLD, 68, CREAM, 0.07, 0.15, "tl"),
        ("你平時塗精油前", FONT_ZH_BOLD, 52, CREAM, 0.07, 0.24, "tl"),
        ("有先稀釋嗎?", FONT_ZH_BOLD, 52, AMBER_YLW, 0.07, 0.31, "tl"),
        ("A  有,用基底油調和", FONT_ZH, 40, CREAM, 0.07, 0.55, "tl"),
        ("B  沒有,直接塗", FONT_ZH, 40, CREAM, 0.07, 0.63, "tl"),
        ("C  看心情", FONT_ZH, 40, CREAM, 0.07, 0.71, "tl"),
        ("留言選你的答案 ↓", FONT_ZH, 34, AMBER_YLW, 0.07, 0.90, "tl"),
    ], f"{OUT_W3}/Stories/MORENE_W3inc_S4.png",
    shadow_opacity=0.20)
    print("S4 done")

    # S5 7/14 晨光剪影 — 晨光金底+瓶剪影
    card(SW, SH, CARAMEL, "甜橙", 0.75, 0.50, 0.88, [
        logo_line(CREAM, 0.07, 0.06),
        ("07.14", FONT_EN, 36, CREAM, 0.07, 0.11, "tl"),
        ("Dawn", FONT_EN_BOLD, 120, CREAM, 0.07, 0.14, "tl"),
        ("清晨的香氣儀式", FONT_ZH_BOLD, 54, CREAM, 0.07, 0.30, "tl"),
        ("在一天的起點,為自己留一分鐘", FONT_ZH, 36, "#EDE7DC", 0.07, 0.38, "tl"),
        ("你的早晨從哪個香調開始?", FONT_ZH_BOLD, 38, AMBER_YLW, 0.07, 0.87, "tl"),
    ], f"{OUT_W3}/Stories/MORENE_W3inc_S5.png",
    shadow_offset_x=50, shadow_opacity=0.25)
    print("S5 done")

    # S6 7/14 早晨儀式三格投票 — 奶油白
    card(SW, SH, CREAM, "佛手柑", 0.60, 0.55, 0.80, [
        logo_line(BLACK, 0.07, 0.06),
        ("07.14", FONT_EN, 36, TERRA, 0.07, 0.11, "tl"),
        ("Morning Mood Poll", FONT_EN_BOLD, 60, BLACK, 0.07, 0.15, "tl"),
        ("你的早晨是哪種狀態?", FONT_ZH_BOLD, 50, BLACK, 0.07, 0.23, "tl"),
        ("A  活力滿滿,出發!", FONT_ZH, 40, TERRA, 0.07, 0.52, "tl"),
        ("B  慢慢醒,需要儀式感", FONT_ZH, 40, "#8C8079", 0.07, 0.60, "tl"),
        ("C  半夢半醒,靠咖啡撐", FONT_ZH, 40, "#8C8079", 0.07, 0.68, "tl"),
        ("留言選你的 →", FONT_ZH, 34, TERRA, 0.07, 0.90, "tl"),
    ], f"{OUT_W3}/Stories/MORENE_W3inc_S6.png")
    print("S6 done")

    # S7 7/15 佛手柑果實預告 — 奶油白
    card(SW, SH, CREAM, "佛手柑", 0.70, 0.55, 0.82, [
        logo_line(BLACK, 0.07, 0.06),
        ("07.15", FONT_EN, 36, CARAMEL, 0.07, 0.11, "tl"),
        ("Bergamot", FONT_EN_BOLD, 96, BLACK, 0.07, 0.15, "tl"),
        ("佛手柑", FONT_ZH_BOLD, 68, BLACK, 0.07, 0.27, "tl"),
        ("義大利海岸的陽光果實", FONT_ZH, 38, "#8C8079", 0.07, 0.37, "tl"),
        ("Citrus bergamia · 義大利卡拉布里亞", FONT_ZH, 30, CARAMEL, 0.07, 0.44, "tl"),
        ("明天完整介紹這支精油 ✦", FONT_ZH_BOLD, 40, CARAMEL, 0.07, 0.87, "tl"),
    ], f"{OUT_W3}/Stories/MORENE_W3inc_S7.png")
    print("S7 done")

    # S8 7/15 佛手柑投票 — 黃底(芥末)
    card(SW, SH, AMBER_YLW, "佛手柑", 0.66, 0.55, 0.82, [
        logo_line(BLACK, 0.07, 0.06),
        ("07.15", FONT_EN, 36, TERRA, 0.07, 0.11, "tl"),
        ("你對佛手柑的印象?", FONT_ZH_BOLD, 54, BLACK, 0.07, 0.16, "tl"),
        ("A  陽光柑橘,清新", FONT_ZH, 44, BLACK, 0.07, 0.50, "tl"),
        ("B  伯爵茶的那個香", FONT_ZH, 44, BLACK, 0.07, 0.59, "tl"),
        ("C  沒特別印象", FONT_ZH, 44, BLACK, 0.07, 0.68, "tl"),
        ("D  沒聞過", FONT_ZH, 44, BLACK, 0.07, 0.77, "tl"),
        ("留言告訴我們 ↓", FONT_ZH, 34, TERRA, 0.07, 0.91, "tl"),
    ], f"{OUT_W3}/Stories/MORENE_W3inc_S8.png",
    shadow_opacity=0.18)
    print("S8 done")

    # S9 7/16 甜橙 vs 乳香投票 — 橘棕分割(用橘底帶乳香暗色)
    card(SW, SH, ORANGE, "乳香", 0.65, 0.60, 0.82, [
        logo_line(CREAM, 0.07, 0.06),
        ("07.16", FONT_EN, 36, CREAM, 0.07, 0.11, "tl"),
        ("甜橙 vs 乳香", FONT_ZH_BOLD, 62, CREAM, 0.07, 0.16, "tl"),
        ("你更常用哪支?", FONT_ZH, 42, CREAM, 0.07, 0.25, "tl"),
        ("甜橙", FONT_ZH_BOLD, 56, AMBER_YLW, 0.07, 0.55, "tl"),
        ("活力・柑橘・早晨", FONT_ZH, 34, CREAM, 0.07, 0.63, "tl"),
        ("乳香", FONT_ZH_BOLD, 56, WARMSAND, 0.55, 0.55, "tl"),
        ("沉靜・木質・睡前", FONT_ZH, 34, CREAM, 0.55, 0.63, "tl"),
        ("留言選你的 →", FONT_ZH, 34, CREAM, 0.07, 0.90, "tl"),
    ], f"{OUT_W3}/Stories/MORENE_W3inc_S9.png",
    shadow_opacity=0.20)
    print("S9 done")

    # S10 7/16 向內向外型 — 深藍底+問號
    card(SW, SH, NAVY, "乳香", 0.66, 0.58, 0.84, [
        logo_line(CREAM, 0.07, 0.06),
        ("07.16", FONT_EN, 36, FOGBLUE, 0.07, 0.11, "tl"),
        ("Inward or Outward?", FONT_EN_BOLD, 60, CREAM, 0.07, 0.15, "tl"),
        ("你是向內型,還是向外型?", FONT_ZH_BOLD, 50, CREAM, 0.07, 0.24, "tl"),
        ("精油香氣往往最誠實", FONT_ZH, 38, FOGBLUE, 0.07, 0.33, "tl"),
        ("向內型 — 木質・樹脂・大地", FONT_ZH, 36, WARMSAND, 0.07, 0.55, "tl"),
        ("向外型 — 柑橘・青草・花香", FONT_ZH, 36, AMBER_YLW, 0.07, 0.63, "tl"),
        ("你呢?留言告訴我們 ↓", FONT_ZH_BOLD, 40, CREAM, 0.07, 0.88, "tl"),
    ], f"{OUT_W3}/Stories/MORENE_W3inc_S10.png",
    shadow_opacity=0.18)
    print("S10 done")

    # S11 7/17 運動毛巾預告 — 暗色底
    card(SW, SH, DARK_GY, "大西洋雪松", 0.68, 0.56, 0.83, [
        logo_line(CREAM, 0.07, 0.06),
        ("07.17", FONT_EN, 36, SAGE, 0.07, 0.11, "tl"),
        ("Post-Workout", FONT_EN_BOLD, 80, CREAM, 0.07, 0.15, "tl"),
        ("運動後的香氣切換", FONT_ZH_BOLD, 54, CREAM, 0.07, 0.27, "tl"),
        ("流汗之後,一支精油", FONT_ZH, 38, "#8C8079", 0.07, 0.36, "tl"),
        ("幫你從運動模式切換回來", FONT_ZH, 38, "#8C8079", 0.07, 0.43, "tl"),
        ("明天完整分享 →", FONT_ZH_BOLD, 38, SAGE, 0.07, 0.87, "tl"),
    ], f"{OUT_W3}/Stories/MORENE_W3inc_S11.png",
    shadow_offset_x=40, shadow_opacity=0.22)
    print("S11 done")

    # S12 7/17 運動投票 — 健身深色底
    card(SW, SH, DARK_GY, "大西洋雪松", 0.62, 0.60, 0.80, [
        logo_line(CREAM, 0.07, 0.06),
        ("07.17", FONT_EN, 36, SAGE, 0.07, 0.11, "tl"),
        ("你運動後都怎麼放鬆?", FONT_ZH_BOLD, 52, CREAM, 0.07, 0.16, "tl"),
        ("A  洗澡/泡澡", FONT_ZH, 42, CREAM, 0.07, 0.50, "tl"),
        ("B  靜坐/冥想", FONT_ZH, 42, CREAM, 0.07, 0.59, "tl"),
        ("C  攤著滑手機", FONT_ZH, 42, CREAM, 0.07, 0.68, "tl"),
        ("D  用精油/擴香", FONT_ZH, 42, SAGE, 0.07, 0.77, "tl"),
        ("留言告訴我們 ↓", FONT_ZH, 34, "#8C8079", 0.07, 0.90, "tl"),
    ], f"{OUT_W3}/Stories/MORENE_W3inc_S12.png",
    shadow_opacity=0.20)
    print("S12 done")

    # S13 7/18 農場製程 — 奶油白底
    card(SW, SH, CREAM, "真正薰衣草", 0.68, 0.52, 0.82, [
        logo_line(BLACK, 0.07, 0.06),
        ("07.18", FONT_EN, 36, FOGBLUE, 0.07, 0.11, "tl"),
        ("From Field to Bottle", FONT_EN_BOLD, 60, BLACK, 0.07, 0.15, "tl"),
        ("農場到瓶身的旅程", FONT_ZH_BOLD, 52, BLACK, 0.07, 0.24, "tl"),
        ("薰衣草·普羅旺斯·蒸氣蒸餾", FONT_ZH, 36, "#8C8079", 0.07, 0.33, "tl"),
        ("Lavandula angustifolia", FONT_EN, 30, FOGBLUE, 0.07, 0.40, "tl"),
        ("每一支精油背後都有一個農場", FONT_ZH, 36, "#8C8079", 0.07, 0.47, "tl"),
        ("IFA 國際芳療師監製", FONT_ZH_BOLD, 38, FOGBLUE, 0.07, 0.88, "tl"),
    ], f"{OUT_W3}/Stories/MORENE_W3inc_S13.png")
    print("S13 done")

    # S14 7/18 買精油在意三選一 — 奶油白
    card(SW, SH, CREAM, "真正薰衣草", 0.60, 0.55, 0.80, [
        logo_line(BLACK, 0.07, 0.06),
        ("07.18", FONT_EN, 36, TERRA, 0.07, 0.11, "tl"),
        ("你買精油最在意什麼?", FONT_ZH_BOLD, 52, BLACK, 0.07, 0.16, "tl"),
        ("A  學名產地透明", FONT_ZH, 44, TERRA, 0.07, 0.48, "tl"),
        ("B  香氣本身合不合", FONT_ZH, 44, BLACK, 0.07, 0.57, "tl"),
        ("C  價格", FONT_ZH, 44, BLACK, 0.07, 0.66, "tl"),
        ("只能選一個 ↓", FONT_ZH_BOLD, 38, TERRA, 0.07, 0.87, "tl"),
    ], f"{OUT_W3}/Stories/MORENE_W3inc_S14.png")
    print("S14 done")


# =====================
# IG ×7  (1080×1350)
# =====================
IW, IH = 1080, 1350

def make_ig():
    os.makedirs(f"{OUT_W3}/IG", exist_ok=True)

    # IG1 7/12 老子引用 — 陶土橘底+乳香瓶+引言
    card(IW, IH, TERRA, "乳香", 0.70, 0.60, 0.84, [
        logo_line(CREAM, 0.07, 0.055),
        ("07.12", FONT_EN, 32, FOGPINK, 0.07, 0.10, "tl"),
        ('"知人者智,', FONT_ZH_BOLD, 72, CREAM, 0.07, 0.15, "tl"),
        ('自知者明。"', FONT_ZH_BOLD, 72, CREAM, 0.07, 0.24, "tl"),
        ('—— 老子《道德經》', FONT_ZH, 34, FOGPINK, 0.07, 0.34, "tl"),
        ("選一支香氣,是認識自己的起點", FONT_ZH, 38, CREAM, 0.07, 0.42, "tl"),
        ("MORENE 每支精油 · 學名產地透明", FONT_ZH, 28, FOGPINK, 0.07, 0.90, "tl"),
    ], f"{OUT_W3}/IG/MORENE_W3inc_IG1.png",
    shadow_opacity=0.22)
    print("IG1 done")

    # IG2 7/13 塗抹位置科普 — 奶油白
    card(IW, IH, CREAM, "甜橙", 0.65, 0.58, 0.82, [
        logo_line(BLACK, 0.07, 0.055),
        ("07.13", FONT_EN, 32, TERRA, 0.07, 0.10, "tl"),
        ("Where to Apply", FONT_EN_BOLD, 70, BLACK, 0.07, 0.14, "tl"),
        ("精油塗哪裡效果最好?", FONT_ZH_BOLD, 52, BLACK, 0.07, 0.24, "tl"),
        ("手腕內側  ·  脈搏溫度幫助揮發", FONT_ZH, 34, "#8C8079", 0.07, 0.33, "tl"),
        ("頸側後方  ·  靠近神經叢,反應快", FONT_ZH, 34, "#8C8079", 0.07, 0.40, "tl"),
        ("腳底湧泉  ·  角質厚,刺激小", FONT_ZH, 34, "#8C8079", 0.07, 0.47, "tl"),
        ("塗前  ·  建議以 2-3% 基底油稀釋", FONT_ZH_BOLD, 34, TERRA, 0.07, 0.57, "tl"),
        ("IFA 國際芳療師監製 · 完整 INCI 公開", FONT_ZH, 26, "#8C8079", 0.07, 0.90, "tl"),
    ], f"{OUT_W3}/IG/MORENE_W3inc_IG2.png")
    print("IG2 done")

    # IG3 7/14 晨間儀式 — 橙暖光底
    card(IW, IH, CARAMEL, "甜橙", 0.72, 0.54, 0.84, [
        logo_line(CREAM, 0.07, 0.055),
        ("07.14", FONT_EN, 32, CREAM, 0.07, 0.10, "tl"),
        ("Morning Ritual", FONT_EN_BOLD, 78, CREAM, 0.07, 0.14, "tl"),
        ("為自己設計一個", FONT_ZH_BOLD, 56, CREAM, 0.07, 0.25, "tl"),
        ("晨間香氣儀式", FONT_ZH_BOLD, 56, AMBER_YLW, 0.07, 0.33, "tl"),
        ("佛手柑 · 清新啟動", FONT_ZH, 36, CREAM, 0.07, 0.44, "tl"),
        ("甜橙 · 溫暖陽光感", FONT_ZH, 36, CREAM, 0.07, 0.51, "tl"),
        ("你的早晨從哪支香氣開始?", FONT_ZH_BOLD, 36, AMBER_YLW, 0.07, 0.88, "tl"),
    ], f"{OUT_W3}/IG/MORENE_W3inc_IG3.png",
    shadow_offset_x=50, shadow_opacity=0.24)
    print("IG3 done")

    # IG4 7/15 佛手柑聚光 — 黃底強投影
    card(IW, IH, AMBER_YLW, "佛手柑", 0.75, 0.54, 0.86, [
        logo_line(BLACK, 0.07, 0.055),
        ("07.15", FONT_EN, 32, TERRA, 0.07, 0.10, "tl"),
        ("Bergamot", FONT_EN_BOLD, 96, BLACK, 0.07, 0.14, "tl"),
        ("佛手柑", FONT_ZH_BOLD, 74, BLACK, 0.07, 0.26, "tl"),
        ("Citrus bergamia", FONT_EN, 34, TERRA, 0.07, 0.36, "tl"),
        ("義大利卡拉布里亞·冷壓萃取", FONT_ZH, 32, "#8C8079", 0.07, 0.43, "tl"),
        ("使用後 12 小時避免陽光直曬", FONT_ZH_BOLD, 32, TERRA, 0.07, 0.52, "tl"),
        ("IFA 監製 · 學名產地透明 · INCI 公開", FONT_ZH, 26, BLACK, 0.07, 0.89, "tl"),
    ], f"{OUT_W3}/IG/MORENE_W3inc_IG4.png",
    shadow_offset_x=65, shadow_blur=50, shadow_opacity=0.30)
    print("IG4 done")

    # IG5 7/16 UGC 旅行 — 奶油白
    card(IW, IH, CREAM, "佛手柑", 0.64, 0.55, 0.80, [
        logo_line(BLACK, 0.07, 0.055),
        ("07.16", FONT_EN, 32, FOGBLUE, 0.07, 0.10, "tl"),
        ("Travel With Me", FONT_EN_BOLD, 72, BLACK, 0.07, 0.14, "tl"),
        ("帶一支精油出發", FONT_ZH_BOLD, 56, BLACK, 0.07, 0.24, "tl"),
        ("旅行包裡,你會帶哪支?", FONT_ZH, 38, "#8C8079", 0.07, 0.33, "tl"),
        ("佛手柑  —  陌生城市的陽光感", FONT_ZH, 34, FOGBLUE, 0.07, 0.43, "tl"),
        ("大西洋雪松  —  旅館夜晚的穩定感", FONT_ZH, 34, FOGBLUE, 0.07, 0.50, "tl"),
        ("留言分享你的旅行精油 →", FONT_ZH_BOLD, 36, BLACK, 0.07, 0.88, "tl"),
    ], f"{OUT_W3}/IG/MORENE_W3inc_IG5.png")
    print("IG5 done")

    # IG6 7/17 運動香氣 — 暗調
    card(IW, IH, DARK_GY, "大西洋雪松", 0.70, 0.56, 0.84, [
        logo_line(CREAM, 0.07, 0.055),
        ("07.17", FONT_EN, 32, SAGE, 0.07, 0.10, "tl"),
        ("After The Sweat", FONT_EN_BOLD, 72, CREAM, 0.07, 0.14, "tl"),
        ("運動後的香氣切換", FONT_ZH_BOLD, 54, CREAM, 0.07, 0.24, "tl"),
        ("大西洋雪松 · 木質大地感", FONT_ZH, 36, SAGE, 0.07, 0.34, "tl"),
        ("幫你從亢奮模式切換回平靜", FONT_ZH, 34, "#8C8079", 0.07, 0.41, "tl"),
        ("岩蘭草 · 穩定深沉", FONT_ZH, 36, WARMSAND, 0.07, 0.49, "tl"),
        ("與大西洋雪松搭配使用效果更佳", FONT_ZH, 30, "#8C8079", 0.07, 0.56, "tl"),
        ("IFA 監製 · 學名產地透明", FONT_ZH, 26, SAGE, 0.07, 0.88, "tl"),
    ], f"{OUT_W3}/IG/MORENE_W3inc_IG6.png",
    shadow_offset_x=45, shadow_opacity=0.22)
    print("IG6 done")

    # IG7 7/18 產地透明 — 薰衣草紫/奶油白
    card(IW, IH, CREAM, "真正薰衣草", 0.70, 0.54, 0.84, [
        logo_line(BLACK, 0.07, 0.055),
        ("07.18", FONT_EN, 32, FOGBLUE, 0.07, 0.10, "tl"),
        ("Transparency", FONT_EN_BOLD, 80, BLACK, 0.07, 0.14, "tl"),
        ("產地透明,是誠信的起點", FONT_ZH_BOLD, 50, BLACK, 0.07, 0.25, "tl"),
        ("真正薰衣草", FONT_ZH_BOLD, 56, FOGBLUE, 0.07, 0.34, "tl"),
        ("Lavandula angustifolia", FONT_EN, 30, "#8C8079", 0.07, 0.43, "tl"),
        ("普羅旺斯 · 蒸氣蒸餾 · IFA 監製", FONT_ZH, 32, "#8C8079", 0.07, 0.50, "tl"),
        ("學名·產地·INCI 全公開", FONT_ZH_BOLD, 36, FOGBLUE, 0.07, 0.59, "tl"),
        ("你有資格知道你擦了什麼", FONT_ZH, 32, "#8C8079", 0.07, 0.67, "tl"),
        ("morene.com.tw", FONT_EN, 28, FOGBLUE, 0.07, 0.89, "tl"),
    ], f"{OUT_W3}/IG/MORENE_W3inc_IG7.png")
    print("IG7 done")


# =====================
# FB ×7  (1080×1080)
# =====================
FW, FH = 1080, 1080

def make_fb():
    os.makedirs(f"{OUT_W3}/FB", exist_ok=True)

    _fb_specs = [
        # (bottle, scale, xf, yf, bg, lines, suffix)
        ("乳香", 0.65, 0.60, 0.82, TERRA, [
            logo_line(CREAM, 0.07, 0.07),
            ("07.12", FONT_EN, 30, FOGPINK, 0.07, 0.13, "tl"),
            ('"知人者智,自知者明。"', FONT_ZH_BOLD, 58, CREAM, 0.07, 0.18, "tl"),
            ('—— 老子《道德經》', FONT_ZH, 30, FOGPINK, 0.07, 0.28, "tl"),
            ("選香,是認識自己的一刻", FONT_ZH, 34, CREAM, 0.07, 0.35, "tl"),
            ("MORENE · 學名產地透明", FONT_ZH, 24, FOGPINK, 0.07, 0.88, "tl"),
        ], "FB1"),
        ("甜橙", 0.60, 0.58, 0.80, CREAM, [
            logo_line(BLACK, 0.07, 0.07),
            ("07.13", FONT_EN, 30, TERRA, 0.07, 0.13, "tl"),
            ("精油塗哪裡最有效?", FONT_ZH_BOLD, 54, BLACK, 0.07, 0.18, "tl"),
            ("手腕・頸側・腳底・胸口", FONT_ZH, 36, TERRA, 0.07, 0.28, "tl"),
            ("塗前建議稀釋 2-3%", FONT_ZH, 32, "#8C8079", 0.07, 0.36, "tl"),
            ("IFA 監製 · INCI 公開", FONT_ZH, 24, "#8C8079", 0.07, 0.87, "tl"),
        ], "FB2"),
        ("甜橙", 0.62, 0.56, 0.82, CARAMEL, [
            logo_line(CREAM, 0.07, 0.07),
            ("07.14", FONT_EN, 30, CREAM, 0.07, 0.13, "tl"),
            ("晨間香氣儀式", FONT_ZH_BOLD, 60, CREAM, 0.07, 0.18, "tl"),
            ("佛手柑 · 清新 / 甜橙 · 溫暖", FONT_ZH, 36, AMBER_YLW, 0.07, 0.29, "tl"),
            ("一分鐘,為自己留下儀式感", FONT_ZH, 32, CREAM, 0.07, 0.37, "tl"),
            ("morene.com.tw", FONT_EN, 26, CREAM, 0.07, 0.87, "tl"),
        ], "FB3"),
        ("佛手柑", 0.66, 0.56, 0.82, AMBER_YLW, [
            logo_line(BLACK, 0.07, 0.07),
            ("07.15", FONT_EN, 30, TERRA, 0.07, 0.13, "tl"),
            ("Bergamot / 佛手柑", FONT_ZH_BOLD, 56, BLACK, 0.07, 0.18, "tl"),
            ("Citrus bergamia · 義大利", FONT_ZH, 28, TERRA, 0.07, 0.28, "tl"),
            ("使用後 12 小時避免陽光直曬", FONT_ZH_BOLD, 30, TERRA, 0.07, 0.35, "tl"),
            ("IFA 監製 · INCI 公開", FONT_ZH, 24, BLACK, 0.07, 0.87, "tl"),
        ], "FB4"),
        ("佛手柑", 0.58, 0.56, 0.78, CREAM, [
            logo_line(BLACK, 0.07, 0.07),
            ("07.16", FONT_EN, 30, FOGBLUE, 0.07, 0.13, "tl"),
            ("帶一支精油出發", FONT_ZH_BOLD, 58, BLACK, 0.07, 0.18, "tl"),
            ("旅行包裡你會帶哪支?", FONT_ZH, 36, "#8C8079", 0.07, 0.28, "tl"),
            ("留言分享你的旅行精油 →", FONT_ZH_BOLD, 32, FOGBLUE, 0.07, 0.36, "tl"),
            ("morene.com.tw", FONT_EN, 26, "#8C8079", 0.07, 0.87, "tl"),
        ], "FB5"),
        ("大西洋雪松", 0.64, 0.56, 0.82, DARK_GY, [
            logo_line(CREAM, 0.07, 0.07),
            ("07.17", FONT_EN, 30, SAGE, 0.07, 0.13, "tl"),
            ("運動後的香氣切換", FONT_ZH_BOLD, 56, CREAM, 0.07, 0.18, "tl"),
            ("大西洋雪松 · 岩蘭草", FONT_ZH, 36, SAGE, 0.07, 0.28, "tl"),
            ("從亢奮模式切換回平靜", FONT_ZH, 32, "#8C8079", 0.07, 0.36, "tl"),
            ("IFA 監製 · 學名產地透明", FONT_ZH, 24, SAGE, 0.07, 0.87, "tl"),
        ], "FB6"),
        ("真正薰衣草", 0.64, 0.54, 0.82, CREAM, [
            logo_line(BLACK, 0.07, 0.07),
            ("07.18", FONT_EN, 30, FOGBLUE, 0.07, 0.13, "tl"),
            ("產地透明,是誠信的起點", FONT_ZH_BOLD, 54, BLACK, 0.07, 0.18, "tl"),
            ("真正薰衣草 · 普羅旺斯", FONT_ZH_BOLD, 42, FOGBLUE, 0.07, 0.29, "tl"),
            ("學名·產地·INCI 全公開", FONT_ZH, 34, "#8C8079", 0.07, 0.37, "tl"),
            ("morene.com.tw", FONT_EN, 26, FOGBLUE, 0.07, 0.87, "tl"),
        ], "FB7"),
    ]

    for (bottle, scale, xf, yf, bg, lines, suffix) in _fb_specs:
        card(FW, FH, bg, bottle, scale, xf, yf, lines,
             f"{OUT_W3}/FB/MORENE_W3inc_{suffix}.png")
        print(f"{suffix} done")


# =====================
# REELS 分鏡 ×3×6  (1080×1920)
# =====================
def make_reels():
    os.makedirs(f"{OUT_W3}/Reels", exist_ok=True)

    # R1: 7/12 老子選香 (6 幀)
    r1_frames = [
        # f1 封面
        (TERRA, "乳香", 0.70, 0.58, 0.84, [
            logo_line(CREAM, 0.07, 0.06),
            ('"知人者智,自知者明。"', FONT_ZH_BOLD, 58, CREAM, 0.07, 0.14, "tl"),
            ('—— 老子《道德經》', FONT_ZH, 32, FOGPINK, 0.07, 0.24, "tl"),
            ('選一支懂你的香氣', FONT_ZH_BOLD, 50, CREAM, 0.07, 0.31, "tl"),
        ]),
        # f2 精油架猶豫
        (CREAM, "甜橙", 0.62, 0.52, 0.80, [
            logo_line(BLACK, 0.07, 0.06),
            ("選香的那一刻", FONT_ZH_BOLD, 58, BLACK, 0.07, 0.14, "tl"),
            ("你是用眼睛選,還是用鼻子選?", FONT_ZH, 40, "#8C8079", 0.07, 0.23, "tl"),
        ]),
        # f3 拿瓶聞
        (AMBER_YLW, "佛手柑", 0.68, 0.55, 0.83, [
            logo_line(BLACK, 0.07, 0.06),
            ("先聞前調", FONT_ZH_BOLD, 64, BLACK, 0.07, 0.14, "tl"),
            ("再等中調浮現", FONT_ZH, 44, TERRA, 0.07, 0.23, "tl"),
            ("後調才是真正的你", FONT_ZH_BOLD, 42, BLACK, 0.07, 0.31, "tl"),
        ]),
        # f4 品牌說明
        (TERRA, "乳香", 0.60, 0.58, 0.78, [
            logo_line(CREAM, 0.07, 0.06),
            ("MORENE 每支精油", FONT_ZH_BOLD, 52, CREAM, 0.07, 0.14, "tl"),
            ("學名・產地・INCI 全公開", FONT_ZH, 40, FOGPINK, 0.07, 0.23, "tl"),
            ("IFA 國際芳療師監製", FONT_ZH_BOLD, 44, AMBER_YLW, 0.07, 0.31, "tl"),
        ]),
        # f5 香氣人格提示
        (CREAM, "甜橙", 0.58, 0.54, 0.78, [
            logo_line(BLACK, 0.07, 0.06),
            ("你是哪種香氣人格?", FONT_ZH_BOLD, 56, BLACK, 0.07, 0.14, "tl"),
            ("柑橘型 · 木質型 · 花香型 · 大地型", FONT_ZH, 34, "#8C8079", 0.07, 0.24, "tl"),
        ]),
        # f6 CTA
        (NAVY, "乳香", 0.62, 0.55, 0.80, [
            logo_line(CREAM, 0.07, 0.06),
            ("測你的香氣人格", FONT_ZH_BOLD, 60, CREAM, 0.07, 0.14, "tl"),
            ("morene.com.tw/pages/scent-personality", FONT_EN, 24, FOGBLUE, 0.07, 0.25, "tl"),
            ("點選 bio 連結 →", FONT_ZH_BOLD, 40, SAGE, 0.07, 0.33, "tl"),
        ]),
    ]

    for fi, (bg, bottle, scale, xf, yf, lines) in enumerate(r1_frames, 1):
        _assert_no_tofu(lines)
        card(SW, SH, bg, bottle, scale, xf, yf, lines,
             f"{OUT_W3}/Reels/MORENE_W3inc_R1_f{fi}.png")
        print(f"R1_f{fi} done")

    # R2: 7/15 佛手柑 (6 幀)
    r2_frames = [
        # f1 封面
        (AMBER_YLW, "佛手柑", 0.74, 0.54, 0.86, [
            logo_line(BLACK, 0.07, 0.06),
            ("Bergamot", FONT_EN_BOLD, 100, BLACK, 0.07, 0.14, "tl"),
            ("佛手柑", FONT_ZH_BOLD, 72, BLACK, 0.07, 0.28, "tl"),
            ("陽光裡的義大利香氣", FONT_ZH, 40, TERRA, 0.07, 0.38, "tl"),
        ]),
        # f2 義大利產地
        (CREAM, "佛手柑", 0.65, 0.54, 0.80, [
            logo_line(BLACK, 0.07, 0.06),
            ("Origin", FONT_EN_BOLD, 80, BLACK, 0.07, 0.14, "tl"),
            ("義大利卡拉布里亞", FONT_ZH_BOLD, 56, TERRA, 0.07, 0.25, "tl"),
            ("Citrus bergamia · 冷壓萃取", FONT_ZH, 30, "#8C8079", 0.07, 0.34, "tl"),
            ("每批學名產地透明標示", FONT_ZH, 36, "#8C8079", 0.07, 0.41, "tl"),
        ]),
        # f3 開瓶聞香
        (CARAMEL, "佛手柑", 0.70, 0.54, 0.83, [
            logo_line(CREAM, 0.07, 0.06),
            ("Open & Inhale", FONT_EN_BOLD, 72, CREAM, 0.07, 0.14, "tl"),
            ("前調:柑橘清新", FONT_ZH_BOLD, 50, CREAM, 0.07, 0.25, "tl"),
            ("中調:花香微甜", FONT_ZH, 40, AMBER_YLW, 0.07, 0.33, "tl"),
            ("後調:淡淡木質", FONT_ZH, 40, CREAM, 0.07, 0.41, "tl"),
        ]),
        # f4 光敏提醒字卡
        (NAVY, "佛手柑", 0.58, 0.58, 0.78, [
            logo_line(CREAM, 0.07, 0.06),
            ("使用注意", FONT_ZH_BOLD, 64, FOGPINK, 0.07, 0.14, "tl"),
            ("佛手柑含呋喃香豆素", FONT_ZH, 40, CREAM, 0.07, 0.25, "tl"),
            ("塗抹後 12 小時", FONT_ZH_BOLD, 50, AMBER_YLW, 0.07, 0.33, "tl"),
            ("請避免陽光直曬皮膚", FONT_ZH_BOLD, 50, AMBER_YLW, 0.07, 0.42, "tl"),
            ("尤其戶外活動前請留意", FONT_ZH, 34, FOGBLUE, 0.07, 0.52, "tl"),
        ]),
        # f5 搭配建議
        (CREAM, "甜橙", 0.62, 0.54, 0.80, [
            logo_line(BLACK, 0.07, 0.06),
            ("Blending Tip", FONT_EN_BOLD, 68, BLACK, 0.07, 0.14, "tl"),
            ("佛手柑 + 甜橙", FONT_ZH_BOLD, 54, TERRA, 0.07, 0.24, "tl"),
            ("夏天早晨最清新的組合", FONT_ZH, 38, "#8C8079", 0.07, 0.33, "tl"),
            ("稀釋後塗手腕或頸側", FONT_ZH, 36, "#8C8079", 0.07, 0.41, "tl"),
        ]),
        # f6 CTA
        (AMBER_YLW, "佛手柑", 0.64, 0.54, 0.80, [
            logo_line(BLACK, 0.07, 0.06),
            ("morene.com.tw", FONT_EN_BOLD, 52, BLACK, 0.07, 0.14, "tl"),
            ("完整了解佛手柑精油", FONT_ZH_BOLD, 50, TERRA, 0.07, 0.24, "tl"),
            ("點選 bio 連結 →", FONT_ZH, 40, BLACK, 0.07, 0.33, "tl"),
        ]),
    ]

    for fi, (bg, bottle, scale, xf, yf, lines) in enumerate(r2_frames, 1):
        _assert_no_tofu(lines)
        card(SW, SH, bg, bottle, scale, xf, yf, lines,
             f"{OUT_W3}/Reels/MORENE_W3inc_R2_f{fi}.png")
        print(f"R2_f{fi} done")

    # R3: 7/17 運動後切換 (6 幀)
    r3_frames = [
        # f1 封面
        (DARK_GY, "大西洋雪松", 0.72, 0.56, 0.84, [
            logo_line(CREAM, 0.07, 0.06),
            ("After The Workout", FONT_EN_BOLD, 68, CREAM, 0.07, 0.14, "tl"),
            ("運動後的香氣切換", FONT_ZH_BOLD, 56, CREAM, 0.07, 0.25, "tl"),
            ("從亢奮模式回到自己", FONT_ZH, 38, SAGE, 0.07, 0.34, "tl"),
        ]),
        # f2 換衣後儀式
        (CREAM, "大西洋雪松", 0.62, 0.54, 0.80, [
            logo_line(BLACK, 0.07, 0.06),
            ("換衣之後", FONT_ZH_BOLD, 64, BLACK, 0.07, 0.14, "tl"),
            ("是儀式的開始", FONT_ZH_BOLD, 64, TERRA, 0.07, 0.24, "tl"),
            ("一個深呼吸 + 一滴精油", FONT_ZH, 38, "#8C8079", 0.07, 0.34, "tl"),
        ]),
        # f3 擴香信號
        (DARK_GY, "大西洋雪松", 0.66, 0.54, 0.82, [
            logo_line(CREAM, 0.07, 0.06),
            ("Diffuse Signal", FONT_EN_BOLD, 72, CREAM, 0.07, 0.14, "tl"),
            ("大西洋雪松", FONT_ZH_BOLD, 58, SAGE, 0.07, 0.25, "tl"),
            ("木質大地,告訴身體:可以放鬆了", FONT_ZH, 36, CREAM, 0.07, 0.34, "tl"),
        ]),
        # f4 木質柑橘對比
        (CREAM, "岩蘭草", 0.60, 0.58, 0.78, [
            logo_line(BLACK, 0.07, 0.06),
            ("木質 vs 柑橘", FONT_ZH_BOLD, 60, BLACK, 0.07, 0.14, "tl"),
            ("運動後想要穩定  →  木質", FONT_ZH, 38, TERRA, 0.07, 0.25, "tl"),
            ("大西洋雪松 / 岩蘭草", FONT_ZH_BOLD, 44, TERRA, 0.07, 0.33, "tl"),
            ("運動前想要提振  →  柑橘", FONT_ZH, 38, FOGBLUE, 0.07, 0.44, "tl"),
            ("甜橙 / 佛手柑", FONT_ZH_BOLD, 44, FOGBLUE, 0.07, 0.52, "tl"),
        ]),
        # f5 品牌信任
        (DARK_GY, "大西洋雪松", 0.62, 0.54, 0.80, [
            logo_line(CREAM, 0.07, 0.06),
            ("MORENE 每支精油", FONT_ZH_BOLD, 52, CREAM, 0.07, 0.14, "tl"),
            ("學名 · 產地 · INCI 全公開", FONT_ZH, 40, SAGE, 0.07, 0.24, "tl"),
            ("IFA 國際芳療師監製", FONT_ZH_BOLD, 44, AMBER_YLW, 0.07, 0.33, "tl"),
        ]),
        # f6 CTA
        (CREAM, "大西洋雪松", 0.60, 0.54, 0.78, [
            logo_line(BLACK, 0.07, 0.06),
            ("找到你的運動後香氣", FONT_ZH_BOLD, 54, BLACK, 0.07, 0.14, "tl"),
            ("morene.com.tw", FONT_EN_BOLD, 44, FOGBLUE, 0.07, 0.25, "tl"),
            ("點選 bio 連結 →", FONT_ZH, 38, TERRA, 0.07, 0.33, "tl"),
        ]),
    ]

    for fi, (bg, bottle, scale, xf, yf, lines) in enumerate(r3_frames, 1):
        _assert_no_tofu(lines)
        card(SW, SH, bg, bottle, scale, xf, yf, lines,
             f"{OUT_W3}/Reels/MORENE_W3inc_R3_f{fi}.png")
        print(f"R3_f{fi} done")


# =====================
# CANARY TEST (S2 老子引言, R2_f4 光敏字卡)
# =====================
def make_canary():
    os.makedirs(f"{OUT_W3}/Stories", exist_ok=True)
    print("=== CANARY: S2 (老子引言) ===")
    card(SW, SH, NAVY, "乳香", 0.68, 0.60, 0.85, [
        logo_line(CREAM, 0.07, 0.06),
        ("07.12 CANARY", FONT_EN, 36, FOGBLUE, 0.07, 0.11, "tl"),
        ('"知人者智,', FONT_ZH_BOLD, 64, CREAM, 0.07, 0.16, "tl"),
        ('自知者明。"', FONT_ZH_BOLD, 64, CREAM, 0.07, 0.24, "tl"),
        ('—— 老子《道德經》', FONT_ZH, 34, "#82A8CC", 0.07, 0.33, "tl"),
        ('選香,也是認識自己的一刻', FONT_ZH, 38, "#CBA98A", 0.07, 0.40, "tl"),
    ], f"{OUT_W3}/Stories/MORENE_W3inc_CANARY_S2.png",
    shadow_opacity=0.18)
    print("Canary S2 saved.")


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode == "canary":
        make_canary()
    elif mode == "stories":
        make_stories()
    elif mode == "ig":
        make_ig()
    elif mode == "fb":
        make_fb()
    elif mode == "reels":
        make_reels()
    else:
        print("=== W3inc: Stories ===")
        make_stories()
        print("=== W3inc: IG ===")
        make_ig()
        print("=== W3inc: FB ===")
        make_fb()
        print("=== W3inc: Reels ===")
        make_reels()
        print("=== ALL DONE ===")
