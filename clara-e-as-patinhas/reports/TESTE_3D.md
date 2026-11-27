# Teste 3D e episódio piloto: avaliação honesta

## O que foi produzido
| Arquivo | Conteúdo |
|---|---|
| `output/teste_3d_light.mp4` | Teste de 14,5 s (refrão 1, de 0:25,0 a 0:39,5 da música). 1920×1080 (ampliado de 720p), 24 fps, H.264 CRF 23, áudio do instrumental-guia. 10 MB |
| `output/teste_3d_contact_sheet.jpg` | 15 frames do teste (1 por segundo) |
| `output/danca_das_patinhas_1080p.mp4` | Episódio completo, 2:47,4, 1920×1080, 24 fps, CRF 18, 329 MB |
| `output/danca_das_patinhas_light.mp4` | Mesmo episódio a 2,4 Mbit/s, **53 MB** |
| `assets/characters/<nome>/sheet_turnaround.png`, `sheet_expressions.png`, `sheet_pose.png` | Model sheets |
| `assets/characters/grupo.png`, `assets/characters/proporcoes.png` | Imagem de grupo e régua de proporções |

**Atenção:** a trilha do vídeo é o **instrumental-guia SEM VOZ**. A geração cantada (Eleven Music) foi bloqueada pelas permissões da sessão (veja `reports/ELEVEN_MUSIC_PLAN.md`). A boca da Clara segue as notas da melodia-guia, ou seja, onde a voz *vai* estar.

## Configuração de render escolhida e tempos medidos
- **EEVEE** (OpenGL em software, llvmpipe), **1280×720**, **8 amostras**, sombras suaves (cubo de 512, cascata de 2048), AO ligado e bloom leve.
- **LOD 0.6** (menos polígonos), **24 fps**, ampliado para 1080p com Lanczos no ffmpeg.
- **Medido:** de 4,6 a 5,7 s por frame em lotes de 9,5 min (de 97 a 121 frames por lote), média de **≈5,3 s/frame**.
- **Episódio completo:** 4.016 frames ≈ **6 h de CPU**, mais uns 20 min para refazer um segmento com um PNG corrompido. Rodou em ~43 lotes retomáveis.
- **Alternativas descartadas, com números** (veja `reports/DIAGNOSTICO.md`):
  - 1080p a 16 amostras: 29–35 s/frame, o que daria ~36 h.
  - Cycles na CPU sem denoiser: >60 s/frame com ruído, o que daria mais de 70 h.
  - Workbench: 1,4 s/frame, mas sem materiais nem luz de verdade.

## Checagem dos frames (feita por mim, olhando os frames)
| Item | Resultado |
|---|---|
| Manchas merle da Ayra | **Fixas**: estão gravadas numa textura UV gerada uma vez (ruído determinístico) e acompanham o corpo. Iguais em todas as cenas e nas sheets. Peito, patas e ponta da cauda brancos |
| Pandora branca e fofa | Branca em todas as cenas. A "fofura" vem de deslocamento + 5 *fur shells* com alpha. De perto aparecem pontinhos (alpha-clip) e falta definição de pelo |
| Pelagem da Tifa | Dorso cinza-aço e rosto/patas/peito castanho-dourados, consistentes. A bandana verde está presente |
| Clara | Cabelo castanho brilhante na altura dos ombros com franja lateral, presilha de flor, macacão amarelo, camiseta branca e tênis rosa/azul, consistentes em todas as cenas |
| Escala | Clara 1,00 m; Ayra ~0,36 m (até o joelho, como pede o brief); Pandora ~0,27 m; Tifa ~0,24 m |
| Pés no chão | No geral, sim. A raiz fica no chão (no lago e na ponte segue a altura da ponte). Nos pulos o corpo sobe de propósito. No passo para trás da Clara o pé pode entrar uns mm no gramado |
| Deformações | **Não há deformação de malha** porque o rig é rígido (cada parte presa a um osso). Em compensação, as articulações são "de boneco": em giros extremos o braço gira dentro da manga e a perna dentro do quadril. Sem cotovelo/joelho com pele contínua |
| Sincronia | As cenas trocam nas mudanças de seção ou de verso. Palmas da Clara nos tempos 2 e 4 do refrão e das pausas (coincidem com as palmas do áudio). 3 pulinhos da Tifa exatamente em "um, dois, três". Pulinhos das cachorrinhas nos "AU". Nomes cantados com pulinho de cada cachorrinha |
| Áudio | Pico de -1,3 dBFS, média de -19 dB, sem clipping |
| Integridade | `ffmpeg -v error` com 0 erros nos 3 MP4. Episódio de 167,4 s |
| Problema corrigido no QC | Um PNG ficou truncado por um timeout e o segmento 14 saiu com um frame deslocado. **Re-renderizado**, e o driver agora valida os PNGs antes de codificar |

