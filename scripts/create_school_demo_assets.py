from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("projects/scene-packs/scene_demo_school_01")
BACKGROUNDS = ROOT / "backgrounds"
PROPS = ROOT / "props"
PREVIEWS = ROOT / "previews"


def canvas(w: int, h: int) -> Image.Image:
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def draw_poly(draw: ImageDraw.ImageDraw, points, fill, outline=(25, 27, 32, 255), width=5):
    draw.polygon(points, fill=fill)
    draw.line(points + [points[0]], fill=outline, width=width, joint="curve")


def save_phone_close(path: Path) -> None:
    img = canvas(520, 760)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((95, 38, 425, 722), radius=44, fill=(34, 38, 46, 255), outline=(20, 20, 22, 255), width=8)
    d.rounded_rectangle((126, 92, 394, 658), radius=22, fill=(13, 18, 25, 255), outline=(82, 94, 110, 255), width=4)
    d.rectangle((150, 140, 370, 220), fill=(52, 165, 205, 255))
    d.rectangle((150, 248, 370, 310), fill=(238, 244, 250, 255))
    d.rectangle((150, 330, 370, 392), fill=(238, 244, 250, 255))
    d.rectangle((150, 412, 310, 474), fill=(255, 224, 104, 255))
    d.ellipse((240, 678, 280, 718), fill=(83, 91, 104, 255))
    d.line((152, 124, 230, 94), fill=(255, 255, 255, 120), width=7)
    img.save(path)


def save_book_hand(path: Path, close: bool = False) -> None:
    w, h = (560, 520) if close else (230, 180)
    img = canvas(w, h)
    d = ImageDraw.Draw(img)
    s = w / 230
    pts = [(22 * s, 52 * s), (155 * s, 18 * s), (210 * s, 70 * s), (82 * s, 135 * s)]
    draw_poly(d, pts, (142, 202, 112, 255), width=max(4, int(5 * s)))
    d.polygon([(82 * s, 135 * s), (210 * s, 70 * s), (203 * s, 118 * s), (86 * s, 166 * s)], fill=(248, 238, 214, 255))
    d.line([(82 * s, 135 * s), (86 * s, 166 * s), (203 * s, 118 * s), (210 * s, 70 * s)], fill=(25, 27, 32, 255), width=max(4, int(5 * s)))
    d.line([(48 * s, 61 * s), (168 * s, 31 * s)], fill=(80, 125, 86, 255), width=max(2, int(3 * s)))
    d.line([(92 * s, 146 * s), (198 * s, 104 * s)], fill=(188, 154, 116, 255), width=max(2, int(3 * s)))
    if close:
        d.rounded_rectangle((360, 265, 535, 360), radius=24, fill=(255, 220, 178, 255), outline=(30, 30, 32, 255), width=6)
        d.rectangle((350, 285, 452, 342), fill=(255, 220, 178, 255))
    img.save(path)


def save_cup_close(path: Path) -> None:
    img = canvas(420, 520)
    d = ImageDraw.Draw(img)
    d.ellipse((88, 62, 332, 158), fill=(246, 246, 238, 255), outline=(28, 28, 28, 255), width=7)
    d.rounded_rectangle((105, 112, 315, 420), radius=28, fill=(175, 88, 82, 255), outline=(28, 28, 28, 255), width=7)
    d.ellipse((105, 370, 315, 470), fill=(145, 70, 67, 255), outline=(28, 28, 28, 255), width=7)
    d.rectangle((128, 95, 292, 164), fill=(252, 252, 246, 255))
    d.arc((88, 62, 332, 158), 0, 180, fill=(28, 28, 28, 255), width=7)
    d.rounded_rectangle((150, 210, 270, 295), radius=16, fill=(254, 246, 226, 255), outline=(120, 60, 56, 255), width=4)
    img.save(path)


def save_paper(path: Path, hand: bool = False, close: bool = False) -> None:
    w, h = (640, 500) if close else (260, 190)
    img = canvas(w, h)
    d = ImageDraw.Draw(img)
    s = w / 260
    paper = [(26 * s, 28 * s), (210 * s, 15 * s), (236 * s, 140 * s), (52 * s, 168 * s)]
    draw_poly(d, paper, (255, 247, 215, 255), width=max(4, int(5 * s)))
    for i in range(4):
        y = (58 + i * 24) * s
        d.line((58 * s, y, 198 * s, y - 10 * s), fill=(72, 98, 130, 255), width=max(2, int(3 * s)))
    d.line((78 * s, 132 * s, 165 * s, 118 * s), fill=(205, 70, 70, 255), width=max(3, int(4 * s)))
    if hand or close:
        d.rounded_rectangle((5 * s, 120 * s, 96 * s, 184 * s), radius=int(18 * s), fill=(255, 220, 178, 255), outline=(28, 28, 28, 255), width=max(4, int(5 * s)))
    img.save(path)


