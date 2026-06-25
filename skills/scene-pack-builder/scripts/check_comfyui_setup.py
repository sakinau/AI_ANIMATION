import argparse
import json
import urllib.request
from pathlib import Path


MODEL_DIRS = {
    "checkpoints": "ComfyUI/models/checkpoints",
    "diffusion_models": "ComfyUI/models/diffusion_models",
    "vae": "ComfyUI/models/vae",
    "clip": "ComfyUI/models/clip",
    "loras": "ComfyUI/models/loras",
}


def real_model_files(path: Path):
    if not path.exists():
        return []
    return [
        p
        for p in path.rglob("*")
        if p.is_file()
        and not p.name.startswith("put_")
        and p.suffix.lower() in {".safetensors", ".ckpt", ".pt", ".pth", ".bin"}
    ]


def server_status(server: str):
    try:
        with urllib.request.urlopen(f"{server.rstrip('/')}/system_stats", timeout=3) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return {"available": False, "error": f"{type(exc).__name__}: {exc}"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="D:/ComfyUI_windows_portable", help="ComfyUI portable root")
    parser.add_argument("--server", default="http://127.0.0.1:8188")
    args = parser.parse_args()

    root = Path(args.root)
    result = {
        "root": str(root),
        "exists": root.exists(),
        "server": args.server,
        "server_status": server_status(args.server),
        "launchers": [],
        "models": {},
        "recommendations": [],
    }

    for name in ("run_nvidia_gpu.bat", "run_amd_gpu.bat", "run_amd_gpu_enable_dynamic_vram.bat", "run_cpu.bat"):
        launcher = root / name
        if launcher.exists():
            result["launchers"].append(str(launcher))

    for key, rel in MODEL_DIRS.items():
        files = real_model_files(root / rel)
        result["models"][key] = [{"path": str(p), "size_mb": round(p.stat().st_size / 1024 / 1024, 1)} for p in files[:20]]

    if not result["launchers"]:
        result["recommendations"].append("No known launcher .bat was found under the portable root.")
    if not result["models"]["checkpoints"] and not result["models"]["diffusion_models"]:
        result["recommendations"].append("No checkpoint/diffusion model found. Add at least one model before text-to-image generation.")
    if result["server_status"].get("available") is False:
        result["recommendations"].append("ComfyUI server is not running. Start the matching .bat file, then open http://127.0.0.1:8188.")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
