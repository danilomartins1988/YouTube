# QC — piloto "Pata Pata Patatá" (vídeo universal), 2026-11-27

## Entregas
| Item | Arquivo | Situação |
|---|---|---|
| **Vídeo principal (faixa original pt-BR)**, 1920×1080, 30 fps | `output/pata_pata_patata_pt_1080p.mp4` (197 MB, H.264 CRF 16, AAC 256k) | pronto |
| Versões leves 1280×720 (PT, EN, ES) | scratchpad `pilot/pata_pata_patata_{pt,en,es}_light.mp4` (~11,7 MB cada) | prontas |
| Exportações completas EN/ES 1080p (contingência) | renderizadas no pod e **não baixadas** (falta de disco). Recriar em segundos, sem re-render: `ffmpeg -i output/pata_pata_patata_pt_1080p.mp4 -i <audio_en.wav> -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k pata_pata_patata_en_1080p.mp4` | sob demanda |
| Faixas de áudio para o YouTube Studio (EN, ES; e PT) | scratchpad `pilot/youtube_studio_audio/pata_pata_patata_audio_{pt,en,es}.wav` — WAV 48 kHz/24 bits, **145,567 s = duração exata do vídeo** (música 144,56 s + 1 s de silêncio final) | prontas |
| Instrumental | `music/masters/pata_pata_patata_instrumental.{wav,mp3}` | pronto |
| Miniaturas | `thumbnails/pilot/thumb_pt-BR.jpg` (principal), `thumb_en-US.jpg`, `thumb_es-LATAM.jpg`, `thumb_universal_notext.jpg` | prontas (1280×720) |
| Metadados | `metadata/pilot/pt-BR.md` (principal), `en-US.md`, `es-LATAM.md` | rascunhos |
| Logo global, foto de perfil, banner, wordmarks PT/ES | `assets/branding/global/` | rascunhos |
| Teste de animação dos 5 (§41, 12 s) | scratchpad `pilot/teste_5_personagens.mp4` | feito antes do render completo |

## Verificações técnicas (medidas)
- 4.367 quadros renderizados (0 vazios); 145,567 s; vídeo 1920×1080 a 30/1 fps; decodificação sem erros (PT, EN, ES, leve).
- **Congelamento** (freezedetect, −60 dB, > 1 s): nenhum. **Tela preta** (> 0,2 s): nenhuma.
- **Loudness** das três versões: −14,0 LUFS integrado (igual entre idiomas).
- **Sincronia:** a animação é guiada pela grade de batidas do mapa de tempos comum (94,85 BPM, compasso 2,526 s). As vozes EN/ES foram medidas a ≤ 12 ms da grade PT (máx. 35 ms em uma janela). Os cortes de câmera caem nas fronteiras de seção.
- **Desfoque de movimento nos cortes:** o primeiro teste mostrou rastro de câmera no quadro do corte; corrigido (escolha de plano pelo quadro inteiro + re-render sem motion blur dos 22 quadros de corte).
- **Lip-sync universal:** a boca da Clara segue a voz PT (principal) com abertura mínima onde EN/ES cantam (0,6 × máx. EN/ES) e um "tremor" silábico no ritmo; sem formas fonéticas de um idioma. Cachorrinhos abrem a boca nos "au/woof/guau", Milo nos "miau/meow".
- **Personagens no modelo:** Clara, Ayra, Pandora, Toby (macho, topete, bandana verde) e Milo (laranja rajado, olhos verdes, coleira roxa, bigodes) aparecem em todo o vídeo; pés no chão nos quadros conferidos; sem objetos soltos (a coleira do Milo, que flutuava sobre a cabeça no primeiro layout, foi corrigida).

## Nota honesta (matriz do Aditivo 01, §39)
| Critério | Peso | Nota (0–10) | Justificativa |
|---|---:|---:|---|
| Originalidade e qualidade da melodia | 20% | 7 | Melodia de 4 notas, gancho claro, arranjo de xote agradável; originalidade melódica não verificável por base de dados; gancho com risco de nome aceito pelo proprietário |
| Memorização do refrão | 15% | 9 | refrão repetido 6×, idêntico em cada volta |
| Qualidade do canto | 15% | 7 | voz agradável e consistente (mesma família de "Cadê? Achou!"); dicção às vezes pouco nítida (ES "aplauda", EN "paw") |
| Adequação à faixa etária | 10% | 9 | andamento calmo, frases curtas, onomatopeias com ação |
| Design e carisma dos personagens | 10% | 6 | procedurais, fofos mas simples; cães e gato pequenos no quadro largo |
| Consistência visual | 10% | 8 | mesmo modelo, cores e acessórios do início ao fim |
| Qualidade das animações | 10% | 5 | movimentos repetitivos por grade, rigs rígidos, sem animação facial rica; boca abre/fecha estilizada |
| Sincronização audiovisual | 5% | 8 | ações na batida; lip-sync estilizado aceitável nos 3 idiomas |
| Eficiência tecnológica e comercial | 5% | 9 | 1 render serve 3 idiomas; custo de render ~US$ 0,67 |
| **Total ponderado** | | **≈ 7,4 / 10 (74/100)** | meta aspiracional 95/100 **não atingida**; o principal limite é visual (personagens e animação) |

## Limitações conhecidas
- Personagens pequenos nos planos largos dos refrões; a Clara domina o quadro.
- A coreografia segue a grade de batidas, não as palavras exatas de cada idioma: em alguns versos o gesto pode adiantar/atrasar ~0,1–0,3 s em relação à sílaba cantada.
- Miniaturas mostram os 5 personagens (o aditivo prefere 1–2 em destaque); é um rascunho.
- Exportações completas EN/ES 1080p não foram baixadas (disco); recriáveis com o comando acima.

## Custo do render
RunPod RTX 4090 (Secure Cloud, US$ 0,89/h; Community sem disponibilidade), host com 128 núcleos: **0,75 h ≈ US$ 0,67** (teste dos 5 personagens + 4.367 quadros com 10 instâncias Blender EEVEE em paralelo + 22 quadros de corte + encodes). Pod encerrado. Saldo RunPod: ~US$ 8,85.