def save_delivery_bag(path: Path, hand: bool = False) -> None:
    img = canvas(300, 260)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((42, 75, 250, 230), radius=18, fill=(245, 145, 48, 255), outline=(28, 28, 28, 255), width=6)
    d.polygon([(42, 75), (92, 25), (210, 25), (250, 75)], fill=(255, 179, 68, 255), outline=(28, 28, 28, 255))
    d.line((92, 25, 210, 25, 250, 75), fill=(28, 28, 28, 255), width=6)
    d.rounded_rectangle((96, 112, 198, 168), radius=14, fill=(255, 244, 214, 255), outline=(28, 28, 28, 255), width=4)
    d.line((112, 132, 182, 132), fill=(220, 80, 52, 255), width=5)
    d.line((112, 150, 165, 150), fill=(220, 80, 52, 255), width=5)
    if hand:
        d.rounded_rectangle((188, 18, 292, 88), radius=22, fill=(255, 220, 178, 255), outline=(28, 28, 28, 255), width=5)
    img.save(path)


def save_key(path: Path, hand: bool = False) -> None:
    img = canvas(240, 160)
    d = ImageDraw.Draw(img)
    d.ellipse((24, 42, 94, 112), fill=(245, 202, 70, 255), outline=(28, 28, 28, 255), width=6)
    d.ellipse((45, 63, 73, 91), fill=(0, 0, 0, 0), outline=(28, 28, 28, 255), width=5)
    d.rounded_rectangle((88, 70, 190, 88), radius=7, fill=(245, 202, 70, 255), outline=(28, 28, 28, 255), width=5)
    d.rectangle((160, 86, 176, 112), fill=(245, 202, 70, 255), outline=(28, 28, 28, 255))
    d.rectangle((185, 86, 202, 106), fill=(245, 202, 70, 255), outline=(28, 28, 28, 255))
    if hand:
        d.rounded_rectangle((120, 12, 232, 74), radius=22, fill=(255, 220, 178, 255), outline=(28, 28, 28, 255), width=5)
    img.save(path)


def save_chalk(path: Path, hand: bool = False) -> None:
    img = canvas(240, 150)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((34, 62, 188, 88), radius=12, fill=(245, 245, 236, 255), outline=(28, 28, 28, 255), width=5)
    d.line((58, 70, 156, 70), fill=(210, 210, 200, 255), width=3)
    if hand:
        d.rounded_rectangle((112, 18, 232, 80), radius=22, fill=(255, 220, 178, 255), outline=(28, 28, 28, 255), width=5)
    img.save(path)


def save_order_popup(path: Path) -> None:
    img = canvas(620, 430)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((18, 18, 602, 412), radius=32, fill=(250, 250, 244, 245), outline=(28, 28, 32, 255), width=8)
    d.rounded_rectangle((48, 52, 572, 126), radius=18, fill=(255, 186, 64, 255), outline=(28, 28, 32, 255), width=5)
    d.rectangle((72, 80, 312, 100), fill=(38, 38, 42, 255))
    d.rounded_rectangle((54, 158, 566, 220), radius=16, fill=(235, 242, 250, 255), outline=(80, 90, 100, 255), width=4)
    d.rounded_rectangle((54, 244, 566, 306), radius=16, fill=(235, 242, 250, 255), outline=(80, 90, 100, 255), width=4)
    d.rounded_rectangle((54, 334, 260, 386), radius=18, fill=(90, 180, 96, 255), outline=(28, 28, 32, 255), width=4)
    d.rounded_rectangle((360, 334, 566, 386), radius=18, fill=(226, 84, 72, 255), outline=(28, 28, 32, 255), width=4)
    d.rectangle((84, 176, 378, 190), fill=(45, 70, 95, 255))
    d.rectangle((84, 262, 516, 276), fill=(45, 70, 95, 255))
    img.save(path)


