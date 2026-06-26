from __future__ import annotations

import math
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont


ROOT = Path("projects/scene-packs/scene_overlay_vfx_01")
BACKGROUNDS = ROOT / "backgrounds"
LAYERS = ROOT / "layers"
PROPS = ROOT / "props"
PREVIEWS = ROOT / "previews"
SIZE = (1920, 1080)


def rgba(size=SIZE, color=(0, 0, 0, 0)) -> Image.Image:
    return Image.new("RGBA", size, color)


def font(size: int):
    for name in ("msyh.ttc", "simhei.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def paste_center(canvas: Image.Image, path: Path, anchor: dict, scale: float = 1.0) -> None:
    img = Image.open(path).convert("RGBA")
    final = scale * float(anchor.get("scale", 1.0))
    w = max(1, int(img.width * final))
    h = max(1, int(img.height * final))
    img = img.resize((w, h), Image.Resampling.LANCZOS)
    canvas.alpha_composite(img, (int(anchor["x"] * SIZE[0] - w / 2), int(anchor["y"] * SIZE[1] - h / 2)))


def draw_stage(path: Path, mode: str = "neutral") -> None:
    img = rgba(color=(230, 226, 214, 255))
    d = ImageDraw.Draw(img)
    if mode == "dark":
        d.rectangle((0, 0, 1920, 1080), fill=(35, 38, 46, 255))
        d.rectangle((0, 700, 1920, 1080), fill=(54, 50, 52, 255))
    elif mode == "bright":
        d.rectangle((0, 0, 1920, 1080), fill=(238, 232, 205, 255))
        d.rectangle((0, 700, 1920, 1080), fill=(198, 184, 144, 255))
    elif mode == "speed":
        d.rectangle((0, 0, 1920, 1080), fill=(78, 92, 120, 255))
        for i in range(-300, 2200, 120):
            d.polygon([(i, 0), (i + 70, 0), (i - 230, 1080), (i - 300, 1080)], fill=(105, 124, 158, 255))
    else:
        d.rectangle((0, 0, 1920, 700), fill=(216, 220, 224, 255))
        d.rectangle((0, 700, 1920, 1080), fill=(164, 154, 142, 255))
        for y in range(760, 1080, 88):
            d.line((0, y, 1920, y), fill=(128, 118, 108, 255), width=5)
        for x in range(-120, 2100, 240):
            d.line((x, 700, x + 180, 1080), fill=(128, 118, 108, 255), width=5)
    img.save(path)


def save_dim_overlay(path: Path) -> None:
    img = rgba()
    ImageDraw.Draw(img).rectangle((0, 0, 1920, 1080), fill=(0, 0, 0, 120))
    img.save(path)


def save_vignette(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    for i in range(16):
        alpha = int(10 + i * 8)
        inset = i * 34
        d.rectangle((inset, inset, 1920 - inset, 1080 - inset), outline=(0, 0, 0, alpha), width=34)
    img.save(path)


def save_speed_lines(path: Path, radial: bool = False) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    if radial:
        cx, cy = 960, 540
        for i in range(44):
            angle = i * math.tau / 44
            inner = 190 + (i % 4) * 28
            outer = 1050
            x1 = cx + math.cos(angle) * inner
            y1 = cy + math.sin(angle) * inner
            x2 = cx + math.cos(angle) * outer
            y2 = cy + math.sin(angle) * outer
            d.line((x1, y1, x2, y2), fill=(255, 255, 255, 165), width=8 + (i % 3) * 3)
    else:
        for y in range(70, 1080, 74):
            d.polygon([(0, y), (1420, y - 50), (1920, y - 34), (520, y + 38)], fill=(255, 255, 255, 140))
            d.line((80, y + 20, 1780, y - 38), fill=(35, 45, 70, 140), width=5)
    img.save(path)


def save_focus_spotlight(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 1920, 1080), fill=(0, 0, 0, 132))
    d.ellipse((560, 230, 1360, 940), fill=(0, 0, 0, 0), outline=(255, 244, 190, 150), width=10)
    img.save(path)


def save_portal(path: Path, close: bool = False) -> None:
    img = rgba((680, 760) if close else (460, 560))
    d = ImageDraw.Draw(img)
    w, h = img.size
    for i, color in enumerate(((92, 42, 150, 120), (158, 68, 220, 150), (240, 125, 255, 190), (255, 235, 255, 145))):
        inset = 18 + i * 36
        d.ellipse((inset, inset, w - inset, h - inset), fill=color, outline=(245, 210, 255, 170), width=8)
    for x in range(w // 5, w - w // 5, max(1, w // 8)):
        d.arc((x - w // 4, h // 6, x + w // 4, h - h // 6), 245, 85, fill=(255, 255, 255, 95), width=6)
    img.save(path)


def save_transition_wipe(path: Path, style: str) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    if style == "black":
        d.rectangle((0, 0, 1920, 1080), fill=(0, 0, 0, 255))
    elif style == "white_flash":
        d.rectangle((0, 0, 1920, 1080), fill=(255, 255, 255, 230))
    else:
        for i in range(-260, 2200, 160):
            d.polygon([(i, 0), (i + 120, 0), (i - 260, 1080), (i - 380, 1080)], fill=(18, 18, 22, 235))
    img.save(path)


def save_dialogue_bubble(path: Path, side: str) -> None:
    img = rgba((640, 340))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((24, 24, 616, 260), radius=38, fill=(255, 252, 235, 245), outline=(28, 28, 30, 255), width=7)
    if side == "left":
        d.polygon([(100, 252), (42, 322), (172, 262)], fill=(255, 252, 235, 245), outline=(28, 28, 30, 255))
    else:
        d.polygon([(540, 252), (598, 322), (468, 262)], fill=(255, 252, 235, 245), outline=(28, 28, 30, 255))
    for y, w in ((76, 420), (126, 500), (176, 310)):
        d.rounded_rectangle((82, y, 82 + w, y + 24), radius=8, fill=(42, 42, 46, 255))
    img.save(path)


def save_reaction_icon(path: Path, kind: str) -> None:
    img = rgba((320, 320))
    d = ImageDraw.Draw(img)
    if kind == "exclaim":
        d.polygon([(160, 20), (206, 136), (292, 72), (230, 174), (286, 260), (178, 220), (120, 300), (110, 198), (26, 222), (90, 142), (50, 54)], fill=(255, 220, 62, 255), outline=(42, 34, 28, 255))
        d.rectangle((150, 92, 170, 198), fill=(42, 34, 28, 255))
        d.ellipse((140, 216, 180, 256), fill=(42, 34, 28, 255))
    elif kind == "question":
        d.ellipse((42, 38, 278, 274), fill=(120, 200, 255, 240), outline=(28, 36, 44, 255), width=8)
        d.arc((106, 86, 214, 178), 195, 35, fill=(28, 36, 44, 255), width=18)
        d.line((166, 174, 166, 210), fill=(28, 36, 44, 255), width=16)
        d.ellipse((148, 226, 184, 262), fill=(28, 36, 44, 255))
    else:
        d.ellipse((52, 52, 268, 268), fill=(255, 120, 120, 240), outline=(48, 32, 32, 255), width=8)
        d.rectangle((98, 142, 222, 172), fill=(255, 245, 230, 255))
        d.rectangle((145, 80, 175, 235), fill=(255, 245, 230, 255))
    img.save(path)


def save_order_popup(path: Path, warning: bool = False) -> None:
    img = rgba((720, 460))
    d = ImageDraw.Draw(img)
    fill = (44, 28, 36, 246) if warning else (252, 250, 238, 246)
    outline = (240, 80, 90, 255) if warning else (28, 28, 32, 255)
    d.rounded_rectangle((20, 20, 700, 440), radius=34, fill=fill, outline=outline, width=8)
    d.rounded_rectangle((58, 58, 662, 136), radius=18, fill=(255, 186, 64, 255), outline=(28, 28, 32, 255), width=5)
    if warning:
        d.polygon([(104, 180), (164, 300), (44, 300)], fill=(255, 212, 72, 255), outline=(20, 20, 22, 255))
        d.rectangle((100, 220, 112, 272), fill=(20, 20, 22, 255))
        d.ellipse((94, 282, 118, 306), fill=(20, 20, 22, 255))
    for y, w in ((184, 430), (250, 520), (318, 330)):
        d.rounded_rectangle((210, y, 210 + w, y + 26), radius=8, fill=(40, 40, 44, 255) if not warning else (255, 240, 220, 255))
    img.save(path)


def save_comic_burst(path: Path) -> None:
    img = rgba((720, 520))
    d = ImageDraw.Draw(img)
    cx, cy = 360, 260
    points = []
    for i in range(32):
        angle = i * math.tau / 32
        r = 250 if i % 2 == 0 else 178
        points.append((cx + math.cos(angle) * r, cy + math.sin(angle) * r))
    d.polygon(points, fill=(255, 238, 94, 250), outline=(44, 34, 24, 255))
    d.ellipse((230, 150, 490, 370), fill=(255, 255, 246, 245), outline=(44, 34, 24, 255), width=8)
    img.save(path)


def save_contact_sheet(path: Path, assets: list[tuple[str, Path]]) -> None:
    thumb = (180, 150)
    margin = 24
    label_h = 30
    cols = 4
    rows = (len(assets) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (thumb[0] + margin) + margin, rows * (thumb[1] + label_h + margin) + margin), (232, 228, 220))
    d = ImageDraw.Draw(sheet)
    fnt = font(15)
    for i, (label, asset_path) in enumerate(assets):
        x = margin + (i % cols) * (thumb[0] + margin)
        y = margin + (i // cols) * (thumb[1] + label_h + margin)
        checker = Image.new("RGB", thumb, (250, 250, 250))
        cd = ImageDraw.Draw(checker)
        for yy in range(0, thumb[1], 16):
            for xx in range((yy // 16) % 2 * 16, thumb[0], 32):
                cd.rectangle((xx, yy, xx + 15, yy + 15), fill=(220, 220, 220))
        sheet.paste(checker, (x, y))
        img = Image.open(asset_path).convert("RGBA")
        img.thumbnail(thumb, Image.Resampling.LANCZOS)
        sheet.paste(img, (x + (thumb[0] - img.width) // 2, y + (thumb[1] - img.height) // 2), img)
        d.rectangle((x, y, x + thumb[0], y + thumb[1]), outline=(70, 70, 70), width=2)
        d.text((x, y + thumb[1] + 8), label, fill=(20, 20, 20), font=fnt)
    sheet.save(path)


def scene_yaml() -> dict:
    return {
        "scene_id": "scene_overlay_vfx_01",
        "name": "universal overlay transition and reaction VFX pack",
        "version": "0.1.0",
        "format": {"width": 1920, "height": 1080},
        "backgrounds": {
            "neutral_stage": "backgrounds/neutral_stage.png",
            "dark_stage": "backgrounds/dark_stage.png",
            "bright_stage": "backgrounds/bright_stage.png",
            "speed_stage": "backgrounds/speed_stage.png",
        },
        "layers": {
            "background": ["backgrounds/neutral_stage.png"],
            "behind_character": [],
            "front_character": [],
            "overlay": ["layers/dim_overlay.png", "layers/vignette_overlay.png"],
        },
        "anchors": {
            "screen_center": {"x": 0.50, "y": 0.50, "scale": 1.0},
            "screen_top": {"x": 0.50, "y": 0.18, "scale": 1.0},
            "screen_bottom": {"x": 0.50, "y": 0.82, "scale": 1.0},
            "left_dialogue": {"x": 0.30, "y": 0.28, "scale": 1.0},
            "right_dialogue": {"x": 0.70, "y": 0.28, "scale": 1.0},
            "left_reaction": {"x": 0.30, "y": 0.32, "scale": 1.0},
            "right_reaction": {"x": 0.70, "y": 0.32, "scale": 1.0},
            "order_popup_center": {"x": 0.50, "y": 0.42, "scale": 1.0},
            "portal_center": {"x": 0.50, "y": 0.54, "scale": 1.0},
            "focus_center": {"x": 0.50, "y": 0.50, "scale": 1.0},
            "wipe_center": {"x": 0.50, "y": 0.50, "scale": 1.0},
            "burst_center": {"x": 0.50, "y": 0.42, "scale": 1.0},
        },
        "props": {
            "speed_lines": {
                "label": "speed lines",
                "variants": {"horizontal": "props/speed_lines_horizontal.png", "radial": "props/speed_lines_radial.png"},
                "default_anchor": "screen_center",
                "pivot": "center",
                "variant_scales": {"horizontal": 1.0, "radial": 1.0},
            },
            "portal": {
                "label": "portal transition",
                "variants": {"open": "props/portal_open.png", "close": "props/portal_close.png"},
                "default_anchor": "portal_center",
                "pivot": "center",
                "variant_scales": {"open": 1.0, "close": 0.95},
            },
            "transition_wipe": {
                "label": "transition wipe",
                "variants": {"black": "props/wipe_black.png", "white_flash": "props/wipe_white_flash.png", "diagonal": "props/wipe_diagonal.png"},
                "default_anchor": "wipe_center",
                "pivot": "center",
                "variant_scales": {"black": 1.0, "white_flash": 1.0, "diagonal": 1.0},
            },
            "dialogue_bubble": {
                "label": "dialogue bubble",
                "variants": {"left": "props/dialogue_bubble_left.png", "right": "props/dialogue_bubble_right.png"},
                "default_anchor": "left_dialogue",
                "pivot": "center",
                "variant_scales": {"left": 0.9, "right": 0.9},
            },
            "reaction_icon": {
                "label": "reaction icon",
                "variants": {"exclaim": "props/reaction_exclaim.png", "question": "props/reaction_question.png", "plus": "props/reaction_plus.png"},
                "default_anchor": "left_reaction",
                "pivot": "center",
                "variant_scales": {"exclaim": 0.72, "question": 0.72, "plus": 0.72},
            },
            "order_popup": {
                "label": "order popup",
                "variants": {"normal": "props/order_popup_normal.png", "warning": "props/order_popup_warning.png"},
                "default_anchor": "order_popup_center",
                "pivot": "center",
                "variant_scales": {"normal": 0.82, "warning": 0.82},
            },
            "focus_spotlight": {
                "label": "focus spotlight",
                "variants": {"spot": "props/focus_spotlight.png"},
                "default_anchor": "focus_center",
                "pivot": "center",
                "variant_scales": {"spot": 1.0},
            },
            "comic_burst": {
                "label": "comic burst",
                "variants": {"burst": "props/comic_burst.png"},
                "default_anchor": "burst_center",
                "pivot": "center",
                "variant_scales": {"burst": 0.9},
            },
        },
        "supported_actions": [
            "show_speed_lines",
            "show_radial_impact",
            "open_portal_transition",
            "white_flash",
            "black_cut",
            "diagonal_wipe",
            "show_dialogue_bubble",
            "reaction_pop",
            "show_order_popup",
            "show_warning_popup",
            "focus_spotlight",
            "comic_burst",
        ],
        "action_templates": {
            "show_speed_lines": {"duration": 0.6, "prop": "speed_lines", "prop_sequence": [{"time": 0.0, "variant": "horizontal", "anchor": "screen_center", "motion": "slide_left"}]},
            "show_radial_impact": {"duration": 0.5, "prop": "speed_lines", "prop_sequence": [{"time": 0.0, "variant": "radial", "anchor": "screen_center", "motion": "scale_burst"}]},
            "open_portal_transition": {"duration": 1.0, "prop": "portal", "prop_sequence": [{"time": 0.0, "variant": "open", "anchor": "portal_center", "motion": "pulse"}]},
            "white_flash": {"duration": 0.35, "prop": "transition_wipe", "prop_sequence": [{"time": 0.0, "variant": "white_flash", "anchor": "wipe_center", "motion": "flash"}]},
            "black_cut": {"duration": 0.35, "prop": "transition_wipe", "prop_sequence": [{"time": 0.0, "variant": "black", "anchor": "wipe_center"}]},
            "diagonal_wipe": {"duration": 0.65, "prop": "transition_wipe", "prop_sequence": [{"time": 0.0, "variant": "diagonal", "anchor": "wipe_center", "motion": "slide_right"}]},
            "show_dialogue_bubble": {"duration": 0.8, "prop": "dialogue_bubble", "prop_sequence": [{"time": 0.0, "variant": "left", "anchor": "left_dialogue", "motion": "pop_in"}]},
            "reaction_pop": {"duration": 0.45, "prop": "reaction_icon", "prop_sequence": [{"time": 0.0, "variant": "exclaim", "anchor": "left_reaction", "motion": "pop_in"}]},
            "show_order_popup": {"duration": 0.8, "prop": "order_popup", "prop_sequence": [{"time": 0.0, "variant": "normal", "anchor": "order_popup_center", "motion": "pop_in"}]},
            "show_warning_popup": {"duration": 0.8, "prop": "order_popup", "prop_sequence": [{"time": 0.0, "variant": "warning", "anchor": "order_popup_center", "motion": "shake"}]},
            "focus_spotlight": {"duration": 0.8, "prop": "focus_spotlight", "prop_sequence": [{"time": 0.0, "variant": "spot", "anchor": "focus_center", "motion": "fade_in"}]},
            "comic_burst": {"duration": 0.55, "prop": "comic_burst", "prop_sequence": [{"time": 0.0, "variant": "burst", "anchor": "burst_center", "motion": "scale_burst"}]},
        },
    }


def render_base(data: dict, bg_key: str = "neutral_stage") -> Image.Image:
    return Image.open(ROOT / data["backgrounds"][bg_key]).convert("RGBA")


def render_previews(data: dict) -> None:
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    fnt = font(34)
    small = font(24)
    anchors = data["anchors"]

    canvas = render_base(data)
    draw = ImageDraw.Draw(canvas)
    for anchor_id, anchor in anchors.items():
        x = int(anchor["x"] * SIZE[0])
        y = int(anchor["y"] * SIZE[1])
        draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(255, 90, 50, 255), outline=(0, 0, 0, 255), width=3)
        draw.text((x + 12, y - 22), anchor_id, fill=(255, 244, 190, 255), font=small, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_wide.png")

    canvas = render_base(data, bg_key="speed_stage")
    paste_center(canvas, PROPS / "speed_lines_horizontal.png", anchors["screen_center"], 1.0)
    paste_center(canvas, PROPS / "speed_lines_radial.png", anchors["screen_center"], 1.0)
    ImageDraw.Draw(canvas).text((60, 60), "speed overlays", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_speed_lines.png")

    canvas = render_base(data, bg_key="dark_stage")
    paste_center(canvas, PROPS / "portal_open.png", anchors["portal_center"], 1.0)
    paste_center(canvas, PROPS / "wipe_diagonal.png", anchors["wipe_center"], 1.0)
    ImageDraw.Draw(canvas).text((60, 60), "portal + diagonal wipe", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_portal_wipe.png")

    canvas = render_base(data)
    paste_center(canvas, PROPS / "dialogue_bubble_left.png", anchors["left_dialogue"], 0.9)
    paste_center(canvas, PROPS / "dialogue_bubble_right.png", anchors["right_dialogue"], 0.9)
    paste_center(canvas, PROPS / "reaction_exclaim.png", anchors["left_reaction"], 0.72)
    paste_center(canvas, PROPS / "reaction_question.png", anchors["right_reaction"], 0.72)
    ImageDraw.Draw(canvas).text((60, 60), "dialogue + reactions", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_dialogue_reactions.png")

    canvas = render_base(data)
    paste_center(canvas, PROPS / "order_popup_normal.png", anchors["order_popup_center"], 0.82)
    paste_center(canvas, PROPS / "reaction_plus.png", anchors["right_reaction"], 0.72)
    ImageDraw.Draw(canvas).text((60, 60), "order popup", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_order_popup.png")

    canvas = render_base(data, bg_key="dark_stage")
    paste_center(canvas, PROPS / "focus_spotlight.png", anchors["focus_center"], 1.0)
    paste_center(canvas, PROPS / "comic_burst.png", anchors["burst_center"], 0.9)
    ImageDraw.Draw(canvas).text((60, 60), "focus + comic burst", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_focus_burst.png")

    canvas = render_base(data, bg_key="bright_stage")
    paste_center(canvas, PROPS / "wipe_white_flash.png", anchors["wipe_center"], 1.0)
    paste_center(canvas, PROPS / "order_popup_warning.png", anchors["order_popup_center"], 0.82)
    ImageDraw.Draw(canvas).text((60, 60), "flash + warning popup", fill=(32, 28, 24, 255), font=fnt, stroke_width=3, stroke_fill=(255, 255, 255, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_flash_warning.png")

    save_contact_sheet(
        PREVIEWS / "overlay_vfx_contact_sheet.png",
        [
            ("speed_horizontal", PROPS / "speed_lines_horizontal.png"),
            ("speed_radial", PROPS / "speed_lines_radial.png"),
            ("portal_open", PROPS / "portal_open.png"),
            ("wipe_diagonal", PROPS / "wipe_diagonal.png"),
            ("dialogue_left", PROPS / "dialogue_bubble_left.png"),
            ("dialogue_right", PROPS / "dialogue_bubble_right.png"),
            ("reaction_exclaim", PROPS / "reaction_exclaim.png"),
            ("reaction_question", PROPS / "reaction_question.png"),
            ("order_popup", PROPS / "order_popup_normal.png"),
            ("warning_popup", PROPS / "order_popup_warning.png"),
            ("focus_spotlight", PROPS / "focus_spotlight.png"),
            ("comic_burst", PROPS / "comic_burst.png"),
        ],
    )


def main() -> None:
    for folder in (BACKGROUNDS, LAYERS, PROPS, PREVIEWS):
        folder.mkdir(parents=True, exist_ok=True)

    draw_stage(BACKGROUNDS / "neutral_stage.png")
    draw_stage(BACKGROUNDS / "dark_stage.png", "dark")
    draw_stage(BACKGROUNDS / "bright_stage.png", "bright")
    draw_stage(BACKGROUNDS / "speed_stage.png", "speed")
    save_dim_overlay(LAYERS / "dim_overlay.png")
    save_vignette(LAYERS / "vignette_overlay.png")

    save_speed_lines(PROPS / "speed_lines_horizontal.png")
    save_speed_lines(PROPS / "speed_lines_radial.png", radial=True)
    save_portal(PROPS / "portal_open.png")
    save_portal(PROPS / "portal_close.png", close=True)
    save_transition_wipe(PROPS / "wipe_black.png", "black")
    save_transition_wipe(PROPS / "wipe_white_flash.png", "white_flash")
    save_transition_wipe(PROPS / "wipe_diagonal.png", "diagonal")
    save_dialogue_bubble(PROPS / "dialogue_bubble_left.png", "left")
    save_dialogue_bubble(PROPS / "dialogue_bubble_right.png", "right")
    save_reaction_icon(PROPS / "reaction_exclaim.png", "exclaim")
    save_reaction_icon(PROPS / "reaction_question.png", "question")
    save_reaction_icon(PROPS / "reaction_plus.png", "plus")
    save_order_popup(PROPS / "order_popup_normal.png")
    save_order_popup(PROPS / "order_popup_warning.png", warning=True)
    save_focus_spotlight(PROPS / "focus_spotlight.png")
    save_comic_burst(PROPS / "comic_burst.png")

    data = scene_yaml()
    (ROOT / "scene.yaml").write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    render_previews(data)
    print(ROOT)


if __name__ == "__main__":
    main()
