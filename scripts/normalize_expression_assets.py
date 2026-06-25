from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "public" / "免费素材库" / "处理后" / "表情"
OUTPUT = ROOT / "public" / "免费素材库" / "处理后" / "表情_标准化"
CANVAS = (180, 132)
FACE_BOX = (132, 92)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in SOURCE.glob("*.png"):
        image = Image.open(path).convert("RGBA")
        bbox = image.getchannel("A").getbbox()
        if bbox is None:
            continue
        cropped = image.crop(bbox)
        scale = min(FACE_BOX[0] / cropped.width, FACE_BOX[1] / cropped.height)
        size = (max(1, int(cropped.width * scale)), max(1, int(cropped.height * scale)))
        resized = cropped.resize(size, Image.Resampling.LANCZOS)
        normalized = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
        x = (CANVAS[0] - size[0]) // 2
        y = 22 + (FACE_BOX[1] - size[1]) // 2
        normalized.alpha_composite(resized, (x, y))
        normalized.save(OUTPUT / path.name)
        count += 1
    print(f"Normalized {count} expression assets into {OUTPUT}")


if __name__ == "__main__":
    main()
