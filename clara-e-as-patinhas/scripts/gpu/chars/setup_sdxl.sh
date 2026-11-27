#!/bin/bash
# Pod-side: Stable Diffusion XL base 1.0 (CreativeML Open RAIL++-M: commercial use allowed with use-based restrictions). Ungated.
set -e
pip install -q "diffusers==0.31.0" "transformers==4.46.3" accelerate safetensors 2>&1 | tail -1
python - <<'PY'
from huggingface_hub import snapshot_download
p = snapshot_download('stabilityai/stable-diffusion-xl-base-1.0', local_dir='/workspace/sdxl',
    allow_patterns=['model_index.json', 'scheduler/*', 'text_encoder/*fp16.safetensors', 'text_encoder/config.json', 'text_encoder_2/*fp16.safetensors',
                    'text_encoder_2/config.json', 'tokenizer/*', 'tokenizer_2/*', 'unet/*fp16.safetensors', 'unet/config.json', 'vae/*fp16.safetensors', 'vae/config.json', 'LICENSE*'])
print('SDXL OK', p)
PY
