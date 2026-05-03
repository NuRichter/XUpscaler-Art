from pathlib import Path
from PIL import Image
from .cache import weight_path
from .downloader import from_url, from_drive

WEIGHTS = {
    "realesrgan":      ("RealESRGAN_x4plus.pth",              "url",   "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"),
    "realesrgan_anime":("RealESRGAN_x4plus_anime_6B.pth",     "url",   "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth"),
    "swinir":          ("001_classicalSR_DIV2K_s48w8_SwinIR-M_x4.pth", "url", "https://github.com/JingyunLiang/SwinIR/releases/download/v0.0/001_classicalSR_DIV2K_s48w8_SwinIR-M_x4.pth"),
    "hat":             ("HAT_SRx4_ImageNet-pretrain.pth",      "drive", "1HpmReFfoUqUbnAOQ7rvOeNU3uf_m69w0"),
    "supir":           ("SUPIR-v0F.ckpt",                      "manual","1yELzm5SvAi9e7kPcO_jPp2XkTs4vK6aR"),
}


def _get(key: str) -> Path:
    filename, kind, src = WEIGHTS[key]
    if kind == "url":
        return from_url(src, filename)
    if kind == "drive":
        return from_drive(src, filename)
    dest = weight_path(filename)
    if not dest.exists():
        raise RuntimeError(
            f"SUPIR weight missing.\n"
            f"  Get from: https://drive.google.com/drive/folders/{src}\n"
            f"  Place '{filename}' in: {dest.parent}"
        )
    return dest


def _refine(img: Image.Image, model_out: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Run model at 4x then resize back to target - refinement pass."""
    return model_out.resize((target_w, target_h), Image.LANCZOS)


def upscale(img_path: Path, scale: int, anime: bool = False) -> Path:
    from .models.realesrgan import run as resr_run
    from .models.spandrel_model import run as spandrel_run

    img    = Image.open(img_path).convert("RGB")
    w, h   = img.size
    tw, th = w * scale, h * scale

    print(f"\n  Source: {w}x{h}  |  Target: {tw}x{th}")
    print(f"  Chain: RealESRGAN -> SwinIR -> HAT -> SUPIR (if available)\n")

    # Step 1: RealESRGAN - base upscale to target
    key = "realesrgan_anime" if anime else "realesrgan"
    print(f"  [1/4] RealESRGAN {'anime' if anime else 'x4plus'}...")
    out = resr_run(img, _get(key), anime=anime)
    out = out.resize((tw, th), Image.LANCZOS)

    # Step 2: SwinIR - refinement pass
    print(f"  [2/4] SwinIR...")
    out_4x = spandrel_run(out, _get("swinir"))
    out    = _refine(out, out_4x, tw, th)

    # Step 3: HAT - refinement pass
    print(f"  [3/4] HAT...")
    out_4x = spandrel_run(out, _get("hat"))
    out    = _refine(out, out_4x, tw, th)

    # Step 4: SUPIR - optional final refinement
    supir_w = weight_path(WEIGHTS["supir"][0])
    if supir_w.exists():
        from .models.supir import run as supir_run
        print(f"  [4/4] SUPIR...")
        try:
            out = supir_run(out, supir_w)
            out = out.resize((tw, th), Image.LANCZOS)
        except NotImplementedError as e:
            print(f"  [4/4] SUPIR skipped: {e}")
    else:
        print(f"  [4/4] SUPIR skipped (weights not found, see README)")

    suffix  = f"_upscaled_{scale}x"
    out_path = img_path.parent / f"{img_path.stem}{suffix}{img_path.suffix}"
    out.save(str(out_path))
    print(f"\n  Done -> {out_path}")
    return out_path
