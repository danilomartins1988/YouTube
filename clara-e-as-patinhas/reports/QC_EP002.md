# QC — Episódio 002 "Cadê? Achou!"

Avaliado em 2026-11-27 a partir dos arquivos reais: `output/cade_achou_1080p.mp4`, `output/cade_achou_light.mp4` e o teste de movimento de 10 s.

## Técnica
| Item | Resultado |
|---|---|
| Vídeo | 1920×1080 **nativo** (no ep. 001 era 720p ampliado), 24 fps, 3.019 frames, 2:05,8 |
| Áudio | `music/masters/cade_achou_final.wav` (aprovado pelo proprietário). MP4: **-14,0 LUFS**, pico -1,3 dBFS (1080p) / -1,2 (light) |
| Arquivos | 1080p CRF 18: 106 MB · light (2 passagens, 2,75 Mbps): **45 MB** |
| Integridade | decodificação `ffmpeg -v error` sem erros nos dois |
| Render | EEVEE "L1M": luz de 3 pontos, gradação + vinheta, DOF, motion blur, sombras de contato, 16 amostras. RunPod, 16 instâncias paralelas, **16,7 min** de render |
| GPU | Host com CUDA quebrado (`cuInit` 999): o Cycles não rodou. O EEVEE rodou por EGL/software nos 144 núcleos do host. Custo total do pod: 0,70 h ≈ **US$ 0,24** |

## Sincronia (frames conferidos nos tempos reais da faixa)
| Momento | Tempo | Antes / depois | OK |
|---|---|---|---|
| ACHOU 1 (flor) | 33,84 s | 33,6: orelha e bandana atrás da flor → 34,1: a cachorrinha de bandana azul no ar saindo da flor | ✅ |
| ACHOU 2 (balde) | 58,66 s | 58,5: rabinho branco no balde → 59,1: a branquinha no ar acima do balde | ✅ |
| ACHOU 3 (chapéu) | 82,20 s | 82,1: chapéu fechado → 82,6: o Yorkshire de pé, chapéu subindo e voando para a menina | ✅ |
| ACHOU 4 (menina) | 98,28 s | 98,1: rosto coberto pelo chapéu → 98,7: chapéu na cabeça, braços para cima | ✅ |
| ACHOU 5 (você) | 111,92 s | 111,8: coberto → 112,4: chapéu na cabeça (com motion blur forte no movimento) | ✅ |
| Boca da menina | | Formas por visema seguem a letra: aberta em "cadê/você", boca fechada no M de "mim", fechada nas partes instrumentais | ✅ |
| Pés no chão e bichos escondidos | | Frames a cada 5 s: pés no chão. Nenhuma cachorrinha visível antes do seu ACHOU | ✅ |
| Nomes na tela | | Nenhum texto no vídeo. Casinhas com patinha | ✅ |

## Limites conhecidos (honestos)
- Nas estrofes 1 a 3 a câmera mostra a menina de costas ou de lado olhando o esconderijo. É intencional (o foco é o esconderijo), mas o rosto dela aparece pouco nesses trechos.
- Motion blur forte nos movimentos rápidos do chapéu e dos braços (obturador de 0,5).
- O rig continua rígido, de peças, sem pele que deforma. A menina tapa o rosto com o chapéu porque os braços não alcançam os olhos.
- O pelo continua aproximado (shells). Os personagens continuam sendo os modelos procedurais do ep. 001. O Yorkshire ganhou um topete curto para ler como macho (Toby).

## Rubrica ponderada (a mesma do QC do ep. 001)
| Critério | Peso | Nota | Comentário |
|---|---|---|---|
| Música e voz | 25% | 8,5 | Aprovada pelo proprietário. Pausas de suspense, refrão repetitivo, voz consistente com o ep. 001 |
| Personagens | 20% | 5,5 | Mesmos modelos, com luz e DOF melhores |
| Animação e sincronia | 15% | 7,5 | ACHOUs no tempo exato, visemas, squash-and-stretch, orelhas e cauda com atraso, entrega do chapéu |
| Consistência | 10% | 8 | |
| Cenário e luz | 10% | 7,5 | Luz de 3 pontos, DOF, props novos |
| Técnica | 10% | 9 | 1080p nativo, -14 LUFS, sem erros |
| Entregáveis e marca | 10% | 8,5 | Thumbnail com uma protagonista, metadados para crianças, divulgação de IA |
| **Total** | | **≈ 7,6 / 10** | O ep. 001 tinha 6,9 |

Para passar de 9 é preciso ter personagens canônicos refeitos (malha que deforma, blendshapes faciais, pelo com grooming) e atuação feita à mão. Com o pipeline de GPU que já funciona, **refazer o render deste episódio com novos modelos canônicos custa pouco**: ~17 min de pod, ≈ US$ 0,10–0,25, mais o encode. O roteiro, as câmeras e a sincronia ficam em `scripts/blender/episode2.py`.
