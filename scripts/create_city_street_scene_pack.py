from __future__ import annotations

from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont


ROOT = Path("projects/scene-packs/scene_city_street_01")
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


def draw_actor(draw: ImageDraw.ImageDraw, anchor: dict, label: str, color: tuple[int, int, int, int], fnt) -> None:
    x = int(anchor["x"] * SIZE[0])
    y = int(anchor["y"] * SIZE[1])
    scale = float(anchor.get("scale", 1))
    body_w = int(145 * scale)
    body_h = int(365 * scale)
    top = y - body_h
    left = x - body_w // 2
    draw.rounded_rectangle((left, top, left + body_w, y), radius=20, fill=color, outline=(18, 18, 20, 255), width=6)
    draw.ellipse((x - 45, top - 66, x + 45, top + 24), fill=(255, 224, 184, 255), outline=(18, 18, 20, 255), width=6)
    draw.text((left - 8, y + 8), label, fill=(255, 245, 180, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))


def paste_center(canvas: Image.Image, path: Path, anchor: dict, scale: float = 1.0) -> None:
    img = Image.open(path).convert("RGBA")
    final = scale * float(anchor.get("scale", 1))
    w = max(1, int(img.width * final))
    h = max(1, int(img.height * final))
    img = img.resize((w, h), Image.Resampling.LANCZOS)
    canvas.alpha_composite(img, (int(anchor["x"] * SIZE[0] - w / 2), int(anchor["y"] * SIZE[1] - h / 2)))


def draw_city_background(path: Path) -> None:
    img = rgba(color=(25, 31, 45, 255))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 1920, 1080), fill=(24, 30, 44, 255))
    d.rectangle((0, 0, 1920, 390), fill=(33, 42, 62, 255))
    d.ellipse((-180, -120, 280, 260), fill=(212, 218, 194, 255))
    for x, h, c in ((80, 330, 58), (250, 420, 49), (1330, 380, 52), (1520, 460, 45), (1700, 340, 56)):
        d.rectangle((x, 390 - h, x + 130, 590), fill=(c, c + 5, c + 15, 255), outline=(18, 20, 28, 255), width=5)
        for yy in range(390 - h + 30, 560, 70):
            for xx in range(x + 20, x + 110, 42):
                d.rectangle((xx, yy, xx + 24, yy + 30), fill=(236, 190, 82, 220))

    # Storefronts.
    d.rectangle((0, 390, 1920, 730), fill=(74, 72, 80, 255))
    d.rectangle((80, 430, 560, 720), fill=(92, 80, 72, 255), outline=(22, 22, 26, 255), width=7)
    d.rectangle((120, 470, 520, 540), fill=(245, 150, 55, 255), outline=(22, 22, 26, 255), width=6)
    d.rectangle((160, 565, 315, 720), fill=(34, 42, 50, 255), outline=(22, 22, 26, 255), width=6)
    d.rectangle((340, 565, 510, 690), fill=(45, 65, 78, 255), outline=(22, 22, 26, 255), width=6)

    d.rectangle((680, 430, 1180, 720), fill=(72, 84, 92, 255), outline=(22, 22, 26, 255), width=7)
    d.rectangle((730, 475, 1130, 535), fill=(67, 175, 220, 255), outline=(22, 22, 26, 255), width=6)
    d.rectangle((735, 570, 920, 700), fill=(42, 54, 64, 255), outline=(22, 22, 26, 255), width=6)
    d.rectangle((955, 570, 1125, 690), fill=(48, 74, 82, 255), outline=(22, 22, 26, 255), width=6)

    d.rectangle((1260, 430, 1810, 720), fill=(80, 70, 82, 255), outline=(22, 22, 26, 255), width=7)
    d.rectangle((1310, 470, 1760, 540), fill=(210, 92, 88, 255), outline=(22, 22, 26, 255), width=6)
    d.rectangle((1345, 570, 1515, 720), fill=(38, 42, 50, 255), outline=(22, 22, 26, 255), width=6)
    d.rectangle((1550, 570, 1740, 685), fill=(52, 70, 78, 255), outline=(22, 22, 26, 255), width=6)

    # Road and sidewalk.
    d.rectangle((0, 720, 1920, 815), fill=(96, 94, 96, 255))
    d.rectangle((0, 815, 1920, 1080), fill=(40, 42, 48, 255))
    for y in (835, 925, 1015):
        d.line((0, y, 1920, y), fill=(30, 32, 36, 255), width=5)
    for x in range(80, 1920, 310):
        d.rectangle((x, 930, x + 165, 950), fill=(226, 216, 142, 255))
    # Rain streaks.
    for x in range(20, 1920, 58):
        y = (x * 37) % 850
        d.line((x, y, x - 32, y + 95), fill=(180, 205, 230, 105), width=3)
    img.save(path)


