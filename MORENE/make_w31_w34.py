#!/usr/bin/env python3
"""
MORENE W31–W34 香氣人格深化 · 圖卡生成腳本
沿用 make_covers_v2.py 視覺系統(Y2K 攝影風 + 單色飽和底 + 瓶身主角)
新增: 雙寫(mw-social-assets + Desktop 03_圖卡_Assets)、MORENE_ 前綴強制
"""

import os, sys, shutil
sys.path.insert(0, "/Users/morrislin/mw-social-assets/MORENE")
from make_covers_v2 import (
    compose_card, compose_multi_bottle,
    FONT_EN_BOLD, FONT_EN, FONT_ZH, FONT_ZH_BOLD,
    CREAM, BLACK, TERRA, MUSTARD, SAGE, ORANGE, GREEN, LEMON, WHITE,
    OUT_BASE,
)

# =====================
# 常數
# =====================
BASE_PROD = "/Users/morrislin/Desktop/MORENE/03_MORENE/03_Assets/A009：MORENE-產品相關/01.產品相關/01. 產品資料/05. 產品照片/素材/商品大圖/01_精油"
DESK_ASSETS = "/Users/morrislin/Desktop/MORENE/MORENE_社群營運_Social/03_圖卡_Assets"
LOGO_CREAM = "/Users/morrislin/mw-social-assets/MORENE/_fonts/MORENE_logo_cream.png"
LOGO_BLACK = "/Users/morrislin/mw-social-assets/MORENE/_fonts/MORENE_logo_black.png"

# W31-W34 特定瓶身路徑 (補充 make_covers_v2 的 get_bottle 沒有的油)
EXTRA_BOTTLES = {
    "岩蘭草":   f"{BASE_PROD}/岩蘭草/MORENE_精油瓶_去背_岩蘭草.png",
    "白葡萄柚": f"{BASE_PROD}/5MOEO011_白葡萄柚/MORENE_精油瓶_去背_白葡萄柚.png",
    "迷迭香":   f"{BASE_PROD}/桉油葉迷迭香/MORENE_精油瓶_去背_桉油葉迷迭香.png",
    "真正薰衣草": f"{BASE_PROD}/5MOEO015_真正薰衣草/MORENE_精油瓶_去背_真正薰衣草.png",
    "乳香":     f"{BASE_PROD}/5MOEO009_乳香/MORENE_精油瓶_去背_乳香.png",
    "甜橙":     f"{BASE_PROD}/甜橙/MORENE_精油瓶_去背_甜橙.png",
    "玫瑰天竺葵": f"{BASE_PROD}/5MOEO025_玫瑰天竺葵/MORENE_精油瓶_去背_玫瑰天竺葵.png",
}

# =====================
# 雙寫輔助
# =====================
def dual_save(week: str, channel: str, filename: str, src_path: str):
    """
    確保 filename 有 MORENE_ 前綴,寫到:
      ~/mw-social-assets/MORENE/W{week}/{channel}/MORENE_{filename}
      ~/Desktop/.../03_圖卡_Assets/W{week}/{channel}/MORENE_{filename}
    src_path 是 compose_card 已寫的主路徑,只需 copy 到 Desktop.
    """
    if not filename.startswith("MORENE_"):
        raise ValueError(f"Filename must start with MORENE_: {filename}")
    desk_dir = f"{DESK_ASSETS}/{week}/{channel}"
    os.makedirs(desk_dir, exist_ok=True)
    desk_path = f"{desk_dir}/{filename}"
    shutil.copy2(src_path, desk_path)
    print(f"  dual-write → {desk_path}")

def save_and_dual(week: str, channel: str, filename: str, **compose_kwargs):
    """compose_card wrapper: 寫到 OUT_BASE 並雙寫到 Desktop."""
    if not filename.startswith("MORENE_"):
        raise ValueError(f"Filename must start with MORENE_: {filename}")
    nas_dir = f"{OUT_BASE}/{week}/{channel}"
    os.makedirs(nas_dir, exist_ok=True)
    nas_path = f"{nas_dir}/{filename}"
    compose_card(out_path=nas_path, **compose_kwargs)
    dual_save(week, channel, filename, nas_path)
    return nas_path

def save_multi_and_dual(week: str, channel: str, filename: str, **compose_kwargs):
    """compose_multi_bottle wrapper with dual-write."""
    if not filename.startswith("MORENE_"):
        raise ValueError(f"Filename must start with MORENE_: {filename}")
    nas_dir = f"{OUT_BASE}/{week}/{channel}"
    os.makedirs(nas_dir, exist_ok=True)
    nas_path = f"{nas_dir}/{filename}"
    compose_multi_bottle(out_path=nas_path, **compose_kwargs)
    dual_save(week, channel, filename, nas_path)
    return nas_path

# Monkey-patch get_bottle in make_covers_v2 to include extra bottles
import make_covers_v2 as _m
_orig_get_bottle = _m.get_bottle
def _patched_get_bottle(name):
    if name in EXTRA_BOTTLES:
        return EXTRA_BOTTLES[name]
    return _orig_get_bottle(name)
_m.get_bottle = _patched_get_bottle


