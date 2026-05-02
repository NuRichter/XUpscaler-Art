import os, platform, urllib.request
from pathlib import Path


def cache_dir() -> Path:
    sys = platform.system()
    if sys == "Windows":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    d = base / "xupscaler-art" / "weights"
    d.mkdir(parents=True, exist_ok=True)
    return d


REGISTRY = {
    "RealESRGAN_x4plus": {
        "file": "RealESRGAN_x4plus.pth",
        "url":  "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",
        "drive_folder": None,
    },
    "RealESRGAN_x4plus_anime_6B": {
        "file": "RealESRGAN_x4plus_anime_6B.pth",
        "url":  "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth",
        "drive_folder": None,
    },
    "SwinIR": {
        "file": "001_classicalSR_DIV2K_s48w8_SwinIR-M_x4.pth",
        "url":  "https://github.com/JingyunLiang/SwinIR/releases/download/v0.0/001_classicalSR_DIV2K_s48w8_SwinIR-M_x4.pth",
        "drive_folder": None,
    },
    "HAT": {
        "file": "HAT_SRx4_ImageNet-pretrain.pth",
        "url":  None,
        "drive_folder": "1HpmReFfoUqUbnAOQ7rvOeNU3uf_m69w0",
    },
    "SUPIR": {
        "file": "SUPIR-v0F.ckpt",
        "url":  None,
        "drive_folder": None,
    },
}


def _progress(block, block_size, total):
    done = min(block * block_size, total)
    pct = done / total * 100 if total > 0 else 0
    print(f"\r  {pct:5.1f}%  {done//1024//1024} MB", end="", flush=True)


def get_weight(model_name: str) -> Path:
    info = REGISTRY[model_name]
    dest = cache_dir() / info["file"]

    if dest.exists():
        return dest

    if model_name == "SUPIR":
        raise RuntimeError(
            "SUPIR weights require manual download.\n"
            "  Get SUPIR-v0F.ckpt from:\n"
            "  https://drive.google.com/drive/folders/1yELzm5SvAi9e7kPcO_jPp2XkTs4vK6aR\n"
            f"  Place it in: {cache_dir()}"
        )

    print(f"Downloading {model_name} weights...")

    if info["url"]:
        urllib.request.urlretrieve(info["url"], dest, _progress)
        print()
        return dest

    if info["drive_folder"]:
        import gdown
        try:
            out = str(cache_dir())
            gdown.download_folder(id=info["drive_folder"], output=out, quiet=False, use_cookies=False)
            if dest.exists():
                return dest
            raise FileNotFoundError(f"{info['file']} not found after folder download.")
        except Exception as exc:
            raise RuntimeError(
                f"Auto-download failed for {model_name}: {exc}\n"
                f"  Manual: https://drive.google.com/drive/folders/{info['drive_folder']}\n"
                f"  Place '{info['file']}' in: {cache_dir()}"
            ) from exc

    raise RuntimeError(f"No download source configured for {model_name}.")
