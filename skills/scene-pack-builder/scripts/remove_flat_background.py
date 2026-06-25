import argparse
from collections import deque
from pathlib import Path

from PIL import Image


def color_distance(a, b):
    return sum((int(a[i]) - int(b[i])) ** 2 for i in range(3)) ** 0.5


def remove_background(source: Path, target: Path, threshold: float, feather: int, pad: int) -> None:
    img = Image.open(source).convert("RGBA")
    pixels = img.load()
    w, h = img.size

    corners = [pixels[0, 0], pixels[w - 1, 0], pixels[0, h - 1], pixels[w - 1, h - 1]]
    bg = tuple(sum(c[i] for c in corners) // len(corners) for i in range(4))

    visited = bytearray(w * h)
    bgmask = bytearray(w * h)
    queue = deque()
    for x in range(w):
        queue.append((x, 0))
        queue.append((x, h - 1))
    for y in range(h):
        queue.append((0, y))
        queue.append((w - 1, y))

    while queue:
        x, y = queue.popleft()
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        idx = y * w + x
        if visited[idx]:
            continue
        visited[idx] = 1
        if color_distance(pixels[x, y], bg) > threshold:
            continue
        bgmask[idx] = 1
        queue.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))

    out = Image.new("RGBA", img.size)
    out_pixels = out.load()
    for y in range(h):
        for x in range(w):
            idx = y * w + x
            r, g, b, a = pixels[x, y]
            if bgmask[idx]:
                out_pixels[x, y] = (r, g, b, 0)
            else:
                alpha = a
                if feather > 0:
                    near_bg = False
                    for yy in range(max(0, y - feather), min(h, y + feather + 1)):
                        for xx in range(max(0, x - feather), min(w, x + feather + 1)):
                            if bgmask[yy * w + xx]:
                                near_bg = True
                                break
                        if near_bg:
                            break
                    if near_bg:
                        alpha = max(96, int(a * 0.88))
                out_pixels[x, y] = (r, g, b, alpha)

    bbox = out.getbbox()
    if bbox:
        left = max(0, bbox[0] - pad)
        top = max(0, bbox[1] - pad)
        right = min(w, bbox[2] + pad)
        bottom = min(h, bbox[3] + pad)
        out = out.crop((left, top, right, bottom))

    target.parent.mkdir(parents=True, exist_ok=True)
    out.save(target)


def main() -> None:
    parser = argparse.ArgumentParser(description="Remove a flat background from a generated prop PNG.")
    parser.add_argument("source")
    parser.add_argument("target")
    parser.add_argument("--threshold", type=float, default=36)
    parser.add_argument("--feather", type=int, default=1)
    parser.add_argument("--pad", type=int, default=24)
    args = parser.parse_args()
    remove_background(Path(args.source), Path(args.target), args.threshold, args.feather, args.pad)
    print(args.target)


if __name__ == "__main__":
    main()
