#!/usr/bin/env python3
"""
MORENE 父親節_8月 批次圖卡生成腳本
主題: 送他一份安靜 · 沉靜木質/樹脂送禮
策略: 攝影主導 + 深色木質/樹脂沉穩底 + 真實琥珀瓶 + 極少字 + 克制留白

逐日主題 (8/1–8/8):
  8/1 乳香 · 序章「送他一份安靜」    深可可沉靜底 (乳香)
  8/2 岩蘭草 · 沉穩大地              大地褐底   (岩蘭草)
  8/3 大西洋雪松 · 書房木質          木質暖棕底 (雪松)
  8/4 為他配一組沉靜香 · 香氣人格     禮物組概念 (三瓶: 乳香/岩蘭草/雪松)
  8/5 送禮文學「給沉默的他」          米白引言印卡 (乳香)
  8/6 包裝一份安靜 · 禮物儀式        包裝留白 (雪松)
  8/7 父親節前夕 · 乳香的留白        乳香留白 (乳香)
  8/8 父親節快樂 · 送他一份安靜       節日溫暖收束 (乳香)

Reels:
  R1 沉靜的禮物開場 (8/1 樹脂 · 乳香)
  R2 三支木質樹脂禮物組 (8/4 · 乳香/岩蘭草/雪松)
  R3 父親節一份安靜的禮物 (8/8 · 乳香)

命名規則:
  Stories: MORENE_FD_S01 ~ S16 (2 位補零)
  IG:      MORENE_FD_IG1 ~ IG8 (不補零)
  FB:      MORENE_FD_FB1 ~ FB8 (不補零)
  Reels:   MORENE_FD_R1_f1~f6 / R2_f1~f6 / R3_f1~f6 (共18)
  共 16+8+8+18 = 50 PNG

⚠️ 不放 ISO/GMP/認證標章
⚠️ 不寫療效詞 (助眠/修復/治療/舒緩/放鬆/療癒)
⚠️ CJK tofu 防呆: 含 CJK 字元必用 FONT_ZH / FONT_ZH_BOLD
⚠️ 信任點: IFA 國際芳療師監製 · 學名/萃取部位透明
⚠️ 產地: 乳香產地以瓶身標籤為準=印度(避免與標籤矛盾); 岩蘭草/雪松不杜撰產地, 只放學名+萃取部位
"""

import os
import sys
import shutil
sys.path.insert(0, "/Users/morrislin/mw-social-assets/MORENE")

from make_covers_v2 import (
    compose_card,
    compose_multi_bottle,
    FONT_EN_BOLD, FONT_EN, FONT_ZH, FONT_ZH_BOLD,
    CREAM, BLACK, TERRA, MUSTARD, SAGE, WHITE,
    OUT_BASE,
    get_bottle,
)
import make_covers_v2 as _m

# =====================
# 父親節色彩 (VIS 暖色票 · 沉靜木質/樹脂)
# =====================
WARMCREAM  = "#EDE7DC"   # 奶油
WARMWHITE  = "#F5F0E8"   # 暖白
GREYBROWN  = "#8C8079"   # 灰褐
WARMSAND   = "#CBA98A"   # 暖沙
CARAMEL    = "#C9853E"   # 焦糖
GOLDYELLOW = "#E8CE8C"   # 芥末淡
TEAL       = "#8DBFBE"   # 霧藍綠
COCOA      = "#2A1A10"   # 深可可 (乳香夜底 · 沉靜)
DARKBROWN  = "#3D2B1F"   # 暖棕深
EARTHBROWN = "#5A4632"   # 大地褐 (岩蘭草)
WOODTAN    = "#7A5E42"   # 木質暖棕 (雪松書房)
DEEPRESIN  = "#23170E"   # 深樹脂 (Reels 開場)

WEEK = "FathersDay_Aug"

# =====================
# 路徑
# =====================
BASE_PROD = "/Users/morrislin/Desktop/MORENE/03_MORENE/03_Assets/A009：MORENE-產品相關/01.產品相關/01. 產品資料/05. 產品照片/素材/商品大圖/01_精油"
DESK_ASSETS = "/Users/morrislin/Desktop/MORENE/MORENE_社群營運_Social/03_圖卡_Assets"

