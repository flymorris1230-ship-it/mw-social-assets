#!/usr/bin/env python3
"""
MORENE W5 增量圖卡生成腳本 (Wave 5, 7/26–7/31, 高量增量最後一波, 27則)
規格: Stories/Reels 1080×1920; IG 1080×1350; FB 1080×1080
樣式: Y2K 攝影主導 + 單色暖色底 + 真實琥珀瓶 + 極少字
字體: BW Gradual/英 + Noto Sans TC/中 + Outfit/小字
無 ISO/認證標章 | 無療效詞 | 無急迫話術
色票: 全用 MORENE VIS 官方暖色票
立秋 8/7 提前預熱 → 暖橘+深棕強調
"""

import os, sys
sys.path.insert(0, "/Users/morrislin/mw-social-assets/MORENE")
from make_covers_v2 import (
    compose_card,
    FONT_EN_BOLD, FONT_EN, FONT_ZH, FONT_ZH_BOLD,
    CREAM, BLACK, TERRA, WHITE,
    OUT_BASE, hex2rgb, fnt, get_logo, add_contact_shadow, add_directional_shadow,
    crop_to_bottle,
)
from PIL import Image, ImageDraw, ImageFont

# =====================
# VIS 暖色票補充
# =====================
CARAMEL   = "#C9853E"   # 焦糖
MUSTARD   = "#E8CE8C"   # 芥末黃
FOGPINK   = "#E9C5B9"   # 霧粉
WARMSAND  = "#CBA98A"   # 暖沙
FOGBLUE   = "#82A8CC"   # 霧藍
FOGSAGE   = "#8DBFBE"   # 霧藍綠
GRYBROWN  = "#8C8079"   # 灰褐
DARKBROWN = "#2A2520"   # 深暗褐 (廣藿香/可可底)
COCOA     = "#3A2C24"   # 更深可可底
WARMSTONE = "#D1CBC5"   # 柔灰白
AMBER     = "#C9853E"   # 暖橘黃 (佛手柑主色)

# =====================
# 路徑常數
# =====================
BASE_PROD = "/Users/morrislin/Desktop/MORENE/03_MORENE/03_Assets/A009：MORENE-產品相關/01.產品相關/01. 產品資料/05. 產品照片/素材/商品大圖/01_精油"
OUT_W5    = "/Users/morrislin/mw-social-assets/MORENE/W_increment"

