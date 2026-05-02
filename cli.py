from pathlib import Path
from .pipeline import upscale

MODELS = [
    "RealESRGAN_x4plus",
    "RealESRGAN_x4plus_anime_6B",
    "SwinIR",
    "HAT",
    "SUPIR",
]

EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}


def _ask_path() -> Path:
    while True:
        raw = input("\nImage path (drag & drop or paste): ").strip().strip('"').strip("'")
        p = Path(raw)
        if not p.is_file():
            print(f"  Not found: {p}")
            continue
        if p.suffix.lower() not in EXTS:
            print(f"  Unsupported format. Use: {', '.join(EXTS)}")
            continue
        return p


def _ask_scale() -> int:
    while True:
        raw = input("Scale (2 / 4 / 8): ").strip().replace("x", "")
        if raw in {"2", "4", "8"}:
            return int(raw)
        print("  Enter 2, 4, or 8.")


def _ask_model() -> str:
    print("\nModel:")
    for i, m in enumerate(MODELS, 1):
        note = "  (manual setup)" if m == "SUPIR" else ""
        print(f"  {i}. {m}{note}")
    while True:
        raw = input("Pick (1-5): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= 5:
            return MODELS[int(raw) - 1]
        print("  Pick 1-5.")


def run():
    print("\n  XUpscaler-Art ~\n")
    try:
        path  = _ask_path()
        scale = _ask_scale()
        model = _ask_model()
        print()
        upscale(path, scale, model)
    except KeyboardInterrupt:
        print("\n  Bye!")
    except Exception as e:
        print(f"\n  Error: {e}")
