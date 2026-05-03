import subprocess, sys

_DEPS = [
    ("PIL",        "Pillow"),
    ("numpy",      "numpy"),
    ("requests",   "requests"),
    ("gdown",      "gdown"),
    ("cv2",        "opencv-python"),
    ("torch",      "torch"),
    ("torchvision","torchvision"),
    ("spandrel",   "spandrel"),
    ("basicsr",    "basicsr"),
    ("realesrgan", "realesrgan"),
]

def ensure_all():
    for import_name, pip_name in _DEPS:
        try:
            __import__(import_name)
        except ImportError:
            print(f"[deps] installing {pip_name}...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pip_name, "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
