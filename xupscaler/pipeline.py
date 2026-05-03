import urllib.request
from pathlib import Path
from .cache import weight_path


def _progress(block, block_size, total):
    done = min(block * block_size, total)
    pct  = done / total * 100 if total > 0 else 0
    print(f"\r  {pct:5.1f}%  ({done // 1024 // 1024} MB)", end="", flush=True)


def from_url(url: str, filename: str) -> Path:
    dest = weight_path(filename)
    if dest.exists():
        return dest
    print(f"  Downloading {filename}...")
    urllib.request.urlretrieve(url, dest, _progress)
    print()
    return dest


def from_drive(folder_id: str, filename: str) -> Path:
    dest = weight_path(filename)
    if dest.exists():
        return dest
    import gdown
    print(f"  Downloading {filename} from Drive...")
    try:
        gdown.download_folder(id=folder_id, output=str(dest.parent), quiet=False, use_cookies=False)
        if dest.exists():
            return dest
        raise FileNotFoundError(f"{filename} not found after folder download.")
    except Exception as exc:
        raise RuntimeError(
            f"Drive download failed for {filename}.\n"
            f"  Manual: https://drive.google.com/drive/folders/{folder_id}\n"
            f"  Place '{filename}' in: {dest.parent}"
        ) from exc