# =====================
# W31 命定香氣的一天
# =====================
def make_w31():
    print("\n=== W31 命定香氣的一天 ===")

    # FB hero 1080x1080 — 陶土底 + 真正薰衣草瓶
    print("W31 FB hero...")
    save_and_dual(
        "W31", "FB", "MORENE_W31_FB_hero.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=TERRA,
        bottle_name="真正薰衣草",
        bottle_scale=0.72,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.95,
        shadow_offset_x=68, shadow_offset_y=30,
        shadow_blur=46, shadow_opacity=0.20,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            ("命定香氣", FONT_ZH, 72, CREAM, 0.055, 0.100, "tl"),
            ("的一天", FONT_ZH, 72, CREAM, 0.055, 0.195, "tl"),
            ("工作,是愛的具現。", FONT_ZH, 22, CREAM, 0.055, 0.305, "tl"),
            ("— 紀伯倫《先知·論工作》", FONT_ZH, 17, CREAM, 0.055, 0.344, "tl"),
            ("SCENT PERSONALITY DEEP DIVE · W31", FONT_EN, 18, CREAM, 0.055, 0.944, "tl"),
        ],
    )

    # IG p1 封面 1080x1350 — 芥末底 + 真正薰衣草
    print("W31 IG p1 cover...")
    save_and_dual(
        "W31", "IG", "MORENE_W31_p1.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=MUSTARD,
        bottle_name="真正薰衣草",
        bottle_scale=0.73,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.93,
        shadow_offset_x=65, shadow_offset_y=28,
        shadow_blur=44, shadow_opacity=0.18,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("妳的命定香氣", FONT_ZH, 54, BLACK, 0.055, 0.095, "tl"),
            ("一天怎麼用?", FONT_ZH, 54, BLACK, 0.055, 0.170, "tl"),
            ("SCENT PERSONALITY · 四個時刻", FONT_ZH, 20, BLACK, 0.055, 0.254, "tl"),
            ("W31 · MORENE.COM.TW", FONT_EN, 18, BLACK, 0.055, 0.946, "tl"),
        ],
    )

    # IG p2 晨 1080x1350 — 奶油底
    print("W31 IG p2 晨...")
    save_and_dual(
        "W31", "IG", "MORENE_W31_p2.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex="#EDE7DC",
        bottle_name="真正薰衣草",
        bottle_scale=0.60,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.88,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=38, shadow_opacity=0.15,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("02 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("晨", FONT_ZH, 120, TERRA, 0.055, 0.095, "tl"),
            ("MORNING", FONT_EN_BOLD, 32, BLACK, 0.055, 0.252, "tl"),
            ("擴香一兩滴", FONT_ZH, 42, BLACK, 0.055, 0.308, "tl"),
            ("替今天定一個基調", FONT_ZH, 30, BLACK, 0.055, 0.374, "tl"),
            ("純擴香 · 情境使用", FONT_ZH, 16, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # IG p3 勤 1080x1350 — 霧藍綠底
    print("W31 IG p3 勤...")
    save_and_dual(
        "W31", "IG", "MORENE_W31_p3.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=SAGE,
        bottle_name="真正薰衣草",
        bottle_scale=0.60,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.88,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=38, shadow_opacity=0.15,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("03 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("勤", FONT_ZH, 120, BLACK, 0.055, 0.095, "tl"),
            ("WORK", FONT_EN_BOLD, 32, BLACK, 0.055, 0.252, "tl"),
            ("隨身瓶在手腕", FONT_ZH, 42, BLACK, 0.055, 0.308, "tl"),
            ("把注意力帶回來", FONT_ZH, 30, BLACK, 0.055, 0.374, "tl"),
            ("情境使用 · 手腕/衣領", FONT_ZH, 16, BLACK, 0.055, 0.946, "tl"),
        ],
    )

    # IG p4 憩 1080x1350 — 陶土底
    print("W31 IG p4 憩...")
    save_and_dual(
        "W31", "IG", "MORENE_W31_p4.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=TERRA,
        bottle_name="真正薰衣草",
        bottle_scale=0.60,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.88,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=38, shadow_opacity=0.18,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            ("04 / 07", FONT_EN, 14, "#CBA98A", 0.870, 0.048, "tl"),
            ("憩", FONT_ZH, 120, CREAM, 0.055, 0.095, "tl"),
            ("REST", FONT_EN_BOLD, 32, CREAM, 0.055, 0.252, "tl"),
            ("午後三點,窗邊一抹", FONT_ZH, 38, CREAM, 0.055, 0.308, "tl"),
            ("給自己一個喘息的標點", FONT_ZH, 28, CREAM, 0.055, 0.374, "tl"),
            ("情境使用 · 純擴香", FONT_ZH, 16, CREAM, 0.055, 0.946, "tl"),
        ],
    )

    # IG p5 夜 1080x1350 — 深墨底
    print("W31 IG p5 夜...")
    save_and_dual(
        "W31", "IG", "MORENE_W31_p5.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=BLACK,
        bottle_name="真正薰衣草",
        bottle_scale=0.60,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.88,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=38, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            ("05 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("夜", FONT_ZH, 120, MUSTARD, 0.055, 0.095, "tl"),
            ("NIGHT", FONT_EN_BOLD, 32, CREAM, 0.055, 0.252, "tl"),
            ("睡前枕邊一滴", FONT_ZH, 42, CREAM, 0.055, 0.308, "tl"),
            ("替一天輕輕收尾", FONT_ZH, 30, CREAM, 0.055, 0.374, "tl"),
            ("純擴香 · 睡前情境", FONT_ZH, 16, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # IG p6 總結 1080x1350 — 奶油底
    print("W31 IG p6 總結...")
    save_and_dual(
        "W31", "IG", "MORENE_W31_p6.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex="#EDE7DC",
        bottle_name="真正薰衣草",
        bottle_scale=0.65,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.90,
        shadow_offset_x=60, shadow_offset_y=26,
        shadow_blur=42, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("06 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("同一支油", FONT_ZH, 52, TERRA, 0.055, 0.100, "tl"),
            ("四種時刻", FONT_ZH, 52, BLACK, 0.055, 0.175, "tl"),
            ("四種妳", FONT_ZH, 52, BLACK, 0.055, 0.250, "tl"),
            ("留言妳最常什麼時候用精油?", FONT_ZH, 24, BLACK, 0.055, 0.350, "tl"),
        ],
    )

    # IG p7 CTA 1080x1350 — 深墨底
    print("W31 IG p7 CTA...")
    save_and_dual(
        "W31", "IG", "MORENE_W31_p7.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=BLACK,
        bottle_name="真正薰衣草",
        bottle_scale=0.55,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.85,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            ("07 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("還沒對到", FONT_ZH, 52, CREAM, 0.055, 0.100, "tl"),
            ("命定香氣?", FONT_ZH, 52, MUSTARD, 0.055, 0.170, "tl"),
            ("測驗在個人簡介連結", FONT_ZH, 28, CREAM, 0.055, 0.258, "tl"),
            ("morene.com.tw/pages/scent-personality", FONT_EN, 18, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # Reels 封面 1080x1920 — 草綠底 + 真正薰衣草
    print("W31 Reels cover...")
    save_and_dual(
        "W31", "Reels", "MORENE_W31_Reels_cover.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=GREEN,
        bottle_name="真正薰衣草",
        bottle_scale=0.68,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.88,
        shadow_offset_x=72, shadow_offset_y=32,
        shadow_blur=50, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, WHITE, 0.055, 0.040, "tl"),
            ("一支精油", FONT_ZH, 110, WHITE, 0.055, 0.076, "tl"),
            ("的一天", FONT_ZH, 110, WHITE, 0.055, 0.180, "tl"),
            ("晨 · 勤 · 憩 · 夜 · 四個時刻", FONT_ZH, 30, WHITE, 0.055, 0.294, "tl"),
            ("SCENT PERSONALITY W31", FONT_EN, 22, WHITE, 0.055, 0.944, "tl"),
        ],
    )

    # Stories ×3 (1080x1920)
    # S1: 投票 — 芥末底
    print("W31 Stories S1...")
    save_and_dual(
        "W31", "Stories", "MORENE_W31_S1.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=MUSTARD,
        bottle_name="真正薰衣草",
        bottle_scale=0.55,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.80,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("STORIES · W31", FONT_EN, 14, "#8C8079", 0.055, 0.092, "tl"),
            ("妳都什麼時候", FONT_ZH, 56, BLACK, 0.055, 0.130, "tl"),
            ("用精油?", FONT_ZH, 56, BLACK, 0.055, 0.210, "tl"),
            ("早晨 / 工作 / 睡前", FONT_ZH, 34, TERRA, 0.055, 0.296, "tl"),
            ("留言告訴我 👇", FONT_ZH, 28, BLACK, 0.055, 0.354, "tl"),
            ("SCENT PERSONALITY · 命定香氣的一天", FONT_ZH, 18, BLACK, 0.055, 0.944, "tl"),
        ],
    )

    # S2: 隨身瓶用法 — 霧藍綠底
    print("W31 Stories S2...")
    save_and_dual(
        "W31", "Stories", "MORENE_W31_S2.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=SAGE,
        bottle_name="真正薰衣草",
        bottle_scale=0.55,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=48, shadow_offset_y=20,
        shadow_blur=34, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("隨身瓶", FONT_ZH, 88, BLACK, 0.055, 0.100, "tl"),
            ("3 種用法", FONT_ZH, 54, BLACK, 0.055, 0.213, "tl"),
            ("01  手腕内側", FONT_ZH, 32, BLACK, 0.055, 0.310, "tl"),
            ("02  衣領/頸部", FONT_ZH, 32, BLACK, 0.055, 0.370, "tl"),
            ("03  掌心搓熱深吸", FONT_ZH, 32, BLACK, 0.055, 0.430, "tl"),
            ("情境使用,不宣稱功效 | 趣味體驗非診斷", FONT_ZH, 15, "#8C8079", 0.055, 0.944, "tl"),
        ],
    )

    # S3: 問答 — 奶油底
    print("W31 Stories S3...")
    save_and_dual(
        "W31", "Stories", "MORENE_W31_S3.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex="#EDE7DC",
        bottle_name="真正薰衣草",
        bottle_scale=0.50,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.75,
        shadow_offset_x=44, shadow_offset_y=18,
        shadow_blur=32, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("妳的命定香氣", FONT_ZH, 56, BLACK, 0.055, 0.100, "tl"),
            ("是哪一支?", FONT_ZH, 56, TERRA, 0.055, 0.180, "tl"),
            ("留言分享你的香氣人格型", FONT_ZH, 28, BLACK, 0.055, 0.272, "tl"),
            ("還沒測? 個人簡介連結做測驗", FONT_ZH, 24, "#8C8079", 0.055, 0.326, "tl"),
            ("morene.com.tw", FONT_EN, 18, "#8C8079", 0.055, 0.944, "tl"),
        ],
    )

    print("W31 完成。")


# =====================
# W32 社群回響 / 16型共鳴金句
# =====================
def make_w32():
    print("\n=== W32 社群回響 / 共鳴金句 ===")

    # FB hero 1080x1080 — 霧粉底 + 玫瑰天竺葵
    print("W32 FB hero...")
    save_and_dual(
        "W32", "FB", "MORENE_W32_FB_resonance.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex="#E9C5B9",
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.72,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.95,
        shadow_offset_x=65, shadow_offset_y=28,
        shadow_blur=44, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("這個月", FONT_ZH, 62, BLACK, 0.055, 0.100, "tl"),
            ("妳們的香氣人格說話了", FONT_ZH, 36, BLACK, 0.055, 0.196, "tl"),
            ("原來這麼多人,在一支香氣裡看見自己。", FONT_ZH, 22, TERRA, 0.055, 0.278, "tl"),
            ("SCENT PERSONALITY · UGC · W32", FONT_EN, 18, BLACK, 0.055, 0.944, "tl"),
        ],
    )

    # IG p1 封面 1080x1350 — 陶土底 + 玫瑰天竺葵
    print("W32 IG p1 cover...")
    save_and_dual(
        "W32", "IG", "MORENE_W32_p1.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=TERRA,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.73,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.93,
        shadow_offset_x=68, shadow_offset_y=30,
        shadow_blur=46, shadow_opacity=0.18,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            ("哪一句", FONT_ZH, 88, CREAM, 0.055, 0.095, "tl"),
            ("是妳?", FONT_ZH, 88, MUSTARD, 0.055, 0.220, "tl"),
            ("16 型 Forer 共鳴金句", FONT_ZH, 28, CREAM, 0.055, 0.352, "tl"),
            ("SCENT PERSONALITY · W32", FONT_EN, 19, CREAM, 0.055, 0.946, "tl"),
        ],
    )

    # IG p2–p5: 每頁 4 型,逐字 Forer 金句
    # 每張用不同底色,對應家族色
    forer_data = [
        # (型, 名, Forer一句, 底色, 文字色)
        ("INFJ", "靜默的引光者", "話不多,卻總被人放心地說出秘密。", SAGE, BLACK),
        ("INFP", "未完成的詩", "心裡住著一個理想世界。別人看妳溫和隨和,只有妳知道妳對「真」有多固執。", "#E9C5B9", BLACK),
        ("ENFJ", "會發光的主理人", "很少人發現,妳也偷偷希望有人來照顧你。", MUSTARD, BLACK),
        ("ENFP", "點燃全場的火花", "看似無憂無慮,其實比誰都認真地想被深深理解。", ORANGE, BLACK),
        ("INTJ", "遠方的建築師", "獨來獨往不是孤僻,是大多數對話跟不上妳想去的地方。", BLACK, CREAM),
        ("INTP", "拆解世界的人", "看似抽離,其實把能量都用在思考上。", "#82A8CC", BLACK),
        ("ENTJ", "天生的指揮", "妳扛得起也願意扛,只是偶爾也想聽到有人說「交給我」。", GREEN, WHITE),
        ("ENTP", "停不下來的辯手", "不是愛抬槓,是真心覺得換個角度世界更有趣。", TERRA, CREAM),
        ("ISTJ", "靠得住的基石", "妳的浪漫藏在被默默維持好的秩序裡。", "#CBA98A", BLACK),
        ("ISFJ", "溫柔的守護者", "不太說自己累,因為照顧人對妳太自然。", "#E9C5B9", BLACK),
        ("ESTJ", "把事做成的人", "妳直接,是因為真的想把事情做對、做好。", MUSTARD, BLACK),
        ("ESFJ", "把大家聚起來的人", "被需要讓妳快樂,但妳也值得被同樣地在乎。", SAGE, BLACK),
        ("ISTP", "冷靜的拆解高手", "危機時最冷靜的往往是妳。", BLACK, CREAM),
        ("ISFP", "安靜的美感家", "用作品和選擇說話,而不是言語。", "#EDE7DC", BLACK),
        ("ESTP", "先衝再說的行動派", "把無聊變刺激是妳的本事。", ORANGE, BLACK),
        ("ESFP", "天生的舞台中心", "看似只顧玩樂,其實比誰都珍惜「在一起」的時光。", MUSTARD, BLACK),
    ]

    # p2–p5: 每張 4 型 (型別小字版,一屏 4 型)
    # 用單瓶+4 段文字排版
    for page_idx in range(4):
        pg_num = page_idx + 2  # 2,3,4,5
        items = forer_data[page_idx*4:(page_idx+1)*4]
        # 底色取第一型的色
        bg = items[0][3]
        txt_col = items[0][4]
        filename = f"MORENE_W32_p{pg_num}.png"
        print(f"W32 IG p{pg_num} (4型共鳴)...")

        # 文字行: logo + 頁碼 + 4 型各兩行
        lines = [
            ("MORENE", FONT_EN_BOLD, 28, txt_col, 0.055, 0.048, "tl"),
            (f"0{pg_num} / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
        ]
        y_start = 0.120
        y_step = 0.195
        for i, (code, name, forer, _, _tc) in enumerate(items):
            y = y_start + i * y_step
            lines.append((f"{code}  {name}", FONT_EN_BOLD, 26, txt_col, 0.055, y, "tl"))
            # Forer 金句最多 24 字元一行
            lines.append((forer[:28], FONT_ZH, 22, txt_col, 0.055, y + 0.038, "tl"))
            if len(forer) > 28:
                lines.append((forer[28:], FONT_ZH, 22, txt_col, 0.055, y + 0.074, "tl"))

        # 用甜橙瓶作裝飾(右側半透,暗色)
        save_and_dual(
            "W32", "IG", filename,
            canvas_w=1080, canvas_h=1350,
            bg_hex=bg,
            bottle_name="甜橙",
            bottle_scale=0.50,
            bottle_x_frac=0.78,
            bottle_bottom_frac=0.92,
            shadow_offset_x=40, shadow_offset_y=18,
            shadow_blur=30, shadow_opacity=0.10,
            text_lines=lines,
        )

    # IG p6 標記朋友 1080x1350 — 霧藍綠底
    print("W32 IG p6 標記...")
    save_and_dual(
        "W32", "IG", "MORENE_W32_p6.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=SAGE,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.60,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.88,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("06 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("哪一句戳到妳?", FONT_ZH, 52, BLACK, 0.055, 0.095, "tl"),
            ("標記那個「一聞就是她」的朋友", FONT_ZH, 28, BLACK, 0.055, 0.215, "tl"),
            ("RESONANCE · 香氣人格 W32", FONT_ZH, 18, BLACK, 0.055, 0.946, "tl"),
        ],
    )

    # IG p7 CTA 1080x1350 — 深墨底
    print("W32 IG p7 CTA...")
    save_and_dual(
        "W32", "IG", "MORENE_W32_p7.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=BLACK,
        bottle_name="伊蘭",
        bottle_scale=0.55,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.85,
        shadow_offset_x=50, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            ("07 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("還沒測到妳的型?", FONT_ZH, 46, CREAM, 0.055, 0.100, "tl"),
            ("個人簡介連結, 8 題直覺作答", FONT_ZH, 26, CREAM, 0.055, 0.196, "tl"),
            ("SCENT PERSONALITY · 16 TYPES · MORENE.COM.TW", FONT_EN, 16, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # Reels 封面 1080x1920 — 橘底
    print("W32 Reels cover...")
    save_and_dual(
        "W32", "Reels", "MORENE_W32_Reels_cover.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=ORANGE,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.68,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.88,
        shadow_offset_x=70, shadow_offset_y=30,
        shadow_blur=48, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("哪一句", FONT_ZH, 110, BLACK, 0.055, 0.076, "tl"),
            ("戳到妳?", FONT_ZH, 80, BLACK, 0.055, 0.210, "tl"),
            ("16 型共鳴金句快閃", FONT_ZH, 32, BLACK, 0.055, 0.316, "tl"),
            ("SCENT PERSONALITY W32", FONT_EN, 22, BLACK, 0.055, 0.944, "tl"),
        ],
    )

    # Stories ×3
    # S1: UGC 精選 — 陶土底
    print("W32 Stories S1...")
    save_and_dual(
        "W32", "Stories", "MORENE_W32_S1.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=TERRA,
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.50,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=44, shadow_offset_y=18,
        shadow_blur=32, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, CREAM, 0.055, 0.040, "tl"),
            ("STORIES · W32", FONT_EN, 14, "#CBA98A", 0.055, 0.092, "tl"),
            ("看到你們說", FONT_ZH, 60, CREAM, 0.055, 0.130, "tl"),
            ("「這就是我」", FONT_ZH, 60, MUSTARD, 0.055, 0.218, "tl"),
            ("這週最溫暖的留言 ↓", FONT_ZH, 28, CREAM, 0.055, 0.318, "tl"),
            ("@morene_organic", FONT_EN, 18, "#CBA98A", 0.055, 0.944, "tl"),
        ],
    )

    # S2: 型別最讓妳意外 — 霧藍底
    print("W32 Stories S2...")
    save_and_dual(
        "W32", "Stories", "MORENE_W32_S2.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex="#82A8CC",
        bottle_name="伊蘭",
        bottle_scale=0.50,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=44, shadow_offset_y=18,
        shadow_blur=32, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("哪一型最讓妳意外?", FONT_ZH, 44, BLACK, 0.055, 0.130, "tl"),
            ("留言告訴我 👇", FONT_ZH, 36, BLACK, 0.055, 0.218, "tl"),
            ("RESONANCE · W32", FONT_EN, 18, BLACK, 0.055, 0.944, "tl"),
        ],
    )

    # S3: 測驗導流 — 芥末底
    print("W32 Stories S3...")
    save_and_dual(
        "W32", "Stories", "MORENE_W32_S3.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=MUSTARD,
        bottle_name="甜橙",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.80,
        shadow_offset_x=46, shadow_offset_y=20,
        shadow_blur=34, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("還沒測的朋友", FONT_ZH, 52, BLACK, 0.055, 0.130, "tl"),
            ("個人簡介連結", FONT_ZH, 44, TERRA, 0.055, 0.218, "tl"),
            ("8 題直覺作答 ↑", FONT_ZH, 34, BLACK, 0.055, 0.306, "tl"),
            ("SCENT PERSONALITY · morene.com.tw", FONT_EN, 18, BLACK, 0.055, 0.944, "tl"),
        ],
    )

    print("W32 完成。")