def crop_bg(source: Path, target: Path, box: tuple[int, int, int, int]) -> None:
    img = Image.open(source).convert("RGBA").crop(box).resize(SIZE, Image.Resampling.LANCZOS)
    img.save(target)


def save_layer_awning(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    d.polygon([(95, 535), (550, 535), (610, 620), (35, 620)], fill=(42, 54, 68, 220), outline=(20, 20, 24, 255))
    d.rectangle((35, 610, 610, 645), fill=(28, 34, 44, 230), outline=(20, 20, 24, 255))
    img.save(path)


def save_layer_bus_stop(path: Path) -> None:
    img = rgba()
    d = ImageDraw.Draw(img)
    d.rectangle((1375, 610, 1740, 795), fill=(40, 45, 52, 80), outline=(18, 18, 22, 210), width=6)
    d.rectangle((1390, 640, 1725, 770), fill=(90, 135, 155, 75))
    d.rectangle((1380, 790, 1400, 945), fill=(28, 30, 34, 230))
    d.rectangle((1715, 790, 1735, 945), fill=(28, 30, 34, 230))
    img.save(path)


def save_scooter(path: Path, side: bool = True) -> None:
    img = rgba((560, 300))
    d = ImageDraw.Draw(img)
    d.ellipse((58, 198, 158, 298), fill=(32, 34, 38, 255), outline=(10, 10, 12, 255), width=7)
    d.ellipse((382, 198, 482, 298), fill=(32, 34, 38, 255), outline=(10, 10, 12, 255), width=7)
    d.ellipse((86, 226, 130, 270), fill=(104, 112, 122, 255))
    d.ellipse((410, 226, 454, 270), fill=(104, 112, 122, 255))
    d.polygon([(140, 205), (230, 120), (365, 130), (435, 210)], fill=(245, 140, 48, 255), outline=(18, 18, 22, 255))
    d.rounded_rectangle((210, 82, 355, 130), radius=18, fill=(48, 58, 70, 255), outline=(18, 18, 22, 255), width=5)
    d.line((360, 126, 455, 72), fill=(28, 28, 32, 255), width=8)
    d.rectangle((238, 36, 372, 94), fill=(250, 165, 56, 255), outline=(18, 18, 22, 255), width=5)
    d.rounded_rectangle((260, 52, 350, 78), radius=7, fill=(255, 242, 220, 255), outline=(18, 18, 22, 255), width=3)
    img.save(path)


def save_delivery_bag(path: Path, hand: bool = False) -> None:
    img = rgba((300, 260))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((42, 75, 250, 230), radius=18, fill=(245, 145, 48, 255), outline=(28, 28, 28, 255), width=6)
    d.polygon([(42, 75), (92, 25), (210, 25), (250, 75)], fill=(255, 179, 68, 255), outline=(28, 28, 28, 255))
    d.rounded_rectangle((96, 112, 198, 168), radius=14, fill=(255, 244, 214, 255), outline=(28, 28, 28, 255), width=4)
    d.line((112, 132, 182, 132), fill=(220, 80, 52, 255), width=5)
    if hand:
        d.rounded_rectangle((188, 18, 292, 88), radius=22, fill=(255, 220, 178, 255), outline=(28, 28, 28, 255), width=5)
    img.save(path)


def save_phone_order(path: Path, close: bool = False) -> None:
    img = rgba((560, 760) if close else (220, 300))
    d = ImageDraw.Draw(img)
    s = img.width / 220
    d.rounded_rectangle((38 * s, 12 * s, 182 * s, 288 * s), radius=int(22 * s), fill=(34, 38, 46, 255), outline=(16, 16, 20, 255), width=max(4, int(5 * s)))
    d.rounded_rectangle((52 * s, 38 * s, 168 * s, 250 * s), radius=int(10 * s), fill=(12, 18, 24, 255), outline=(82, 94, 110, 255), width=max(2, int(3 * s)))
    d.rectangle((65 * s, 55 * s, 155 * s, 88 * s), fill=(255, 178, 60, 255))
    for y, w in ((110, 78), (145, 92), (180, 65)):
        d.rectangle((65 * s, y * s, (65 + w) * s, (y + 14) * s), fill=(238, 244, 250, 255))
    d.rounded_rectangle((65 * s, 212 * s, 155 * s, 238 * s), radius=int(8 * s), fill=(90, 180, 96, 255))
    img.save(path)


def save_order_popup(path: Path) -> None:
    img = rgba((620, 430))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((18, 18, 602, 412), radius=32, fill=(250, 250, 244, 245), outline=(28, 28, 32, 255), width=8)
    d.rounded_rectangle((48, 52, 572, 126), radius=18, fill=(255, 186, 64, 255), outline=(28, 28, 32, 255), width=5)
    d.rectangle((72, 80, 312, 100), fill=(38, 38, 42, 255))
    d.rounded_rectangle((54, 158, 566, 220), radius=16, fill=(235, 242, 250, 255), outline=(80, 90, 100, 255), width=4)
    d.rounded_rectangle((54, 244, 566, 306), radius=16, fill=(235, 242, 250, 255), outline=(80, 90, 100, 255), width=4)
    d.rounded_rectangle((54, 334, 260, 386), radius=18, fill=(90, 180, 96, 255), outline=(28, 28, 32, 255), width=4)
    d.rounded_rectangle((360, 334, 566, 386), radius=18, fill=(226, 84, 72, 255), outline=(28, 28, 32, 255), width=4)
    img.save(path)


def save_customer_door(path: Path) -> None:
    img = rgba((640, 680))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 640, 680), fill=(94, 86, 78, 255))
    d.rounded_rectangle((170, 64, 470, 642), radius=10, fill=(62, 48, 42, 255), outline=(24, 24, 28, 255), width=10)
    d.rectangle((210, 112, 430, 300), fill=(42, 36, 34, 255), outline=(24, 24, 28, 255), width=6)
    d.rectangle((210, 336, 430, 585), fill=(42, 36, 34, 255), outline=(24, 24, 28, 255), width=6)
    d.ellipse((408, 312, 456, 360), fill=(230, 195, 80, 255), outline=(24, 24, 28, 255), width=5)
    img.save(path)


