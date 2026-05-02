from pathlib import Path
from PIL import Image


def run(img: Image.Image, weight_path: Path, model_name: str) -> Image.Image:
    raise NotImplementedError(
        "SUPIR requires a full manual environment setup.\n"
        "  Repo:    https://github.com/Fanghua-Yu/SUPIR\n"
        "  Weights: https://drive.google.com/drive/folders/1yELzm5SvAi9e7kPcO_jPp2XkTs4vK6aR\n"
        "  Follow the repo README, then place SUPIR-v0F.ckpt in your weights cache."
    )