def save_warning_popup(path: Path) -> None:
    img = canvas(680, 360)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((18, 18, 662, 342), radius=28, fill=(42, 35, 44, 248), outline=(255, 224, 88, 255), width=9)
    d.polygon([(78, 84), (138, 220), (18, 220)], fill=(255, 208, 58, 255), outline=(28, 28, 32, 255))
    d.rectangle((72, 122, 84, 178), fill=(28, 28, 32, 255))
    d.ellipse((68, 190, 88, 210), fill=(28, 28, 32, 255))
    for y, w in ((96, 430), (154, 360), (212, 480)):
        d.rounded_rectangle((180, y, 180 + w, y + 28), radius=10, fill=(244, 244, 232, 255))
    img.save(path)


def save_dialogue_bubble(path: Path, tail: str = "left") -> None:
    img = canvas(560, 260)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((28, 24, 532, 188), radius=34, fill=(255, 255, 250, 245), outline=(28, 28, 32, 255), width=6)
    if tail == "left":
        d.polygon([(118, 184), (72, 238), (178, 188)], fill=(255, 255, 250, 245), outline=(28, 28, 32, 255))
    else:
        d.polygon([(442, 184), (488, 238), (382, 188)], fill=(255, 255, 250, 245), outline=(28, 28, 32, 255))
    for y, w in ((70, 390), (112, 310), (154, 360)):
        d.rounded_rectangle((84, y, 84 + w, y + 14), radius=5, fill=(48, 64, 82, 255))
    img.save(path)


def save_reaction_mark(path: Path, kind: str) -> None:
    img = canvas(240, 240)
    d = ImageDraw.Draw(img)
    if kind == "exclaim":
        d.polygon([(108, 28), (154, 28), (142, 146), (120, 146)], fill=(255, 226, 64, 255), outline=(28, 28, 32, 255))
        d.ellipse((103, 166, 157, 220), fill=(255, 226, 64, 255), outline=(28, 28, 32, 255), width=6)
    elif kind == "question":
        d.arc((54, 28, 182, 150), 200, 535, fill=(86, 190, 235, 255), width=24)
        d.line((126, 142, 126, 164), fill=(86, 190, 235, 255), width=22)
        d.ellipse((101, 184, 151, 234), fill=(86, 190, 235, 255), outline=(28, 28, 32, 255), width=5)
    else:
        for i, x in enumerate((40, 80, 120, 160)):
            d.line((x, 210, x + 34, 40 + i * 12), fill=(255, 255, 255, 220), width=10)
            d.line((x, 210, x + 34, 40 + i * 12), fill=(78, 160, 220, 255), width=5)
    img.save(path)


def save_blackboard_insert(path: Path) -> None:
    img = canvas(900, 520)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((34, 34, 866, 430), radius=14, fill=(42, 78, 66, 255), outline=(36, 28, 22, 255), width=12)
    d.rectangle((70, 465, 830, 492), fill=(115, 82, 54, 255), outline=(36, 28, 22, 255))
    for i, y in enumerate((100, 160, 220, 292)):
        d.line((110, y, 760 - i * 70, y + 10), fill=(235, 238, 218, 210), width=9)
    d.line((112, 350, 420, 388), fill=(255, 226, 72, 255), width=12)
    d.line((620, 456, 740, 456), fill=(245, 245, 235, 255), width=12)
    img.save(path)


def save_door_insert(path: Path) -> None:
    img = canvas(760, 620)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 760, 620), fill=(205, 196, 174, 255))
    d.rounded_rectangle((190, 48, 540, 594), radius=8, fill=(70, 56, 48, 255), outline=(28, 28, 32, 255), width=10)
    d.rectangle((232, 96, 500, 298), fill=(54, 45, 42, 255), outline=(28, 28, 32, 255), width=6)
    d.rectangle((232, 332, 500, 548), fill=(54, 45, 42, 255), outline=(28, 28, 32, 255), width=6)
    d.ellipse((470, 298, 520, 348), fill=(236, 196, 72, 255), outline=(28, 28, 32, 255), width=5)
    d.polygon([(544, 64), (710, 0), (710, 620), (544, 594)], fill=(38, 31, 29, 210))
    img.save(path)


