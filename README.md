# XUpscaler-Art ~

hey! this runs your image through a full chain of SR models, one after another.
not just upscaling - each model refines the previous output. one input, one output, maximum detail.

**chain order:**
```
RealESRGAN -> SwinIR -> HAT -> SUPIR (optional)
```

---

## how the chain works

```
Input (512x512), scale 4x = target 2048x2048

[1] RealESRGAN:  512  -> 2048        (base upscale to target)
[2] SwinIR:     2048  -> 8192 -> 2048 (refinement pass)
[3] HAT:        2048  -> 8192 -> 2048 (refinement pass)
[4] SUPIR:      2048  -> 2048        (restoration, if weights present)

Output: 2048x2048 (single file)
```

each step after the first runs at 4x internally then resizes back to target.
this injects each model's learned detail without blowing up resolution.

SUPIR is skipped gracefully if weights are not found.

---

## install

```bash
git clone https://github.com/you/XUpscaler-Art
cd XUpscaler-Art
pip install .
```

> install PyTorch with CUDA first for GPU: https://pytorch.org/get-started/locally
> CPU fallback works automatically.

---

## first run

weights download automatically on first run, per model.
nothing downloads at install time.

cache:
- **Linux / macOS:** `~/.cache/xupscaler-art/weights/`
- **Windows:** `%LOCALAPPDATA%\xupscaler-art\weights\`

**SUPIR** requires manual download (SDXL backbone, too heavy to auto-install):
1. download `SUPIR-v0F.ckpt` from https://drive.google.com/drive/folders/1yELzm5SvAi9e7kPcO_jPp2XkTs4vK6aR
2. place it in your cache folder above
3. follow full env setup at https://github.com/Fanghua-Yu/SUPIR

if the file is not there, SUPIR step is skipped - the chain still runs fine.

---

## usage

```bash
xupscaler
```

```
  XUpscaler-Art ~
  chain: RealESRGAN -> SwinIR -> HAT -> SUPIR

Image path (drag & drop or paste): /art/my_sketch.png
Scale (2 / 4 / 8): 4
Anime / flat illustration? (y/n): y

  Source: 512x512  |  Target: 2048x2048
  Chain: RealESRGAN -> SwinIR -> HAT -> SUPIR (if available)

  [1/4] RealESRGAN anime...
  [2/4] SwinIR...
  [3/4] HAT...
  [4/4] SUPIR skipped (weights not found, see README)

  Done -> /art/my_sketch_upscaled_4x.png
```

output saves next to input with suffix `_upscaled_4x`.

---

## troubleshooting

**HAT download fails (Drive quota)**
manually download `HAT_SRx4_ImageNet-pretrain.pth` from:
https://drive.google.com/drive/folders/1HpmReFfoUqUbnAOQ7rvOeNU3uf_m69w0
place it in the weights cache folder.

**out of VRAM on SwinIR or HAT**
auto-falls back to CPU. slow but works.

**basicsr install fails**
```bash
pip install basicsr --no-build-isolation
```

**image looks over-sharpened**
try scale 2x instead of 8x. the chain is aggressive - it's designed to be.

---

## OS notes

| platform | notes |
|---|---|
| Windows | drag-drop quotes stripped automatically |
| Ubuntu 23.04+ | use a virtualenv |
| Kali Linux | may need `--break-system-packages` outside venv |
| Arch Linux | works as-is |
| macOS (Apple Silicon) | CPU fallback, MPS not targeted |

---

made for artists who want every pixel to matter ^^
