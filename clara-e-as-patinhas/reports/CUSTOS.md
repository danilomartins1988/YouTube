# Custos — Clara e as Patinhas

## Resumo por categoria (até agora)

| Categoria | Item | Custo externo |
|---|---|---|
| Software | Blender 4.0.2 (GPL, apt), FluidSynth 2.3.4 (LGPL), ffmpeg, Python | US$ 0 |
| Som | Soundfont FluidR3_GM (MIT) | US$ 0 |
| Computação | CPU do container (sem GPU, sem nuvem paga) | US$ 0 |
| Assets 3D | Tudo procedural, gerado por script | US$ 0 |
| Fontes | DejaVu (licença livre, já instalada) | US$ 0 |
| Música IA | ElevenLabs Eleven Music: veja o log abaixo | veja abaixo |
| Transcrição | OpenAI Whisper (verificação da letra): veja o log abaixo | veja abaixo |

Preços de referência (consultados em 2026-11-27):
- Eleven Music pela API: **US$ 0,15 por minuto** (https://elevenlabs.io/pricing/api), **~900 créditos por minuto** (https://elevenlabs.io/pricing). Gerar o plano de composição (`/v1/music/plan`) não gasta créditos (https://elevenlabs.io/docs/api-reference/music/create-composition-plan).
- Música de ~2:45 (164,9 s): **~2.473 créditos ≈ US$ 0,41**. Com uma nova tentativa: **~4.946 créditos ≈ US$ 0,82**.
- OpenAI Whisper (`whisper-1`): US$ 0,006 por minuto (https://openai.com/api/pricing/). Uma música de 2:45 custa ≈ US$ 0,017.

## Conta ElevenLabs (informada pelo proprietário)
- Plano visível: **€5/mês (Starter)**, pago e com assinatura própria. O proprietário diz ter um plano superior e ~**150.000 créditos** disponíveis. Não dá para verificar pela API porque a chave não tem `user_read`.
- A assinatura é custo fixo do proprietário e não entra como gasto deste projeto. Abaixo ficam só os créditos consumidos.
- Limite do Starter (https://elevenlabs.io/music-terms, Exhibit A): **17 min de geração por mês**.

## Log de gastos

| Data | Serviço | O que | Créditos | US$ |
|---|---|---|---|---|

_Atualização: o proprietário/coordenador fez a geração Eleven Music fora desta sub-sessão. Os valores exatos estão nas linhas que ele registrou acima. Resumo estimado: **≈4 chamadas** (v1, v2 e 2 inpaints: `inpaint_ayra_v1`, `inpaint_intro_v1`) **≈ até US$ 1,64** (≈ 4 × 2,75 min × US$ 0,15/min, pelo preço de lista da API). Não houve chamada de stems._

| Data | Serviço | O que | Créditos | US$ |
|---|---|---|---|---|
| 2026-11-27 | OpenAI Whisper (`whisper-1`) | 2 transcrições do master final de 2:44,8 (sem prompt e com prompt) | n/a | ≈ 2 × 2,75 min × US$ 0,006 ≈ **US$ 0,033** |

## Computação local (sem custo externo)
| Tarefa | Tempo de CPU (4 núcleos, sem GPU) |
|---|---|
| Render do episódio (4.016 frames, EEVEE 720p, 8 amostras) | ≈6 h (≈43 lotes de 9,5 min), mais ≈20 min para refazer o segmento 14 |
| Model sheets + grupo + proporções | ≈14 min |
| Testes, diagnósticos e stills de validação | ≈1 h |
| Montagem e codificação (1080p, light, teste) | ≈12 min |

**Gasto externo estimado: ≈ US$ 1,64 (Eleven Music, teto estimado; os valores exatos estão no log do proprietário) + ≈ US$ 0,03 (Whisper) ≈ US$ 1,67.** A assinatura ElevenLabs é custo fixo do proprietário.

| Re-render com a música real (3.978 frames) | ≈6 h de CPU |
| 2026-11-27 | ElevenLabs Eleven Music (music_v2_5) | 1 geração v1, 165 s | ~2473 créditos (estimado) | ~US$ 0.41 (preço de lista API; débito real no plano do proprietário) |
| 2026-11-27 | ElevenLabs Eleven Music (music_v2_5) | 1 geração v2, 165 s | ~2473 créditos (estimado) | ~US$ 0.41 (preço de lista API; débito real no plano do proprietário) |
| 2026-11-27 | ElevenLabs Eleven Music (music_v2_5) | 1 geração v2 (voz consistente; melodia mudou, descartada) | ~2473 créditos (estimado) | ~US$ 0.41 |
| 2026-11-27 | ElevenLabs Eleven Music (music_v2_5) | inpainting: v1 mantida, só o verso da Ayra regerado (16,7 s gerados + 148 s referenciados) | não informado pela API; estimativa ≤ 2473 créditos | ≤ US$ 0.41 |
| 2026-11-27 | ElevenLabs Eleven Music (music_v2_5) | inpainting: v1 mantida, só a introdução (0:08–0:25) regerada | não informado pela API; estimativa ≤ 2473 créditos | ≤ US$ 0.41 |
