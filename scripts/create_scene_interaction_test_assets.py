from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("projects/scene-interaction-test")
PUBLIC = Path("public/scene-interaction-test")
ASSETS = ROOT / "assets"
PUBLIC_ASSETS = PUBLIC / "assets"
SIZE = (1920, 1080)


def rgba(size=(420, 420), color=(0, 0, 0, 0)) -> Image.Image:
    return Image.new("RGBA", size, color)


def font(size: int):
    for name in ("msyh.ttc", "simhei.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def save_fridge(path: Path, open_door: bool = False) -> None:
    img = rgba((520, 760))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((120, 30, 430, 720), radius=24, fill=(225, 236, 240, 255), outline=(28, 32, 36, 255), width=8)
    d.line((120, 320, 430, 320), fill=(28, 32, 36, 255), width=6)
    d.rectangle((390, 90, 410, 250), fill=(110, 120, 128, 255))
    d.rectangle((390, 390, 410, 620), fill=(110, 120, 128, 255))
    if open_door:
        d.polygon([(115, 48), (22, 110), (22, 672), (115, 718)], fill=(205, 224, 232, 255), outline=(28, 32, 36, 255))
        d.rectangle((45, 170, 92, 220), fill=(255, 245, 190, 255), outline=(28, 32, 36, 255), width=3)
        d.rectangle((45, 270, 92, 320), fill=(154, 204, 238, 255), outline=(28, 32, 36, 255), width=3)
        d.ellipse((230, 210, 285, 265), fill=(255, 246, 210, 255), outline=(28, 32, 36, 255), width=4)
        d.ellipse((300, 210, 355, 265), fill=(255, 246, 210, 255), outline=(28, 32, 36, 255), width=4)
        d.rectangle((230, 375, 360, 540), fill=(150, 210, 245, 255), outline=(28, 32, 36, 255), width=5)
        d.rectangle((250, 405, 340, 455), fill=(255, 255, 245, 255), outline=(28, 32, 36, 255), width=3)
    img.save(path)


def save_breakfast(path: Path, close: bool = False) -> None:
    img = rgba((680, 420) if close else (420, 260))
    d = ImageDraw.Draw(img)
    s = img.width / 420
    d.ellipse((45 * s, 64 * s, 250 * s, 210 * s), fill=(250, 250, 236, 255), outline=(28, 28, 28, 255), width=max(4, int(5 * s)))
    d.ellipse((95 * s, 102 * s, 155 * s, 162 * s), fill=(250, 196, 72, 255), outline=(28, 28, 28, 255), width=max(3, int(4 * s)))
    d.ellipse((165 * s, 102 * s, 225 * s, 162 * s), fill=(250, 196, 72, 255), outline=(28, 28, 28, 255), width=max(3, int(4 * s)))
    d.rectangle((290 * s, 56 * s, 374 * s, 220 * s), fill=(154, 210, 245, 255), outline=(28, 28, 28, 255), width=max(4, int(5 * s)))
    d.rectangle((304 * s, 90 * s, 360 * s, 132 * s), fill=(255, 255, 245, 255), outline=(28, 28, 28, 255), width=max(2, int(3 * s)))
    img.save(path)


def save_phone_call(path: Path) -> None:
    img = rgba((560, 760))
    d = ImageDraw.Draw(img)
    fnt = font(34)
    d.rounded_rectangle((68, 20, 492, 740), radius=48, fill=(24, 28, 34, 255), outline=(10, 10, 12, 255), width=8)
    d.rounded_rectangle((96, 76, 464, 666), radius=24, fill=(238, 246, 250, 255))
    d.ellipse((205, 122, 355, 272), fill=(126, 184, 230, 255), outline=(30, 40, 50, 255), width=6)
    d.text((178, 306), "朋友阿强", fill=(24, 28, 34, 255), font=fnt)
    d.rounded_rectangle((156, 520, 404, 592), radius=32, fill=(72, 190, 96, 255), outline=(30, 40, 50, 255), width=5)
    d.text((208, 532), "通话中", fill=(255, 255, 245, 255), font=fnt)
    img.save(path)


def save_activity_banner(path: Path) -> None:
    img = rgba((860, 430))
    d = ImageDraw.Draw(img)
    f1 = font(48)
    f2 = font(34)
    d.rounded_rectangle((20, 20, 840, 410), radius=30, fill=(255, 244, 210, 248), outline=(36, 30, 24, 255), width=8)
    d.rectangle((52, 58, 808, 138), fill=(230, 86, 70, 255), outline=(36, 30, 24, 255), width=5)
    d.text((120, 72), "下午三点 活动现场见", fill=(255, 255, 245, 255), font=f1)
    d.text((88, 180), "城市广场限时试吃大会", fill=(36, 30, 24, 255), font=f2)
    d.text((88, 238), "凭电话暗号领取双倍早餐券", fill=(36, 30, 24, 255), font=f2)
    d.rounded_rectangle((88, 318, 372, 372), radius=18, fill=(80, 160, 230, 255), outline=(36, 30, 24, 255), width=4)
    d.text((116, 324), "立即出发", fill=(255, 255, 245, 255), font=f2)
    img.save(path)


def save_actor(path: Path, body: tuple[int, int, int, int], label: str) -> None:
    img = rgba((260, 520))
    d = ImageDraw.Draw(img)
    fnt = font(30)
    d.rounded_rectangle((72, 170, 188, 470), radius=28, fill=body, outline=(18, 18, 20, 255), width=7)
    d.ellipse((55, 62, 205, 212), fill=(255, 224, 184, 255), outline=(18, 18, 20, 255), width=7)
    d.rectangle((84, 92, 114, 112), fill=(18, 18, 20, 255))
    d.rectangle((146, 92, 176, 112), fill=(18, 18, 20, 255))
    d.arc((98, 132, 162, 176), 0, 180, fill=(18, 18, 20, 255), width=5)
    d.text((62, 474), label, fill=(255, 244, 190, 255), font=fnt, stroke_width=3, stroke_fill=(0, 0, 0, 255))
    img.save(path)


def copy_scene_asset(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    for folder in (ASSETS, PUBLIC_ASSETS):
        folder.mkdir(parents=True, exist_ok=True)

    save_fridge(ASSETS / "fridge_closed.png")
    save_fridge(ASSETS / "fridge_open.png", open_door=True)
    save_breakfast(ASSETS / "breakfast_table.png")
    save_breakfast(ASSETS / "breakfast_close.png", close=True)
    save_phone_call(ASSETS / "phone_call_friend.png")
    save_activity_banner(ASSETS / "activity_banner.png")
    save_actor(ASSETS / "xiaoming.png", (76, 142, 224, 255), "小明")
    save_actor(ASSETS / "friend.png", (214, 92, 76, 255), "朋友")

    for file in ASSETS.glob("*.png"):
        copy_scene_asset(file, PUBLIC_ASSETS / file.name)

    scene_assets = [
        "scene_customer_room_01/backgrounds/wide.png",
        "scene_customer_room_01/backgrounds/close_table.png",
        "scene_customer_room_01/backgrounds/close_tv.png",
        "scene_customer_room_01/layers/coffee_table_front.png",
        "scene_customer_room_01/layers/sofa_front.png",
        "scene_customer_room_01/props/phone_table.png",
        "scene_customer_room_01/props/tv_popup_warning.png",
        "scene_fantasy_market_01/backgrounds/wide.png",
        "scene_fantasy_market_01/props/notice_close.png",
        "scene_overlay_vfx_01/backgrounds/speed_stage.png",
        "scene_overlay_vfx_01/props/dialogue_bubble_left.png",
        "scene_overlay_vfx_01/props/dialogue_bubble_right.png",
        "scene_overlay_vfx_01/props/order_popup_normal.png",
        "scene_overlay_vfx_01/props/reaction_exclaim.png",
        "scene_overlay_vfx_01/props/reaction_question.png",
        "scene_overlay_vfx_01/props/speed_lines_horizontal.png",
        "scene_overlay_vfx_01/props/wipe_white_flash.png",
    ]
    for rel in scene_assets:
        copy_scene_asset(Path("projects/scene-packs") / rel, PUBLIC / "scene-packs" / rel)

    print(PUBLIC)


if __name__ == "__main__":
    main()