def save_cropped_backgrounds() -> list[tuple[str, Path]]:
    wide = Image.open(BACKGROUNDS / "wide.png").convert("RGBA")
    crops = [
        ("close_blackboard", BACKGROUNDS / "close_blackboard.png", (420, 180, 1350, 700)),
        ("close_door", BACKGROUNDS / "close_door.png", (230, 360, 820, 910)),
    ]
    outputs = []
    for label, out, box in crops:
        crop = wide.crop(box).resize((1920, 1080), Image.Resampling.LANCZOS)
        crop.save(out)
        outputs.append((label, out))
    return outputs


def save_contact_sheet(output_path: Path, assets: list[tuple[str, Path]]) -> None:
    thumb = (180, 150)
    margin = 24
    label_h = 30
    cols = 4
    rows = (len(assets) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (thumb[0] + margin) + margin, rows * (thumb[1] + label_h + margin) + margin), (236, 236, 230))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
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
        d.text((x, y + thumb[1] + 8), label, fill=(20, 20, 20), font=font)
    sheet.save(output_path)


def main() -> None:
    BACKGROUNDS.mkdir(parents=True, exist_ok=True)
    PROPS.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    outputs = [
        ("phone_close", PROPS / "phone_close.png", lambda p: save_phone_close(p)),
        ("book_hand", PROPS / "book_hand.png", lambda p: save_book_hand(p)),
        ("book_close", PROPS / "book_close.png", lambda p: save_book_hand(p, close=True)),
        ("cup_close", PROPS / "cup_close.png", lambda p: save_cup_close(p)),
        ("paper_note_table", PROPS / "paper_note_table.png", lambda p: save_paper(p)),
        ("paper_note_hand", PROPS / "paper_note_hand.png", lambda p: save_paper(p, hand=True)),
        ("paper_note_close", PROPS / "paper_note_close.png", lambda p: save_paper(p, close=True)),
        ("delivery_bag_floor", PROPS / "delivery_bag_floor.png", lambda p: save_delivery_bag(p)),
        ("delivery_bag_hand", PROPS / "delivery_bag_hand.png", lambda p: save_delivery_bag(p, hand=True)),
        ("key_table", PROPS / "key_table.png", lambda p: save_key(p)),
        ("key_hand", PROPS / "key_hand.png", lambda p: save_key(p, hand=True)),
        ("chalk_table", PROPS / "chalk_table.png", lambda p: save_chalk(p)),
        ("chalk_hand", PROPS / "chalk_hand.png", lambda p: save_chalk(p, hand=True)),
        ("order_popup", PROPS / "order_popup.png", lambda p: save_order_popup(p)),
        ("warning_popup", PROPS / "warning_popup.png", lambda p: save_warning_popup(p)),
        ("dialogue_bubble_left", PROPS / "dialogue_bubble_left.png", lambda p: save_dialogue_bubble(p, "left")),
        ("dialogue_bubble_right", PROPS / "dialogue_bubble_right.png", lambda p: save_dialogue_bubble(p, "right")),
        ("reaction_exclaim", PROPS / "reaction_exclaim.png", lambda p: save_reaction_mark(p, "exclaim")),
        ("reaction_question", PROPS / "reaction_question.png", lambda p: save_reaction_mark(p, "question")),
        ("speed_lines", PROPS / "speed_lines.png", lambda p: save_reaction_mark(p, "speed")),
        ("blackboard_insert", PROPS / "blackboard_insert.png", lambda p: save_blackboard_insert(p)),
        ("door_insert", PROPS / "door_insert.png", lambda p: save_door_insert(p)),
    ]
    for _, path, maker in outputs:
        maker(path)
        print(path)
    bg_outputs = save_cropped_backgrounds()
    for _, path in bg_outputs:
        print(path)
    save_contact_sheet(PREVIEWS / "school_extra_props_contact_sheet.png", [(name, path) for name, path, _ in outputs])
    ui_names = {
        "order_popup",
        "warning_popup",
        "dialogue_bubble_left",
        "dialogue_bubble_right",
        "reaction_exclaim",
        "reaction_question",
        "speed_lines",
        "blackboard_insert",
        "door_insert",
    }
    save_contact_sheet(
        PREVIEWS / "school_ui_state_contact_sheet.png",
        [(name, path) for name, path, _ in outputs if name in ui_names] + bg_outputs,
    )
    print(PREVIEWS / "school_extra_props_contact_sheet.png")
    print(PREVIEWS / "school_ui_state_contact_sheet.png")


if __name__ == "__main__":
    main()
