from pathlib import Path
from PIL import Image
from .weights import get_weight

_MODEL_SCALE = 4  # all bundled models output 4x


def upscale(img_path: Path, scale: int, model_name: str):
    weight_path = get_weight(model_name)
    img = Image.open(img_path).convert("RGB")
    w, h = img.size

    print(f"  {model_name}  |  {w}x{h}  ->  {w*scale}x{h*scale}")

    out_4x = _infer(img, weight_path, model_name)

    tw, th = w * scale, h * scale
    out = out_4x.resize((tw, th), Image.LANCZOS) if (out_4x.size != (tw, th)) else out_4x

    out_path = img_path.parent / f"{img_path.stem}_upscaled_{scale}x{img_path.suffix}"
    out.save(str(out_path))
    print(f"  Saved -> {out_path}")


def _infer(img: Image.Image, weight_path: Path, model_name: str) -> Image.Image:
    if model_name in ("RealESRGAN_x4plus", "RealESRGAN_x4plus_anime_6B"):
        from .models.realesrgan import run
    elif model_name in ("SwinIR", "HAT"):
        from .models.spandrel_model import run
    elif model_name == "SUPIR":
        from .models.supir import run
    else:
        raise ValueError(f"Unknown model: {model_name}")
    return run(img, weight_path, model_name)
