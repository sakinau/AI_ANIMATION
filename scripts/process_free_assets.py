from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "public" / "免费素材库"


def remove_border_white(image: Image.Image, threshold: int = 242) -> Image.Image:
    rgba = image.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size
    visited = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def is_background(x: int, y: int) -> bool:
        r, g, b, _ = pixels[x, y]
        return r >= threshold and g >= threshold and b >= threshold

    for x in range(width):
        if is_background(x, 0):
            queue.append((x, 0))
        if is_background(x, height - 1):
            queue.append((x, height - 1))
    for y in range(height):
        if is_background(0, y):
            queue.append((0, y))
        if is_background(width - 1, y):
            queue.append((width - 1, y))

    while queue:
        x, y = queue.popleft()
        offset = y * width + x
        if visited[offset] or not is_background(x, y):
            continue
        visited[offset] = 1
        r, g, b, _ = pixels[x, y]
        pixels[x, y] = (r, g, b, 0)
        if x:
            queue.append((x - 1, y))
        if x + 1 < width:
            queue.append((x + 1, y))
        if y:
            queue.append((x, y - 1))
        if y + 1 < height:
            queue.append((x, y + 1))

    return rgba


def trim(image: Image.Image, padding: int = 8) -> Image.Image:
    alpha = image.getchannel("A")
    box = alpha.getbbox()
    if box is None:
        return image
    left, top, right, bottom = box
    return image.crop(
        (
            max(0, left - padding),
            max(0, top - padding),
            min(image.width, right + padding),
            min(image.height, bottom + padding),
        )
    )


