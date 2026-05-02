# XUpscaler-Art ~

hey! a tiny CLI for upscaling digital art with real SR models.
drop your image path, pick a scale, done. outputs stay right next to your file.

---

## install

```bash
git clone https://github.com/you/XUpscaler-Art
cd XUpscaler-Art
pip install .
```

or for dev mode:

```bash
pip install -e .
```

this installs a `xupscaler` command globally (in your env).

> **torch + CUDA:** install PyTorch manually first from https://pytorch.org/get-started/locally
> for GPU support. CPU fallback works out of the box.

---

## first run

model weights download automatically the first time you use them.
nothing downloads at install time.

cache location:
- **Linux / macOS:** `~/.cache/xupscaler-art/weights/`
- **Windows:** `%LOCALAPPDATA%\xupscaler-art\weights\`

second run and beyond use the cached weights, instant start.

---

## usage

```bash
xupscaler
```

```
  XUpscaler-Art ~

Image path (drag & drop or paste): /path/to/art.png
Scale (2 / 4 / 8): 4

Model:
  1. RealESRGAN_x4plus
  2. RealESRGAN_x4plus_anime_6B
  3. SwinIR
  4. HAT
  5. SUPIR  (manual setup required)
Pick (1-5): 2

  Downloading RealESRGAN_x4plus_anime_6B.pth...
  100.0%  (17 MB)
  RealESRGAN_x4plus_anime_6B  |  512x512  ->  2048x2048
  Saved -> /path/to/art_upscaled_4x.png
```

---

## models

| model | best for |
|---|---|
| RealESRGAN_x4plus | photos, general art |
| RealESRGAN_x4plus_anime_6B | anime, flat colors, illustration |
| SwinIR | clean lines, classical SR |
| HAT | high detail, textures |
| SUPIR | extreme fidelity (needs manual setup) |

scale 2x and 8x run the model at 4x then resize. all models output 4x natively.

---

## examples

```bash
# quick 2x on a sketch
xupscaler
# -> sketch.png, scale 2, model 2

# high quality 4x photo
xupscaler
# -> photo.jpg, scale 4, model 1

# 8x anime art
xupscaler
# -> art.png, scale 8, model 2
```

output always saves next to the input: `art_upscaled_4x.png`

---

## troubleshooting

**HAT or SUPIR download fails (Drive quota)**
manually download from the links below and place the `.pth` / `.ckpt` in your cache folder.
- HAT: https://drive.google.com/drive/folders/1HpmReFfoUqUbnAOQ7rvOeNU3uf_m69w0
- SUPIR: https://drive.google.com/drive/folders/1yELzm5SvAi9e7kPcO_jPp2XkTs4vK6aR

**SUPIR not working**
it needs SDXL + CLIP, follow the full setup at https://github.com/Fanghua-Yu/SUPIR

**out of VRAM**
SwinIR and HAT fall back to CPU automatically.
RealESRGAN uses tiled processing, safe for large images.

**basicsr install fails**
```bash
pip install basicsr --no-build-isolation
```

---

## OS notes

| platform | notes |
|---|---|
| Windows | drag-drop adds quotes, stripped automatically |
| Ubuntu 23.04+ | use a virtualenv: `python -m venv .venv && source .venv/bin/activate` |
| Kali Linux | may need `--break-system-packages` outside a venv |
| Arch Linux | works as-is with pip |
| macOS (Apple Silicon) | CPU fallback applies, MPS not explicitly targeted |

---

made with love for artists who just want sharper pixels ^^
