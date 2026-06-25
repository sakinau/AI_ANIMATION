from __future__ import annotations

import csv
import json
import urllib.request
from collections import deque
from pathlib import Path

from PIL import Image, ImageSequence


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "magic-delivery"
ASSETS = PROJECT / "assets"
PUBLIC = ROOT / "public" / "magic-delivery"

CHAR_CANDIDATES = ASSETS / "01_characters" / "candidates_shadiao"
FX_SOURCE = ASSETS / "05_fx" / "shadiao_gifs"
BG_SOURCE = ASSETS / "02_backgrounds" / "shadiao_scenes"

CHARACTER_SELECTIONS = {
    "delivery_guy": ("97fb2de9157ff69f.png", 0),
    "demon_king": ("8744c13c7851bc32.png", 0),
    "hero": ("11e6250749702a1b.png", 0),
}

BACKGROUND_URLS = {
    "cinema": "https://www.shadiao.cn/uploads/images/20260218131910_69954bcee44a1.png",
    "factory": "https://www.shadiao.cn/uploads/images/20260218141245_6995585d48076.png",
    "earth_house": "https://www.shadiao.cn/uploads/images/20260218141343_69955897153fd.png",
}

FX_NAMES = {
    "5b1a3b89058849c9.gif": "hit_star",
    "d28798477e8a739b.gif": "dust",
    "08c30af56fae1e4d.gif": "sweat",
    "78674c9a6985dff6.gif": "speed_smoke",
    "86518b7c42067633.gif": "smoke_ring",
}


def remove_border_white(image: Image.Image, threshold: int = 244) -> Image.Image:
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


def component_boxes(image: Image.Image) -> list[tuple[int, int, int, int]]:
    alpha = image.getchannel("A")
    width, height = image.size
    pixels = alpha.load()
    visited = bytearray(width * height)
    boxes: list[tuple[int, int, int, int, int]] = []

    for y in range(height):
        for x in range(width):
            offset = y * width + x
            if visited[offset] or pixels[x, y] == 0:
                continue
            visited[offset] = 1
            queue = deque([(x, y)])
            left = right = x
            top = bottom = y
            count = 0
            while queue:
                cx, cy = queue.popleft()
                count += 1
                left = min(left, cx)
                right = max(right, cx)
                top = min(top, cy)
                bottom = max(bottom, cy)
                for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                    if nx < 0 or nx >= width or ny < 0 or ny >= height:
                        continue
                    neighbor = ny * width + nx
                    if visited[neighbor] or pixels[nx, ny] == 0:
                        continue
                    visited[neighbor] = 1
                    queue.append((nx, ny))
            if count > 120:
                boxes.append((left, top, right + 1, bottom + 1, count))
    return [(l, t, r, b) for l, t, r, b, _ in sorted(boxes, key=lambda item: item[0])]


def crop_with_padding(image: Image.Image, box: tuple[int, int, int, int], padding: int = 8) -> Image.Image:
    left, top, right, bottom = box
    return image.crop(
        (
            max(0, left - padding),
            max(0, top - padding),
            min(image.width, right + padding),
            min(image.height, bottom + padding),
        )
    )


def prepare_characters() -> None:
    out_dir = PUBLIC / "characters"
    out_dir.mkdir(parents=True, exist_ok=True)
    for character, (filename, pose_index) in CHARACTER_SELECTIONS.items():
        source = CHAR_CANDIDATES / filename
        cleaned = remove_border_white(Image.open(source))
        boxes = component_boxes(cleaned)
        if pose_index >= len(boxes):
            raise RuntimeError(f"{filename} has only {len(boxes)} poses")
        pose = crop_with_padding(cleaned, boxes[pose_index], padding=10)
        pose.save(out_dir / f"{character}.png")


def download_backgrounds() -> None:
    BG_SOURCE.mkdir(parents=True, exist_ok=True)
    public_dir = PUBLIC / "backgrounds"
    public_dir.mkdir(parents=True, exist_ok=True)
    for name, url in BACKGROUND_URLS.items():
        source = BG_SOURCE / f"{name}.png"
        if not source.exists():
            urllib.request.urlretrieve(url, source)
        Image.open(source).convert("RGB").save(public_dir / f"{name}.jpg", quality=90)


def extract_gifs() -> None:
    public_dir = PUBLIC / "fx"
    public_dir.mkdir(parents=True, exist_ok=True)
    for filename, effect_name in FX_NAMES.items():
        source = FX_SOURCE / filename
        out_dir = public_dir / effect_name
        out_dir.mkdir(parents=True, exist_ok=True)
        gif = Image.open(source)
        for index, frame in enumerate(ImageSequence.Iterator(gif)):
            if index >= 24:
                break
            frame.convert("RGBA").save(out_dir / f"frame-{index:03d}.png")


