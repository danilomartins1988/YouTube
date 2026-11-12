# Assets — Short pt-BR "CBS: +30 dias para o acerto" (news-explainer edit)

Licence basis for Agência Brasil photos: EBC terms of use (https://www.ebc.com.br/termos-de-uso-e-condicoes-gerais-do-portal-da-ebc) —
"Reprodução autorizada mediante indicação da fonte." Credit is burned into every shot that uses the photo.
Only the 1600x800 versions published on the article pages were used. Files live in `output/assets_pt_cbs/raw/` and
`remotion/public/shorts_pt/cbs/` (both git-ignored); they are not committed.

| File | Content | Credit (on screen) | Source URL | Article |
|---|---|---|---|---|
| congresso_arcos_raf01889.jpg | Congresso Nacional visto pelos arcos do Itamaraty | Foto: Rafa Neddermeyer/Agência Brasil | https://imagens.ebc.com.br/k8sesXIxUz9iDwBr5RiKkfnHptg=/1600x800/https://agenciabrasil.ebc.com.br/sites/default/files/thumbnails/image/2024/03/27/raf01889.jpg?itok=PngGtDFy | https://agenciabrasil.ebc.com.br/economia/noticia/2026-11/pacote-fiscal-preve-120-dias-para-congresso-discutir-supersalarios |
| cedulas_raf1032.jpg | Calculadora no celular, moedas e notas | Foto: Rafa Neddermeyer/Agência Brasil | https://imagens.ebc.com.br/EiUeP5A3dgpqWkxfNEW0GqfdylA=/1600x800/https://agenciabrasil.ebc.com.br/sites/default/files/thumbnails/image/2026/07/10/_raf1032_1.jpg?itok=gO6u3PZx | https://agenciabrasil.ebc.com.br/economia/noticia/2026-11/inpc-inflacao-que-corrige-salarios-acumula-449-em-12-meses |
| receita_mcam20022020.jpg | Fachada da Receita Federal (downloaded; dropped from the test — crop too blurry) | Foto: Marcelo Camargo/Agência Brasil | https://imagens.ebc.com.br/CHv5QgVOukO3vAx5P2uH5X65MC8=/1600x800/https://agenciabrasil.ebc.com.br/sites/default/files/thumbnails/image/mcam20022020.jpg?itok=X8zaudZo | https://agenciabrasil.ebc.com.br/economia/noticia/2026-10/restituicoes-do-ir-batem-recorde-e-chegam-r-41-bilhoes-em-2026 |

## News card
Headline quoted as a citation (recreated, not a screenshot): IstoÉ Dinheiro, 11/11/2026 —
"CBS: governo propõe ampliar em 30 dias prazo para acerto do imposto". On-screen note: "Manchete reproduzida como citação".

## Audio
- Narration: owner's own cloned voice (ElevenLabs `rjdBsuq3BG78Nr8NKTlM`, eleven_multilingual_v2, stability 0.35 /
  similarity 0.8 / style 0.35 / speaker boost), one request for the whole script, 888 characters. No EQ/echo/tempo.
- Music bed and whoosh SFX: synthesised locally with FFmpeg (aevalsrc pad, filtered pink noise) — no third-party audio.
- Mix: voice + ducked bed (sidechaincompress) + SFX, loudnorm to −14 LUFS (style test measured −14.6 LUFS integrated).

## Unavailable sources (2026-11-12)
Wikimedia Commons (429), Openverse/Pixabay/Pexels (403), Unsplash (bot check) — not used.
