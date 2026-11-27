#!/bin/bash
# Pod-side: TRELLIS (MIT code + MIT weights). nvdiffrast is NOT installed on purpose (NVIDIA non-commercial licence);
# we export the decoded mesh with vertex colours instead of the nvdiffrast texture bake.
set -e
cd /workspace && [ -d TRELLIS ] || git clone -q --recurse-submodules https://github.com/microsoft/TRELLIS.git
pip install -q pillow imageio imageio-ffmpeg tqdm easydict opencv-python-headless scipy ninja rembg onnxruntime trimesh xatlas pyvista pymeshfix igraph plyfile 2>&1 | tail -1
pip install -q git+https://github.com/EasternJournalist/utils3d.git@9a4eb15e4021b67b12c460c7057d642626897ec8 2>&1 | tail -1
pip install -q xformers==0.0.27.post2 2>&1 | tail -1
pip install -q spconv-cu120 2>&1 | tail -1
pip install -q kaolin -f https://nvidia-kaolin.s3.us-east-2.amazonaws.com/torch-2.4.0_cu121.html 2>&1 | tail -1
python -c "import torch, xformers, spconv, kaolin; print('TRELLIS deps OK', torch.__version__, xformers.__version__, kaolin.__version__)"