def update_manifest() -> None:
    manifest = ASSETS / "00_license_records" / "asset_manifest.csv"
    existing = set()
    rows: list[dict[str, str]] = []
    if manifest.exists():
        with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                existing.add(row.get("asset_id", ""))
                rows.append(row)

    fieldnames = [
        "asset_id",
        "category",
        "asset_name",
        "intended_use",
        "source_type",
        "source_site",
        "source_url",
        "download_url",
        "author_or_vendor",
        "license_name",
        "commercial_use_allowed",
        "attribution_required",
        "modification_allowed",
        "redistribution_allowed",
        "ai_training_restriction",
        "purchase_price",
        "invoice_or_order_id",
        "download_date",
        "license_capture_path",
        "local_file_path",
        "file_format",
        "resolution_or_sample_rate",
        "has_alpha",
        "style_notes",
        "risk_level",
        "approval_status",
        "notes",
    ]

    def add(row: dict[str, str]) -> None:
        if row["asset_id"] not in existing:
            existing.add(row["asset_id"])
            rows.append({key: row.get(key, "") for key in fieldnames})

    for character, (filename, _) in CHARACTER_SELECTIONS.items():
        add(
            {
                "asset_id": f"SHADIAO_CHAR_{character.upper()}",
                "category": "Character",
                "asset_name": character,
                "intended_use": "1分钟高潮测试片角色替换",
                "source_type": "Free Candidate",
                "source_site": "shadiao.cn",
                "source_url": "https://www.shadiao.cn/character.html",
                "download_url": "",
                "author_or_vendor": "沙雕动画素材网",
                "license_name": "Site says free download; footer says All rights reserved",
                "commercial_use_allowed": "Unclear",
                "attribution_required": "Unclear",
                "modification_allowed": "Unclear",
                "redistribution_allowed": "Unclear",
                "purchase_price": "0",
                "download_date": "2026-06-23",
                "local_file_path": f"public/magic-delivery/characters/{character}.png",
                "file_format": "PNG",
                "has_alpha": "Yes",
                "style_notes": "测试片替换用，正式商用前需确认授权",
                "risk_level": "Medium",
                "approval_status": "Candidate",
            }
        )

    for name, url in BACKGROUND_URLS.items():
        add(
            {
                "asset_id": f"SHADIAO_BG_{name.upper()}",
                "category": "Background",
                "asset_name": name,
                "intended_use": "1分钟高潮测试片背景替换",
                "source_type": "Free Candidate",
                "source_site": "shadiao.cn",
                "source_url": "https://www.shadiao.cn/scene.html",
                "download_url": url,
                "author_or_vendor": "沙雕动画素材网",
                "license_name": "Site says free download; footer says All rights reserved",
                "commercial_use_allowed": "Unclear",
                "attribution_required": "Unclear",
                "modification_allowed": "Unclear",
                "redistribution_allowed": "Unclear",
                "purchase_price": "0",
                "download_date": "2026-06-23",
                "local_file_path": f"public/magic-delivery/backgrounds/{name}.jpg",
                "file_format": "JPG",
                "has_alpha": "No",
                "style_notes": "测试片替换用，非最终魔王城美术",
                "risk_level": "Medium",
                "approval_status": "Candidate",
            }
        )

    for filename, effect_name in FX_NAMES.items():
        add(
            {
                "asset_id": f"SHADIAO_FX_{effect_name.upper()}",
                "category": "FX",
                "asset_name": effect_name,
                "intended_use": "1分钟高潮测试片特效替换",
                "source_type": "Free Candidate",
                "source_site": "shadiao.cn",
                "source_url": "https://www.shadiao.cn/effect.html",
                "author_or_vendor": "沙雕动画素材网",
                "license_name": "Site says free download; footer says All rights reserved",
                "commercial_use_allowed": "Unclear",
                "attribution_required": "Unclear",
                "modification_allowed": "Unclear",
                "redistribution_allowed": "Unclear",
                "purchase_price": "0",
                "download_date": "2026-06-23",
                "local_file_path": f"public/magic-delivery/fx/{effect_name}/frame-000.png",
                "file_format": "GIF extracted to PNG sequence",
                "has_alpha": "Yes",
                "style_notes": "测试片替换用，正式商用前需确认授权",
                "risk_level": "Medium",
                "approval_status": "Candidate",
            }
        )

    with manifest.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    prepare_characters()
    download_backgrounds()
    extract_gifs()
    update_manifest()
    print(json.dumps({"public": str(PUBLIC), "status": "ok"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