## Avaliação honesta contra o objetivo "série infantil 3D premium e cinematográfica"
**Isto NÃO é 3D cinematográfico premium.** É uma **animação 3D estilizada, limpa e colorida, de nível "protótipo/animatic de alta qualidade"**, feita 100% por código, numa CPU de 4 núcleos e sem GPU. Ela serve bem para validar personagens, cores, coreografia, ritmo e enquadramentos com o público e o proprietário, mas não chega a padrões como Cocomelon, Bluey 3D ou Pixar.

O que funciona:
- Personagens fofos, legíveis e com silhueta clara.
- Paleta fiel ao brief, olhos grandes com brilho e expressões distintas.
- Jardim completo: casa, casinhas com nomes, lago, ponte, balanço, flores, borboletas e brinquedos.
- Coreografia ligada à letra, câmeras que mudam com a música e ambiente iluminado e agradável.

O que falta para "premium":
1. **Modelagem e rig:** as formas são primitivas (elipsoides e cápsulas) e o rig é rígido, sem skinning, blendshapes nem squash & stretch. Isso precisa de um artista 3D: escultura, topologia, weight painting, controles faciais.
2. **Pelo:** os *fur shells* são uma aproximação. Pelo de verdade (curvas de cabelo com sombreamento de fios) precisa de Cycles/EEVEE Next com GPU ou de muito mais tempo de CPU. No teste com partículas de cabelo no EEVEE por llvmpipe, os fios ficaram escuros e ruins, então foram descartados.
3. **Animação:** é procedural, com curvas senoidais e *easing*. Falta atuação: antecipação, *overlap*, peso, poses-chave. Isso exige um animador, ou no mínimo keyframing manual.
4. **Iluminação e render:** EEVEE a 720p com 8 amostras, ampliado. Sem GI real, sem SSR nem reflexos no lago, AA limitado. Uma GPU (mesmo modesta) com EEVEE Next ou Cycles e denoise permitiria 1080p/4K, GI e profundidade de campo em horas, não dias.
5. **Lip-sync:** abrir e fechar a boca pela envoltória das notas da melodia-guia. Com a voz real dá para fazer visemas pelos tempos de palavra do Whisper, mas ainda seria básico.
6. **Áudio:** sem voz cantada. O instrumental-guia é General MIDI/FluidR3 (som de demonstração).

## Próximos passos recomendados
1. Liberar a geração Eleven Music (1 comando, ~US$ 0,41). Depois: detectar o BPM, transcrever com Whisper, escrever `timeline_final.json` e re-renderizar (~6 h na mesma máquina).
2. Para subir o nível visual: máquina com GPU (Blender 4.2+ com EEVEE Next ou Cycles + OptiX/OIDN). Encomendar a um artista 3D os 4 personagens finais com rig de deformação e controles faciais, usando as model sheets daqui como referência de design.
3. Manter este pipeline (timeline → coreografia → câmeras → render em lotes → montagem) como esqueleto. Ele aceita assets melhores sem mudar a lógica.
