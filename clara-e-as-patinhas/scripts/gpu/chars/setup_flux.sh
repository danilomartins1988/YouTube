#!/bin/bash
# Pod-side: FLUX.1-schnell (Apache-2.0) via diffusers. Downloads only the diffusers-format weights (~33 GB).
set -e
pip install -q "diffusers==0.31.0" "transformers==4.46.3" accelerate sentencepiece protobuf "huggingface_hub>=0.26" 2>&1 | tail -2
python - <<'PY'
from huggingface_hub import snapshot_download
p = snapshot_download('black-forest-labs/FLUX.1-schnell', local_dir='/workspace/flux',
    allow_patterns=['model_index.json', 'scheduler/*', 'text_encoder/*', 'text_encoder_2/*', 'tokenizer/*', 'tokenizer_2/*', 'transformer/*', 'vae/*', 'LICENSE*', 'README.md'])
print('FLUX OK', p)
PY