EXTRA_BOTTLES = {
    "乳香":       f"{BASE_PROD}/5MOEO009_乳香/MORENE_精油瓶_去背_乳香.png",
    "大西洋雪松": f"{BASE_PROD}/5MOEO005_大西洋雪松/MORENE_精油瓶_去背_大西洋雪松.png",
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
# 合規禁字防呆
# =====================
_FORBIDDEN = ["助眠", "修復", "治療", "舒緩", "放鬆", "療癒", "保證", "限時搶購", "ISO", "GMP", "認證"]
def assert_compliant(text_lines, card_name=""):
    for (text, *_rest) in text_lines:
        for w in _FORBIDDEN:
            if w in text:
                raise ValueError(f"[compliance] {card_name}: forbidden word '{w}' in '{text}'")

# =====================
# 雙寫輔助 (Desktop 備份, 不影響 git)
# =====================
def dual_save(week, channel, filename, src_path):
    desk_dir = f"{DESK_ASSETS}/{week}/{channel}"
    try:
        os.makedirs(desk_dir, exist_ok=True)
        shutil.copy2(src_path, f"{desk_dir}/{filename}")
    except Exception as e:
        print(f"  (dual-write skipped: {e})")

def save_and_dual(week, channel, filename, **kw):
    if not filename.startswith("MORENE_"):
        raise ValueError(f"Filename must start with MORENE_: {filename}")
    tl = kw.get("text_lines", [])
    assert_no_cjk_tofu(tl, card_name=filename)
    assert_compliant(tl, card_name=filename)
    nas_dir = f"{OUT_BASE}/{week}/{channel}"
    os.makedirs(nas_dir, exist_ok=True)
    nas_path = f"{nas_dir}/{filename}"
    compose_card(out_path=nas_path, **kw)
    dual_save(week, channel, filename, nas_path)
    return nas_path

def save_and_dual_multi(week, channel, filename, **kw):
    """禮物組多瓶卡 — 走 compose_multi_bottle, 共用 tofu/合規/path 邏輯"""
    if not filename.startswith("MORENE_"):
        raise ValueError(f"Filename must start with MORENE_: {filename}")
    tl = kw.get("text_lines", [])
    assert_no_cjk_tofu(tl, card_name=filename)
    assert_compliant(tl, card_name=filename)
    nas_dir = f"{OUT_BASE}/{week}/{channel}"
    os.makedirs(nas_dir, exist_ok=True)
    nas_path = f"{nas_dir}/{filename}"
    compose_multi_bottle(out_path=nas_path, **kw)
    dual_save(week, channel, filename, nas_path)
    return nas_path

FOOTER_NT = "情境使用 · 非療效宣稱 · MORENE.COM.TW"
GIFT3 = ["乳香", "岩蘭草", "大西洋雪松"]


# =====================================================================
# IG ×8 (1080×1350) + FB ×8 (1080×1080)  逐日同主題雙出
# 8/1→IG1/FB1 ... 8/8→IG8/FB8
# =====================================================================
def make_ig_fb():
    print("\n=== 父親節 IG + FB (8 天) ===")

    # ---- 8/1 IG1/FB1 乳香 · 序章「送他一份安靜」深可可底 ----
    print("IG1/FB1 8/1 乳香序章...")
    save_and_dual(WEEK, "IG", "MORENE_FD_IG1.png",
        canvas_w=1080, canvas_h=1350, bg_hex=COCOA,
        bottle_name="乳香", bottle_scale=0.62, bottle_x_frac=0.69, bottle_bottom_frac=0.88,
        shadow_offset_x=58, shadow_offset_y=26, shadow_blur=42, shadow_opacity=0.09,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, WARMCREAM, 0.055, 0.048, "tl"),
            ("01 / 08", FONT_EN, 14, GREYBROWN, 0.870, 0.048, "tl"),
            ("送他", FONT_ZH, 104, WARMCREAM, 0.055, 0.100, "tl"),
            ("一份安靜", FONT_ZH, 76, GOLDYELLOW, 0.055, 0.250, "tl"),
            ("父親節 · 沉靜香氣序章", FONT_ZH, 28, WARMCREAM, 0.055, 0.372, "tl"),
            ("乳香 · Boswellia carterii", FONT_ZH, 26, GREYBROWN, 0.055, 0.422, "tl"),
            ("印度 · 樹脂 · 木質溫暖", FONT_ZH, 24, GREYBROWN, 0.055, 0.466, "tl"),
            (FOOTER_NT, FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ])
    save_and_dual(WEEK, "FB", "MORENE_FD_FB1.png",
        canvas_w=1080, canvas_h=1080, bg_hex=COCOA,
        bottle_name="乳香", bottle_scale=0.68, bottle_x_frac=0.70, bottle_bottom_frac=0.92,
        shadow_offset_x=62, shadow_offset_y=28, shadow_blur=44, shadow_opacity=0.09,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, WARMCREAM, 0.055, 0.048, "tl"),
            ("送他一份安靜", FONT_ZH, 72, WARMCREAM, 0.055, 0.110, "tl"),
            ("父親節沉靜香氣", FONT_ZH, 40, GOLDYELLOW, 0.055, 0.250, "tl"),
            ("乳香 · Boswellia carterii", FONT_ZH, 24, GREYBROWN, 0.055, 0.350, "tl"),
            (FOOTER_NT, FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ])

    # ---- 8/2 IG2/FB2 岩蘭草 · 沉穩大地 大地褐底 ----
    print("IG2/FB2 8/2 岩蘭草...")
    save_and_dual(WEEK, "IG", "MORENE_FD_IG2.png",
        canvas_w=1080, canvas_h=1350, bg_hex=EARTHBROWN,
        bottle_name="岩蘭草", bottle_scale=0.62, bottle_x_frac=0.69, bottle_bottom_frac=0.88,
        shadow_offset_x=58, shadow_offset_y=26, shadow_blur=42, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, WARMCREAM, 0.055, 0.048, "tl"),
            ("02 / 08", FONT_EN, 14, WARMSAND, 0.870, 0.048, "tl"),
            ("岩蘭草", FONT_ZH, 96, WARMCREAM, 0.055, 0.100, "tl"),
            ("沉穩如大地", FONT_ZH, 50, GOLDYELLOW, 0.055, 0.270, "tl"),
            ("Chrysopogon zizanioides", FONT_EN, 24, WARMSAND, 0.055, 0.356, "tl"),
            ("根部蒸餾 · 深沉土質木香", FONT_ZH, 26, WARMCREAM, 0.055, 0.410, "tl"),
            ("IFA 國際芳療師監製 · 學名透明", FONT_ZH, 20, WARMSAND, 0.055, 0.462, "tl"),
            (FOOTER_NT, FONT_ZH, 15, WARMSAND, 0.055, 0.946, "tl"),
        ])
    save_and_dual(WEEK, "FB", "MORENE_FD_FB2.png",
        canvas_w=1080, canvas_h=1080, bg_hex=EARTHBROWN,
        bottle_name="岩蘭草", bottle_scale=0.68, bottle_x_frac=0.70, bottle_bottom_frac=0.92,
        shadow_offset_x=62, shadow_offset_y=28, shadow_blur=44, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, WARMCREAM, 0.055, 0.048, "tl"),
            ("岩蘭草", FONT_ZH, 80, WARMCREAM, 0.055, 0.110, "tl"),
            ("沉穩如大地", FONT_ZH, 42, GOLDYELLOW, 0.055, 0.262, "tl"),
            ("Chrysopogon zizanioides · 根部蒸餾", FONT_ZH, 22, WARMSAND, 0.055, 0.352, "tl"),
            (FOOTER_NT, FONT_ZH, 14, WARMSAND, 0.055, 0.944, "tl"),
        ])

    # ---- 8/3 IG3/FB3 大西洋雪松 · 書房木質 木質暖棕底 ----
    print("IG3/FB3 8/3 大西洋雪松...")
    save_and_dual(WEEK, "IG", "MORENE_FD_IG3.png",
        canvas_w=1080, canvas_h=1350, bg_hex=WOODTAN,
        bottle_name="大西洋雪松", bottle_scale=0.62, bottle_x_frac=0.69, bottle_bottom_frac=0.88,
        shadow_offset_x=58, shadow_offset_y=26, shadow_blur=42, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, WARMCREAM, 0.055, 0.048, "tl"),
            ("03 / 08", FONT_EN, 14, WARMWHITE, 0.870, 0.048, "tl"),
            ("書房裡的", FONT_ZH, 72, WARMCREAM, 0.055, 0.100, "tl"),
            ("木質時光", FONT_ZH, 72, WARMWHITE, 0.055, 0.210, "tl"),
            ("大西洋雪松", FONT_ZH, 40, GOLDYELLOW, 0.055, 0.330, "tl"),
            ("Cedrus atlantica · 木材蒸餾", FONT_ZH, 24, WARMWHITE, 0.055, 0.400, "tl"),
            ("IFA 國際芳療師監製 · 學名透明", FONT_ZH, 20, WARMWHITE, 0.055, 0.452, "tl"),
            (FOOTER_NT, FONT_ZH, 15, WARMWHITE, 0.055, 0.946, "tl"),
        ])
    save_and_dual(WEEK, "FB", "MORENE_FD_FB3.png",
        canvas_w=1080, canvas_h=1080, bg_hex=WOODTAN,
        bottle_name="大西洋雪松", bottle_scale=0.68, bottle_x_frac=0.70, bottle_bottom_frac=0.92,
        shadow_offset_x=62, shadow_offset_y=28, shadow_blur=44, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, WARMCREAM, 0.055, 0.048, "tl"),
            ("書房裡的木質時光", FONT_ZH, 52, WARMCREAM, 0.055, 0.110, "tl"),
            ("大西洋雪松", FONT_ZH, 44, WARMWHITE, 0.055, 0.250, "tl"),
            ("Cedrus atlantica · 木材蒸餾", FONT_ZH, 22, GOLDYELLOW, 0.055, 0.340, "tl"),
            (FOOTER_NT, FONT_ZH, 14, WARMWHITE, 0.055, 0.944, "tl"),
        ])

    # ---- 8/4 IG4/FB4 為他配一組沉靜香 · 香氣人格 禮物組三瓶 ----
    print("IG4/FB4 8/4 沉靜香禮物組 (三瓶)...")
    save_and_dual_multi(WEEK, "IG", "MORENE_FD_IG4.png",
        canvas_w=1080, canvas_h=1350, bg_hex=WARMSAND,
        bottle_names=GIFT3, bottle_height_frac=0.40, bottle_bottom_frac=0.90,
        margin_frac=0.07, spacing=26,
        shadow_offset_x=40, shadow_offset_y=20, shadow_blur=32, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("04 / 08", FONT_EN, 14, GREYBROWN, 0.870, 0.048, "tl"),
            ("為他配一組", FONT_ZH, 66, BLACK, 0.055, 0.100, "tl"),
            ("沉靜的香", FONT_ZH, 66, TERRA, 0.055, 0.196, "tl"),
            ("乳香 · 岩蘭草 · 大西洋雪松", FONT_ZH, 30, BLACK, 0.055, 0.310, "tl"),
            ("樹脂 × 大地 × 木質的沉穩三重奏", FONT_ZH, 24, GREYBROWN, 0.055, 0.360, "tl"),
            ("主頁玩香氣人格測驗 →", FONT_ZH, 26, TERRA, 0.055, 0.412, "tl"),
            (FOOTER_NT, FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ])
    save_and_dual_multi(WEEK, "FB", "MORENE_FD_FB4.png",
        canvas_w=1080, canvas_h=1080, bg_hex=WARMSAND,
        bottle_names=GIFT3, bottle_height_frac=0.42, bottle_bottom_frac=0.92,
        margin_frac=0.08, spacing=26,
        shadow_offset_x=40, shadow_offset_y=20, shadow_blur=32, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("為他配一組沉靜的香", FONT_ZH, 48, BLACK, 0.055, 0.110, "tl"),
            ("乳香 · 岩蘭草 · 大西洋雪松", FONT_ZH, 26, TERRA, 0.055, 0.232, "tl"),
            ("主頁玩香氣人格測驗 →", FONT_ZH, 24, GREYBROWN, 0.055, 0.292, "tl"),
            (FOOTER_NT, FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ])

    # ---- 8/5 IG5/FB5 送禮文學「給沉默的他」米白引言印卡 ----
    print("IG5/FB5 8/5 送禮文學...")
    save_and_dual(WEEK, "IG", "MORENE_FD_IG5.png",
        canvas_w=1080, canvas_h=1350, bg_hex=WARMWHITE,
        bottle_name="乳香", bottle_scale=0.50, bottle_x_frac=0.72, bottle_bottom_frac=0.90,
        shadow_offset_x=52, shadow_offset_y=22, shadow_blur=40, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("05 / 08 · 文學 × 芳療", FONT_ZH, 18, GREYBROWN, 0.055, 0.100, "tl"),
            ("給沉默的他", FONT_ZH, 70, BLACK, 0.055, 0.150, "tl"),
            ("有些情感不靠言語", FONT_ZH, 38, BLACK, 0.055, 0.276, "tl"),
            ("而是靠陪伴與氣味", FONT_ZH, 38, TERRA, 0.055, 0.336, "tl"),
            ("一份香氣 · 一句沒說出口的謝謝", FONT_ZH, 26, GREYBROWN, 0.055, 0.408, "tl"),
            ("乳香 · 為父親節而選", FONT_ZH, 24, GREYBROWN, 0.055, 0.460, "tl"),
            (FOOTER_NT, FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ])
    save_and_dual(WEEK, "FB", "MORENE_FD_FB5.png",
        canvas_w=1080, canvas_h=1080, bg_hex=WARMWHITE,
        bottle_name="乳香", bottle_scale=0.56, bottle_x_frac=0.74, bottle_bottom_frac=0.92,
        shadow_offset_x=54, shadow_offset_y=24, shadow_blur=42, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("給沉默的他", FONT_ZH, 60, BLACK, 0.055, 0.120, "tl"),
            ("有些情感不靠言語", FONT_ZH, 32, BLACK, 0.055, 0.262, "tl"),
            ("而是靠陪伴與氣味", FONT_ZH, 32, TERRA, 0.055, 0.318, "tl"),
            (FOOTER_NT, FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ])

    # ---- 8/6 IG6/FB6 包裝一份安靜 · 禮物儀式 包裝留白 (雪松) ----
    print("IG6/FB6 8/6 禮物儀式...")
    save_and_dual(WEEK, "IG", "MORENE_FD_IG6.png",
        canvas_w=1080, canvas_h=1350, bg_hex=WARMCREAM,
        bottle_name="大西洋雪松", bottle_scale=0.56, bottle_x_frac=0.72, bottle_bottom_frac=0.90,
        shadow_offset_x=54, shadow_offset_y=24, shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("06 / 08", FONT_EN, 14, GREYBROWN, 0.870, 0.048, "tl"),
            ("包裝", FONT_ZH, 100, BLACK, 0.055, 0.110, "tl"),
            ("一份安靜", FONT_ZH, 64, TERRA, 0.055, 0.262, "tl"),
            ("緞帶 · 牛皮 · 一張手寫卡", FONT_ZH, 28, BLACK, 0.055, 0.376, "tl"),
            ("禮物的儀式從包裝開始", FONT_ZH, 24, GREYBROWN, 0.055, 0.428, "tl"),
            (FOOTER_NT, FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ])
    save_and_dual(WEEK, "FB", "MORENE_FD_FB6.png",
        canvas_w=1080, canvas_h=1080, bg_hex=WARMCREAM,
        bottle_name="大西洋雪松", bottle_scale=0.62, bottle_x_frac=0.73, bottle_bottom_frac=0.92,
        shadow_offset_x=56, shadow_offset_y=26, shadow_blur=42, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("包裝一份安靜", FONT_ZH, 60, BLACK, 0.055, 0.120, "tl"),
            ("禮物的儀式從包裝開始", FONT_ZH, 32, TERRA, 0.055, 0.262, "tl"),
            ("緞帶 · 牛皮 · 一張手寫卡", FONT_ZH, 22, GREYBROWN, 0.055, 0.336, "tl"),
            (FOOTER_NT, FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ])

    # ---- 8/7 IG7/FB7 父親節前夕 · 乳香的留白 ----
    print("IG7/FB7 8/7 乳香的留白...")
    save_and_dual(WEEK, "IG", "MORENE_FD_IG7.png",
        canvas_w=1080, canvas_h=1350, bg_hex=WARMWHITE,
        bottle_name="乳香", bottle_scale=0.58, bottle_x_frac=0.70, bottle_bottom_frac=0.89,
        shadow_offset_x=54, shadow_offset_y=24, shadow_blur=40, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("07 / 08", FONT_EN, 14, GREYBROWN, 0.870, 0.048, "tl"),
            ("父親節前夕", FONT_ZH, 64, BLACK, 0.055, 0.110, "tl"),
            ("留一點安靜給他", FONT_ZH, 48, TERRA, 0.055, 0.214, "tl"),
            ("乳香 · 樹脂的留白", FONT_ZH, 30, BLACK, 0.055, 0.312, "tl"),
            ("Boswellia carterii · 印度", FONT_ZH, 24, GREYBROWN, 0.055, 0.364, "tl"),
            ("明天 · 把這份安靜送出去", FONT_ZH, 24, GREYBROWN, 0.055, 0.416, "tl"),
            (FOOTER_NT, FONT_ZH, 15, GREYBROWN, 0.055, 0.946, "tl"),
        ])
    save_and_dual(WEEK, "FB", "MORENE_FD_FB7.png",
        canvas_w=1080, canvas_h=1080, bg_hex=WARMWHITE,
        bottle_name="乳香", bottle_scale=0.64, bottle_x_frac=0.71, bottle_bottom_frac=0.92,
        shadow_offset_x=56, shadow_offset_y=26, shadow_blur=42, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("父親節前夕", FONT_ZH, 58, BLACK, 0.055, 0.120, "tl"),
            ("留一點安靜給他", FONT_ZH, 40, TERRA, 0.055, 0.256, "tl"),
            ("乳香 · 樹脂的留白", FONT_ZH, 24, GREYBROWN, 0.055, 0.346, "tl"),
            (FOOTER_NT, FONT_ZH, 14, GREYBROWN, 0.055, 0.944, "tl"),
        ])

    # ---- 8/8 IG8/FB8 父親節快樂 · 送他一份安靜 節日溫暖收束 ----
    print("IG8/FB8 8/8 父親節快樂...")
    save_and_dual(WEEK, "IG", "MORENE_FD_IG8.png",
        canvas_w=1080, canvas_h=1350, bg_hex=DARKBROWN,
        bottle_name="乳香", bottle_scale=0.60, bottle_x_frac=0.70, bottle_bottom_frac=0.88,
        shadow_offset_x=56, shadow_offset_y=26, shadow_blur=42, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, WARMCREAM, 0.055, 0.048, "tl"),
            ("08 / 08", FONT_EN, 14, WARMSAND, 0.870, 0.048, "tl"),
            ("父親節", FONT_ZH, 96, WARMCREAM, 0.055, 0.100, "tl"),
            ("快樂", FONT_ZH, 96, GOLDYELLOW, 0.055, 0.250, "tl"),
            ("送他一份安靜", FONT_ZH, 36, WARMCREAM, 0.055, 0.404, "tl"),
            ("謝謝你 · 用沉穩撐起一個家", FONT_ZH, 24, WARMSAND, 0.055, 0.460, "tl"),
            (FOOTER_NT, FONT_ZH, 15, WARMSAND, 0.055, 0.946, "tl"),
        ])
    save_and_dual(WEEK, "FB", "MORENE_FD_FB8.png",
        canvas_w=1080, canvas_h=1080, bg_hex=DARKBROWN,
        bottle_name="乳香", bottle_scale=0.66, bottle_x_frac=0.71, bottle_bottom_frac=0.92,
        shadow_offset_x=58, shadow_offset_y=28, shadow_blur=44, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, WARMCREAM, 0.055, 0.048, "tl"),
            ("父親節快樂", FONT_ZH, 72, WARMCREAM, 0.055, 0.110, "tl"),
            ("送他一份安靜", FONT_ZH, 40, GOLDYELLOW, 0.055, 0.260, "tl"),
            ("謝謝你 · 用沉穩撐起一個家", FONT_ZH, 22, WARMSAND, 0.055, 0.350, "tl"),
            (FOOTER_NT, FONT_ZH, 14, WARMSAND, 0.055, 0.944, "tl"),
        ])

    print("父親節 IG+FB 完成。")


