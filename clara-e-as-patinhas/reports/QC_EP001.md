# QC — Episódio 001 "A Dança das Patinhas" (piloto, versão com a música cantada final)

Avaliado em 2026-11-27 a partir dos arquivos reais:
- `output/danca_das_patinhas_1080p.mp4`
- `output/danca_das_patinhas_light.mp4`
- `output/teste_3d_light.mp4`
- `music/masters/danca_das_patinhas_final.wav`
- `music/compositions/timeline_final.json`

## Música: master e letra
| Item | Resultado |
|---|---|
| Fonte | Eleven Music v1 (song_id `ao9quB5WWogkhSuGxTuH`) com a intro (8,35–25,04 s) refeita por inpainting. Aprovada pelo proprietário |
| Master final | `music/masters/danca_das_patinhas_final.wav` (48 kHz, 24 bits, estéreo, 164,76 s) + `.mp3` (256 kbps). **-13,98 LUFS integrado, -1,48 dBTP** (loudnorm em 2 passagens; o original tinha -12,9 LUFS e -0,12 dBTP) |
| Instrumental separado | **Não existe.** Stems seriam um recurso pago extra, não usado |
| BPM | **115,0** (rastreio de batidas por seção, todas as seções entre 114,3 e 115,1; mediana global 115,01). Bate com o plano |
| Whisper (whisper-1, pt, palavras, **sem** prompt) | **A letra é cantada e inteligível do começo ao fim.** "Aira, Pandora e Tifa também" foi transcrito corretamente ("Aira" = pronúncia de Ayra). "Clara e as Patinhas" sai como "Clare as patinhas" (elisão normal no canto). Única diferença em relação à letra escrita: **um "Au, au, au, vamos brincar" a mais na pausa de dança 2 (~1:15)**, registrado em `music/lyrics/a-danca-das-patinhas.md` como "versão cantada final" |
| Alinhamento letra ↔ áudio | 207 de 208 palavras casadas com os carimbos do Whisper. "Au, au, au" redistribuído em colcheias a partir do primeiro "au" |

## Vídeo: sincronia (checagem por frame nos tempos reais das palavras)
| Momento (palavra cantada) | Tempo | O que se vê | OK |
|---|---|---|---|
| "**Ayra**" (intro) | 16,6 s | Ayra no ar (pulinho do nome) | ✅ |
| "Pandora" / "Tifa" | 17,5 / 18,8 s | Pulinho de cada uma | ✅ (Pandora começando a pular) |
| "pra **frente**" | 26,1 s | Clara com o pé à frente, cachorrinhas levantando a pata | ✅ |
| "pra **trás**" | 28,2 s | Passinho para trás | ✅ |
| "**Au**, au, au" | 33,3 s | Cachorrinhas pulando, Clara batendo palmas | ✅ |
| "bate **palma**" | 37,9 s | Mãos da Clara juntas | ✅ |
| "**um**, **dois**, **três**" (Tifa) | 106,7 / 107,2 / 108,2 s | Tifa no ar nas três contagens | ✅ |
| Boca da Clara | | Fechada nas partes instrumentais (vinheta, pausas, cauda: média 0,0). Abre e fecha com a voz nos trechos cantados (média 0,44–0,47) | ✅ (aproximado, sem visemas) |
| Câmeras | | Trocam nas mudanças de seção/verso do timeline real | ✅ |
| Palmas | | Nos tempos 2 e 4 da grade de batidas real (refrões, pausas, final) | ✅ |

## Técnica
| Item | Resultado |
|---|---|
| Duração | Música 164,76 s; vídeo 165,75 s (cauda de 1 s com o logo final) |
| Resolução | 1920×1080 (render a 1280×720, ampliado com Lanczos), 24 fps |
| Integridade | `ffmpeg -v error` com **0 erros** nos três MP4 |
| Áudio no MP4 | -14,08 LUFS; pico real -0,40 dBTP depois da codificação AAC. **Sem clipping** |
| Tamanhos | 1080p: 325 MB (CRF 18); light: **52,5 MB**; teste: 9,7 MB |
| Render | 3.978 frames, EEVEE 720p, 8 amostras. ~42 lotes de 9,5 min, **≈6 h de CPU** |
| Consistência (frames a cada 5 s em todas as cenas) | Merle fixo da Ayra, Pandora branca, Tifa castanho/cinza-aço, Clara com cabelo e macacão amarelo, iguais em todas as cenas |
| Pés no chão / deformações | Pés no chão. O rig é rígido, então não há deformação de malha (articulações "de boneco") |

## Rubrica ponderada (honesta)
> A cópia do brief que recebi não trazia os pesos da rubrica do proprietário. Os pesos abaixo seguem as prioridades do brief.

| Critério | Peso | Nota | Comentário |
|---|---|---|---|
| Música e voz cantada | 25% | **8** | Voz feminina em pt-BR, inteligível, refrão grudento, estrutura e tempo fiéis ao plano. Gerada por IA, sem instrumental separado |
| Qualidade visual dos personagens | 20% | **5** | Fofos e legíveis, mas com formas primitivas, rig rígido e pelo aproximado. Não é "premium cinematográfico" |
| Animação, coreografia e sincronia | 15% | **6,5** | Coreografia nas palavras reais, palmas no tempo real, contagem da Tifa exata, boca pela voz. Movimento procedural sem atuação nem visemas |
| Consistência | 10% | **8** | |
| Cenário e luz | 10% | **6,5** | Todos os elementos do brief. Sem GI nem reflexos |
| Integridade técnica | 10% | **9** | |
| Entregáveis e marca | 10% | **8** | |
| **Total** | 100% | **6,9 / 10** | Era 5,7 com o instrumental-guia |

## Pendências e limites
- Lip-sync por abertura de boca (envoltória × janelas das palavras), sem visemas por fonema.
- Sem instrumental/stems (só com recurso pago extra).
- Qualidade 3D de protótipo; veja `reports/TESTE_3D.md` para o caminho até o "premium".
