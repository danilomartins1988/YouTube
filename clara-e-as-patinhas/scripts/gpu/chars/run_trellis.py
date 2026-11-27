"""Pod-side: image -> 3D with TRELLIS-image-large. Exports vertex-coloured mesh (PLY/GLB via trimesh) per image.
Usage: python run_trellis.py img1.png [img2.png ...]"""
import os, sys
os.environ['ATTN_BACKEND'] = 'xformers'; os.environ['SPCONV_ALGO'] = 'native'
sys.path.insert(0, '/workspace/TRELLIS')
import numpy as np, torch, trimesh
from PIL import Image
from trellis.pipelines import TrellisImageTo3DPipeline
pipe = TrellisImageTo3DPipeline.from_pretrained('JeffreyXiang/TRELLIS-image-large'); pipe.cuda()
for p in sys.argv[1:]:
    img = Image.open(p)
    out = pipe.run(img, seed=1, formats=['mesh'], sparse_structure_sampler_params={'steps': 12, 'cfg_strength': 7.5},
                   slat_sampler_params={'steps': 12, 'cfg_strength': 3})
    m = out['mesh'][0]
    v = m.vertices.detach().cpu().numpy(); f = m.faces.detach().cpu().numpy()
    attrs = m.vertex_attrs.detach().cpu().numpy() if getattr(m, 'vertex_attrs', None) is not None else None
    col = (np.clip(attrs[:, :3], 0, 1) * 255).astype(np.uint8) if attrs is not None else None
    v = v @ np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])  # y-up -> z-up for Blender
    tm = trimesh.Trimesh(vertices=v, faces=f, vertex_colors=col, process=False)
    base = os.path.splitext(p)[0]
    tm.export(base + '_trellis.ply'); print('mesh', p, len(v), 'verts', len(f), 'faces', flush=True)
