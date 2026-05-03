import torch
import numpy as np
from pathlib import Path
from PIL import Image


def run(img: Image.Image, weight: Path) -> Image.Image:
    from spandrel import ModelLoader

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model  = ModelLoader().load_from_file(str(weight))
    model.eval().to(device)

    arr = np.array(img).astype(np.float32) / 255.0
    t   = torch.from_numpy(arr).permute(2, 0, 1).unsqueeze(0).to(device)

    try:
        with torch.no_grad():
            out = model(t)
    except (torch.cuda.OutOfMemoryError, RuntimeError) as exc:
        if "memory" in str(exc).lower() or "cuda" in str(exc).lower():
            print("  VRAM low, retrying on CPU...")
            model.to("cpu")
            with torch.no_grad():
                out = model(t.to("cpu"))
        else:
            raise

    result = out.squeeze(0).permute(1, 2, 0).clamp(0, 1).mul(255).byte().cpu().numpy()
    return Image.fromarray(result)
