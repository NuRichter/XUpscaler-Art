from pathlib import Path
from .pipeline import upscale, REGISTRY

EXTS        = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}
MODEL_NAMES = list(REGISTRY.keys())


def _ask_path() -> Path:
    while True:
        raw = input("\nImage path (drag & drop or paste): ").strip().strip('"').strip("'")
        p = Path(raw)
        if not p.is_file():
            print(f"  Not found: {p}")
            continue
        if p.suffix.lower() not in EXTS:
            print(f"  Unsupported: {p.suffix}")
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
    for i, name in enumerate(MODEL_NAMES, 1):
        note = "  (manual setup required)" if name == "SUPIR" else ""
        print(f"  {i}. {name}{note}")
    n = len(MODEL_NAMES)
    while True:
        raw = input(f"Pick (1-{n}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= n:
            return MODEL_NAMES[int(raw) - 1]
        print(f"  Pick 1-{n}.")


def main():
    print("\n  XUpscaler-Art ~\n")
    try:
        path  = _ask_path()
        scale = _ask_scale()
        model = _ask_model()
        print()
        upscale(path, scale, model)
    except KeyboardInterrupt:
        print("\n  Bye!")
    except Exception as exc:
        print(f"\n  Error: {exc}")
