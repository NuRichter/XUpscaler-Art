import numpy as np
from pathlib import Path
from PIL import Image


def run(img: Image.Image, weight: Path, anime: bool = False) -> Image.Image:
    import cv2
    from basicsr.archs.rrdbnet_arch import RRDBNet
    from realesrgan import RealESRGANer

    arch = RRDBNet(
        num_in_ch=3, num_out_ch=3,
        num_feat=64, num_block=6 if anime else 23,
        num_grow_ch=32, scale=4,
    )
    up = RealESRGANer(
        scale=4, model_path=str(weight), model=arch,
        tile=512, tile_pad=10, pre_pad=0, half=False,
    )
    bgr    = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    out, _ = up.enhance(bgr, outscale=4)
    return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