# =====================
# W33 雙油煉金
# =====================
def make_w33():
    print("\n=== W33 雙油煉金 ===")

    # FB hero 1080x1080 — 深墨底 + 岩蘭草(基調代表)
    print("W33 FB hero...")
    save_and_dual(
        "W33", "FB", "MORENE_W33_FB_alchemy.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex=BLACK,
        bottle_name="岩蘭草",
        bottle_scale=0.70,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.95,
        shadow_offset_x=65, shadow_offset_y=28,
        shadow_blur=44, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            ("一支是妳的底色", FONT_ZH, 46, CREAM, 0.055, 0.100, "tl"),
            ("一支是妳此刻的能量", FONT_ZH, 40, MUSTARD, 0.055, 0.178, "tl"),
            ("嗅覺與情緒記憶相連 · Scent with Science", FONT_ZH, 20, "#8C8079", 0.055, 0.280, "tl"),
            ("趣味體驗非診斷 | 科普參考,不宣稱療效", FONT_ZH, 14, "#8C8079", 0.055, 0.340, "tl"),
            ("DOUBLE OIL ALCHEMY · W33", FONT_EN, 18, CREAM, 0.055, 0.944, "tl"),
        ],
    )

    # IG p1 封面 1080x1350 — 芥末底 + 岩蘭草
    print("W33 IG p1 cover...")
    save_and_dual(
        "W33", "IG", "MORENE_W33_p1.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=MUSTARD,
        bottle_name="岩蘭草",
        bottle_scale=0.73,
        bottle_x_frac=0.70,
        bottle_bottom_frac=0.93,
        shadow_offset_x=65, shadow_offset_y=28,
        shadow_blur=44, shadow_opacity=0.18,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("雙油", FONT_ZH, 110, BLACK, 0.055, 0.095, "tl"),
            ("煉金術", FONT_ZH, 80, TERRA, 0.055, 0.252, "tl"),
            ("BASE + MODIFIER · SCENT WITH SCIENCE", FONT_EN, 20, BLACK, 0.055, 0.360, "tl"),
            ("趣味體驗非診斷 · W33", FONT_ZH, 18, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # IG p2 什麼是基調油 1080x1350 — 奶油底
    print("W33 IG p2 基調油...")
    save_and_dual(
        "W33", "IG", "MORENE_W33_p2.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex="#EDE7DC",
        bottle_name="乳香",
        bottle_scale=0.62,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.88,
        shadow_offset_x=58, shadow_offset_y=26,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("02 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("基調油", FONT_ZH, 88, TERRA, 0.055, 0.095, "tl"),
            ("BASE OIL", FONT_EN_BOLD, 36, BLACK, 0.055, 0.244, "tl"),
            ("妳的氣質底色", FONT_ZH, 38, BLACK, 0.055, 0.308, "tl"),
            ("由 16 型香氣人格決定的那支命定油", FONT_ZH, 24, BLACK, 0.055, 0.380, "tl"),
        ],
    )

    # IG p3 什麼是變調油 1080x1350 — 霧藍綠底
    print("W33 IG p3 變調油...")
    save_and_dual(
        "W33", "IG", "MORENE_W33_p3.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=SAGE,
        bottle_name="白葡萄柚",
        bottle_scale=0.62,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.88,
        shadow_offset_x=58, shadow_offset_y=26,
        shadow_blur=40, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("03 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("變調油", FONT_ZH, 88, BLACK, 0.055, 0.095, "tl"),
            ("MODIFIER OIL", FONT_EN_BOLD, 32, BLACK, 0.055, 0.244, "tl"),
            ("妳此刻的能量", FONT_ZH, 38, BLACK, 0.055, 0.308, "tl"),
            ("4 種方向,今天妳需要哪一種?", FONT_ZH, 24, BLACK, 0.055, 0.380, "tl"),
        ],
    )

    # IG p4 四能量瓶並排 1080x1350 — 深墨底
    print("W33 IG p4 四瓶並排...")
    save_multi_and_dual(
        "W33", "IG", "MORENE_W33_p4.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=BLACK,
        bottle_names=["岩蘭草", "白葡萄柚", "迷迭香", "真正薰衣草"],
        bottle_height_frac=0.46,
        bottle_bottom_frac=0.82,
        spacing=14,
        shadow_offset_x=20, shadow_offset_y=10,
        shadow_blur=22, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            ("04 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("4 種能量", FONT_ZH, 72, MUSTARD, 0.055, 0.095, "tl"),
            ("沉穩 · 明亮 · 俐落 · 柔和", FONT_ZH, 28, CREAM, 0.055, 0.220, "tl"),
            ("岩蘭草 / 白葡萄柚 / 迷迭香 / 真正薰衣草", FONT_ZH, 22, "#8C8079", 0.055, 0.270, "tl"),
            ("趣味體驗非診斷", FONT_ZH, 16, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # IG p5 怎麼疊 1080x1350 — 陶土底
    print("W33 IG p5 怎麼疊...")
    save_and_dual(
        "W33", "IG", "MORENE_W33_p5.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=TERRA,
        bottle_name="岩蘭草",
        bottle_scale=0.58,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.86,
        shadow_offset_x=52, shadow_offset_y=22,
        shadow_blur=36, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            ("05 / 07", FONT_EN, 14, "#CBA98A", 0.870, 0.048, "tl"),
            ("怎麼疊?", FONT_ZH, 76, CREAM, 0.055, 0.095, "tl"),
            ("基調油 2–3 滴 → 攤手心", FONT_ZH, 28, CREAM, 0.055, 0.230, "tl"),
            ("+ 變調油 1–2 滴 → 搓熱", FONT_ZH, 28, CREAM, 0.055, 0.282, "tl"),
            ("→ 掌心深吸,感受今天的妳", FONT_ZH, 28, CREAM, 0.055, 0.334, "tl"),
            ("情境使用,不宣稱療效 | 趣味體驗非診斷", FONT_ZH, 15, CREAM, 0.055, 0.946, "tl"),
        ],
    )

    # IG p6 雙油範例 INFP 玫瑰天竺葵 × 白葡萄柚 1080x1350 — 霧粉底
    print("W33 IG p6 雙油範例...")
    save_and_dual(
        "W33", "IG", "MORENE_W33_p6.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex="#E9C5B9",
        bottle_name="玫瑰天竺葵",
        bottle_scale=0.60,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.88,
        shadow_offset_x=55, shadow_offset_y=24,
        shadow_blur=38, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("06 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("範例", FONT_ZH, 72, TERRA, 0.055, 0.095, "tl"),
            ("INFP 玫瑰天竺葵", FONT_ZH, 36, BLACK, 0.055, 0.220, "tl"),
            ("× 白葡萄柚(明亮創意)", FONT_ZH, 32, BLACK, 0.055, 0.282, "tl"),
            ("粉甜底色 + 清亮朝氣 · 今天的妳", FONT_ZH, 24, "#8C8079", 0.055, 0.352, "tl"),
        ],
    )

    # IG p7 CTA 1080x1350 — 深墨底
    print("W33 IG p7 CTA...")
    save_and_dual(
        "W33", "IG", "MORENE_W33_p7.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=BLACK,
        bottle_name="白葡萄柚",
        bottle_scale=0.55,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.85,
        shadow_offset_x=48, shadow_offset_y=20,
        shadow_blur=34, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            ("07 / 07", FONT_EN, 14, "#8C8079", 0.870, 0.048, "tl"),
            ("基調 + 變調", FONT_ZH, 54, MUSTARD, 0.055, 0.100, "tl"),
            ("SCENT-SET 85折", FONT_ZH, 44, CREAM, 0.055, 0.196, "tl"),
            ("morene.com.tw", FONT_EN, 26, CREAM, 0.055, 0.288, "tl"),
            ("DOUBLE OIL ALCHEMY · W33", FONT_EN, 16, "#8C8079", 0.055, 0.946, "tl"),
        ],
    )

    # Reels 封面 1080x1920 — 陶土底
    print("W33 Reels cover...")
    save_and_dual(
        "W33", "Reels", "MORENE_W33_Reels_cover.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=TERRA,
        bottle_name="岩蘭草",
        bottle_scale=0.68,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.88,
        shadow_offset_x=70, shadow_offset_y=30,
        shadow_blur=48, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, CREAM, 0.055, 0.040, "tl"),
            ("兩支油", FONT_ZH, 110, CREAM, 0.055, 0.076, "tl"),
            ("調出妳的此刻", FONT_ZH, 64, MUSTARD, 0.055, 0.220, "tl"),
            ("雙油調香示範", FONT_ZH, 32, CREAM, 0.055, 0.320, "tl"),
            ("趣味體驗非診斷 · SCENT WITH SCIENCE W33", FONT_ZH, 18, CREAM, 0.055, 0.944, "tl"),
        ],
    )

    # Stories ×3
    # S1: 能量投票 — 深墨底
    print("W33 Stories S1...")
    save_and_dual(
        "W33", "Stories", "MORENE_W33_S1.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=BLACK,
        bottle_name="岩蘭草",
        bottle_scale=0.50,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=42, shadow_offset_y=18,
        shadow_blur=30, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, CREAM, 0.055, 0.040, "tl"),
            ("STORIES · W33", FONT_EN, 14, "#8C8079", 0.055, 0.092, "tl"),
            ("妳此刻需要哪種能量?", FONT_ZH, 44, CREAM, 0.055, 0.130, "tl"),
            ("沉穩主導  岩蘭草", FONT_ZH, 30, MUSTARD, 0.055, 0.228, "tl"),
            ("明亮創意  白葡萄柚", FONT_ZH, 30, CREAM, 0.055, 0.286, "tl"),
            ("俐落規範  迷迭香", FONT_ZH, 30, CREAM, 0.055, 0.344, "tl"),
            ("柔和和諧  真正薰衣草", FONT_ZH, 30, CREAM, 0.055, 0.402, "tl"),
            ("留言告訴我 👇 趣味體驗非診斷", FONT_ZH, 22, "#8C8079", 0.055, 0.944, "tl"),
        ],
    )

    # S2: 四瓶小科普 — 霧藍綠底
    print("W33 Stories S2...")
    save_and_dual(
        "W33", "Stories", "MORENE_W33_S2.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=SAGE,
        bottle_name="白葡萄柚",
        bottle_scale=0.50,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=42, shadow_offset_y=18,
        shadow_blur=30, shadow_opacity=0.12,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("Scent with Science", FONT_EN_BOLD, 32, BLACK, 0.055, 0.130, "tl"),
            ("嗅覺與情緒記憶相連", FONT_ZH, 40, BLACK, 0.055, 0.196, "tl"),
            ("氣味信號直通邊緣系統", FONT_ZH, 30, BLACK, 0.055, 0.278, "tl"),
            ("這是感官科普,不是療效宣稱", FONT_ZH, 24, "#8C8079", 0.055, 0.350, "tl"),
            ("趣味體驗非診斷", FONT_ZH, 18, "#8C8079", 0.055, 0.944, "tl"),
        ],
    )

    # S3: 導購 — 芥末底
    print("W33 Stories S3...")
    save_and_dual(
        "W33", "Stories", "MORENE_W33_S3.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=MUSTARD,
        bottle_name="迷迭香",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.80,
        shadow_offset_x=44, shadow_offset_y=18,
        shadow_blur=32, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("基底 + 變調", FONT_ZH, 64, BLACK, 0.055, 0.130, "tl"),
            ("SCENT-SET 雙油組", FONT_ZH_BOLD, 32, TERRA, 0.055, 0.234, "tl"),
            ("85 折 · morene.com.tw", FONT_ZH, 34, BLACK, 0.055, 0.296, "tl"),
            ("個人簡介連結 ↑", FONT_ZH, 28, BLACK, 0.055, 0.370, "tl"),
            ("DOUBLE OIL · W33", FONT_EN, 18, BLACK, 0.055, 0.944, "tl"),
        ],
    )

    print("W33 完成。")


