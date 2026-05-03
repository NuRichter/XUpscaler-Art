import os, platform
from pathlib import Path


def weights_dir() -> Path:
    if platform.system() == "Windows":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    d = base / "xupscaler-art" / "weights"
    d.mkdir(parents=True, exist_ok=True)
    return d


def weight_path(filename: str) -> Path:
    return weights_dir() / filename