# =====================================================================
# STORIES ×16 (1080×1920)  8天 × 2 (S01-02 .. S15-16)
# =====================================================================
def make_stories():
    print("\n=== 父親節 Stories S01–S16 ===")

    # 8/1 乳香序章
    save_and_dual(WEEK, "Stories", "MORENE_FD_S01.png",
        canvas_w=1080, canvas_h=1920, bg_hex=COCOA,
        bottle_name="乳香", bottle_scale=0.50, bottle_x_frac=0.68, bottle_bottom_frac=0.76,
        shadow_offset_x=46, shadow_offset_y=20, shadow_blur=36, shadow_opacity=0.09,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("父親節 · 8/1", FONT_ZH, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("送他一份安靜", FONT_ZH, 78, WARMCREAM, 0.055, 0.130, "tl"),
            ("沉靜香氣序章", FONT_ZH, 40, GOLDYELLOW, 0.055, 0.286, "tl"),
            ("乳香 · 樹脂木質", FONT_ZH, 28, GREYBROWN, 0.055, 0.346, "tl"),
            (FOOTER_NT, FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ])
    save_and_dual(WEEK, "Stories", "MORENE_FD_S02.png",
        canvas_w=1080, canvas_h=1920, bg_hex=DARKBROWN,
        bottle_name="乳香", bottle_scale=0.52, bottle_x_frac=0.66, bottle_bottom_frac=0.76,
        shadow_offset_x=46, shadow_offset_y=20, shadow_blur=36, shadow_opacity=0.11,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("父親節 · 8/1", FONT_ZH, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("乳香", FONT_ZH, 100, WARMCREAM, 0.055, 0.130, "tl"),
            ("沉靜的開場", FONT_ZH, 44, GOLDYELLOW, 0.055, 0.270, "tl"),
            ("Boswellia carterii", FONT_EN, 22, GREYBROWN, 0.055, 0.346, "tl"),
            ("印度 · 樹脂蒸餾", FONT_ZH, 26, GREYBROWN, 0.055, 0.392, "tl"),
            ("主頁看圖文 →", FONT_ZH, 30, WARMCREAM, 0.055, 0.448, "tl"),
            (FOOTER_NT, FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ])

    # 8/2 岩蘭草
    save_and_dual(WEEK, "Stories", "MORENE_FD_S03.png",
        canvas_w=1080, canvas_h=1920, bg_hex=EARTHBROWN,
        bottle_name="岩蘭草", bottle_scale=0.52, bottle_x_frac=0.68, bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22, shadow_blur=36, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("父親節 · 8/2", FONT_ZH, 14, WARMSAND, 0.055, 0.092, "tl"),
            ("沉穩", FONT_ZH, 100, WARMCREAM, 0.055, 0.130, "tl"),
            ("如大地", FONT_ZH, 68, GOLDYELLOW, 0.055, 0.270, "tl"),
            ("岩蘭草 · 根部蒸餾", FONT_ZH, 28, WARMCREAM, 0.055, 0.378, "tl"),
            (FOOTER_NT, FONT_ZH, 16, WARMSAND, 0.055, 0.944, "tl"),
        ])
    save_and_dual(WEEK, "Stories", "MORENE_FD_S04.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WOODTAN,
        bottle_name="岩蘭草", bottle_scale=0.54, bottle_x_frac=0.68, bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22, shadow_blur=36, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("父親節 · 8/2", FONT_ZH, 14, WARMWHITE, 0.055, 0.092, "tl"),
            ("岩蘭草", FONT_ZH, 90, WARMCREAM, 0.055, 0.130, "tl"),
            ("Chrysopogon zizanioides", FONT_EN, 22, WARMWHITE, 0.055, 0.272, "tl"),
            ("根部 · 深沉土質木香", FONT_ZH, 28, WARMWHITE, 0.055, 0.322, "tl"),
            ("主頁看全文 →", FONT_ZH, 30, GOLDYELLOW, 0.055, 0.382, "tl"),
            (FOOTER_NT, FONT_ZH, 16, WARMWHITE, 0.055, 0.944, "tl"),
        ])

    # 8/3 大西洋雪松
    save_and_dual(WEEK, "Stories", "MORENE_FD_S05.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WOODTAN,
        bottle_name="大西洋雪松", bottle_scale=0.52, bottle_x_frac=0.68, bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22, shadow_blur=36, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("父親節 · 8/3", FONT_ZH, 14, WARMWHITE, 0.055, 0.092, "tl"),
            ("書房裡的", FONT_ZH, 80, WARMCREAM, 0.055, 0.130, "tl"),
            ("木質時光", FONT_ZH, 64, GOLDYELLOW, 0.055, 0.262, "tl"),
            ("大西洋雪松 · 書桌上的沉穩", FONT_ZH, 28, WARMWHITE, 0.055, 0.366, "tl"),
            (FOOTER_NT, FONT_ZH, 16, WARMWHITE, 0.055, 0.944, "tl"),
        ])
    save_and_dual(WEEK, "Stories", "MORENE_FD_S06.png",
        canvas_w=1080, canvas_h=1920, bg_hex=DARKBROWN,
        bottle_name="大西洋雪松", bottle_scale=0.54, bottle_x_frac=0.68, bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22, shadow_blur=36, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("父親節 · 8/3", FONT_ZH, 14, WARMSAND, 0.055, 0.092, "tl"),
            ("大西洋雪松", FONT_ZH, 76, WARMCREAM, 0.055, 0.130, "tl"),
            ("Cedrus atlantica", FONT_EN, 22, WARMSAND, 0.055, 0.258, "tl"),
            ("木材蒸餾 · 乾爽木質", FONT_ZH, 28, WARMCREAM, 0.055, 0.308, "tl"),
            ("主頁看書房香氣 →", FONT_ZH, 30, GOLDYELLOW, 0.055, 0.368, "tl"),
            (FOOTER_NT, FONT_ZH, 16, WARMSAND, 0.055, 0.944, "tl"),
        ])

    # 8/4 禮物組 (多瓶)
    save_and_dual_multi(WEEK, "Stories", "MORENE_FD_S07.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WARMSAND,
        bottle_names=GIFT3, bottle_height_frac=0.26, bottle_bottom_frac=0.74,
        margin_frac=0.10, spacing=24,
        shadow_offset_x=38, shadow_offset_y=18, shadow_blur=30, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("父親節 · 8/4", FONT_ZH, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("為他配一組", FONT_ZH, 76, BLACK, 0.055, 0.130, "tl"),
            ("沉靜的香", FONT_ZH, 56, TERRA, 0.055, 0.250, "tl"),
            ("乳香 · 岩蘭草 · 雪松", FONT_ZH, 28, BLACK, 0.055, 0.806, "tl"),
            (FOOTER_NT, FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ])
    save_and_dual_multi(WEEK, "Stories", "MORENE_FD_S08.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WARMCREAM,
        bottle_names=GIFT3, bottle_height_frac=0.26, bottle_bottom_frac=0.74,
        margin_frac=0.10, spacing=24,
        shadow_offset_x=38, shadow_offset_y=18, shadow_blur=30, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("父親節 · 8/4", FONT_ZH, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("香氣人格測驗", FONT_ZH, 66, BLACK, 0.055, 0.130, "tl"),
            ("找出最適合他的沉靜香", FONT_ZH, 36, TERRA, 0.055, 0.246, "tl"),
            ("主頁玩測驗 →", FONT_ZH, 32, BLACK, 0.055, 0.314, "tl"),
            (FOOTER_NT, FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ])

    # 8/5 文學
    save_and_dual(WEEK, "Stories", "MORENE_FD_S09.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WARMWHITE,
        bottle_name="乳香", bottle_scale=0.46, bottle_x_frac=0.70, bottle_bottom_frac=0.78,
        shadow_offset_x=44, shadow_offset_y=18, shadow_blur=34, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("文學 × 芳療", FONT_ZH, 20, GREYBROWN, 0.055, 0.092, "tl"),
            ("給沉默的他", FONT_ZH, 64, BLACK, 0.055, 0.130, "tl"),
            ("有些情感不靠言語", FONT_ZH, 38, BLACK, 0.055, 0.262, "tl"),
            ("而是靠陪伴與氣味", FONT_ZH, 38, TERRA, 0.055, 0.318, "tl"),
            ("父親節 · 送禮文學", FONT_ZH, 24, GREYBROWN, 0.055, 0.382, "tl"),
            (FOOTER_NT, FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ])
    save_and_dual(WEEK, "Stories", "MORENE_FD_S10.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WARMSAND,
        bottle_name="乳香", bottle_scale=0.50, bottle_x_frac=0.68, bottle_bottom_frac=0.78,
        shadow_offset_x=46, shadow_offset_y=20, shadow_blur=36, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("父親節 · 8/5", FONT_ZH, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("給沉默的他", FONT_ZH, 72, BLACK, 0.055, 0.130, "tl"),
            ("一份香氣 · 一句謝謝", FONT_ZH, 38, TERRA, 0.055, 0.258, "tl"),
            ("主頁看送禮文學 →", FONT_ZH, 30, BLACK, 0.055, 0.330, "tl"),
            (FOOTER_NT, FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ])

    # 8/6 禮物儀式
    save_and_dual(WEEK, "Stories", "MORENE_FD_S11.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WARMCREAM,
        bottle_name="大西洋雪松", bottle_scale=0.48, bottle_x_frac=0.70, bottle_bottom_frac=0.78,
        shadow_offset_x=46, shadow_offset_y=20, shadow_blur=36, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("父親節 · 8/6", FONT_ZH, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("包裝", FONT_ZH, 100, BLACK, 0.055, 0.130, "tl"),
            ("一份安靜", FONT_ZH, 60, TERRA, 0.055, 0.286, "tl"),
            ("緞帶 · 牛皮 · 手寫卡", FONT_ZH, 28, BLACK, 0.055, 0.392, "tl"),
            (FOOTER_NT, FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ])
    save_and_dual(WEEK, "Stories", "MORENE_FD_S12.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WARMWHITE,
        bottle_name="大西洋雪松", bottle_scale=0.50, bottle_x_frac=0.68, bottle_bottom_frac=0.78,
        shadow_offset_x=46, shadow_offset_y=20, shadow_blur=36, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("父親節 · 8/6", FONT_ZH, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("禮物的儀式", FONT_ZH, 76, BLACK, 0.055, 0.130, "tl"),
            ("從包裝開始", FONT_ZH, 48, TERRA, 0.055, 0.256, "tl"),
            ("主頁看包裝靈感 →", FONT_ZH, 30, BLACK, 0.055, 0.330, "tl"),
            (FOOTER_NT, FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ])

    # 8/7 乳香留白
    save_and_dual(WEEK, "Stories", "MORENE_FD_S13.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WARMWHITE,
        bottle_name="乳香", bottle_scale=0.50, bottle_x_frac=0.70, bottle_bottom_frac=0.78,
        shadow_offset_x=46, shadow_offset_y=20, shadow_blur=36, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("父親節 · 8/7", FONT_ZH, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("前夕", FONT_ZH, 100, BLACK, 0.055, 0.130, "tl"),
            ("留一點安靜給他", FONT_ZH, 48, TERRA, 0.055, 0.286, "tl"),
            ("乳香 · 樹脂的留白", FONT_ZH, 28, GREYBROWN, 0.055, 0.358, "tl"),
            (FOOTER_NT, FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ])
    save_and_dual(WEEK, "Stories", "MORENE_FD_S14.png",
        canvas_w=1080, canvas_h=1920, bg_hex=COCOA,
        bottle_name="乳香", bottle_scale=0.52, bottle_x_frac=0.68, bottle_bottom_frac=0.76,
        shadow_offset_x=46, shadow_offset_y=20, shadow_blur=36, shadow_opacity=0.09,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("父親節 · 8/7", FONT_ZH, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("明天", FONT_ZH, 100, WARMCREAM, 0.055, 0.130, "tl"),
            ("把這份安靜送出去", FONT_ZH, 44, GOLDYELLOW, 0.055, 0.286, "tl"),
            ("乳香 · Boswellia carterii", FONT_ZH, 26, GREYBROWN, 0.055, 0.358, "tl"),
            ("主頁看父親節選香 →", FONT_ZH, 30, WARMCREAM, 0.055, 0.414, "tl"),
            (FOOTER_NT, FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ])

    # 8/8 父親節快樂
    save_and_dual(WEEK, "Stories", "MORENE_FD_S15.png",
        canvas_w=1080, canvas_h=1920, bg_hex=DARKBROWN,
        bottle_name="乳香", bottle_scale=0.52, bottle_x_frac=0.68, bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22, shadow_blur=38, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("父親節 · 8/8", FONT_ZH, 14, WARMSAND, 0.055, 0.092, "tl"),
            ("父親節", FONT_ZH, 96, WARMCREAM, 0.055, 0.130, "tl"),
            ("快樂", FONT_ZH, 72, GOLDYELLOW, 0.055, 0.286, "tl"),
            ("送他一份安靜", FONT_ZH, 36, WARMCREAM, 0.055, 0.392, "tl"),
            (FOOTER_NT, FONT_ZH, 16, WARMSAND, 0.055, 0.944, "tl"),
        ])
    save_and_dual(WEEK, "Stories", "MORENE_FD_S16.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WARMSAND,
        bottle_name="乳香", bottle_scale=0.52, bottle_x_frac=0.68, bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=22, shadow_blur=36, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("父親節 · 8/8", FONT_ZH, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("謝謝你", FONT_ZH, 88, BLACK, 0.055, 0.130, "tl"),
            ("用沉穩撐起一個家", FONT_ZH, 40, TERRA, 0.055, 0.270, "tl"),
            ("主頁看父親節選香 →", FONT_ZH, 30, BLACK, 0.055, 0.342, "tl"),
            (FOOTER_NT, FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ])

    print("父親節 Stories 完成。")


# =====================================================================
# REELS ×3 各6幀 (1080×1920)
# R1 沉靜的禮物開場 (8/1 樹脂·乳香)
# R2 三支木質樹脂禮物組 (8/4)
# R3 父親節一份安靜的禮物 (8/8)
# =====================================================================
def make_reels():
    print("\n=== 父親節 Reels ===")

    # ---------- R1 沉靜的禮物開場 (乳香) ----------
    print("--- R1 沉靜的禮物開場 ---")
    # f1 封面 — 深樹脂底, 必須好看
    save_and_dual(WEEK, "Reels", "MORENE_FD_R1_f1.png",
        canvas_w=1080, canvas_h=1920, bg_hex=DEEPRESIN,
        bottle_name="乳香", bottle_scale=0.56, bottle_x_frac=0.64, bottle_bottom_frac=0.80,
        shadow_offset_x=50, shadow_offset_y=22, shadow_blur=38, shadow_opacity=0.08,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("一份", FONT_ZH, 110, WARMCREAM, 0.055, 0.130, "tl"),
            ("沉靜的禮物", FONT_ZH, 70, GOLDYELLOW, 0.055, 0.300, "tl"),
            ("父親節 · 乳香樹脂", FONT_ZH, 28, WARMSAND, 0.055, 0.404, "tl"),
        ])
    save_and_dual(WEEK, "Reels", "MORENE_FD_R1_f2.png",
        canvas_w=1080, canvas_h=1920, bg_hex=COCOA,
        bottle_name="乳香", bottle_scale=0.58, bottle_x_frac=0.64, bottle_bottom_frac=0.80,
        shadow_offset_x=52, shadow_offset_y=24, shadow_blur=40, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("乳香", FONT_ZH, 110, WARMCREAM, 0.055, 0.130, "tl"),
            ("Boswellia carterii", FONT_EN, 26, GREYBROWN, 0.055, 0.304, "tl"),
            ("印度 · 樹脂 · 木質溫暖", FONT_ZH, 28, GREYBROWN, 0.055, 0.358, "tl"),
        ])
    save_and_dual(WEEK, "Reels", "MORENE_FD_R1_f3.png",
        canvas_w=1080, canvas_h=1920, bg_hex=DARKBROWN,
        bottle_name="乳香", bottle_scale=0.55, bottle_x_frac=0.65, bottle_bottom_frac=0.80,
        shadow_offset_x=48, shadow_offset_y=22, shadow_blur=38, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("沉默的他", FONT_ZH, 80, WARMCREAM, 0.055, 0.130, "tl"),
            ("不擅長熱鬧", FONT_ZH, 40, GOLDYELLOW, 0.055, 0.262, "tl"),
            ("一份木質香 · 剛好懂他", FONT_ZH, 28, GREYBROWN, 0.055, 0.328, "tl"),
        ])
    save_and_dual(WEEK, "Reels", "MORENE_FD_R1_f4.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WARMSAND,
        bottle_name="乳香", bottle_scale=0.54, bottle_x_frac=0.68, bottle_bottom_frac=0.80,
        shadow_offset_x=48, shadow_offset_y=22, shadow_blur=36, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("滴一滴在掌心", FONT_ZH, 72, BLACK, 0.055, 0.130, "tl"),
            ("讓木質香慢慢散開", FONT_ZH, 38, TERRA, 0.055, 0.258, "tl"),
            ("情境使用 · 非療效宣稱", FONT_ZH, 22, GREYBROWN, 0.055, 0.330, "tl"),
        ])
    save_and_dual(WEEK, "Reels", "MORENE_FD_R1_f5.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WARMCREAM,
        bottle_name="乳香", bottle_scale=0.54, bottle_x_frac=0.68, bottle_bottom_frac=0.80,
        shadow_offset_x=46, shadow_offset_y=20, shadow_blur=36, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R1", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("給他的", FONT_ZH, 84, BLACK, 0.055, 0.130, "tl"),
            ("不只是香氣", FONT_ZH, 52, TERRA, 0.055, 0.270, "tl"),
            ("是一段安靜的陪伴", FONT_ZH, 30, GREYBROWN, 0.055, 0.346, "tl"),
        ])
    save_and_dual(WEEK, "Reels", "MORENE_FD_R1_f6.png",
        canvas_w=1080, canvas_h=1920, bg_hex=COCOA,
        bottle_name="乳香", bottle_scale=0.56, bottle_x_frac=0.66, bottle_bottom_frac=0.80,
        shadow_offset_x=50, shadow_offset_y=22, shadow_blur=38, shadow_opacity=0.09,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("送他一份安靜", FONT_ZH, 72, WARMCREAM, 0.055, 0.130, "tl"),
            ("乳香 · 父親節選香", FONT_ZH, 36, GOLDYELLOW, 0.055, 0.252, "tl"),
            ("主頁 MORENE.COM.TW →", FONT_ZH, 24, WARMSAND, 0.055, 0.322, "tl"),
            (FOOTER_NT, FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ])

    # ---------- R2 三支木質樹脂禮物組 ----------
    print("--- R2 木質樹脂禮物組 ---")
    save_and_dual_multi(WEEK, "Reels", "MORENE_FD_R2_f1.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WARMSAND,
        bottle_names=GIFT3, bottle_height_frac=0.27, bottle_bottom_frac=0.74,
        margin_frac=0.10, spacing=24,
        shadow_offset_x=38, shadow_offset_y=18, shadow_blur=30, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R2", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("沉靜香", FONT_ZH, 100, BLACK, 0.055, 0.130, "tl"),
            ("禮物組", FONT_ZH, 76, TERRA, 0.055, 0.286, "tl"),
            ("乳香 · 岩蘭草 · 雪松", FONT_ZH, 28, BLACK, 0.055, 0.806, "tl"),
        ])
    save_and_dual(WEEK, "Reels", "MORENE_FD_R2_f2.png",
        canvas_w=1080, canvas_h=1920, bg_hex=COCOA,
        bottle_name="乳香", bottle_scale=0.56, bottle_x_frac=0.66, bottle_bottom_frac=0.80,
        shadow_offset_x=50, shadow_offset_y=22, shadow_blur=38, shadow_opacity=0.09,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R2 · 01", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("乳香", FONT_ZH, 104, WARMCREAM, 0.055, 0.130, "tl"),
            ("樹脂的溫暖", FONT_ZH, 44, GOLDYELLOW, 0.055, 0.294, "tl"),
            ("Boswellia carterii", FONT_EN, 24, GREYBROWN, 0.055, 0.366, "tl"),
        ])
    save_and_dual(WEEK, "Reels", "MORENE_FD_R2_f3.png",
        canvas_w=1080, canvas_h=1920, bg_hex=EARTHBROWN,
        bottle_name="岩蘭草", bottle_scale=0.56, bottle_x_frac=0.66, bottle_bottom_frac=0.80,
        shadow_offset_x=50, shadow_offset_y=22, shadow_blur=38, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R2 · 02", FONT_EN, 14, WARMSAND, 0.055, 0.092, "tl"),
            ("岩蘭草", FONT_ZH, 96, WARMCREAM, 0.055, 0.130, "tl"),
            ("大地的沉穩", FONT_ZH, 44, GOLDYELLOW, 0.055, 0.272, "tl"),
            ("Chrysopogon zizanioides", FONT_EN, 22, WARMSAND, 0.055, 0.344, "tl"),
        ])
    save_and_dual(WEEK, "Reels", "MORENE_FD_R2_f4.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WOODTAN,
        bottle_name="大西洋雪松", bottle_scale=0.56, bottle_x_frac=0.66, bottle_bottom_frac=0.80,
        shadow_offset_x=50, shadow_offset_y=22, shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R2 · 03", FONT_EN, 14, WARMWHITE, 0.055, 0.092, "tl"),
            ("大西洋雪松", FONT_ZH, 76, WARMCREAM, 0.055, 0.130, "tl"),
            ("乾爽的木質", FONT_ZH, 44, GOLDYELLOW, 0.055, 0.258, "tl"),
            ("Cedrus atlantica", FONT_EN, 24, WARMWHITE, 0.055, 0.330, "tl"),
        ])
    save_and_dual_multi(WEEK, "Reels", "MORENE_FD_R2_f5.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WARMCREAM,
        bottle_names=GIFT3, bottle_height_frac=0.27, bottle_bottom_frac=0.74,
        margin_frac=0.10, spacing=24,
        shadow_offset_x=38, shadow_offset_y=18, shadow_blur=30, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R2", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("樹脂 × 大地 × 木質", FONT_ZH, 50, BLACK, 0.055, 0.130, "tl"),
            ("沉穩三重奏", FONT_ZH, 56, TERRA, 0.055, 0.210, "tl"),
            ("為他配一組沉靜的香", FONT_ZH, 28, GREYBROWN, 0.055, 0.806, "tl"),
        ])
    save_and_dual_multi(WEEK, "Reels", "MORENE_FD_R2_f6.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WARMSAND,
        bottle_names=GIFT3, bottle_height_frac=0.27, bottle_bottom_frac=0.74,
        margin_frac=0.10, spacing=24,
        shadow_offset_x=38, shadow_offset_y=18, shadow_blur=30, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("為他配一組沉靜的香", FONT_ZH, 50, BLACK, 0.055, 0.130, "tl"),
            ("香氣人格測驗 · 主頁玩 →", FONT_ZH, 34, TERRA, 0.055, 0.210, "tl"),
            ("乳香 · 岩蘭草 · 雪松", FONT_ZH, 28, GREYBROWN, 0.055, 0.806, "tl"),
            (FOOTER_NT, FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ])

    # ---------- R3 父親節一份安靜的禮物 (乳香) ----------
    print("--- R3 父親節一份安靜的禮物 ---")
    save_and_dual(WEEK, "Reels", "MORENE_FD_R3_f1.png",
        canvas_w=1080, canvas_h=1920, bg_hex=DARKBROWN,
        bottle_name="乳香", bottle_scale=0.56, bottle_x_frac=0.64, bottle_bottom_frac=0.80,
        shadow_offset_x=50, shadow_offset_y=22, shadow_blur=38, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, WARMSAND, 0.055, 0.092, "tl"),
            ("父親節", FONT_ZH, 104, WARMCREAM, 0.055, 0.130, "tl"),
            ("一份安靜的禮物", FONT_ZH, 50, GOLDYELLOW, 0.055, 0.300, "tl"),
            ("乳香 · 沉靜香氣", FONT_ZH, 28, WARMSAND, 0.055, 0.376, "tl"),
        ])
    save_and_dual(WEEK, "Reels", "MORENE_FD_R3_f2.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WARMWHITE,
        bottle_name="乳香", bottle_scale=0.52, bottle_x_frac=0.68, bottle_bottom_frac=0.80,
        shadow_offset_x=46, shadow_offset_y=20, shadow_blur=36, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("他總是把話", FONT_ZH, 72, BLACK, 0.055, 0.130, "tl"),
            ("放在心裡", FONT_ZH, 72, TERRA, 0.055, 0.244, "tl"),
            ("那就用香氣替你說", FONT_ZH, 30, GREYBROWN, 0.055, 0.366, "tl"),
        ])
    save_and_dual(WEEK, "Reels", "MORENE_FD_R3_f3.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WARMSAND,
        bottle_name="乳香", bottle_scale=0.52, bottle_x_frac=0.68, bottle_bottom_frac=0.80,
        shadow_offset_x=48, shadow_offset_y=22, shadow_blur=36, shadow_opacity=0.13,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("木質 · 樹脂", FONT_ZH, 80, BLACK, 0.055, 0.130, "tl"),
            ("沉穩而溫暖", FONT_ZH, 44, TERRA, 0.055, 0.262, "tl"),
            ("像他給家的感覺", FONT_ZH, 28, GREYBROWN, 0.055, 0.334, "tl"),
        ])
    save_and_dual(WEEK, "Reels", "MORENE_FD_R3_f4.png",
        canvas_w=1080, canvas_h=1920, bg_hex=WARMCREAM,
        bottle_name="乳香", bottle_scale=0.50, bottle_x_frac=0.70, bottle_bottom_frac=0.80,
        shadow_offset_x=46, shadow_offset_y=20, shadow_blur=36, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("包成一份", FONT_ZH, 84, BLACK, 0.055, 0.130, "tl"),
            ("安靜的禮物", FONT_ZH, 56, TERRA, 0.055, 0.270, "tl"),
            ("緞帶 · 手寫卡 · 心意", FONT_ZH, 28, GREYBROWN, 0.055, 0.346, "tl"),
        ])
    save_and_dual(WEEK, "Reels", "MORENE_FD_R3_f5.png",
        canvas_w=1080, canvas_h=1920, bg_hex=COCOA,
        bottle_name="乳香", bottle_scale=0.54, bottle_x_frac=0.66, bottle_bottom_frac=0.80,
        shadow_offset_x=50, shadow_offset_y=22, shadow_blur=38, shadow_opacity=0.09,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("REELS · R3", FONT_EN, 14, GREYBROWN, 0.055, 0.092, "tl"),
            ("謝謝你", FONT_ZH, 96, WARMCREAM, 0.055, 0.130, "tl"),
            ("用沉穩撐起一個家", FONT_ZH, 40, GOLDYELLOW, 0.055, 0.286, "tl"),
            ("父親節快樂", FONT_ZH, 30, WARMSAND, 0.055, 0.354, "tl"),
        ])
    save_and_dual(WEEK, "Reels", "MORENE_FD_R3_f6.png",
        canvas_w=1080, canvas_h=1920, bg_hex=DARKBROWN,
        bottle_name="乳香", bottle_scale=0.56, bottle_x_frac=0.66, bottle_bottom_frac=0.80,
        shadow_offset_x=50, shadow_offset_y=22, shadow_blur=38, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WARMCREAM, 0.055, 0.040, "tl"),
            ("送他一份安靜", FONT_ZH, 72, WARMCREAM, 0.055, 0.130, "tl"),
            ("父親節選香 · 乳香", FONT_ZH, 36, GOLDYELLOW, 0.055, 0.252, "tl"),
            ("主頁 MORENE.COM.TW →", FONT_ZH, 24, WARMSAND, 0.055, 0.322, "tl"),
            (FOOTER_NT, FONT_ZH, 16, GREYBROWN, 0.055, 0.944, "tl"),
        ])

    print("父親節 Reels 完成。")