def keep_largest_component(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    width, height = rgba.size
    opaque = alpha.load()
    visited = bytearray(width * height)
    largest: list[int] = []

    for y in range(height):
        for x in range(width):
            offset = y * width + x
            if visited[offset] or opaque[x, y] == 0:
                continue
            visited[offset] = 1
            queue = deque([(x, y)])
            component: list[int] = []
            while queue:
                cx, cy = queue.popleft()
                component.append(cy * width + cx)
                for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                    if nx < 0 or nx >= width or ny < 0 or ny >= height:
                        continue
                    neighbor = ny * width + nx
                    if visited[neighbor] or opaque[nx, ny] == 0:
                        continue
                    visited[neighbor] = 1
                    queue.append((nx, ny))
            if len(component) > len(largest):
                largest = component

    keep = bytearray(width * height)
    for offset in largest:
        keep[offset] = 1
    pixels = rgba.load()
    for y in range(height):
        for x in range(width):
            if not keep[y * width + x]:
                r, g, b, _ = pixels[x, y]
                pixels[x, y] = (r, g, b, 0)
    return rgba


def process_character(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    cleaned = trim(remove_border_white(Image.open(source)))
    cleaned.save(output)


def split_four_pose_sheet(source: Path, output_dir: Path) -> None:
    image = Image.open(source)
    output_dir.mkdir(parents=True, exist_ok=True)
    names = ["指向", "抱臂", "行走", "坐姿"]
    # The seated pose extends left into the walking pose's nominal quarter.
    boxes = [
        (200, 0, 630, image.height),
        (630, 0, 950, image.height),
        (950, 0, 1180, image.height),
        (1180, 0, 1660, image.height),
    ]
    for name, box in zip(names, boxes):
        pose = image.crop(box)
        cleaned = keep_largest_component(remove_border_white(pose))
        trim(cleaned).save(output_dir / f"橙衣男-{name}.png")


def crop_face_sheet(
    source: Path,
    columns: int,
    rows: int,
    selections: dict[str, int],
    output_dir: Path,
) -> None:
    image = Image.open(source)
    output_dir.mkdir(parents=True, exist_ok=True)
    cell_width = image.width / columns
    cell_height = image.height / rows
    for name, index in selections.items():
        column = index % columns
        row = index // columns
        box = (
            round(column * cell_width),
            round(row * cell_height),
            round((column + 1) * cell_width),
            round((row + 1) * cell_height),
        )
        face = image.crop(box)
        trim(remove_border_white(face, threshold=248), padding=4).save(
            output_dir / f"表情-{name}.png"
        )


def extract_gif(source: Path, output_dir: Path, max_frames: int = 24) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    gif = Image.open(source)
    count = min(getattr(gif, "n_frames", 1), max_frames)
    for index in range(count):
        gif.seek(index)
        frame = gif.convert("RGBA")
        frame.save(output_dir / f"frame-{index:03d}.png")


def make_expression_faces(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    def face(name: str, mood: str) -> None:
        image = Image.new("RGBA", (180, 140), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        black = (18, 18, 18, 255)

        if mood == "neutral":
            draw.arc((34, 42, 72, 66), 0, 180, fill=black, width=5)
            draw.arc((108, 42, 146, 66), 0, 180, fill=black, width=5)
            draw.arc((76, 58, 104, 88), 285, 95, fill=black, width=4)
            draw.arc((72, 92, 112, 118), 200, 340, fill=black, width=5)
        elif mood == "serious":
            draw.line((28, 38, 68, 50), fill=black, width=6)
            draw.line((112, 50, 152, 38), fill=black, width=6)
            draw.ellipse((44, 58, 62, 72), outline=black, width=4)
            draw.ellipse((118, 58, 136, 72), outline=black, width=4)
            draw.arc((78, 58, 104, 88), 285, 95, fill=black, width=4)
            draw.arc((74, 96, 112, 116), 200, 340, fill=black, width=5)
        elif mood == "worried":
            draw.line((34, 42, 70, 30), fill=black, width=6)
            draw.line((110, 30, 146, 42), fill=black, width=6)
            draw.ellipse((42, 56, 66, 80), outline=black, width=4)
            draw.ellipse((114, 56, 138, 80), outline=black, width=4)
            draw.arc((76, 60, 104, 90), 285, 95, fill=black, width=4)
            draw.arc((68, 98, 120, 132), 200, 340, fill=black, width=6)
        elif mood == "shocked":
            draw.ellipse((36, 44, 70, 80), outline=black, width=5)
            draw.ellipse((110, 44, 144, 80), outline=black, width=5)
            draw.arc((76, 58, 104, 88), 285, 95, fill=black, width=4)
            draw.ellipse((78, 94, 108, 124), outline=black, width=6)
        elif mood == "blank":
            draw.ellipse((48, 58, 58, 68), fill=black)
            draw.ellipse((124, 58, 134, 68), fill=black)
            draw.line((74, 104, 112, 104), fill=black, width=5)
        elif mood == "smile":
            draw.arc((34, 42, 72, 66), 0, 180, fill=black, width=5)
            draw.arc((108, 42, 146, 66), 0, 180, fill=black, width=5)
            draw.arc((76, 58, 104, 88), 285, 95, fill=black, width=4)
            draw.arc((64, 82, 124, 126), 20, 160, fill=black, width=7)

        image.save(output_dir / f"表情-{name}.png")

    face("平静", "neutral")
    face("怀疑", "serious")
    face("恐惧", "worried")
    face("惊讶", "shocked")
    face("悲伤", "blank")
    face("邪笑", "smile")


def main() -> None:
    processed = LIB / "处理后"
    process_character(
        LIB / "人物" / "潮男-站姿.png",
        processed / "人物" / "潮男-站姿.png",
    )
    process_character(
        LIB / "人物" / "黑西装-站姿.png",
        processed / "人物" / "黑西装-站姿.png",
    )
    split_four_pose_sheet(
        LIB / "人物" / "橙衣男-四动作.png",
        processed / "人物" / "橙衣男",
    )

    crop_face_sheet(
        LIB / "表情" / "基础表情组.png",
        columns=7,
        rows=3,
        selections={"恐惧": 0, "平静": 3, "怀疑": 5, "愤怒": 10, "惊讶": 19},
        output_dir=processed / "表情",
    )
    crop_face_sheet(
        LIB / "表情" / "夸张表情组.png",
        columns=6,
        rows=3,
        selections={"邪笑": 0, "狂喜": 1, "暴怒": 4, "悲伤": 11},
        output_dir=processed / "表情",
    )
    make_expression_faces(processed / "表情")

    for gif in (LIB / "特效").glob("*.gif"):
        extract_gif(gif, processed / "特效帧" / gif.stem)


if __name__ == "__main__":
    main()