def save_portal_rift(path: Path) -> None:
    img = rgba((500, 620))
    d = ImageDraw.Draw(img)
    for i, color in enumerate(((80, 40, 120, 110), (140, 66, 205, 150), (230, 118, 255, 195))):
        inset = i * 34
        d.ellipse((inset, inset, 500 - inset, 620 - inset), fill=color, outline=(245, 210, 255, 170), width=8)
    for x in range(105, 410, 75):
        d.arc((x - 90, 100, x + 110, 540), 250, 80, fill=(255, 255, 255, 90), width=5)
    img.save(path)


def save_rain_splash(path: Path) -> None:
    img = rgba((320, 180))
    d = ImageDraw.Draw(img)
    for x in range(28, 300, 38):
        d.line((x, 20, x - 22, 95), fill=(180, 220, 255, 180), width=6)
        d.arc((x - 34, 102, x + 28, 150), 200, 340, fill=(180, 220, 255, 180), width=4)
    img.save(path)


def save_contact_sheet(path: Path, assets: list[tuple[str, Path]]) -> None:
    thumb = (180, 150)
    margin = 24
    label_h = 30
    cols = 4
    rows = (len(assets) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (thumb[0] + margin) + margin, rows * (thumb[1] + label_h + margin) + margin), (230, 230, 226))
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
        "scene_id": "scene_city_street_01",
        "name": "现实城市雨夜街头交互样板",
        "version": "0.1.0",
        "format": {"width": 1920, "height": 1080},
        "backgrounds": {
            "wide": "backgrounds/wide.png",
            "medium": "backgrounds/medium.png",
            "close_phone": "backgrounds/close_phone.png",
            "close_store": "backgrounds/close_store.png",
            "close_customer_door": "backgrounds/close_customer_door.png",
        },
        "layers": {
            "background": ["backgrounds/wide.png"],
            "behind_character": [],
            "front_character": ["layers/awning_front.png", "layers/bus_stop_front.png"],
            "overlay": [],
        },
        "anchors": {
            "stand_left": {"x": 0.30, "y": 0.84, "scale": 0.86, "facing": "right"},
            "stand_right": {"x": 0.66, "y": 0.84, "scale": 0.86, "facing": "left"},
            "store_counter": {"x": 0.18, "y": 0.67, "scale": 1.0},
            "store_door": {"x": 0.13, "y": 0.72, "scale": 1.0},
            "scooter_park": {"x": 0.43, "y": 0.82, "scale": 0.9},
            "scooter_ride": {"x": 0.55, "y": 0.83, "scale": 0.92},
            "phone_hand": {"x": 0.44, "y": 0.52, "scale": 1.0},
            "ui_center": {"x": 0.50, "y": 0.36, "scale": 1.0},
            "delivery_bag_anchor": {"x": 0.31, "y": 0.69, "scale": 1.0},
            "customer_door": {"x": 0.78, "y": 0.68, "scale": 1.0},
            "portal_center": {"x": 0.78, "y": 0.50, "scale": 1.0},
            "close_insert_center": {"x": 0.50, "y": 0.50, "scale": 1.0},
            "rain_ground": {"x": 0.50, "y": 0.90, "scale": 1.0},
        },
        "props": {
            "scooter": {
                "label": "外卖电动车",
                "variants": {"park": "props/scooter_park.png", "ride": "props/scooter_ride.png"},
                "default_anchor": "scooter_park",
                "pivot": "center",
                "variant_scales": {"park": 0.95, "ride": 1.0},
            },
            "delivery_bag": {
                "label": "外卖箱",
                "variants": {"floor": "props/delivery_bag_floor.png", "hand": "props/delivery_bag_hand.png"},
                "default_anchor": "delivery_bag_anchor",
                "pivot": "center",
                "variant_scales": {"floor": 0.72, "hand": 0.58},
            },
            "phone_order": {
                "label": "手机订单",
                "variants": {"hand": "props/phone_order_hand.png", "close": "props/phone_order_close.png"},
                "default_anchor": "phone_hand",
                "pivot": "center",
                "variant_scales": {"hand": 0.75, "close": 1.0},
            },
            "order_popup": {
                "label": "订单弹窗",
                "variants": {"order": "props/order_popup.png"},
                "default_anchor": "ui_center",
                "pivot": "center",
                "variant_scales": {"order": 0.82},
            },
            "customer_door": {
                "label": "客户门口",
                "variants": {"close": "props/customer_door_close.png"},
                "default_anchor": "customer_door",
                "pivot": "center",
                "variant_scales": {"close": 0.78},
            },
            "portal_rift": {
                "label": "穿越裂缝",
                "variants": {"open": "props/portal_rift_open.png"},
                "default_anchor": "portal_center",
                "pivot": "center",
                "variant_scales": {"open": 1.0},
            },
            "rain_splash": {
                "label": "雨水飞溅",
                "variants": {"loop": "props/rain_splash.png"},
                "default_anchor": "rain_ground",
                "pivot": "center",
                "variant_scales": {"loop": 1.25},
            },
        },
        "supported_actions": [
            "stand",
            "pick_up_delivery",
            "check_order",
            "show_order_popup",
            "ride_scooter",
            "arrive_customer_door",
            "open_portal",
            "enter_portal",
            "rain_loop",
            "inspect_close",
        ],
        "action_templates": {
            "pick_up_delivery": {
                "duration": 1.1,
                "prop": "delivery_bag",
                "prop_sequence": [
                    {"time": 0.0, "variant": "floor", "anchor": "delivery_bag_anchor"},
                    {"time": 0.65, "variant": "hand", "anchor": "actor.hand_r"},
                ],
            },
            "check_order": {
                "duration": 1.3,
                "prop": "phone_order",
                "prop_sequence": [
                    {"time": 0.0, "variant": "hand", "anchor": "phone_hand"},
                    {"time": 0.7, "variant": "close", "anchor": "close_insert_center"},
                ],
            },
            "show_order_popup": {
                "duration": 1.0,
                "prop": "order_popup",
                "prop_sequence": [{"time": 0.0, "variant": "order", "anchor": "ui_center", "motion": "pop_in"}],
            },
            "ride_scooter": {
                "duration": 1.4,
                "prop": "scooter",
                "prop_sequence": [
                    {"time": 0.0, "variant": "park", "anchor": "scooter_park"},
                    {"time": 0.7, "variant": "ride", "anchor": "scooter_ride", "motion": "slide_right"},
                ],
            },
            "arrive_customer_door": {
                "duration": 1.2,
                "background": "close_customer_door",
                "prop": "customer_door",
                "prop_sequence": [{"time": 0.0, "variant": "close", "anchor": "close_insert_center"}],
            },
            "open_portal": {
                "duration": 1.0,
                "prop": "portal_rift",
                "prop_sequence": [{"time": 0.0, "variant": "open", "anchor": "portal_center"}],
            },
            "enter_portal": {
                "duration": 1.0,
                "actor_state_sequence": ["ride", "accelerate", "vanish"],
                "target_anchor": "portal_center",
            },
            "rain_loop": {
                "duration": 0.8,
                "prop": "rain_splash",
                "prop_sequence": [{"time": 0.0, "variant": "loop", "anchor": "rain_ground"}],
            },
        },
    }