# =====================
# W5 瓶身路徑
# =====================
BOTTLES = {
    "佛手柑":     f"{BASE_PROD}/5MOEO003_佛手柑/MORENE_精油瓶_去背_佛手柑.png",
    "大西洋雪松": f"{BASE_PROD}/5MOEO005_大西洋雪松/MORENE_精油瓶_去背_大西洋雪松.png",
    "苦橙葉":     f"{BASE_PROD}/苦橙葉/MORENE_精油瓶_去背_苦橙葉.png",
    "廣藿香":     f"{BASE_PROD}/廣藿香/MORENE_精油瓶_去背_廣藿香.png",
    "甜橙":       f"{BASE_PROD}/甜橙/MORENE_精油瓶_去背_甜橙.png",
    "真正薰衣草": f"{BASE_PROD}/5MOEO015_真正薰衣草/MORENE_精油瓶_去背_真正薰衣草.png",
    "乳香":       f"{BASE_PROD}/5MOEO009_乳香/MORENE_精油瓶_去背_乳香.png",
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

def card(w, h, bg, bottle, bscale, bxf, byf, lines, out, **kwargs):
    _assert_no_tofu(lines)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    return compose_card(w, h, bg, bottle, bscale, bxf, byf, lines, out, **kwargs)

def logo_line(color_hex, xf, yf):
    return ("MORENE", FONT_EN_BOLD, 1, color_hex, xf, yf, "tl")


# =====================
# STORIES ×12  (1080×1920)
# =====================
SW, SH = 1080, 1920

def make_stories():
    os.makedirs(f"{OUT_W5}/Stories", exist_ok=True)

    # S1  7/26 週日清甜vs沉靜投票 — 黃/棕雙色分割(佛手柑+大西洋雪松)
    # 左半 CARAMEL 右半 DARKBROWN — 手工繪製分割背景
    def s1():
        canvas = Image.new("RGB", (SW, SH), hex2rgb(CARAMEL))
        right = Image.new("RGB", (SW // 2, SH), hex2rgb(DARKBROWN))
        canvas.paste(right, (SW // 2, 0))
        # 佛手柑瓶(左)
        b1 = Image.open(BOTTLES["佛手柑"]).convert("RGBA")
        b1 = crop_to_bottle(b1, 60)
        th = int(SH * 0.62)
        b1 = b1.resize((int(b1.width * th / b1.height), th), Image.LANCZOS)
        b1 = add_directional_shadow(b1, shadow_opacity=0.22, offset_x=40, offset_y=20, shadow_blur=35)
        cx1 = int(SW * 0.28) - b1.width // 2
        cy1 = int(SH * 0.82) - b1.height
        canvas.paste(b1.convert("RGB"), (cx1, cy1), b1.split()[3])
        # 大西洋雪松瓶(右)
        b2 = Image.open(BOTTLES["大西洋雪松"]).convert("RGBA")
        b2 = crop_to_bottle(b2, 60)
        b2 = b2.resize((int(b2.width * th / b2.height), th), Image.LANCZOS)
        b2 = add_directional_shadow(b2, shadow_opacity=0.22, offset_x=40, offset_y=20, shadow_blur=35)
        cx2 = int(SW * 0.75) - b2.width // 2
        cy2 = int(SH * 0.82) - b2.height
        canvas.paste(b2.convert("RGB"), (cx2, cy2), b2.split()[3])
        # LOGO
        logo = Image.open(LOGO_CREAM).convert("RGBA")
        lw = 220
        logo = logo.resize((lw, max(1, int(logo.height * lw / logo.width))), Image.LANCZOS)
        canvas.paste(logo.convert("RGB"), (64, 96), logo.split()[3])
        # 文字
        draw = ImageDraw.Draw(canvas)
        _assert_no_tofu([
            ("清甜 vs 沉靜", FONT_ZH_BOLD, 58, CREAM, 0.07, 0.18, "tl"),
            ("你的週日是哪一種?", FONT_ZH, 44, CREAM, 0.07, 0.26, "tl"),
            ("A  佛手柑・清甜晨光", FONT_ZH, 40, MUSTARD, 0.07, 0.52, "tl"),
            ("B  大西洋雪松・沉靜木林", FONT_ZH, 40, CREAM, 0.07, 0.60, "tl"),
            ("留言投票 ↓", FONT_ZH_BOLD, 42, MUSTARD, 0.07, 0.88, "tl"),
        ])
        def draw_text(text, font_path, size, color_hex, xf, yf):
            f = fnt(font_path, size)
            x = int(SW * xf)
            y = int(SH * yf)
            r, g, b = hex2rgb(color_hex)
            draw.text((x, y), text, font=f, fill=(r, g, b))
        draw_text("清甜 vs 沉靜", FONT_ZH_BOLD, 58, CREAM, 0.07, 0.18)
        draw_text("你的週日是哪一種?", FONT_ZH, 44, CREAM, 0.07, 0.26)
        draw_text("A  佛手柑・清甜晨光", FONT_ZH, 40, MUSTARD, 0.07, 0.52)
        draw_text("B  大西洋雪松・沉靜木林", FONT_ZH, 40, CREAM, 0.07, 0.60)
        draw_text("留言投票 ↓", FONT_ZH_BOLD, 42, MUSTARD, 0.07, 0.88)
        out = f"{OUT_W5}/Stories/MORENE_W5inc_S1.png"
        canvas.save(out, "PNG")
        print("S1 done")
    s1()

    # S2  7/26 佛手柑 Reels 預告 — 暖橘底+佛手柑瓶
    card(SW, SH, CARAMEL, "佛手柑", 0.70, 0.58, 0.82, [
        logo_line(CREAM, 0.07, 0.05),
        ("07.26", FONT_EN, 36, CREAM, 0.07, 0.10, "tl"),
        ("Bergamot", FONT_EN_BOLD, 82, CREAM, 0.07, 0.14, "tl"),
        ("佛手柑精油今日上線", FONT_ZH_BOLD, 48, CREAM, 0.07, 0.26, "tl"),
        ("義大利 calabria 產區", FONT_ZH, 38, MUSTARD, 0.07, 0.34, "tl"),
        ("完整介紹 → 點 bio 連結", FONT_ZH_BOLD, 40, MUSTARD, 0.07, 0.88, "tl"),
    ], f"{OUT_W5}/Stories/MORENE_W5inc_S2.png",
    shadow_offset_x=50, shadow_opacity=0.22)
    print("S2 done")

    # S3  7/27 通勤帶精油投票 — 奶油白底+苦橙葉+捷運感小字
    card(SW, SH, CREAM, "苦橙葉", 0.68, 0.60, 0.82, [
        logo_line(BLACK, 0.07, 0.05),
        ("07.27", FONT_EN, 36, TERRA, 0.07, 0.10, "tl"),
        ("Commute Scent", FONT_EN_BOLD, 68, BLACK, 0.07, 0.14, "tl"),
        ("通勤你帶哪支精油?", FONT_ZH_BOLD, 52, BLACK, 0.07, 0.24, "tl"),
        ("A  苦橙葉・清新解壓", FONT_ZH, 42, TERRA, 0.07, 0.52, "tl"),
        ("B  真正薰衣草・平穩安定", FONT_ZH, 42, BLACK, 0.07, 0.61, "tl"),
        ("C  佛手柑・清甜提神", FONT_ZH, 42, GRYBROWN, 0.07, 0.70, "tl"),
        ("留言選你的通勤香 ↓", FONT_ZH, 36, GRYBROWN, 0.07, 0.88, "tl"),
    ], f"{OUT_W5}/Stories/MORENE_W5inc_S3.png")
    print("S3 done")

    # S4  7/27 通勤新文導流 — 暖日光焦糖底+苦橙葉
    card(SW, SH, CARAMEL, "苦橙葉", 0.66, 0.56, 0.80, [
        logo_line(CREAM, 0.07, 0.05),
        ("07.27", FONT_EN, 36, CREAM, 0.07, 0.10, "tl"),
        ("Daily Carry", FONT_EN_BOLD, 72, CREAM, 0.07, 0.14, "tl"),
        ("通勤精油怎麼選?", FONT_ZH_BOLD, 54, CREAM, 0.07, 0.24, "tl"),
        ("苦橙葉・稀釋後輕抹手腕", FONT_ZH, 40, MUSTARD, 0.07, 0.34, "tl"),
        ("感受清新、不刺激旁人", FONT_ZH, 38, CREAM, 0.07, 0.42, "tl"),
        ("完整選油指南 → 點 bio", FONT_ZH_BOLD, 40, MUSTARD, 0.07, 0.88, "tl"),
    ], f"{OUT_W5}/Stories/MORENE_W5inc_S4.png",
    shadow_offset_x=45, shadow_opacity=0.20)
    print("S4 done")

    # S5  7/28 學名產地品牌 — 奶油白底+瓶標學名特寫感
    card(SW, SH, CREAM, "佛手柑", 0.74, 0.62, 0.84, [
        logo_line(BLACK, 0.07, 0.05),
        ("07.28", FONT_EN, 36, TERRA, 0.07, 0.10, "tl"),
        ("Citrus bergamia", FONT_EN_BOLD, 58, TERRA, 0.07, 0.15, "tl"),
        ("學名產地,看得見的透明", FONT_ZH_BOLD, 48, BLACK, 0.07, 0.25, "tl"),
        ("IFA 國際芳療師監製", FONT_ZH, 38, GRYBROWN, 0.07, 0.34, "tl"),
        ("完整 INCI 公開", FONT_ZH, 38, GRYBROWN, 0.07, 0.42, "tl"),
        ("點 bio 查每支精油學名 →", FONT_ZH_BOLD, 36, TERRA, 0.07, 0.88, "tl"),
    ], f"{OUT_W5}/Stories/MORENE_W5inc_S5.png")
    print("S5 done")

    # S6  7/28 買精油最在意投票 — 乾淨白底+大西洋雪松瓶展示
    card(SW, SH, WARMSTONE, "大西洋雪松", 0.70, 0.60, 0.82, [
        logo_line(BLACK, 0.07, 0.05),
        ("07.28", FONT_EN, 36, GRYBROWN, 0.07, 0.10, "tl"),
        ("你買精油最在意什麼?", FONT_ZH_BOLD, 50, BLACK, 0.07, 0.15, "tl"),
        ("A  香氣是否喜歡", FONT_ZH, 42, BLACK, 0.07, 0.50, "tl"),
        ("B  產地與學名透明", FONT_ZH, 42, BLACK, 0.07, 0.59, "tl"),
        ("C  IFA 芳療師認可", FONT_ZH, 42, BLACK, 0.07, 0.68, "tl"),
        ("D  CP 值", FONT_ZH, 42, GRYBROWN, 0.07, 0.77, "tl"),
        ("留言告訴我們 ↓", FONT_ZH, 36, GRYBROWN, 0.07, 0.88, "tl"),
    ], f"{OUT_W5}/Stories/MORENE_W5inc_S6.png")
    print("S6 done")

    # S7  7/29 立秋換季預熱 — 深綠感用深暗褐模擬,葉片文字視覺
    card(SW, SH, DARKBROWN, "乳香", 0.68, 0.60, 0.84, [
        logo_line(CREAM, 0.07, 0.05),
        ("07.29", FONT_EN, 36, FOGPINK, 0.07, 0.10, "tl"),
        ("End of Summer", FONT_EN_BOLD, 70, CREAM, 0.07, 0.15, "tl"),
        ("立秋將至", FONT_ZH_BOLD, 72, MUSTARD, 0.07, 0.26, "tl"),
        ("木質香正要接棒", FONT_ZH, 48, CREAM, 0.07, 0.37, "tl"),
        ("你準備好換香了嗎?", FONT_ZH_BOLD, 44, FOGPINK, 0.07, 0.88, "tl"),
    ], f"{OUT_W5}/Stories/MORENE_W5inc_S7.png",
    shadow_offset_x=40, shadow_opacity=0.18)
    print("S7 done")

    # S8  7/29 入秋換香投票 — 秋色用焦糖漸層感
    card(SW, SH, CARAMEL, "大西洋雪松", 0.72, 0.60, 0.84, [
        logo_line(CREAM, 0.07, 0.05),
        ("07.29", FONT_EN, 36, CREAM, 0.07, 0.10, "tl"),
        ("Autumn Shift", FONT_EN_BOLD, 72, CREAM, 0.07, 0.14, "tl"),
        ("入秋你會換哪類香氣?", FONT_ZH_BOLD, 50, CREAM, 0.07, 0.25, "tl"),
        ("A  木質・沉穩大地", FONT_ZH, 42, MUSTARD, 0.07, 0.52, "tl"),
        ("B  花香・溫柔過渡", FONT_ZH, 42, CREAM, 0.07, 0.61, "tl"),
        ("C  不換・一年到頭柑橘", FONT_ZH, 42, CREAM, 0.07, 0.70, "tl"),
        ("留言投票 ↓", FONT_ZH_BOLD, 40, MUSTARD, 0.07, 0.88, "tl"),
    ], f"{OUT_W5}/Stories/MORENE_W5inc_S8.png",
    shadow_offset_x=50, shadow_opacity=0.22)
    print("S8 done")

    # S9  7/30 廣藿香的人 — 深棕/可可底+廣藿香瓶大圖,極少字
    card(SW, SH, COCOA, "廣藿香", 0.78, 0.58, 0.88, [
        logo_line(CREAM, 0.07, 0.05),
        ("Patchouli", FONT_EN_BOLD, 88, WARMSAND, 0.07, 0.14, "tl"),
        ("懂廣藿香的人", FONT_ZH_BOLD, 58, CREAM, 0.07, 0.28, "tl"),
        ("不需要理由", FONT_ZH, 48, FOGPINK, 0.07, 0.37, "tl"),
    ], f"{OUT_W5}/Stories/MORENE_W5inc_S9.png",
    shadow_offset_x=35, shadow_opacity=0.15)
    print("S9 done")

    # S10  7/30 聞過廣藿香投票 — 熱帶葉感,深底
    card(SW, SH, DARKBROWN, "廣藿香", 0.70, 0.62, 0.82, [
        logo_line(CREAM, 0.07, 0.05),
        ("07.30", FONT_EN, 36, WARMSAND, 0.07, 0.10, "tl"),
        ("你聞過廣藿香嗎?", FONT_ZH_BOLD, 54, CREAM, 0.07, 0.16, "tl"),
        ("A  聞過,意外的喜歡", FONT_ZH, 42, MUSTARD, 0.07, 0.52, "tl"),
        ("B  聞過,太重不接受", FONT_ZH, 42, CREAM, 0.07, 0.61, "tl"),
        ("C  還沒聞過,好奇中", FONT_ZH, 42, FOGPINK, 0.07, 0.70, "tl"),
        ("留言告訴我 ↓", FONT_ZH_BOLD, 40, WARMSAND, 0.07, 0.88, "tl"),
    ], f"{OUT_W5}/Stories/MORENE_W5inc_S10.png",
    shadow_offset_x=40, shadow_opacity=0.18)
    print("S10 done")

    # S11  7/31 送自己什麼新文導流 — 緞帶禮物感,暖白底+甜橙瓶
    card(SW, SH, CREAM, "甜橙", 0.68, 0.60, 0.82, [
        logo_line(BLACK, 0.07, 0.05),
        ("07.31", FONT_EN, 36, TERRA, 0.07, 0.10, "tl"),
        ("Gift Yourself", FONT_EN_BOLD, 72, BLACK, 0.07, 0.14, "tl"),
        ("這個夏天,送自己一瓶好油", FONT_ZH_BOLD, 48, BLACK, 0.07, 0.25, "tl"),
        ("新文上線 → 三瓶入門選油指南", FONT_ZH, 38, GRYBROWN, 0.07, 0.35, "tl"),
        ("點 bio 連結閱讀 →", FONT_ZH_BOLD, 40, TERRA, 0.07, 0.88, "tl"),
    ], f"{OUT_W5}/Stories/MORENE_W5inc_S11.png")
    print("S11 done")

    # S12  7/31 夏天學到新事問答 — 多瓶暖橘底感
    card(SW, SH, CARAMEL, "甜橙", 0.70, 0.60, 0.84, [
        logo_line(CREAM, 0.07, 0.05),
        ("07.31", FONT_EN, 36, CREAM, 0.07, 0.10, "tl"),
        ("Summer Learnings", FONT_EN_BOLD, 64, CREAM, 0.07, 0.14, "tl"),
        ("這個夏天你學到什麼?", FONT_ZH_BOLD, 52, CREAM, 0.07, 0.25, "tl"),
        ("關於香氣・關於自己", FONT_ZH, 42, MUSTARD, 0.07, 0.35, "tl"),
        ("留言分享你的答案 ↓", FONT_ZH_BOLD, 42, MUSTARD, 0.07, 0.88, "tl"),
    ], f"{OUT_W5}/Stories/MORENE_W5inc_S12.png",
    shadow_offset_x=45, shadow_opacity=0.20)
    print("S12 done")


# =====================
# IG ×6  (1080×1350)  + FB ×6  (1080×1080)
# =====================
IW, IH = 1080, 1350
FW, FH = 1080, 1080

def make_ig_fb():
    os.makedirs(f"{OUT_W5}/IG", exist_ok=True)
    os.makedirs(f"{OUT_W5}/FB", exist_ok=True)

    for (w, h, out_dir, prefix, bscale, byf) in [
        (IW, IH, "IG", "IG", 0.70, 0.82),
        (FW, FH, "FB", "FB", 0.65, 0.78),
    ]:
        # IG1/FB1  7/26 佛手柑聚光 — 晨光黃底強投影
        card(w, h, CARAMEL, "佛手柑", bscale, 0.60, byf, [
            logo_line(CREAM, 0.07, 0.05),
            ("Bergamot", FONT_EN_BOLD, 92, CREAM, 0.07, 0.12, "tl"),
            ("義大利 Calabria 產區", FONT_ZH, 38, MUSTARD, 0.07, 0.25, "tl"),
            ("Citrus bergamia", FONT_EN, 32, CREAM, 0.07, 0.31, "tl"),
            ("清甜柑橘・輕盈晨光", FONT_ZH_BOLD, 44, CREAM, 0.07, 0.38, "tl"),
        ], f"{OUT_W5}/{out_dir}/MORENE_W5inc_{prefix}1.png",
        shadow_offset_x=65, shadow_opacity=0.28, shadow_blur=45)
        print(f"{prefix}1 done")

        # IG2/FB2  7/27 通勤苦橙葉輕香 — 極簡奶油白
        card(w, h, CREAM, "苦橙葉", bscale, 0.58, byf, [
            logo_line(BLACK, 0.07, 0.05),
            ("Petitgrain", FONT_EN_BOLD, 92, BLACK, 0.07, 0.12, "tl"),
            ("苦橙葉・通勤輕香首選", FONT_ZH_BOLD, 44, BLACK, 0.07, 0.25, "tl"),
            ("稀釋後抹手腕,清爽不搶", FONT_ZH, 36, GRYBROWN, 0.07, 0.33, "tl"),
            ("Citrus aurantium bigarade", FONT_EN, 28, GRYBROWN, 0.07, 0.39, "tl"),
        ], f"{OUT_W5}/{out_dir}/MORENE_W5inc_{prefix}2.png")
        print(f"{prefix}2 done")

        # IG3/FB3  7/28 品牌信任學名 — 暖石灰白底
        card(w, h, WARMSTONE, "大西洋雪松", bscale, 0.62, byf, [
            logo_line(BLACK, 0.07, 0.05),
            ("Transparency", FONT_EN_BOLD, 80, BLACK, 0.07, 0.12, "tl"),
            ("學名・產地・INCI 全公開", FONT_ZH_BOLD, 44, BLACK, 0.07, 0.24, "tl"),
            ("IFA 國際芳療師監製", FONT_ZH, 36, TERRA, 0.07, 0.33, "tl"),
            ("Cedrus atlantica", FONT_EN, 30, GRYBROWN, 0.07, 0.40, "tl"),
        ], f"{OUT_W5}/{out_dir}/MORENE_W5inc_{prefix}3.png")
        print(f"{prefix}3 done")

        # IG4/FB4  7/29 換季疊加科普 — 柑橘瓶+乳香瓶 暖橘→深棕漸層 (右瓶+左瓶)
        # 兩瓶並排手工合成
        def ig4(w=w, h=h, out_dir=out_dir, prefix=prefix, bscale=bscale, byf=byf):
            from PIL import Image, ImageDraw
            import numpy as np
            # 漸層背景: 頂部 CARAMEL → 底部 DARKBROWN
            canvas = Image.new("RGB", (w, h))
            top = hex2rgb(CARAMEL)
            bot = hex2rgb(DARKBROWN)
            for y in range(h):
                r = int(top[0] + (bot[0] - top[0]) * y / h)
                g = int(top[1] + (bot[1] - top[1]) * y / h)
                b_val = int(top[2] + (bot[2] - top[2]) * y / h)
                for x in range(w):
                    canvas.putpixel((x, y), (r, g, b_val))
            # 甜橙瓶(左)
            b1 = Image.open(BOTTLES["甜橙"]).convert("RGBA")
            b1 = crop_to_bottle(b1, 60)
            th = int(h * bscale)
            b1 = b1.resize((int(b1.width * th / b1.height), th), Image.LANCZOS)
            b1 = add_directional_shadow(b1, shadow_opacity=0.22, offset_x=40, offset_y=20, shadow_blur=35)
            x1 = int(w * 0.28) - b1.width // 2
            y1 = int(h * byf) - b1.height
            canvas.paste(b1.convert("RGB"), (x1, y1), b1.split()[3])
            # 乳香瓶(右)
            b2 = Image.open(BOTTLES["乳香"]).convert("RGBA")
            b2 = crop_to_bottle(b2, 60)
            b2 = b2.resize((int(b2.width * th / b2.height), th), Image.LANCZOS)
            b2 = add_directional_shadow(b2, shadow_opacity=0.22, offset_x=40, offset_y=20, shadow_blur=35)
            x2 = int(w * 0.72) - b2.width // 2
            y2 = int(h * byf) - b2.height
            canvas.paste(b2.convert("RGB"), (x2, y2), b2.split()[3])
            # LOGO
            logo = Image.open(LOGO_CREAM).convert("RGBA")
            lw = 200
            logo = logo.resize((lw, max(1, int(logo.height * lw / logo.width))), Image.LANCZOS)
            canvas.paste(logo.convert("RGB"), (64, 60), logo.split()[3])
            # 文字
            draw = ImageDraw.Draw(canvas)
            lines = [
                ("Season Shift", FONT_EN_BOLD, 72, CREAM, 0.07, 0.12),
                ("換季香氣疊加法", FONT_ZH_BOLD, 46, CREAM, 0.07, 0.23),
                ("柑橘 + 木質 = 過渡期最佳解", FONT_ZH, 36, MUSTARD, 0.07, 0.32),
                ("甜橙・乳香 各取所長", FONT_ZH, 34, CREAM, 0.07, 0.39),
            ]
            _assert_no_tofu([(t, f, sz, c, x, y) for t, f, sz, c, x, y in lines])
            for text, font_path, size, color_hex, xf, yf in lines:
                f = fnt(font_path, size)
                x = int(w * xf)
                y = int(h * yf)
                r, g, b = hex2rgb(color_hex)
                draw.text((x, y), text, font=f, fill=(r, g, b))
            out = f"{OUT_W5}/{out_dir}/MORENE_W5inc_{prefix}4.png"
            canvas.save(out, "PNG")
            print(f"{prefix}4 done")
        ig4()

        # IG5/FB5  7/30 廣藿香聚光 — 深棕/可可暗底強投影
        card(w, h, COCOA, "廣藿香", bscale + 0.02, 0.60, byf, [
            logo_line(CREAM, 0.07, 0.05),
            ("Patchouli", FONT_EN_BOLD, 92, WARMSAND, 0.07, 0.12, "tl"),
            ("Pogostemon cablin", FONT_EN, 30, FOGPINK, 0.07, 0.24, "tl"),
            ("大地・木質・神秘", FONT_ZH_BOLD, 48, CREAM, 0.07, 0.30, "tl"),
            ("你準備好了嗎?", FONT_ZH, 38, FOGPINK, 0.07, 0.38, "tl"),
        ], f"{OUT_W5}/{out_dir}/MORENE_W5inc_{prefix}5.png",
        shadow_offset_x=60, shadow_opacity=0.25, shadow_blur=48)
        print(f"{prefix}5 done")

        # IG6/FB6  7/31 送自己三瓶入門 — 三瓶並排暖白
        def ig6(w=w, h=h, out_dir=out_dir, prefix=prefix, bscale=bscale, byf=byf):
            canvas = Image.new("RGB", (w, h), hex2rgb(CREAM))
            oils = ["甜橙", "真正薰衣草", "大西洋雪松"]
            xfracs = [0.22, 0.52, 0.80]
            th = int(h * (bscale - 0.05))
            for oil, xf in zip(oils, xfracs):
                b = Image.open(BOTTLES[oil]).convert("RGBA")
                b = crop_to_bottle(b, 60)
                b = b.resize((int(b.width * th / b.height), th), Image.LANCZOS)
                b = add_directional_shadow(b, shadow_opacity=0.18, offset_x=30, offset_y=15, shadow_blur=30)
                x = int(w * xf) - b.width // 2
                y = int(h * byf) - b.height
                canvas.paste(b.convert("RGB"), (x, y), b.split()[3])
            logo = Image.open(LOGO_BLACK).convert("RGBA")
            lw = 200
            logo = logo.resize((lw, max(1, int(logo.height * lw / logo.width))), Image.LANCZOS)
            canvas.paste(logo.convert("RGB"), (64, 60), logo.split()[3])
            draw = ImageDraw.Draw(canvas)
            lines = [
                ("Gift Yourself", FONT_EN_BOLD, 72, BLACK, 0.07, 0.09),
                ("送自己第一套精油", FONT_ZH_BOLD, 50, BLACK, 0.07, 0.20),
                ("甜橙・真正薰衣草・大西洋雪松", FONT_ZH, 36, TERRA, 0.07, 0.30),
                ("三種個性,三種生活儀式", FONT_ZH, 34, GRYBROWN, 0.07, 0.37),
            ]
            _assert_no_tofu([(t, f, sz, c, x, y) for t, f, sz, c, x, y in lines])
            for text, font_path, size, color_hex, xf, yf in lines:
                f = fnt(font_path, size)
                x = int(w * xf)
                y = int(h * yf)
                r, g, b = hex2rgb(color_hex)
                draw.text((x, y), text, font=f, fill=(r, g, b))
            out = f"{OUT_W5}/{out_dir}/MORENE_W5inc_{prefix}6.png"
            canvas.save(out, "PNG")
            print(f"{prefix}6 done")
        ig6()


# =====================
# REELS 分鏡 ×3  各6幀  (1080×1920)
# =====================
RW, RH = 1080, 1920

def make_reels():
    os.makedirs(f"{OUT_W5}/Reels", exist_ok=True)

    # --- R1  7/26 佛手柑 ---
    # f1: 封面 — CARAMEL底+佛手柑大瓶
    card(RW, RH, CARAMEL, "佛手柑", 0.74, 0.60, 0.84, [
        logo_line(CREAM, 0.07, 0.05),
        ("Bergamot", FONT_EN_BOLD, 100, CREAM, 0.07, 0.12, "tl"),
        ("佛手柑精油完整介紹", FONT_ZH_BOLD, 52, CREAM, 0.07, 0.26, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R1_f1.png",
    shadow_offset_x=60, shadow_opacity=0.25, shadow_blur=45)
    print("R1f1 done")

    # f2: 義大利產地 — 暖石灰白底,學名顯示
    card(RW, RH, WARMSTONE, "佛手柑", 0.66, 0.58, 0.80, [
        logo_line(BLACK, 0.07, 0.05),
        ("Origin", FONT_EN_BOLD, 88, BLACK, 0.07, 0.12, "tl"),
        ("義大利 Calabria", FONT_ZH_BOLD, 56, BLACK, 0.07, 0.24, "tl"),
        ("Citrus bergamia Risso", FONT_EN, 36, TERRA, 0.07, 0.34, "tl"),
        ("冷壓榨取・果皮來源", FONT_ZH, 40, GRYBROWN, 0.07, 0.42, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R1_f2.png")
    print("R1f2 done")

    # f3: 開瓶 — 深暗褐底+佛手柑大圖,情境感
    card(RW, RH, DARKBROWN, "佛手柑", 0.72, 0.60, 0.86, [
        logo_line(CREAM, 0.07, 0.05),
        ("Open the Bottle", FONT_EN_BOLD, 72, CREAM, 0.07, 0.12, "tl"),
        ("輕輕旋開瓶蓋", FONT_ZH_BOLD, 54, CREAM, 0.07, 0.24, "tl"),
        ("帶入一個晴天早晨的空氣", FONT_ZH, 40, MUSTARD, 0.07, 0.33, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R1_f3.png",
    shadow_offset_x=50, shadow_opacity=0.18)
    print("R1f3 done")

    # f4: 光敏使用提示字卡 — 奶油白底,中文為主(tofu 高風險幀)
    card(RW, RH, CREAM, "佛手柑", 0.58, 0.60, 0.84, [
        logo_line(BLACK, 0.07, 0.05),
        ("Photosensitivity Note", FONT_EN_BOLD, 58, TERRA, 0.07, 0.12, "tl"),
        ("光敏注意事項", FONT_ZH_BOLD, 64, BLACK, 0.07, 0.22, "tl"),
        ("佛手柑含呋喃香豆素", FONT_ZH, 44, BLACK, 0.07, 0.34, "tl"),
        ("塗抹皮膚後 12 小時", FONT_ZH, 44, BLACK, 0.07, 0.42, "tl"),
        ("請避免日曬或使用防曬", FONT_ZH_BOLD, 44, TERRA, 0.07, 0.50, "tl"),
        ("擴香/室內使用無此限制", FONT_ZH, 38, GRYBROWN, 0.07, 0.60, "tl"),
        ("稀釋比例請參考包裝說明", FONT_ZH, 36, GRYBROWN, 0.07, 0.67, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R1_f4.png")
    print("R1f4 done")

    # f5: 搭配 — 焦糖底,佛手柑+大西洋雪松搭配
    card(RW, RH, CARAMEL, "大西洋雪松", 0.68, 0.60, 0.84, [
        logo_line(CREAM, 0.07, 0.05),
        ("Blend", FONT_EN_BOLD, 100, CREAM, 0.07, 0.12, "tl"),
        ("搭配推薦", FONT_ZH_BOLD, 58, CREAM, 0.07, 0.25, "tl"),
        ("佛手柑 + 大西洋雪松", FONT_ZH, 44, MUSTARD, 0.07, 0.35, "tl"),
        ("清甜木質・早晨儀式感", FONT_ZH, 40, CREAM, 0.07, 0.44, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R1_f5.png",
    shadow_offset_x=45, shadow_opacity=0.20)
    print("R1f5 done")

    # f6: CTA 測驗 — 深暗褐底
    card(RW, RH, DARKBROWN, "佛手柑", 0.65, 0.62, 0.86, [
        logo_line(CREAM, 0.07, 0.05),
        ("你是哪種香氣人格?", FONT_ZH_BOLD, 54, CREAM, 0.07, 0.14, "tl"),
        ("16 型香氣人格測驗", FONT_ZH, 44, FOGPINK, 0.07, 0.24, "tl"),
        ("點 bio 連結立即測驗 →", FONT_ZH_BOLD, 44, MUSTARD, 0.07, 0.88, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R1_f6.png",
    shadow_offset_x=38, shadow_opacity=0.16)
    print("R1f6 done")

    # --- R2  7/29 換季 ---
    # f1: 封面 — 焦糖底+甜橙
    card(RW, RH, CARAMEL, "甜橙", 0.74, 0.60, 0.84, [
        logo_line(CREAM, 0.07, 0.05),
        ("Season Shift", FONT_EN_BOLD, 88, CREAM, 0.07, 0.12, "tl"),
        ("換季換香的那一刻", FONT_ZH_BOLD, 52, CREAM, 0.07, 0.26, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R2_f1.png",
    shadow_offset_x=60, shadow_opacity=0.24)
    print("R2f1 done")

    # f2: 夏柑橘 — 晨光黃底
    card(RW, RH, MUSTARD, "甜橙", 0.70, 0.60, 0.84, [
        logo_line(BLACK, 0.07, 0.05),
        ("Summer", FONT_EN_BOLD, 96, BLACK, 0.07, 0.12, "tl"),
        ("夏天的柑橘香", FONT_ZH_BOLD, 58, BLACK, 0.07, 0.24, "tl"),
        ("甜橙・佛手柑・苦橙葉", FONT_ZH, 42, TERRA, 0.07, 0.34, "tl"),
        ("輕盈・活力・晨光感", FONT_ZH, 38, BLACK, 0.07, 0.43, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R2_f2.png",
    shadow_offset_x=50, shadow_opacity=0.15)
    print("R2f2 done")

    # f3: 入秋木質 — 深暗褐底+大西洋雪松
    card(RW, RH, DARKBROWN, "大西洋雪松", 0.72, 0.60, 0.85, [
        logo_line(CREAM, 0.07, 0.05),
        ("Autumn", FONT_EN_BOLD, 96, WARMSAND, 0.07, 0.12, "tl"),
        ("入秋的木質沉穩", FONT_ZH_BOLD, 58, CREAM, 0.07, 0.24, "tl"),
        ("大西洋雪松・乳香・廣藿香", FONT_ZH, 40, FOGPINK, 0.07, 0.34, "tl"),
        ("大地・收斂・定神", FONT_ZH, 38, CREAM, 0.07, 0.43, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R2_f3.png",
    shadow_offset_x=45, shadow_opacity=0.18)
    print("R2f3 done")

    # f4: 花系過渡 — 霧粉底+真正薰衣草
    card(RW, RH, FOGPINK, "真正薰衣草", 0.70, 0.60, 0.84, [
        logo_line(BLACK, 0.07, 0.05),
        ("Transition", FONT_EN_BOLD, 80, BLACK, 0.07, 0.12, "tl"),
        ("花香作為過渡橋樑", FONT_ZH_BOLD, 52, BLACK, 0.07, 0.24, "tl"),
        ("真正薰衣草・玫瑰天竺葵", FONT_ZH, 40, DARKBROWN, 0.07, 0.34, "tl"),
        ("柔和連接兩個季節", FONT_ZH, 38, GRYBROWN, 0.07, 0.43, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R2_f4.png",
    shadow_offset_x=40, shadow_opacity=0.16)
    print("R2f4 done")

    # f5: 換季配方 — 暖沙底+甜橙+乳香
    card(RW, RH, WARMSAND, "乳香", 0.68, 0.60, 0.84, [
        logo_line(BLACK, 0.07, 0.05),
        ("Blend Formula", FONT_EN_BOLD, 68, BLACK, 0.07, 0.12, "tl"),
        ("換季配方推薦", FONT_ZH_BOLD, 56, BLACK, 0.07, 0.22, "tl"),
        ("甜橙 3 滴 + 乳香 2 滴", FONT_ZH, 42, TERRA, 0.07, 0.33, "tl"),
        ("大西洋雪松 2 滴", FONT_ZH, 42, TERRA, 0.07, 0.42, "tl"),
        ("擴香使用・無需稀釋", FONT_ZH, 36, DARKBROWN, 0.07, 0.51, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R2_f5.png",
    shadow_offset_x=40, shadow_opacity=0.18)
    print("R2f5 done")

    # f6: CTA 測驗 — 深暗褐底
    card(RW, RH, DARKBROWN, "大西洋雪松", 0.65, 0.62, 0.86, [
        logo_line(CREAM, 0.07, 0.05),
        ("你的秋天香氣人格", FONT_ZH_BOLD, 52, CREAM, 0.07, 0.14, "tl"),
        ("等你來發現", FONT_ZH, 44, MUSTARD, 0.07, 0.23, "tl"),
        ("16 型香氣人格測驗 →", FONT_ZH_BOLD, 44, MUSTARD, 0.07, 0.88, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R2_f6.png",
    shadow_offset_x=38, shadow_opacity=0.16)
    print("R2f6 done")

    # --- R3  7/31 送自己第一瓶 ---
    # f1: 封面 — 奶油白底+甜橙
    card(RW, RH, CREAM, "甜橙", 0.74, 0.60, 0.84, [
        logo_line(BLACK, 0.07, 0.05),
        ("Your First Bottle", FONT_EN_BOLD, 72, BLACK, 0.07, 0.12, "tl"),
        ("送自己第一瓶精油", FONT_ZH_BOLD, 54, BLACK, 0.07, 0.26, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R3_f1.png")
    print("R3f1 done")

    # f2: 甜橙介紹 — 焦糖底
    card(RW, RH, CARAMEL, "甜橙", 0.70, 0.60, 0.84, [
        logo_line(CREAM, 0.07, 0.05),
        ("Sweet Orange", FONT_EN_BOLD, 80, CREAM, 0.07, 0.12, "tl"),
        ("甜橙・第一瓶選它", FONT_ZH_BOLD, 54, CREAM, 0.07, 0.24, "tl"),
        ("Citrus sinensis", FONT_EN, 32, MUSTARD, 0.07, 0.34, "tl"),
        ("擴香最友善・人人喜歡的柑橘", FONT_ZH, 38, CREAM, 0.07, 0.41, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R3_f2.png",
    shadow_offset_x=50, shadow_opacity=0.22)
    print("R3f2 done")

    # f3: 真正薰衣草 — 霧粉底
    card(RW, RH, FOGPINK, "真正薰衣草", 0.70, 0.60, 0.84, [
        logo_line(BLACK, 0.07, 0.05),
        ("True Lavender", FONT_EN_BOLD, 72, BLACK, 0.07, 0.12, "tl"),
        ("真正薰衣草・最多用途", FONT_ZH_BOLD, 52, BLACK, 0.07, 0.24, "tl"),
        ("Lavandula angustifolia", FONT_EN, 30, TERRA, 0.07, 0.34, "tl"),
        ("稀釋後可多種儀式場景使用", FONT_ZH, 38, DARKBROWN, 0.07, 0.41, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R3_f3.png",
    shadow_offset_x=40, shadow_opacity=0.16)
    print("R3f3 done")

    # f4: 大西洋雪松 — 暖石灰白底
    card(RW, RH, WARMSTONE, "大西洋雪松", 0.70, 0.60, 0.84, [
        logo_line(BLACK, 0.07, 0.05),
        ("Atlantic Cedar", FONT_EN_BOLD, 72, BLACK, 0.07, 0.12, "tl"),
        ("大西洋雪松・沉穩錨定", FONT_ZH_BOLD, 52, BLACK, 0.07, 0.24, "tl"),
        ("Cedrus atlantica", FONT_EN, 30, TERRA, 0.07, 0.34, "tl"),
        ("木質大地・給新手最踏實的感受", FONT_ZH, 36, GRYBROWN, 0.07, 0.42, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R3_f4.png")
    print("R3f4 done")

    # f5: 第一瓶不需完美 — 深暗褐底,文學金句
    card(RW, RH, DARKBROWN, "真正薰衣草", 0.64, 0.62, 0.88, [
        logo_line(CREAM, 0.07, 0.05),
        ("第一瓶不需要完美", FONT_ZH_BOLD, 58, CREAM, 0.07, 0.14, "tl"),
        ("只要是你打開的那瓶", FONT_ZH, 46, FOGPINK, 0.07, 0.25, "tl"),
        ("就是對的開始", FONT_ZH_BOLD, 52, MUSTARD, 0.07, 0.34, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R3_f5.png",
    shadow_offset_x=35, shadow_opacity=0.14)
    print("R3f5 done")

    # f6: CTA 選油指南 — 焦糖底
    card(RW, RH, CARAMEL, "甜橙", 0.65, 0.62, 0.86, [
        logo_line(CREAM, 0.07, 0.05),
        ("找你的第一瓶", FONT_ZH_BOLD, 58, CREAM, 0.07, 0.14, "tl"),
        ("點 bio 連結", FONT_ZH, 48, CREAM, 0.07, 0.24, "tl"),
        ("選油指南完整版 →", FONT_ZH_BOLD, 48, MUSTARD, 0.07, 0.88, "tl"),
    ], f"{OUT_W5}/Reels/MORENE_W5inc_R3_f6.png",
    shadow_offset_x=50, shadow_opacity=0.20)
    print("R3f6 done")


# =====================
# 主程式 — 分批執行
# =====================
if __name__ == "__main__":
    import sys
    batch = sys.argv[1] if len(sys.argv) > 1 else "all"

    if batch in ("stories", "all"):
        print("=== BATCH 1: Stories ===")
        make_stories()
    if batch in ("ig_fb", "all"):
        print("=== BATCH 2: IG + FB ===")
        make_ig_fb()
    if batch in ("reels", "all"):
        print("=== BATCH 3: Reels ===")
        make_reels()

    print("=== W5 complete ===")
