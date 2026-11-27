# Registro de origem e licenças dos assets — Clara e as Patinhas

Atualizado em 2026-11-27. Nada aqui foi baixado de bancos de modelos, imagens ou sons, a não ser o que está listado nesta página.

## Personagens, cenário e animação (originais e procedurais)
| Asset | Origem | Licença / titularidade |
|---|---|---|
| Clara, Ayra, Pandora, Tifa (geometria, materiais, rigs, ações) | Gerados por código próprio: `scripts/blender/cp_chars.py`, `cp_lib.py`, `cp_motion.py`, `build_assets.py` → `assets/characters/<nome>/<nome>.blend` | Criação original do projeto e propriedade do dono do projeto |
| Texturas de pelagem (manchas merle fixas da Ayra, cinza-aço/castanho da Tifa, branco da Pandora) | Geradas por ruído numpy determinístico e gravadas em UV (`bake_pattern`), empacotadas nos .blend | Original |
| Jardim, casa, casinhas, lago, ponte, balanço, brinquedos, flores, borboletas, nuvens | `scripts/blender/cp_env.py` (procedural) | Original |
| Coreografia, câmeras, lip-sync | `scripts/blender/episode.py` | Original |
| Renders, frames e vídeos | Gerados com o Blender 4.0.2 | O Blender é GPL-2.0-or-later. **Os renders (saídas) pertencem ao usuário** e não ficam sujeitos à GPL (https://www.blender.org/about/license/) |

## Música
| Asset | Origem | Licença |
|---|---|---|
| Letra "A Dança das Patinhas" | Texto do proprietário, com ajustes de métrica e gênero feitos nesta sessão (`music/lyrics/a-danca-das-patinhas.md`) | Do proprietário |
| Melodia, harmonia, assinatura de marca e arranjo-guia | Compostos nesta sessão (`scripts/compose.py`). Não copiam nenhuma música existente | Original, do proprietário |
| Instrumental-guia (áudio) | MIDI próprio renderizado com FluidSynth (LGPL-2.1) e o soundfont **FluidR3_GM** | O FluidR3_GM (Frank Wen) é distribuído no Debian/Ubuntu pelo pacote `fluid-soundfont-gm` sob **licença MIT** ("I hereby release Fluid under the MIT license", em `/usr/share/doc/fluid-soundfont-gm/copyright`); o áudio resultante pode ser usado comercialmente |
| Latidinhos do guia | Sintetizados em numpy (`scripts/render_guide.py`), sem amostras gravadas | Original |
| **Música cantada (Eleven Music)** | Gerada pelo proprietário/coordenador: Eleven Music `music_v1`, song_id `ao9quB5WWogkhSuGxTuH`, a partir de `eleven_music_plan.json`. Intro (8,348–25,043 s) refeita por inpainting (`inpaint_intro_v1.json`). Master final normalizado a -14 LUFS: `music/masters/danca_das_patinhas_final.wav`. **Não há instrumental/stems separados** (stems seriam um recurso pago a mais, não usado) | Veja abaixo (plano Starter) |

### ElevenLabs Eleven Music (quando for gerado)
- Termos: https://elevenlabs.io/music-terms (atualizado em 09/10/2026). Preços: https://elevenlabs.io/pricing e https://elevenlabs.io/pricing/api.
- **Plano informado pelo proprietário:** o painel mostra o plano pago de €5/mês (**Starter**). O proprietário diz ter um plano superior e cerca de 150.000 créditos. **A API não confirma isso**: a chave não tem permissão `user_read`.
- Linha do Starter no Exhibit A dos Music Terms:
  - "For Individual Use Only";
  - **Music Streaming Distribution: "Prohibited"**;
  - Media Rights: "All online and offline commercial use permitted, except film, TV, radio, and Studio Games";
  - sem atribuição obrigatória;
  - limite de geração de 17 min/mês.
- A página de preços diz que o Starter já inclui "Music commercial use". Como "Media Rights" inclui "the right to synchronize Output in timed relation to audiovisual content", **usar a música dentro do vídeo** parece coberto pelo plano pago.
- **Publicar a faixa de áudio sozinha** (Spotify, YouTube Music etc.) conta como "Music Streaming Distribution" e exige **Creator ou superior**.
- Os termos não esclarecem se o YouTube conta como "TV". **O proprietário precisa confirmar o plano e, se possível, tirar essa dúvida com a ElevenLabs antes de monetizar.**
- Pelos termos (§3.1 e §4.4), cabe ao usuário revisar a saída e seguir as regras de divulgação de IA de cada plataforma (no YouTube: "conteúdo alterado ou sintético", quando aplicável).

## Fontes
| Fonte | Onde | Licença |
|---|---|---|
| Fredoka (600/700, woff) | `assets/branding/fonts/`, vinda do npm `@fontsource/fredoka` 5.0.13 | SIL Open Font License 1.1 (`assets/branding/fonts/OFL-Fredoka.txt`) |
| DejaVu Sans | Fonte do sistema, usada nos rótulos das model sheets | Licença Bitstream Vera / DejaVu (livre, permite uso comercial) |
| Fonte embutida do Blender (rótulos das casinhas) | Embutida no Blender 4.0 | Livre (distribuída com o Blender) |

## Logos e identidade visual
Os logos, a paleta, o ícone e a thumbnail foram desenhados por código (`scripts/branding.py`, `scripts/thumbnail.py`) com a fonte Fredoka (OFL) e renders próprios. São originais.

## Serviços externos
- Nenhuma publicação nem upload.
- Gasto externo: veja `reports/CUSTOS.md` (US$ 0 até agora; a geração Eleven Music está bloqueada).
- Transcrição com OpenAI Whisper (`whisper-1`): usada só para verificar a letra e marcar o tempo das palavras. Nada foi publicado.

## Episódio 002 "Cadê? Achou!" (2026-11-27)
| Asset | Origem | Licença |
|---|---|---|
| Letra "Cadê? Achou!" | Escrita nesta sessão a partir do rascunho do proprietário (`music/lyrics/cade-achou.md`). Original: só o formato genérico de pergunta e resposta "cadê?/achou!" é comum ao gênero. Nenhum verso, melodia ou tema de outra canção (incluindo "Sopa", da Palavra Cantada, e as canções conhecidas de "cadê/achou") | Do proprietário |
| Música cantada | Eleven Music `music_v2_5`, song_id `qF8M4uoLJDxZImEDIrIZ`, plano `music/compositions/cade_achou_plan.json`, **sem** conditioning/referência de áudio. O prompt não cita artistas nem títulos. Master: `music/masters/cade_achou_final.wav` (-14 LUFS) | Mesmos termos e ressalvas de plano descritos acima |
| Flor gigante, balde, chapéu de palha, patinhas nas casinhas | `scripts/blender/ep2_scene.py` (procedural) | Original |
