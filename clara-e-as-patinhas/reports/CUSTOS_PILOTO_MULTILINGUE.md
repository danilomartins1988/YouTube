# Custos — piloto "Pata Pata Patatá" (PT/EN/ES), 2026-11-27

Preços de lista: Eleven Music ~US$ 0,15/min (~900 créditos/min); Whisper US$ 0,006/min. **O débito real é em créditos do plano do proprietário e não pode ser lido pela API** (chave sem `user_read`). Não está claro se o inpainting cobra a música inteira ou só o trecho regerado, então há faixa mínima–máxima.

## Gasto desta etapa
| Item (§20 do Aditivo 03) | Chamadas | Mín. US$ | Máx. US$ |
|---|---|---|---|
| Composição / refrão PT (5 propostas de 23 s: A, B descartadas pela voz; C, D, E finalistas) | 5 | 0,28 | 0,28 |
| Música PT completa (1 geração 145 s + 2 inpaintings do verso do Toby) | 3 | 0,40 | 1,08 |
| Adaptação de letra EN/ES | (assistente) | 0 | 0 |
| Vozes EN (refrão 23 s + completa 145 s) | 2 | 0,42 | 0,42 |
| Vozes ES (refrão 23 s + completa 145 s + 3 inpaintings: Ayra/Toby/Clara, depois Toby 2×) | 5 | 0,56 | 1,50 |
| Instrumental (Demucs na CPU local) | — | 0 | 0 |
| Verificação (Whisper, ~12 min de áudio) | ~30 | 0,07 | 0,07 |
| Lip-sync / animação / render / miniaturas | não iniciados | 0 | 0 |
| RunPod (GPU) | 0 (uso bloqueado pela checagem de permissão) | 0 | 0 |
| **Total desta etapa** | | **≈ 1,73** | **≈ 3,35** |
Créditos estimados: ~7 × 345 + 8 × 2.168 ≈ **19.760 créditos** no máximo (se todo inpainting cobrar a música inteira).

**Orçamento do proprietário: US$ 10.** Usado: ~US$ 1,7–3,4. Restante: ~US$ 6,6–8,3. A parte de música passou um pouco da reserva de ~US$ 3 no cenário máximo, por causa de 5 regravações de trechos (palavras erradas/murmuradas que o Whisper detectou), mas o total segue dentro dos US$ 10.

## Custo marginal de mais um idioma (estimativa)
| Item | US$ |
|---|---|
| Refrão (23 s) + música completa (145 s) | 0,42 |
| 0 a 2 inpaintings de correção | 0,00–0,72 |
| Whisper | 0,02 |
| Adaptação de letra, metadados, texto da miniatura | 0 (assistente) |
| Animação | 0 (animação universal, Aditivo 03) |
| **Total por idioma extra** | **≈ 0,45–1,15** |

## Custo por episódio futuro (3 idiomas)
| Item | US$ |
|---|---|
| Música PT (composição + correções) | 0,70–1,40 |
| EN + ES | 0,90–2,30 |
| Render em GPU (se o proprietário autorizar RunPod; ~2 a 6 h de RTX 4090 a US$ 0,34/h) | 0,70–2,00 |
| Verificação, miniaturas, metadados | ~0,10 |
| **Total** | **≈ 2,40–5,80** |
A meta aspiracional de < US$ 3 por episódio fica viável com 1 idioma, ou com 3 idiomas quando as músicas saírem limpas de primeira. Investimento inicial à parte (personagens premium, infraestrutura): ver `reports/PERSONAGENS_ROTA.md`.
