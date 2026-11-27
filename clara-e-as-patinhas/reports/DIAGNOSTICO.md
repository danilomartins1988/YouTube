# Diagnóstico técnico (medido em 2026-11-27)

## Máquina
| Item | Valor |
|---|---|
| SO | Ubuntu 24.04.5 LTS, kernel Linux 6.18 (container na nuvem) |
| CPU | 4 núcleos, Intel Xeon Processor @ 2.10GHz |
| RAM | 15 GB, sem swap |
| GPU | **nenhuma**. Todo o OpenGL roda em software (Mesa 25.2.8, llvmpipe, por EGL *surfaceless*) |
| Disco | 252 GB no total, **~3,2 GB livres** no início (2,4–2,9 GB depois de instalar o Blender) |

## Ferramentas
| Ferramenta | Versão | Situação |
|---|---|---|
| Blender | 4.0.2 (pacote Debian/Ubuntu `blender` 4.0.2+dfsg) | **Instalado nesta sessão** via `apt-get install --no-install-recommends blender`: ~120 MB de download e ~300 MB em disco |
| python3-numpy (para o Python 3.12 embutido no Blender) | 1.26.4 | Instalado nesta sessão (apt) |
| FluidSynth | 2.3.4 | Já estava instalado |
| Soundfont FluidR3_GM | `/usr/share/sounds/sf2/FluidR3_GM.sf2` (148 MB) | Já estava instalado |
| ffmpeg | 6.1.1 (libx264) | Disponível |
| Python 3 (sistema) | 3.13, com `mido` 1.3.3, numpy 2.x e Pillow 12 | Disponível |
| Fonte Fredoka (OFL) | npm `@fontsource/fredoka` 5.0.13 (woff) | Baixada para `assets/branding/fonts/` |

Limitações do build do Blender no Debian:
- **Sem OpenImageDenoise**: o Cycles falha com "Build without OpenImageDenoiser" quando o denoising está ligado, então o Cycles na CPU fica sem denoiser.
- O módulo `gpu` não está disponível em modo background.

## Motores de render que funcionam sem GPU
Cena de teste: 3 esferas, plano, sol e mundo, em **1920×1080**. Script: `scripts/diag_render_test.py`.

| Motor | Configuração | Tempo por frame (medido) | Observações |
|---|---|---|---|
| Workbench | padrão | **1,4 s** | Sombreamento de viewport, sem materiais reais. Não serve como produto final |
| EEVEE (OpenGL por llvmpipe/EGL surfaceless) | 32 amostras TAA | **6,8 s** | Funciona em background. Aparecem avisos de EGL, mas o render completa |
| EEVEE | 64 amostras | **11,7 s** | |
| Cycles (CPU) | 16 amostras, sem denoise | **14,1 s** | Ruído visível |
| Cycles (CPU) | 64 amostras, sem denoise | **56,5 s** | Ainda com ruído, sem denoiser |

## Medições na cena real do episódio
Jardim completo, 4 personagens e fur shells. Cerca de 600 mil polígonos com LOD 1.0; LOD 0.6 em produção.

| Configuração | s/frame |
|---|---|
| EEVEE 1920×1080, 16 amostras, `render()` por frame | 29–35 |
| EEVEE 1280×720, 16 amostras | 27–31 |
| EEVEE 1280×720, 8 amostras, sombras de 512 | 17–19 |
| EEVEE 1280×720, 8 amostras, modo animação (sem reinicializar por frame) | **9,9** |
| idem, com **LOD 0.6** | **6,2** |
| Produção real (render_driver, modo animação, 720p, 8 amostras, LOD 0.6, 24 fps) | **≈5,3–5,6** (≈97 frames por lote de 9,5 min) |

Conclusões:
- O custo é quase todo **por amostra × geometria**: rasterizar e montar mapas de sombra no llvmpipe. Resolução quase não pesa (720p ≈ 1080p).
- Chamar `render.render()` frame a frame custa cerca de 2× mais que `render(animation=True)`, por causa da reinicialização do EEVEE.
- **Escolha de produção:** EEVEE, 1280×720 a 24 fps, 8 amostras e LOD 0.6, depois ampliado para 1920×1080 com Lanczos no ffmpeg. São 4.016 frames × ~5,4 s ≈ **6 h de CPU** para 2:47.
- Cycles na CPU sem denoiser seria inviável: mais de 60 s por frame, o que daria mais de 70 h e ainda com ruído.
