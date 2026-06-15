#!/usr/bin/env python3
"""
MORENE W27-W30 封面重做 v2 — live feed Y2K 攝影版 v3
策略: 去背 PNG 瓶身 → 加接觸影子 → 合成到飽和色底 → 最小文字
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# =====================
# 路徑常數
# =====================
BASE_PROD = "/Users/morrislin/Desktop/MORENE/03_MORENE/03_Assets/A009：MORENE-產品相關/01.產品相關/01. 產品資料/05. 產品照片/素材/商品大圖/01_精油"
OUT_BASE = "/Users/morrislin/mw-social-assets/MORENE"

# =====================
# 字體
# =====================
FONT_EN_BOLD = "/System/Library/Fonts/Futura.ttc"
FONT_EN      = "/System/Library/Fonts/HelveticaNeue.ttc"
FONT_ZH      = "/System/Library/Fonts/STHeiti Medium.ttc"

def fnt(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.truetype(FONT_EN, size)

# =====================
# 色彩工具
# =====================
def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# =====================
# 色票
# =====================
CREAM   = "#EDE7DC"
BLACK   = "#1A1714"
TERRA   = "#A85539"    # 陶土粉
MUSTARD = "#D9B93A"    # 芥末黃(飽和,接近 feed)
SAGE    = "#8DBFBE"
ORANGE  = "#E8622A"    # 飽和橘(feed 色)
GREEN   = "#3A7D44"    # 草綠(feed 色)
LEMON   = "#E2C93A"    # 檸檬黃
WHITE   = "#FFFFFF"

# =====================
# 瓶身路徑
# =====================
def get_bottle(name):
    paths = {
        "玫瑰天竺葵": f"{BASE_PROD}/5MOEO025_玫瑰天竺葵/MORENE_精油瓶_去背_玫瑰天竺葵.png",
        "伊蘭":       f"{BASE_PROD}/伊蘭/MORENE_精油瓶_去背_伊蘭.png",
        "乳香":       f"{BASE_PROD}/5MOEO009_乳香/MORENE_精油瓶_去背_乳香.png",
        "甜橙":       f"{BASE_PROD}/甜橙/MORENE_精油瓶_去背_甜橙.png",
        "苦橙葉":     f"{BASE_PROD}/苦橙葉/MORENE_精油瓶_去背_苦橙葉.png",
    }
    return paths.get(name)

# =====================
# 影子合成
# =====================
def add_contact_shadow(bottle_rgba, bg_rgb, shadow_blur=28, shadow_opacity=0.45, offset_x=18, offset_y=12):
    """
    在去背瓶身下方加接觸影子(橢圓漸層)。
    回傳: 合成後含影子的 RGBA Image(尺寸同 bottle_rgba)
    """
    w, h = bottle_rgba.size
    shadow_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_layer)

    # 取瓶子 alpha,找底部輪廓 x 範圍
    arr = np.array(bottle_rgba)
    alpha = arr[:, :, 3]
    # 找有像素的底部幾列
    col_mask = alpha > 30
    if col_mask.any():
        rows = np.where(col_mask.any(axis=1))[0]
        cols = np.where(col_mask.any(axis=0))[0]
        bot_row = rows[-1]
        left_col = cols[0]
        right_col = cols[-1]
        cx = (left_col + right_col) // 2
        half_w = (right_col - left_col) * 0.45
        ell_h = max(20, int(half_w * 0.22))
        # 接觸影子橢圓
        ey = bot_row + offset_y
        ex = cx + offset_x
        for i in range(shadow_blur):
            ratio = (shadow_blur - i) / shadow_blur
            op = int(shadow_opacity * 255 * ratio * ratio)
            sdraw.ellipse([
                ex - half_w * (1 + i*0.04),
                ey - ell_h * (1 + i*0.04),
                ex + half_w * (1 + i*0.04),
                ey + ell_h * (1 + i*0.04),
            ], fill=(0, 0, 0, op))

    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(shadow_blur // 2))

    # 合成: shadow 先,瓶子上
    result = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    result = Image.alpha_composite(result, shadow_layer)
    result = Image.alpha_composite(result, bottle_rgba)
    return result

def add_directional_shadow(bottle_rgba, direction='right', shadow_blur=35,
                           shadow_opacity=0.30, offset_x=60, offset_y=30):
    """
    方向性陰影(偏右下,模擬 live feed 棚拍光源)
    """
    w, h = bottle_rgba.size
    # 偏移瓶子 alpha 當影子
    offset_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    # 取瓶子 alpha 通道
    r, g, b, a = bottle_rgba.split()
    shadow_color = Image.new('RGB', (w, h), (0, 0, 0))
    shadow_alpha = a.point(lambda x: int(x * shadow_opacity))
    shadow_mask = Image.merge('RGBA', [shadow_color.split()[0], shadow_color.split()[1],
                                        shadow_color.split()[2], shadow_alpha])
    # 貼到偏移位置
    offset_img.paste(shadow_mask, (offset_x, offset_y), shadow_mask)
    offset_img = offset_img.filter(ImageFilter.GaussianBlur(shadow_blur))

    result = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    result = Image.alpha_composite(result, offset_img)
    result = Image.alpha_composite(result, bottle_rgba)
    return result

# =====================
# 核心合成函式
# =====================
def crop_to_bottle(img_rgba, padding=40):
    """裁切 RGBA PNG 到實際瓶身邊界框 + padding"""
    import numpy as np
    a = np.array(img_rgba.split()[3])
    rows = np.where((a > 20).any(axis=1))[0]
    cols = np.where((a > 20).any(axis=0))[0]
    if len(rows) == 0 or len(cols) == 0:
        return img_rgba
    r0 = max(0, rows[0] - padding)
    r1 = min(img_rgba.height, rows[-1] + padding)
    c0 = max(0, cols[0] - padding)
    c1 = min(img_rgba.width, cols[-1] + padding)
    return img_rgba.crop((c0, r0, c1, r1))

def compose_card(
    canvas_w, canvas_h,
    bg_hex,
    bottle_name,
    bottle_scale,       # 瓶子本體高度佔 canvas_h 的比例
    bottle_x_frac,      # 瓶子中心 x (0-1)
    bottle_bottom_frac, # 瓶子底部 y (0-1)
    text_lines,         # [(text, fpath, size, color_hex, x_frac, y_frac, anchor)]
    out_path,
    shadow_offset_x=55, shadow_offset_y=25,
    shadow_blur=40, shadow_opacity=0.28,
):
    bg_rgb = hex2rgb(bg_hex)
    canvas = Image.new('RGB', (canvas_w, canvas_h), bg_rgb)

    # 瓶子
    src_path = get_bottle(bottle_name)
    if src_path and os.path.exists(src_path):
        bottle_img = Image.open(src_path).convert('RGBA')
        # 裁切到實際瓶身
        bottle_img = crop_to_bottle(bottle_img, padding=60)
        bw, bh = bottle_img.size
        target_h = int(canvas_h * bottle_scale)
        target_w = int(bw * target_h / bh)
        bottle_img = bottle_img.resize((target_w, target_h), Image.LANCZOS)

        # 加方向性影子
        bottle_with_shadow = add_directional_shadow(
            bottle_img,
            shadow_opacity=shadow_opacity,
            offset_x=shadow_offset_x,
            offset_y=shadow_offset_y,
            shadow_blur=shadow_blur,
        )
        # 還需要一個接觸影子
        bottle_with_shadow = add_contact_shadow(
            bottle_with_shadow,
            bg_rgb,
            shadow_blur=22, shadow_opacity=0.35,
            offset_x=shadow_offset_x // 2, offset_y=8,
        )

        # 位置計算
        # bottle_with_shadow 高度 = target_h(瓶身) + shadow_offset_y + blur padding
        # 我們要「瓶身本體視覺底部」= canvas_h * bottom_frac
        # bottle_with_shadow 的 y 偏移中,瓶身本體從頂部開始(影子在右下方向偏移,不加高頂部)
        # 所以 bottle 圖像底部 = by + target_h (近似);含影子但影子在右下 offset
        # 直接用: by = bottom_y - target_h,讓瓶身底部對齊
        bottom_y = int(canvas_h * bottle_bottom_frac)
        bx = int(canvas_w * bottle_x_frac) - bottle_with_shadow.width // 2
        by = bottom_y - target_h  # 瓶身本體底部對齊 bottom_y

        # 轉 RGB 貼合(把影子混入背景)
        bg_layer = Image.new('RGBA', (canvas_w, canvas_h), bg_rgb + (255,))
        paste_temp = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
        paste_temp.paste(bottle_with_shadow, (bx, by), bottle_with_shadow)
        combined = Image.alpha_composite(bg_layer, paste_temp).convert('RGB')
        canvas = combined
    else:
        print(f"  WARNING: bottle not found: {src_path}")

    # 文字
    draw = ImageDraw.Draw(canvas)
    anchor_map = {
        'tl': 'la', 'tc': 'ma', 'tr': 'ra',
        'ml': 'lm', 'mc': 'mm', 'mr': 'rm',
        'bl': 'ld', 'bc': 'md', 'br': 'rd',
    }
    for (text, fpath, fsize, color_hex, xf, yf, anc) in text_lines:
        f = fnt(fpath, fsize)
        color = hex2rgb(color_hex)
        px = int(canvas_w * xf)
        py = int(canvas_h * yf)
        a = anchor_map.get(anc, 'la')
        draw.text((px, py), text, font=f, fill=color, anchor=a)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    canvas.save(out_path, 'PNG', optimize=True)
    print(f"  saved: {out_path}")
    return out_path

def compose_multi_bottle(
    canvas_w, canvas_h,
    bg_hex,
    bottle_names,       # list of names
    bottle_height_frac, # 每支瓶高佔 canvas_h 比例
    bottle_bottom_frac,
    text_lines,
    out_path,
    margin_frac=0.05,
    spacing=22,
    shadow_offset_x=35, shadow_offset_y=18,
    shadow_blur=30, shadow_opacity=0.22,
):
    bg_rgb = hex2rgb(bg_hex)
    canvas = Image.new('RGBA', (canvas_w, canvas_h), bg_rgb + (255,))

    n = len(bottle_names)
    margin = int(canvas_w * margin_frac)
    avail_w = canvas_w - 2 * margin - (n - 1) * spacing
    slot_w = avail_w // n
    target_h = int(canvas_h * bottle_height_frac)
    bottle_bottom_y = int(canvas_h * bottle_bottom_frac)

    for i, name in enumerate(bottle_names):
        src = get_bottle(name)
        if not src or not os.path.exists(src):
            print(f"  WARNING: no bottle {name}")
            continue
        bottle_img = Image.open(src).convert('RGBA')
        bottle_img = crop_to_bottle(bottle_img, padding=50)
        bw, bh = bottle_img.size
        target_w = int(bw * target_h / bh)
        bottle_img = bottle_img.resize((target_w, target_h), Image.LANCZOS)

        # 影子
        b_sh = add_directional_shadow(
            bottle_img, shadow_opacity=shadow_opacity,
            offset_x=shadow_offset_x, offset_y=shadow_offset_y,
            shadow_blur=shadow_blur,
        )
        b_sh = add_contact_shadow(
            b_sh, bg_rgb,
            shadow_blur=16, shadow_opacity=0.28,
            offset_x=shadow_offset_x // 2, offset_y=6,
        )

        slot_x = margin + i * (slot_w + spacing)
        cx = slot_x + slot_w // 2
        bx = cx - b_sh.width // 2
        by = bottle_bottom_y - b_sh.height

        canvas.paste(b_sh, (bx, by), b_sh)

    canvas = canvas.convert('RGB')
    draw = ImageDraw.Draw(canvas)
    anchor_map = {
        'tl': 'la', 'tc': 'ma', 'tr': 'ra',
        'ml': 'lm', 'mc': 'mm', 'mr': 'rm',
        'bl': 'ld', 'bc': 'md', 'br': 'rd',
    }
    for (text, fpath, fsize, color_hex, xf, yf, anc) in text_lines:
        f = fnt(fpath, fsize)
        color = hex2rgb(color_hex)
        px = int(canvas_w * xf)
        py = int(canvas_h * yf)
        a = anchor_map.get(anc, 'la')
        draw.text((px, py), text, font=f, fill=color, anchor=a)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    canvas.save(out_path, 'PNG', optimize=True)
    print(f"  saved: {out_path}")
    return out_path


# =====================
# 所有封面
# =====================
def make_all():

    # bottle_scale 現在是「瓶身本體高度 / canvas_h」(裁切後)

    # --- W29 INFP 玫瑰天竺葵 陶土 1080x1350 ---
    print("W29 INFP...")
    compose_card(
        canvas_w=1080, canvas_h=1350,
        bg_hex=TERRA,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.73,    # 瓶身佔畫面 73%
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.92,
        shadow_offset_x=70, shadow_offset_y=30,
        shadow_blur=50, shadow_opacity=0.22,
        out_path=f"{OUT_BASE}/W29/IG/MORENE_W29_INFP.png",
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            ("INFP", FONT_EN_BOLD, 130, CREAM, 0.055, 0.095, "tl"),
            ("未完成的詩", FONT_ZH, 44, CREAM, 0.055, 0.263, "tl"),
            ("「我棲居於可能──", FONT_ZH, 21, CREAM, 0.055, 0.330, "tl"),
            ("  一座比散文更美的屋宇」", FONT_ZH, 21, CREAM, 0.055, 0.362, "tl"),
            ("— Emily Dickinson, Poem 466", FONT_EN, 17, CREAM, 0.055, 0.396, "tl"),
            ("ROSE GERANIUM · SCENT PERSONALITY", FONT_EN, 19, CREAM, 0.055, 0.946, "tl"),
        ],
    )

    # --- W29 ENFP 伊蘭 橘 1080x1350 ---
    print("W29 ENFP...")
    compose_card(
        canvas_w=1080, canvas_h=1350,
        bg_hex=ORANGE,
        bottle_name="伊蘭",
        bottle_scale=0.73,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.92,
        shadow_offset_x=70, shadow_offset_y=30,
        shadow_blur=50, shadow_opacity=0.18,
        out_path=f"{OUT_BASE}/W29/IG/MORENE_W29_ENFP.png",
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("ENFP", FONT_EN_BOLD, 130, BLACK, 0.055, 0.095, "tl"),
            ("點燃全場的火花", FONT_ZH, 44, BLACK, 0.055, 0.263, "tl"),
            ("「我遼闊,我包含眾多」", FONT_ZH, 21, BLACK, 0.055, 0.330, "tl"),
            ("— Walt Whitman, Song of Myself §51", FONT_EN, 17, BLACK, 0.055, 0.364, "tl"),
            ("YLANG YLANG · SCENT PERSONALITY", FONT_EN, 19, BLACK, 0.055, 0.946, "tl"),
        ],
    )

    # --- W27 IG p1 封面 奶白 1080x1350 ---
    print("W27 IG p1...")
    compose_card(
        canvas_w=1080, canvas_h=1350,
        bg_hex="#E8E0D0",
        bottle_name="苦橙葉",
        bottle_scale=0.72,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.94,
        shadow_offset_x=65, shadow_offset_y=28,
        shadow_blur=44, shadow_opacity=0.18,
        out_path=f"{OUT_BASE}/W27/IG/MORENE_W27_p1.png",
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("SCENT", FONT_EN_BOLD, 100, BLACK, 0.055, 0.095, "tl"),
            ("PERSONALITY", FONT_EN_BOLD, 66, BLACK, 0.055, 0.230, "tl"),
            ("16 TYPES", FONT_EN_BOLD, 54, TERRA, 0.055, 0.316, "tl"),
            ("香氣人格", FONT_ZH, 36, BLACK, 0.055, 0.388, "tl"),
            ("你是哪一型?", FONT_ZH, 28, BLACK, 0.055, 0.434, "tl"),
            ("MORENE.COM.TW", FONT_EN, 19, BLACK, 0.055, 0.946, "tl"),
        ],
    )

    # --- W27 FB hero 芥末黃 1080x1080 ---
    print("W27 FB hero...")
    compose_card(
        canvas_w=1080, canvas_h=1080,
        bg_hex=MUSTARD,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.72,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.95,
        shadow_offset_x=70, shadow_offset_y=32,
        shadow_blur=46, shadow_opacity=0.20,
        out_path=f"{OUT_BASE}/W27/FB/MORENE_W27_FB_hero.png",
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("你是哪一型", FONT_ZH, 70, BLACK, 0.055, 0.100, "tl"),
            ("香氣人格?", FONT_ZH, 70, BLACK, 0.055, 0.188, "tl"),
            ("「知人者智,自知者明。」", FONT_ZH, 22, BLACK, 0.055, 0.285, "tl"),
            ("— 老子《道德經》三十三章", FONT_ZH, 18, BLACK, 0.055, 0.320, "tl"),
            ("SCENT PERSONALITY · 香氣人格 · W27", FONT_EN, 18, BLACK, 0.055, 0.944, "tl"),
        ],
    )

    # --- W27 Reels cover 草綠 1080x1920 ---
    print("W27 Reels cover...")
    compose_card(
        canvas_w=1080, canvas_h=1920,
        bg_hex=GREEN,
        bottle_name="苦橙葉",
        bottle_scale=0.70,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.90,
        shadow_offset_x=75, shadow_offset_y=35,
        shadow_blur=52, shadow_opacity=0.18,
        out_path=f"{OUT_BASE}/W27/Reels/MORENE_W27_Reels_cover.png",
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WHITE, 0.055, 0.040, "tl"),
            ("3 秒", FONT_ZH, 120, WHITE, 0.055, 0.076, "tl"),
            ("測香氣人格", FONT_ZH, 72, WHITE, 0.055, 0.192, "tl"),
            ("16 TYPES · 8 QUESTIONS · 1 SCENT", FONT_EN, 26, WHITE, 0.055, 0.280, "tl"),
            ("MORENE.COM.TW", FONT_EN, 22, WHITE, 0.055, 0.944, "tl"),
        ],
    )

    # --- W28 IG p1 四瓶並排 草綠 1080x1350 ---
    print("W28 IG p1 (4-bottle)...")
    compose_multi_bottle(
        canvas_w=1080, canvas_h=1350,
        bg_hex=GREEN,
        bottle_names=["伊蘭", "乳香", "苦橙葉", "甜橙"],
        bottle_height_frac=0.46,   # 四瓶並排,控制在畫面 46%
        bottle_bottom_frac=0.88,
        spacing=14,
        shadow_offset_x=22, shadow_offset_y=12,
        shadow_blur=24, shadow_opacity=0.18,
        out_path=f"{OUT_BASE}/W28/IG/MORENE_W28_p1.png",
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, WHITE, 0.055, 0.048, "tl"),
            ("四大", FONT_ZH, 94, WHITE, 0.055, 0.090, "tl"),
            ("香氣家族", FONT_ZH, 70, WHITE, 0.055, 0.198, "tl"),
            ("FLORAL · RESINOUS · CITRUS · GREEN", FONT_EN, 22, WHITE, 0.055, 0.290, "tl"),
            ("SCENT PERSONALITY · 香氣人格 · W28", FONT_EN, 19, WHITE, 0.055, 0.946, "tl"),
        ],
    )

    # --- W29 Reels cover 橘 1080x1920 ---
    print("W29 Reels cover...")
    compose_card(
        canvas_w=1080, canvas_h=1920,
        bg_hex=ORANGE,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.68,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.88,
        shadow_offset_x=72, shadow_offset_y=32,
        shadow_blur=50, shadow_opacity=0.16,
        out_path=f"{OUT_BASE}/W29/Reels/MORENE_W29_Reels_cover.png",
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("拆解", FONT_ZH, 120, BLACK, 0.055, 0.076, "tl"),
            ("一型", FONT_ZH, 120, BLACK, 0.055, 0.192, "tl"),
            ("INFP × ENFP  花香家族", FONT_ZH, 32, BLACK, 0.055, 0.326, "tl"),
            ("SCENT PERSONALITY W29", FONT_EN, 22, BLACK, 0.055, 0.944, "tl"),
        ],
    )

    # --- W30 IG p1 三瓶並排 芥末黃 1080x1350 ---
    print("W30 IG p1 (3-bottle)...")
    compose_multi_bottle(
        canvas_w=1080, canvas_h=1350,
        bg_hex=MUSTARD,
        bottle_names=["玫瑰天竺葵", "甜橙", "伊蘭"],
        bottle_height_frac=0.60,
        bottle_bottom_frac=0.90,
        margin_frac=0.055,
        spacing=18,
        shadow_offset_x=25, shadow_offset_y=14,
        shadow_blur=26, shadow_opacity=0.18,
        out_path=f"{OUT_BASE}/W30/IG/MORENE_W30_p1.png",
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("人氣 TOP", FONT_ZH, 84, BLACK, 0.055, 0.090, "tl"),
            ("命定組合", FONT_ZH, 62, BLACK, 0.055, 0.200, "tl"),
            ("BEST SELLERS · SCENT PERSONALITY W30", FONT_EN, 22, BLACK, 0.055, 0.292, "tl"),
            ("MORENE.COM.TW", FONT_EN, 19, BLACK, 0.055, 0.946, "tl"),
        ],
    )

    # --- W30 FB closing 奶白 1080x1080 ---
    print("W30 FB closing...")
    compose_card(
        canvas_w=1080, canvas_h=1080,
        bg_hex="#EDE7DC",
        bottle_name="甜橙",
        bottle_scale=0.70,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.95,
        shadow_offset_x=65, shadow_offset_y=30,
        shadow_blur=44, shadow_opacity=0.16,
        out_path=f"{OUT_BASE}/W30/FB/MORENE_W30_FB_closing.png",
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("「只有用心才能看清;", FONT_ZH, 26, BLACK, 0.055, 0.105, "tl"),
            ("真正重要的東西,肉眼是看不見的。」", FONT_ZH, 26, BLACK, 0.055, 0.148, "tl"),
            ("— Antoine de Saint-Exupery, Le Petit Prince", FONT_EN, 18, BLACK, 0.055, 0.196, "tl"),
            ("謝謝一起玩香氣人格", FONT_ZH, 36, BLACK, 0.055, 0.258, "tl"),
            ("找到你的命定香氣了嗎?", FONT_ZH, 28, BLACK, 0.055, 0.312, "tl"),
            ("MORENE.COM.TW · W30", FONT_EN, 19, BLACK, 0.055, 0.944, "tl"),
        ],
    )

    print("\n全部完成 v2。")


if __name__ == "__main__":
    make_all()
