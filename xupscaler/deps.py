from pathlib import Path
from .pipeline import upscale

EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}


def _ask_path() -> Path:
    while True:
        raw = input("\nImage path (drag & drop or paste): ").strip().strip('"').strip("'")
        p = Path(raw)
        if not p.is_file():
            print(f"  Not found: {p}")
            continue
        if p.suffix.lower() not in EXTS:
            print(f"  Unsupported format: {p.suffix}")
            continue
        return p


def _ask_scale() -> int:
    while True:
        raw = input("Scale (2 / 4 / 8): ").strip().replace("x", "")
        if raw in {"2", "4", "8"}:
            return int(raw)
        print("  Enter 2, 4, or 8.")


def _ask_anime() -> bool:
    raw = input("Anime / flat illustration? (y/n): ").strip().lower()
    return raw in {"y", "yes"}


def main():
    print("\n  XUpscaler-Art ~")
    print("  chain: RealESRGAN -> SwinIR -> HAT -> SUPIR\n")
    try:
        path  = _ask_path()
        scale = _ask_scale()
        anime = _ask_anime()
        upscale(path, scale, anime)
    except KeyboardInterrupt:
        print("\n  Bye!")
    except Exception as exc:
        print(f"\n  Error: {exc}")