# =====================
# W34 型別小卡 + 收尾
# =====================
def make_w34():
    print("\n=== W34 深掘 + 收尾 ===")

    # INTJ 型別小卡 1080x1350 — 深墨底 + 芥末對比 (同 W29 格式)
    print("W34 IG INTJ 型別小卡...")
    save_and_dual(
        "W34", "IG", "MORENE_W34_INTJ.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=MUSTARD,  # 下半底色
        bottle_name="乳香",
        bottle_scale=0.73,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.92,
        shadow_offset_x=70, shadow_offset_y=30,
        shadow_blur=50, shadow_opacity=0.22,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, CREAM, 0.055, 0.048, "tl"),
            # 型號大字
            ("INTJ", FONT_EN_BOLD, 130, MUSTARD, 0.055, 0.095, "tl"),
            ("遠方的建築師", FONT_ZH, 44, CREAM, 0.055, 0.267, "tl"),
            # 文學引用 (查證: 王維《終南別業》)
            ("行到水窮處,坐看雲起時。", FONT_ZH, 21, CREAM, 0.055, 0.334, "tl"),
            ("— 王維《終南別業》", FONT_ZH, 17, CREAM, 0.055, 0.368, "tl"),
            # Forer 金句(逐字)
            ("腦中永遠有一張別人還看不到的藍圖。", FONT_ZH, 22, BLACK, 0.055, 0.470, "tl"),
            ("獨來獨往不是孤僻,是大多數對話", FONT_ZH, 22, BLACK, 0.055, 0.510, "tl"),
            ("跟不上妳想去的地方。", FONT_ZH, 22, BLACK, 0.055, 0.550, "tl"),
            # 命定油
            ("乳香 · 命定香氣  NT$880", FONT_ZH, 20, BLACK, 0.055, 0.642, "tl"),
            ("FRANKINCENSE · NT · WOODY RESIN", FONT_EN, 19, BLACK, 0.055, 0.946, "tl"),
        ],
    )

    # ESFP 型別小卡 1080x1350 — 橘底 + 深墨大字 (同 W29 ENFP 格式)
    print("W34 IG ESFP 型別小卡...")
    save_and_dual(
        "W34", "IG", "MORENE_W34_ESFP.png",
        canvas_w=1080, canvas_h=1350,
        bg_hex=ORANGE,
        bottle_name="甜橙",
        bottle_scale=0.73,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.92,
        shadow_offset_x=70, shadow_offset_y=30,
        shadow_blur=50, shadow_opacity=0.18,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("ESFP", FONT_EN_BOLD, 130, BLACK, 0.055, 0.095, "tl"),
            ("天生的舞台中心", FONT_ZH, 44, BLACK, 0.055, 0.267, "tl"),
            # 文學引用 (查證: 李白《月下獨酌》)
            ("舉杯邀明月,對影成三人。", FONT_ZH, 21, BLACK, 0.055, 0.334, "tl"),
            ("行樂須及春。", FONT_ZH, 21, BLACK, 0.055, 0.368, "tl"),
            ("— 李白《月下獨酌·其一》", FONT_ZH, 17, BLACK, 0.055, 0.403, "tl"),
            # Forer 金句(逐字)
            ("走到哪歡笑到哪,最懂怎麼讓當下變難忘。", FONT_ZH, 22, BLACK, 0.055, 0.490, "tl"),
            ("看似只顧玩樂,", FONT_ZH, 22, BLACK, 0.055, 0.530, "tl"),
            ("其實比誰都珍惜「在一起」的時光。", FONT_ZH, 22, BLACK, 0.055, 0.570, "tl"),
            # 命定油
            ("甜橙 · 命定香氣  NT$680", FONT_ZH, 20, BLACK, 0.055, 0.660, "tl"),
            ("SWEET ORANGE · SP · CITRUS", FONT_EN, 19, BLACK, 0.055, 0.946, "tl"),
        ],
    )

    # FB 收尾 1080x1080 — 奶油底
    print("W34 FB 收尾...")
    save_and_dual(
        "W34", "FB", "MORENE_W34_FB_closing.png",
        canvas_w=1080, canvas_h=1080,
        bg_hex="#EDE7DC",
        bottle_name="甜橙",
        bottle_scale=0.70,
        bottle_x_frac=0.72,
        bottle_bottom_frac=0.95,
        shadow_offset_x=65, shadow_offset_y=28,
        shadow_blur=44, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 38, BLACK, 0.055, 0.048, "tl"),
            ("謝謝一起", FONT_ZH, 56, BLACK, 0.055, 0.108, "tl"),
            ("玩深化的妳們", FONT_ZH, 56, TERRA, 0.055, 0.196, "tl"),
            ("命定三支 SCENT-TRIO 88折", FONT_ZH, 26, BLACK, 0.055, 0.300, "tl"),
            ("雙油 SCENT-SET 85折", FONT_ZH, 26, BLACK, 0.055, 0.348, "tl"),
            ("首購 MORENEHELLO", FONT_ZH, 26, BLACK, 0.055, 0.396, "tl"),
            ("morene.com.tw · SCENT PERSONALITY W34", FONT_EN, 17, BLACK, 0.055, 0.944, "tl"),
        ],
    )

    # Reels 封面 1080x1920 — 芥末底 + 甜橙瓶
    print("W34 Reels cover...")
    save_and_dual(
        "W34", "Reels", "MORENE_W34_Reels_cover.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=MUSTARD,
        bottle_name="甜橙",
        bottle_scale=0.68,
        bottle_x_frac=0.65,
        bottle_bottom_frac=0.88,
        shadow_offset_x=68, shadow_offset_y=30,
        shadow_blur=46, shadow_opacity=0.16,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("測完", FONT_ZH, 120, BLACK, 0.055, 0.076, "tl"),
            ("之後呢?", FONT_ZH, 88, TERRA, 0.055, 0.210, "tl"),
            ("用法 → 雙油 → 帶回家", FONT_ZH, 34, BLACK, 0.055, 0.330, "tl"),
            ("SCENT PERSONALITY W34", FONT_EN, 22, BLACK, 0.055, 0.944, "tl"),
        ],
    )

    # Stories ×3
    # S1: 活動倒數 — 深墨底
    print("W34 Stories S1...")
    save_and_dual(
        "W34", "Stories", "MORENE_W34_S1.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=BLACK,
        bottle_name="乳香",
        bottle_scale=0.50,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.78,
        shadow_offset_x=42, shadow_offset_y=18,
        shadow_blur=30, shadow_opacity=0.10,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, CREAM, 0.055, 0.040, "tl"),
            ("STORIES · W34", FONT_EN, 14, "#8C8079", 0.055, 0.092, "tl"),
            ("深化檔期最後一週", FONT_ZH, 44, CREAM, 0.055, 0.130, "tl"),
            ("命定組合限時優惠", FONT_ZH, 44, MUSTARD, 0.055, 0.210, "tl"),
            ("SCENT-TRIO 88折 / SCENT-SET 85折", FONT_ZH, 22, CREAM, 0.055, 0.310, "tl"),
            ("個人簡介連結 ↑", FONT_ZH, 32, CREAM, 0.055, 0.392, "tl"),
            ("morene.com.tw · W34", FONT_EN, 18, "#8C8079", 0.055, 0.944, "tl"),
        ],
    )

    # S2: 命定組合導購 — 陶土底
    print("W34 Stories S2...")
    save_and_dual(
        "W34", "Stories", "MORENE_W34_S2.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=TERRA,
        bottle_name="甜橙",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.80,
        shadow_offset_x=44, shadow_offset_y=18,
        shadow_blur=32, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, CREAM, 0.055, 0.040, "tl"),
            ("找到妳的命定香氣了嗎?", FONT_ZH, 40, CREAM, 0.055, 0.130, "tl"),
            ("命定三支  SCENT-TRIO", FONT_ZH, 34, MUSTARD, 0.055, 0.228, "tl"),
            ("88 折優惠", FONT_ZH, 52, CREAM, 0.055, 0.294, "tl"),
            ("個人簡介連結 ↑", FONT_ZH, 30, CREAM, 0.055, 0.380, "tl"),
            ("morene.com.tw", FONT_EN, 20, "#CBA98A", 0.055, 0.944, "tl"),
        ],
    )

    # S3: 截圖標記 — 芥末底
    print("W34 Stories S3...")
    save_and_dual(
        "W34", "Stories", "MORENE_W34_S3.png",
        canvas_w=1080, canvas_h=1920,
        bg_hex=MUSTARD,
        bottle_name="乳香",
        bottle_scale=0.52,
        bottle_x_frac=0.68,
        bottle_bottom_frac=0.80,
        shadow_offset_x=44, shadow_offset_y=18,
        shadow_blur=32, shadow_opacity=0.14,
        text_lines=[
            ("MORENE", FONT_EN_BOLD, 42, BLACK, 0.055, 0.040, "tl"),
            ("截圖你的命定香氣型", FONT_ZH, 40, BLACK, 0.055, 0.130, "tl"),
            ("標記 @morene_organic", FONT_ZH_BOLD, 28, TERRA, 0.055, 0.228, "tl"),
            ("我看到每一則 💛", FONT_ZH, 34, BLACK, 0.055, 0.296, "tl"),
            ("#MORENE #香氣人格 #香氣儀式", FONT_ZH, 22, BLACK, 0.055, 0.380, "tl"),
            ("W34 · SCENT PERSONALITY", FONT_EN, 18, "#8C8079", 0.055, 0.944, "tl"),
        ],
    )

    print("W34 完成。")


# =====================
# 主程式
# =====================
if __name__ == "__main__":
    print("MORENE W31–W34 圖卡生成開始...")
    make_w31()
    make_w32()
    make_w33()
    make_w34()
    print("\n全部完成。")
