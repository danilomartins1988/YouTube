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
| ir_mg6811.jpg | App da Receita Federal num celular | Foto: Bruno Peres/Agência Brasil | https://imagens.ebc.com.br/Cd0Lt2OOjMnw-SPgMmH75to6CfM=/1600x800/https://agenciabrasil.ebc.com.br/sites/default/files/thumbnails/image/2026/03/24/_mg_6811.jpg?itok=VyatooZv | https://agenciabrasil.ebc.com.br/economia/noticia/2026-10/receita-paga-nesta-sexta-feira-lote-da-malha-fina-do-imposto-de-renda |
| ir_mg6798.jpg | Pessoa usando o site e o app da Receita | Foto: Bruno Peres/Agência Brasil | https://imagens.ebc.com.br/1wTN4qRlB7JbG_ns2lmPUyfGpm8=/1600x800/https://agenciabrasil.ebc.com.br/sites/default/files/thumbnails/image/2026/03/24/_mg_6798.jpg?itok=MmuA2t2H | https://agenciabrasil.ebc.com.br/economia/noticia/2026-10/receita-envia-cartas-498-mil-que-estao-na-malha-fina-ate-o-dia-20 |
| notas_d6a9016.jpg | Maquininha de cartão num balcão | Foto: Fernando Frazão/Agência Brasil | https://imagens.ebc.com.br/Ca9X2xV2_Vws-2ASRWzhLXmLvQE=/1600x800/https://agenciabrasil.ebc.com.br/sites/default/files/thumbnails/image/2025/11/12/_d6a9016.jpg?itok=Pgmo3HEP | https://agenciabrasil.ebc.com.br/economia/noticia/2026-10/reforma-tributaria-86-das-notas-fiscais-destacam-cbs |
| moedas_jfcrz.jpg | Cédulas de R$ 200 e R$ 100 em leque | Foto: José Cruz/Agência Brasil (**inferred**: the file code `jfcrz` is José Cruz's; the article lists him among its photographers but does not tie him to this image — confirm before publishing, or drop the 4 shots) | https://imagens.ebc.com.br/edXhlA_iXSD5sD95m2wU72O5eS8=/1600x800/https://agenciabrasil.ebc.com.br/sites/default/files/thumbnails/image/real_moedadinheiro_jfcrz_abr_1701220048_1.jpg?itok=H30i3fvq | https://agenciabrasil.ebc.com.br/economia/noticia/2026-10/arrecadacao-federal-cresce-562-em-setembro-e-soma-r-2394-bilhoes |

## News card
Headline quoted as a citation (recreated, not a screenshot): IstoÉ Dinheiro, 11/11/2026 —
"CBS: governo propõe ampliar em 30 dias prazo para acerto do imposto". On-screen note: "Manchete reproduzida como citação".

## Audio
- Narration v2 (`output/short_pt_cbs_prazo_v2.mp4`): owner's own cloned voice (ElevenLabs `rjdBsuq3BG78Nr8NKTlM`,
  eleven_multilingual_v2, test-D settings: stability 0.3 / similarity 0.8 / style 0.45 / speaker boost / speed 0.96),
  ONE `/with-timestamps` request for the whole script with `<break/>` pauses, 992 characters. No EQ/echo/tempo.
  Cached in `output/short-pt-cbs-prazo/news_v3/` (not committed).
- Earlier style test: settings A, 888 characters.
- Music bed and whoosh SFX: synthesised locally with FFmpeg (aevalsrc pad, filtered pink noise) — no third-party audio.
- Mix: voice + ducked bed (sidechaincompress) + soft whoosh on each of the 24 cuts, measured gain + peak limiter;
  v2 measured −14.4 LUFS integrated, −1.1 dBFS peak.

## Unavailable sources (2026-11-12)
Wikimedia Commons (429), Openverse/Pixabay/Pexels (403), Unsplash (bot check) — not used.
