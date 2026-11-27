"""Pod-side: character reference images with SDXL base 1.0. Usage: python gen_refs.py prompts.json outdir"""
import json, sys, os, torch
from diffusers import StableDiffusionXLPipeline
P = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
pipe = StableDiffusionXLPipeline.from_pretrained('/workspace/sdxl', torch_dtype=torch.float16, variant='fp16', use_safetensors=True).to('cuda')
NEG = 'photo, realistic, scary, creepy, deformed, extra legs, extra limbs, extra tail, blurry, text, watermark, logo, human, multiple animals, cropped'
for name, spec in P.items():
    for seed in spec['seeds']:
        img = pipe(spec['prompt'], negative_prompt=NEG, num_inference_steps=35, guidance_scale=6.5, height=1024, width=1024,
                   generator=torch.Generator('cuda').manual_seed(seed)).images[0]
        img.save(f'{out}/{name}_s{seed}.png'); print('saved', name, seed, flush=True)