def render_base(data: dict, bg_key: str = "wide", front_layers: bool = True) -> Image.Image:
    canvas = Image.open(ROOT / data["backgrounds"][bg_key]).convert("RGBA")
    if front_layers:
        for rel in data["layers"]["front_character"]:
            canvas.alpha_composite(Image.open(ROOT / rel).convert("RGBA"))
    return canvas


def render_previews(data: dict) -> None:
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    fnt = font(34)
    small = font(25)
    anchors = data["anchors"]

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    for anchor_id, anchor in anchors.items():
        x = int(anchor["x"] * SIZE[0])
        y = int(anchor["y"] * SIZE[1])
        draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(255, 90, 50, 255), outline=(0, 0, 0, 255), width=3)
        draw.text((x + 12, y - 22), anchor_id, fill=(255, 240, 180, 255), font=small, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.alpha_composite(Image.open(LAYERS / "awning_front.png").convert("RGBA"))
    canvas.alpha_composite(Image.open(LAYERS / "bus_stop_front.png").convert("RGBA"))
    canvas.convert("RGB").save(PREVIEWS / "preview_wide.png")

    canvas = render_base(data, front_layers=False)
    paste_center(canvas, PROPS / "scooter_park.png", anchors["scooter_park"], 0.95)
    paste_center(canvas, PROPS / "delivery_bag_floor.png", anchors["delivery_bag_anchor"], 0.72)
    paste_center(canvas, PROPS / "phone_order_hand.png", anchors["phone_hand"], 0.75)
    paste_center(canvas, PROPS / "rain_splash.png", anchors["rain_ground"], 1.25)
    canvas.alpha_composite(Image.open(LAYERS / "awning_front.png").convert("RGBA"))
    ImageDraw.Draw(canvas).text((60, 60), "city street props", fill=(255, 245, 180, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_props.png")

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    draw_actor(draw, anchors["stand_left"], "courier", (80, 145, 230, 255), fnt)
    paste_center(canvas, PROPS / "phone_order_hand.png", anchors["phone_hand"], 0.78)
    paste_center(canvas, PROPS / "order_popup.png", anchors["ui_center"], 0.82)
    ImageDraw.Draw(canvas).text((60, 60), "check_order + popup", fill=(255, 245, 180, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_order_popup.png")

    canvas = render_base(data, front_layers=False)
    draw = ImageDraw.Draw(canvas)
    draw_actor(draw, anchors["stand_left"], "courier", (80, 145, 230, 255), fnt)
    paste_center(canvas, PROPS / "scooter_ride.png", anchors["scooter_ride"], 1.0)
    paste_center(canvas, PROPS / "portal_rift_open.png", anchors["portal_center"], 1.0)
    paste_center(canvas, PROPS / "rain_splash.png", anchors["rain_ground"], 1.25)
    canvas.alpha_composite(Image.open(LAYERS / "bus_stop_front.png").convert("RGBA"))
    ImageDraw.Draw(canvas).text((60, 60), "ride_scooter -> portal", fill=(255, 245, 180, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_ride_portal.png")

    canvas = render_base(data, bg_key="close_phone", front_layers=False)
    paste_center(canvas, PROPS / "phone_order_close.png", anchors["close_insert_center"], 1.0)
    ImageDraw.Draw(canvas).text((60, 60), "phone close insert", fill=(255, 245, 180, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_phone_close.png")

    canvas = render_base(data, bg_key="close_customer_door", front_layers=False)
    paste_center(canvas, PROPS / "customer_door_close.png", anchors["close_insert_center"], 0.78)
    ImageDraw.Draw(canvas).text((60, 60), "customer door close insert", fill=(255, 245, 180, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    canvas.convert("RGB").save(PREVIEWS / "preview_customer_door.png")

    save_contact_sheet(
        PREVIEWS / "city_street_props_contact_sheet.png",
        [
            ("scooter_park", PROPS / "scooter_park.png"),
            ("scooter_ride", PROPS / "scooter_ride.png"),
            ("delivery_bag_floor", PROPS / "delivery_bag_floor.png"),
            ("delivery_bag_hand", PROPS / "delivery_bag_hand.png"),
            ("phone_order_hand", PROPS / "phone_order_hand.png"),
            ("phone_order_close", PROPS / "phone_order_close.png"),
            ("order_popup", PROPS / "order_popup.png"),
            ("customer_door", PROPS / "customer_door_close.png"),
            ("portal_rift", PROPS / "portal_rift_open.png"),
            ("rain_splash", PROPS / "rain_splash.png"),
        ],
    )


def main() -> None:
    for folder in (BACKGROUNDS, LAYERS, PROPS, PREVIEWS):
        folder.mkdir(parents=True, exist_ok=True)
    draw_city_background(BACKGROUNDS / "wide.png")
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "medium.png", (450, 310, 1480, 920))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_phone.png", (600, 360, 1320, 930))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_store.png", (60, 390, 640, 780))
    crop_bg(BACKGROUNDS / "wide.png", BACKGROUNDS / "close_customer_door.png", (1220, 390, 1840, 820))

    save_layer_awning(LAYERS / "awning_front.png")
    save_layer_bus_stop(LAYERS / "bus_stop_front.png")
    save_scooter(PROPS / "scooter_park.png")
    save_scooter(PROPS / "scooter_ride.png")
    save_delivery_bag(PROPS / "delivery_bag_floor.png")
    save_delivery_bag(PROPS / "delivery_bag_hand.png", hand=True)
    save_phone_order(PROPS / "phone_order_hand.png")
    save_phone_order(PROPS / "phone_order_close.png", close=True)
    save_order_popup(PROPS / "order_popup.png")
    save_customer_door(PROPS / "customer_door_close.png")
    save_portal_rift(PROPS / "portal_rift_open.png")
    save_rain_splash(PROPS / "rain_splash.png")

    data = scene_yaml()
    (ROOT / "scene.yaml").write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    render_previews(data)
    print(ROOT)


if __name__ == "__main__":
    main()
