from pathlib import Path
from PIL import Image
from .downloader import from_url, from_drive
from .cache import weight_path


REGISTRY = {
    "RealESRGAN_x4plus": {
        "file": "RealESRGAN_x4plus.pth",
        "url":  "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",
    },
    "RealESRGAN_x4plus_anime_6B": {
        "file": "RealESRGAN_x4plus_anime_6B.pth",
        "url":  "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth",
    },
    "SwinIR": {
        "file": "001_classicalSR_DIV2K_s48w8_SwinIR-M_x4.pth",
        "url":  "https://github.com/JingyunLiang/SwinIR/releases/download/v0.0/001_classicalSR_DIV2K_s48w8_SwinIR-M_x4.pth",
    },
    "HAT": {
        "file":  "HAT_SRx4_ImageNet-pretrain.pth",
        "drive": "1HpmReFfoUqUbnAOQ7rvOeNU3uf_m69w0",
    },
    "SUPIR": {
        "file":   "SUPIR-v0F.ckpt",
        "drive":  "1yELzm5SvAi9e7kPcO_jPp2XkTs4vK6aR",
        "manual": True,
    },
}


def _resolve_weight(model_name: str) -> Path:
    info = REGISTRY[model_name]

    if info.get("manual"):
        dest = weight_path(info["file"])
        if not dest.exists():
            raise RuntimeError(
                "SUPIR requires manual setup.\n"
                "  Repo:    https://github.com/Fanghua-Yu/SUPIR\n"
                f"  Weights: https://drive.google.com/drive/folders/{info['drive']}\n"
                f"  Place '{info['file']}' in: {dest.parent}"
            )
        return dest

    if "url" in info:
        return from_url(info["url"], info["file"])
    return from_drive(info["drive"], info["file"])


def _infer(img: Image.Image, weight: Path, model_name: str) -> Image.Image:
    if model_name in ("RealESRGAN_x4plus", "RealESRGAN_x4plus_anime_6B"):
        from .models.realesrgan import run
    elif model_name in ("SwinIR", "HAT"):
        from .models.spandrel_model import run
    else:
        from .models.supir import run
    return run(img, weight, model_name)


def upscale(img_path: Path, scale: int, model_name: str):
    weight = _resolve_weight(model_name)
    img    = Image.open(img_path).convert("RGB")
    w, h   = img.size

    print(f"  {model_name}  |  {w}x{h}  ->  {w * scale}x{h * scale}")

    out_4x = _infer(img, weight, model_name)

    tw, th = w * scale, h * scale
    out = out_4x.resize((tw, th), Image.LANCZOS) if out_4x.size != (tw, th) else out_4x

    out_path = img_path.parent / f"{img_path.stem}_upscaled_{scale}x{img_path.suffix}"
    out.save(str(out_path))
    print(f"  Saved -> {out_path}")
