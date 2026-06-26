from __future__ import annotations

from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont


ROOT = Path("projects/scene-packs/scene_battlefield_01")
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


def draw_actor(draw: ImageDraw.ImageDraw, anchor: dict, label: str, color: tuple[int, int, int, int], fnt) -> None:
    x = int(anchor["x"] * SIZE[0])
    y = int(anchor["y"] * SIZE[1])
    scale = float(anchor.get("scale", 1.0))
    body_w = int(150 * scale)
    body_h = int(360 * scale)
    top = y - body_h
    left = x - body_w // 2
    draw.rounded_rectangle((left, top, left + body_w, y), radius=20, fill=color, outline=(16, 16, 18, 255), width=6)
    draw.ellipse((x - 46, top - 64, x + 46, top + 24), fill=(255, 224, 184, 255), outline=(16, 16, 18, 255), width=6)
    draw.text((left - 8, y + 8), label, fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))


def draw_battlefield_background(path: Path) -> None:
    img = rgba(color=(62, 58, 64, 255))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 1920, 1080), fill=(56, 54, 64, 255))
    d.rectangle((0, 0, 1920, 380), fill=(92, 88, 104, 255))
    d.ellipse((-240, 120, 360, 500), fill=(70, 74, 74, 255))
    d.ellipse((1540, 90, 2140, 500), fill=(66, 70, 72, 255))
    d.rectangle((0, 380, 1920, 720), fill=(104, 92, 82, 255))
    d.rectangle((0, 720, 1920, 1080), fill=(94, 82, 72, 255))
    for y in range(780, 1080, 88):
        d.line((0, y, 1920, y), fill=(66, 58, 54, 255), width=5)
    for x in range(-120, 2100, 230):
        d.line((x, 720, x + 170, 1080), fill=(66, 58, 54, 255), width=5)

    # Ruined pillars and crater.
    for x, h in ((170, 300), (390, 210), (1390, 260), (1650, 330)):
        d.rounded_rectangle((x, 360, x + 100, 740), radius=12, fill=(114, 106, 100, 255), outline=(38, 34, 34, 255), width=7)
        d.polygon([(x - 20, 360), (x + 120, 360), (x + 92, 300 + h // 10), (x + 8, 330 + h // 12)], fill=(132, 124, 116, 255), outline=(38, 34, 34, 255))
    d.ellipse((700, 680, 1220, 900), fill=(72, 62, 56, 255), outline=(44, 38, 34, 255), width=8)
    d.ellipse((790, 720, 1130, 850), fill=(52, 46, 44, 255))
    for pts in (
        [(895, 735), (850, 650), (930, 705), (970, 605), (1000, 720)],
        [(1050, 750), (1170, 690), (1100, 790), (1210, 825)],
        [(760, 810), (650, 850), (780, 875)],
    ):
        d.line(pts, fill=(36, 32, 32, 255), width=8, joint="curve")

    # Distant banners.
    for x, color in ((560, (170, 64, 60, 255)), (1280, (74, 112, 172, 255))):
        d.rectangle((x, 350, x + 28, 650), fill=(58, 44, 36, 255))
        d.polygon([(x + 28, 365), (x + 190, 420), (x + 28, 475)], fill=color, outline=(38, 34, 34, 255))
    img.save(path)


def crop_bg(source: Path, target: Path, box: tuple[int, int, int, int]) -> None:
    Image.open(source).convert("RGBA").crop(box).resize(SIZE, Image.Resampling.LANCZOS).save(target)


def save_layer_rocks(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    for box in ((95, 855, 310, 1015), (1460, 840, 1795, 1030), (710, 830, 1220, 950)):
        d.ellipse(box, fill=(68, 60, 56, 230), outline=(34, 30, 28, 255), width=6)
    img.save(path)


def save_layer_smoke(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    for box in ((120, 300, 440, 570), (1380, 285, 1780, 600), (760, 420, 1160, 690)):
        d.ellipse(box, fill=(120, 120, 125, 54))
    img.save(path)


def save_explosion(path: Path, close: bool = False) -> None:
    img = rgba((650, 650) if close else (420, 420))
    d = ImageDraw.Draw(img)
    w, h = img.size
    cx, cy = w // 2, h // 2
    outer = []
    inner = []
    for i in range(16):
        angle = i * 3.14159 / 8
        r = w * (0.46 if i % 2 == 0 else 0.27)
        outer.append((cx + int(__import__("math").cos(angle) * r), cy + int(__import__("math").sin(angle) * r)))
        r2 = w * (0.29 if i % 2 == 0 else 0.15)
        inner.append((cx + int(__import__("math").cos(angle) * r2), cy + int(__import__("math").sin(angle) * r2)))
    d.polygon(outer, fill=(240, 82, 48, 225), outline=(72, 38, 28, 255))
    d.polygon(inner, fill=(255, 220, 78, 245), outline=(120, 62, 36, 255))
    d.ellipse((cx - w // 7, cy - h // 7, cx + w // 7, cy + h // 7), fill=(255, 245, 190, 255))
    img.save(path)


def save_slash(path: Path, close: bool = False) -> None:
    img = rgba((720, 360) if close else (480, 240))
    d = ImageDraw.Draw(img)
    w, h = img.size
    d.polygon([(25, h * 0.72), (w * 0.78, 30), (w - 25, h * 0.22), (w * 0.25, h - 25)], fill=(235, 245, 255, 210), outline=(72, 120, 190, 255))
    d.polygon([(w * 0.12, h * 0.72), (w * 0.75, h * 0.18), (w * 0.84, h * 0.24), (w * 0.27, h * 0.78)], fill=(120, 210, 255, 150))
    img.save(path)


def save_shield(path: Path, close: bool = False) -> None:
    img = rgba((620, 620) if close else (420, 420))
    d = ImageDraw.Draw(img)
    w, h = img.size
    for i, alpha in enumerate((72, 108, 145, 180)):
        inset = 26 + i * 34
        d.ellipse((inset, inset, w - inset, h - inset), outline=(110, 200, 255, alpha), width=16)
    d.ellipse((w * 0.24, h * 0.22, w * 0.76, h * 0.78), fill=(110, 200, 255, 62))
    img.save(path)


def save_impact(path: Path) -> None:
    img = rgba((520, 320))
    d = ImageDraw.Draw(img)
    for i in range(9):
        x = 35 + i * 52
        d.polygon([(x, 160), (x + 34, 95), (x + 70, 160), (x + 34, 225)], fill=(255, 230, 90, 210), outline=(62, 44, 30, 255))
    img.save(path)


def save_dust(path: Path) -> None:
    img = rgba((680, 280))
    d = ImageDraw.Draw(img)
    for box, alpha in (
        ((30, 120, 210, 250), 135),
        ((160, 70, 390, 250), 120),
        ((330, 115, 560, 265), 125),
        ((470, 70, 660, 235), 100),
    ):
        d.ellipse(box, fill=(186, 168, 138, alpha), outline=(98, 82, 66, min(255, alpha + 40)))
    img.save(path)


def save_crack(path: Path) -> None:
    img = rgba((620, 260))
    d = ImageDraw.Draw(img)
    main = [(40, 142), (160, 110), (255, 154), (345, 90), (460, 130), (580, 82)]
    d.line(main, fill=(34, 30, 28, 255), width=14, joint="curve")
    for x, y in main[1:-1]:
        d.line((x, y, x - 44, y + 56), fill=(34, 30, 28, 255), width=8)
        d.line((x, y, x + 38, y + 70), fill=(34, 30, 28, 255), width=7)
    img.save(path)


def save_health_bar(path: Path) -> None:
    img = rgba((760, 150))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((20, 35, 740, 112), radius=22, fill=(38, 38, 42, 245), outline=(18, 18, 20, 255), width=6)
    d.rounded_rectangle((48, 56, 492, 92), radius=12, fill=(220, 66, 64, 255))
    d.rounded_rectangle((500, 56, 710, 92), radius=12, fill=(82, 82, 88, 255))
    img.save(path)


def save_warning_banner(path: Path) -> None:
    img = rgba((680, 330))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((18, 18, 662, 312), radius=30, fill=(48, 32, 36, 245), outline=(245, 194, 72, 255), width=8)
    d.polygon([(92, 70), (152, 205), (30, 205)], fill=(255, 212, 72, 255), outline=(22, 22, 22, 255))
    d.rectangle((88, 112, 100, 174), fill=(22, 22, 22, 255))
    d.ellipse((82, 186, 106, 210), fill=(22, 22, 22, 255))
    for y, width in ((88, 330), (146, 420), (206, 260)):
        d.rounded_rectangle((190, y, 190 + width, y + 26), radius=8, fill=(255, 240, 200, 255))
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
        "scene_id": "scene_battlefield_01",
        "name": "battlefield action and VFX pack",
        "version": "0.1.0",
        "format": {"width": 1920, "height": 1080},
        "backgrounds": {
            "wide": "backgrounds/wide.png",
            "medium": "backgrounds/medium.png",
            "close_crater": "backgrounds/close_crater.png",
            "close_left": "backgrounds/close_left.png",
            "close_right": "backgrounds/close_right.png",
            "close_sky": "backgrounds/close_sky.png",
        },
        "layers": {
            "background": ["backgrounds/wide.png"],
            "behind_character": [],
            "front_character": ["layers/foreground_rocks.png"],
            "overlay": ["layers/background_smoke.png"],
        },
        "anchors": {
            "hero_left": {"x": 0.28, "y": 0.84, "scale": 0.86, "facing": "right"},
            "enemy_right": {"x": 0.72, "y": 0.84, "scale": 0.9, "facing": "left"},
            "center_clash": {"x": 0.50, "y": 0.64, "scale": 1.0},
            "ground_center": {"x": 0.50, "y": 0.82, "scale": 1.0},
            "left_ground": {"x": 0.30, "y": 0.84, "scale": 1.0},
            "right_ground": {"x": 0.70, "y": 0.84, "scale": 1.0},
            "slash_mid": {"x": 0.50, "y": 0.50, "scale": 1.0},
            "explosion_mid": {"x": 0.50, "y": 0.56, "scale": 1.0},
            "shield_left": {"x": 0.31, "y": 0.55, "scale": 1.0},
            "shield_right": {"x": 0.69, "y": 0.55, "scale": 1.0},
            "ui_top": {"x": 0.50, "y": 0.12, "scale": 1.0},
            "warning_center": {"x": 0.50, "y": 0.28, "scale": 1.0},
            "close_insert_center": {"x": 0.50, "y": 0.50, "scale": 1.0},
        },
        "props": {
            "explosion": {
                "label": "explosion burst",
                "variants": {"burst": "props/explosion_burst.png", "close": "props/explosion_close.png"},
                "default_anchor": "explosion_mid",
                "pivot": "center",
                "variant_scales": {"burst": 1.0, "close": 0.95},
            },
            "slash": {
                "label": "slash arc",
                "variants": {"arc": "props/slash_arc.png", "close": "props/slash_close.png"},
                "default_anchor": "slash_mid",
                "pivot": "center",
                "variant_scales": {"arc": 1.0, "close": 0.95},
            },
            "shield": {
                "label": "magic shield",
                "variants": {"bubble": "props/shield_bubble.png", "close": "props/shield_close.png"},
                "default_anchor": "shield_left",
                "pivot": "center",
                "variant_scales": {"bubble": 0.9, "close": 0.95},
            },
            "impact": {
                "label": "impact flash",
                "variants": {"flash": "props/impact_flash.png"},
                "default_anchor": "center_clash",
                "pivot": "center",
                "variant_scales": {"flash": 0.9},
            },
            "dust": {
                "label": "dust cloud",
                "variants": {"cloud": "props/dust_cloud.png"},
                "default_anchor": "ground_center",
                "pivot": "center",
                "variant_scales": {"cloud": 1.0},
            },
            "ground_crack": {
                "label": "ground crack",
                "variants": {"crack": "props/ground_crack.png"},
                "default_anchor": "ground_center",
                "pivot": "center",
                "variant_scales": {"crack": 1.0},
            },
            "health_bar": {
                "label": "combat health bar",
                "variants": {"enemy": "props/health_bar_enemy.png"},
                "default_anchor": "ui_top",
                "pivot": "center",
                "variant_scales": {"enemy": 0.95},
            },
            "warning_banner": {
                "label": "combat warning banner",
                "variants": {"danger": "props/warning_banner.png"},
                "default_anchor": "warning_center",
                "pivot": "center",
                "variant_scales": {"danger": 0.8},
            },
        },
        "supported_actions": [
            "stand",
            "enter_battle",
            "slash_attack",
            "cast_shield",
            "impact_clash",
            "explosion_hit",
            "ground_crack",
            "dust_roll",
            "enemy_health_show",
            "warning_flash",
            "knockback",
            "inspect_close",
        ],
        "action_templates": {
            "enter_battle": {"duration": 1.0, "actor_state_sequence": ["offscreen", "dash", "stand"], "target_anchor": "hero_left"},
            "slash_attack": {
                "duration": 0.8,
                "prop": "slash",
                "prop_sequence": [{"time": 0.0, "variant": "arc", "anchor": "slash_mid", "motion": "sweep_right"}],
            },
            "cast_shield": {
                "duration": 1.0,
                "prop": "shield",
                "prop_sequence": [{"time": 0.0, "variant": "bubble", "anchor": "shield_left", "motion": "pulse"}],
            },
            "impact_clash": {
                "duration": 0.7,
                "prop": "impact",
                "prop_sequence": [{"time": 0.0, "variant": "flash", "anchor": "center_clash", "motion": "pop_in"}],
            },
            "explosion_hit": {
                "duration": 0.9,
                "prop": "explosion",
                "prop_sequence": [{"time": 0.0, "variant": "burst", "anchor": "explosion_mid", "motion": "scale_burst"}],
            },
            "ground_crack": {
                "duration": 0.8,
                "prop": "ground_crack",
                "prop_sequence": [{"time": 0.0, "variant": "crack", "anchor": "ground_center", "motion": "reveal"}],
            },
            "dust_roll": {
                "duration": 0.8,
                "prop": "dust",
                "prop_sequence": [{"time": 0.0, "variant": "cloud", "anchor": "ground_center", "motion": "slide_up"}],
            },
            "enemy_health_show": {
                "duration": 0.8,
                "prop": "health_bar",
                "prop_sequence": [{"time": 0.0, "variant": "enemy", "anchor": "ui_top", "motion": "pop_in"}],
            },
            "warning_flash": {
                "duration": 0.8,
                "prop": "warning_banner",
                "prop_sequence": [{"time": 0.0, "variant": "danger", "anchor": "warning_center", "motion": "shake"}],
            },
            "knockback": {"duration": 0.8, "actor_state_sequence": ["hit", "slide_back", "recover"], "from_anchor": "center_clash", "target_anchor": "right_ground"},
        },
    }


def render_base(data: dict, bg_key: str = "wide", front_layers: bool = True, overlays: bool = True) -> Image.Image:
    canvas = Image.open(ROOT / data["backgrounds"][bg_key]).convert("RGBA")
    if overlays:
        for rel in data["layers"]["overlay"]:
            canvas.alpha_composite(Image.open(ROOT / rel).convert("RGBA"))
    if front_layers:
        for rel in data["layers"]["front_character"]:
            canvas.alpha_composite(Image.open(ROOT / rel).convert("RGBA"))
    return canvas


def render_previews(data: dict) -> None:
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    fnt = font(34)
    small = font(24)
    anchors = data["anchors"]

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    for anchor_id, anchor in anchors.items():
        x = int(anchor["x"] * SIZE[0])
        y = int(anchor["y"] * SIZE[1])
        draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(255, 90, 50, 255), outline=(0, 0, 0, 255), width=3)
        draw.text((x + 12, y - 22), anchor_id, fill=(255, 244, 190, 255), font=small, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.alpha_composite(Image.open(LAYERS / "foreground_rocks.png").convert("RGBA"))
    canvas.convert("RGB").save(PREVIEWS / "preview_wide.png")

    canvas = render_base(data, front_layers=False)
    for prop, anchor, scale in (
        ("slash_arc.png", "slash_mid", 1.0),
        ("explosion_burst.png", "explosion_mid", 0.85),
        ("shield_bubble.png", "shield_left", 0.75),
        ("ground_crack.png", "ground_center", 1.0),
        ("dust_cloud.png", "ground_center", 0.9),
        ("health_bar_enemy.png", "ui_top", 0.95),
    ):
        paste_center(canvas, PROPS / prop, anchors[anchor], scale)
    ImageDraw.Draw(canvas).text((60, 60), "battlefield VFX props", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_props.png")

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    draw_actor(draw, anchors["hero_left"], "hero", (80, 145, 230, 255), fnt)
    draw_actor(draw, anchors["enemy_right"], "enemy", (200, 76, 76, 255), fnt)
    paste_center(canvas, PROPS / "slash_arc.png", anchors["slash_mid"], 1.0)
    paste_center(canvas, PROPS / "impact_flash.png", anchors["center_clash"], 0.9)
    ImageDraw.Draw(canvas).text((60, 60), "slash_attack + impact_clash", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_slash_clash.png")

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    draw_actor(draw, anchors["hero_left"], "hero", (80, 145, 230, 255), fnt)
    draw_actor(draw, anchors["enemy_right"], "enemy", (200, 76, 76, 255), fnt)
    paste_center(canvas, PROPS / "shield_bubble.png", anchors["shield_left"], 0.9)
    paste_center(canvas, PROPS / "explosion_burst.png", anchors["explosion_mid"], 0.9)
    ImageDraw.Draw(canvas).text((60, 60), "cast_shield + explosion_hit", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_shield_explosion.png")

    canvas = render_base(data, bg_key="close_crater", front_layers=False)
    paste_center(canvas, PROPS / "ground_crack.png", anchors["close_insert_center"], 1.0)
    paste_center(canvas, PROPS / "dust_cloud.png", anchors["ground_center"], 0.9)
    ImageDraw.Draw(canvas).text((60, 60), "ground_crack + dust_roll", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_ground_crack.png")

    canvas = render_base(data, front_layers=False)
    paste_center(canvas, PROPS / "health_bar_enemy.png", anchors["ui_top"], 0.95)
    paste_center(canvas, PROPS / "warning_banner.png", anchors["warning_center"], 0.8)
    ImageDraw.Draw(canvas).text((60, 60), "health bar + warning", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_combat_ui.png")

    canvas = render_base(data, bg_key="close_sky", front_layers=False)
    paste_center(canvas, PROPS / "explosion_close.png", anchors["close_insert_center"], 0.95)
    ImageDraw.Draw(canvas).text((60, 60), "explosion close insert", fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_explosion_close.png")

    save_contact_sheet(
        PREVIEWS / "battlefield_vfx_contact_sheet.png",
        [
            ("explosion_burst", PROPS / "explosion_burst.png"),
            ("explosion_close", PROPS / "explosion_close.png"),
            ("slash_arc", PROPS / "slash_arc.png"),
            ("slash_close", PROPS / "slash_close.png"),
            ("shield_bubble", PROPS / "shield_bubble.png"),
            ("impact_flash", PROPS / "impact_flash.png"),
            ("dust_cloud", PROPS / "dust_cloud.png"),
            ("ground_crack", PROPS / "ground_crack.png"),
            ("health_bar", PROPS / "health_bar_enemy.png"),
            ("warning_banner", PROPS / "warning_banner.png"),
        ],
    )


def main() -> None:
    for folder in (BACKGROUNDS, LAYERS, PROPS, PREVIEWS):
        folder.mkdir(parents=True, exist_ok=True)

    draw_battlefield_background(BACKGROUNDS / "wide.png")
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "medium.png", (360, 260, 1560, 900))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_crater.png", (600, 575, 1320, 930))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_left.png", (70, 320, 700, 900))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_right.png", (1220, 320, 1850, 900))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_sky.png", (420, 0, 1500, 560))

    save_layer_rocks(LAYERS / "foreground_rocks.png")
    save_layer_smoke(LAYERS / "background_smoke.png")

    save_explosion(PROPS / "explosion_burst.png")
    save_explosion(PROPS / "explosion_close.png", close=True)
    save_slash(PROPS / "slash_arc.png")
    save_slash(PROPS / "slash_close.png", close=True)
    save_shield(PROPS / "shield_bubble.png")
    save_shield(PROPS / "shield_close.png", close=True)
    save_impact(PROPS / "impact_flash.png")
    save_dust(PROPS / "dust_cloud.png")
    save_crack(PROPS / "ground_crack.png")
    save_health_bar(PROPS / "health_bar_enemy.png")
    save_warning_banner(PROPS / "warning_banner.png")

    data = scene_yaml()
    (ROOT / "scene.yaml").write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    render_previews(data)
    print(ROOT)


if __name__ == "__main__":
    main()