# =====================================================================
# 完整性驗證 — 命名/數量斷言 (URL 已綁死, 不容差錯)
# =====================================================================
def verify_complete():
    print("\n=== 完整性驗證 ===")
    expected = {
        "Stories": {f"MORENE_FD_S{i:02d}.png" for i in range(1, 17)},
        "IG":      {f"MORENE_FD_IG{i}.png" for i in range(1, 9)},
        "FB":      {f"MORENE_FD_FB{i}.png" for i in range(1, 9)},
        "Reels":   {f"MORENE_FD_R{r}_f{f}.png" for r in (1, 2, 3) for f in range(1, 7)},
    }
    total = 0
    ok = True
    for ch, exp in expected.items():
        d = f"{OUT_BASE}/{WEEK}/{ch}"
        actual = {x for x in os.listdir(d) if x.endswith(".png")}
        missing = exp - actual
        extra = actual - exp
        total += len(exp & actual)
        print(f"  {ch}: expected {len(exp)}, found {len(exp & actual)}"
              + (f" MISSING {sorted(missing)}" if missing else "")
              + (f" EXTRA {sorted(extra)}" if extra else ""))
        if missing:
            ok = False
    print(f"  TOTAL matched: {total} / 50")
    if not ok or total != 50:
        raise SystemExit("[FAIL] 完整性驗證未通過 — 缺檔或命名錯誤")
    print("  [PASS] 50 檔齊全, 命名精確")


if __name__ == "__main__":
    make_ig_fb()
    make_stories()
    make_reels()
    verify_complete()
    print("\n全部完成 ✓")
