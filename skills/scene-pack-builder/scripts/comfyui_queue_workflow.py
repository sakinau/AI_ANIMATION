import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


def request_json(url: str, data: dict[str, Any] | None = None, timeout: int = 30) -> Any:
    body = None
    headers = {}
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def request_bytes(url: str, timeout: int = 60) -> bytes:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read()


def set_node_input(workflow: dict[str, Any], spec: str) -> None:
    if "=" not in spec or "." not in spec.split("=", 1)[0]:
        raise SystemExit(f"Invalid --set value '{spec}'. Use node_id.input=value")
    lhs, value = spec.split("=", 1)
    node_id, input_name = lhs.split(".", 1)
    if node_id not in workflow:
        raise SystemExit(f"Node '{node_id}' not found in workflow")
    inputs = workflow[node_id].setdefault("inputs", {})
    if input_name not in inputs:
        raise SystemExit(f"Input '{input_name}' not found on node '{node_id}'")
    inputs[input_name] = coerce_value(value)


def coerce_value(value: str) -> Any:
    text = value.strip()
    if text.lower() == "true":
        return True
    if text.lower() == "false":
        return False
    if text.lower() == "null":
        return None
    try:
        if "." in text:
            return float(text)
        return int(text)
    except ValueError:
        return value


def replace_first_clip_text(workflow: dict[str, Any], text: str, negative: bool = False) -> None:
    candidates = []
    for node_id, node in workflow.items():
        if node.get("class_type") != "CLIPTextEncode":
            continue
        inputs = node.get("inputs", {})
        if "text" not in inputs:
            continue
        current = str(inputs["text"]).lower()
        score = 0
        if negative and any(token in current for token in ("negative", "bad", "worst", "low quality")):
            score += 2
        if not negative and not any(token in current for token in ("negative", "bad", "worst", "low quality")):
            score += 1
        candidates.append((score, node_id))
    if not candidates:
        raise SystemExit("No CLIPTextEncode node with a text input found")
    candidates.sort(reverse=True)
    workflow[candidates[0][1]]["inputs"]["text"] = text


def collect_images(history: dict[str, Any]) -> list[dict[str, str]]:
    images = []
    outputs = history.get("outputs", {})
    for output in outputs.values():
        for image in output.get("images", []):
            if {"filename", "subfolder", "type"} <= set(image):
                images.append(image)
    return images


def download_images(server: str, images: list[dict[str, str]], output_dir: Path, prefix: str) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    for index, image in enumerate(images, start=1):
        query = urllib.parse.urlencode(
            {
                "filename": image["filename"],
                "subfolder": image.get("subfolder", ""),
                "type": image.get("type", "output"),
            }
        )
        data = request_bytes(f"{server.rstrip('/')}/view?{query}")
        suffix = Path(image["filename"]).suffix or ".png"
        out = output_dir / f"{prefix}_{index:02d}{suffix}"
        out.write_bytes(data)
        saved.append(out)
    return saved


def main() -> None:
    parser = argparse.ArgumentParser(description="Queue a ComfyUI API workflow and download image outputs.")
    parser.add_argument("workflow_json", help="ComfyUI workflow exported in API format")
    parser.add_argument("--server", default="http://127.0.0.1:8188")
    parser.add_argument("--output-dir", required=True, help="Where downloaded outputs should be saved")
    parser.add_argument("--prefix", default="comfyui_asset")
    parser.add_argument("--prompt", help="Replace the first positive CLIPTextEncode text")
    parser.add_argument("--negative", help="Replace the first likely negative CLIPTextEncode text")
    parser.add_argument("--set", action="append", default=[], help="Override a node input: node_id.input=value")
    parser.add_argument("--wait", action="store_true", help="Wait for completion and download outputs")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--poll", type=float, default=2.0)
    args = parser.parse_args()

    workflow_path = Path(args.workflow_json)
    workflow = json.loads(workflow_path.read_text(encoding="utf-8"))

    if args.prompt:
        replace_first_clip_text(workflow, args.prompt, negative=False)
    if args.negative:
        replace_first_clip_text(workflow, args.negative, negative=True)
    for spec in args.set:
        set_node_input(workflow, spec)

    try:
        stats = request_json(f"{args.server.rstrip('/')}/system_stats", timeout=10)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise SystemExit(f"Cannot reach ComfyUI at {args.server}: {exc}") from exc

    client_id = f"scene-pack-builder-{int(time.time())}"
    result = request_json(f"{args.server.rstrip('/')}/prompt", {"prompt": workflow, "client_id": client_id})
    prompt_id = result.get("prompt_id")
    if not prompt_id:
        raise SystemExit(f"ComfyUI did not return prompt_id: {result}")

    print(json.dumps({"server": args.server, "prompt_id": prompt_id, "device": stats.get("devices", [])[:1]}, ensure_ascii=False, indent=2))
    if not args.wait:
        return

    deadline = time.time() + args.timeout
    history = None
    while time.time() < deadline:
        histories = request_json(f"{args.server.rstrip('/')}/history/{prompt_id}", timeout=30)
        history = histories.get(prompt_id)
        if history and history.get("outputs"):
            break
        time.sleep(args.poll)
    if not history:
        raise SystemExit(f"Timed out waiting for ComfyUI prompt {prompt_id}")

    images = collect_images(history)
    if not images:
        raise SystemExit(f"Prompt {prompt_id} finished but no image outputs were found")
    saved = download_images(args.server, images, Path(args.output_dir), args.prefix)
    print("Downloaded:")
    for path in saved:
        print(path)


if __name__ == "__main__":
    main()
