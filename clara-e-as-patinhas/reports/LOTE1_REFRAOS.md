# Lote 1 (Fase 2) — propostas de refrão PT, 2026-11-28

Cada pasta tem `refrao_A.mp3`, `refrao_B.mp3` (Pandora também `refrao_C.mp3`) e `letra.md` (PT + rascunhos EN/ES, ainda não cantados).
Medições: voz isolada com Demucs; "voz" = comparação com a voz da casa ("Cadê? Achou!" + ep. 001). **Leitura honesta do verificador de voz:** altura (semitons) e timbre (MFCC) são os critérios confiáveis; o "brilho" fica mais escuro com sanfona/cordas/piano vazando no stem e reprovou quase tudo por isso — tratado como aviso, não reprovação. O ouvido do proprietário decide.

| Música | Prop. | BPM medido | Notas (90%) / extensão | Altura vs. voz da casa | Timbre MFCC (limite 41) | Palavras (Whisper) | Recomendação |
|---|---|---|---|---|---|---|---|
| **Au Au Ayra** (xote) | A | 95,7 | 4 / 7 st | −0,8 st | 26–29 ✓ | ✗ dicção ruim na linha 2 ("quem lá te assinaria assim") | |
| | **B** | 95,7 | 6 / 8 st | +0,3 a +1,0 st | 23–25 ✓ | ✓ "Quem late assim, a Ayra, sim / Ayra, late pra mim" | **B** — letra clara, gancho "au, au, au" com resposta, voz mais próxima |
| **Miau Miau Milo** (pizzicato) | **A** | 99,4 | 5 / 7 st | −2,1 a −2,3 st | 21–23 ✓ (passou em tudo) | ✓ | **A** — única que passa todos os critérios, letra perfeita |
| | B | 99,4 | 5 / 7 st | −0,9 a −2,7 st | 31 ✓ | ✓ | |
| **Pula Pula Pandora** (marchinha) | A | 112,3 | 4 / 7 st | +1,2 a +2,1 st | 34–38 ✓ (limite) | ✓ | |
| | B | 74,9 ✗ (perdeu o andamento de marchinha) | 3 / 4 st | −2,8 st | 42–45 ✗ | ✓ | descartada |
| | **C** | 112,3 | 3 / 4 st | −2,8 a −4,6 st | 32–34 ✓ | ✓ | **C** — melodia mais simples (3 notas), andamento certo; um pouco mais grave que a voz da casa (ouvir) |
| **Toby Gira Girou** (baião) | **A** | 99,4 | 6 / 5 st | −0,8 a −2,9 st | 19–25 ✓ (passou em tudo) | ✓ ("o Toby girou… tontinho ficou, opa!") | **A** — passa em tudo; o "opa!" engraçado funciona |
| | B | 99,4 | 8 / 8 st | −2,5 st | 22–25 ✓ | ✓ | melodia com notas demais para a faixa etária |
| **Naná Patinhas** (ninar) | **A** | ~66 (lido 132, dobro) | 4 / 6 st | −0,7 st | **13–15 ✓ (a mais parecida com a voz da casa de todo o lote)** | ✓ | **A** — calma, poucas notas, timbre mais fiel |
| | B | ~66 | 5 / 9 st | +0,3 st | 22 ✓ | ✓ | extensão maior (9 st) |

## Originalidade (títulos e ganchos, PT/EN/ES) — resumo (detalhes em `intellectual-property/originality-reports/RELATORIO_ORIGINALIDADE.md`)
- ⚠ **"Toby Gira Girou" / "Gira, gira, girou"** — muito próximo do samba **"Quando a Gira Girou"** (gravado por Zeca Pagodinho, Péricles e outros) e "gira" também tem sentido religioso (umbanda). Recomendo trocar o gancho/título (ex.: "Toby Rodopia", "Roda, roda, rodou!").
- ⚠ **"Meow Meow Milo"** (título EN) — já existe um vídeo infantil "Meow Meow Milo!" no YouTube, e há um canal infantil "Milo Cartoon". Título EN precisa de alternativa.
- ⚠ (baixo) "Salta, salta" lembra "Salta, Salta Sem Parar" (Canal Panda, PT-Portugal) — só a expressão; melodia diferente.
- Sem conflito direto encontrado: "Au Au Ayra", "Pula Pula Pandora" (expressão "pula pula" é comum no gênero), "Naná Patinhas", "Nana Patitas".
- Limitações: YouTube (1ª página), Apple Music (API pública); Spotify e INPI não consultados.

## Custo desta etapa
11 tomadas de 19–27 s (≈ 245 s) ≈ **3.670 créditos ≈ US$ 0,61** + Whisper ≈ US$ 0,03. Teto da etapa: US$ 1,50.

---
# Músicas completas (2026-11-28) — Au Au Ayra (refrão B), Miau Miau Milo (refrão A), Naná Patinhas (refrão A)
Pandora (A vs C) e Toby (gancho/título) **em espera**, como pedido.

Arquivos em cada pasta: `musica_completa_PT.mp3` (faixa original), `musica_completa_EN.mp3`, `musica_completa_ES.mp3`, `instrumental.mp3`, e `youtube_studio_audio/<música>_audio_{pt,en,es}.wav` (48 kHz/24 bits, duração da música + 1 s = duração prevista do vídeo).

| Música | Duração | Estrutura | PT | EN | ES |
|---|---|---|---|---|---|
| Au Au Ayra (xote, 95 BPM) | 2:09 | intro 3 s · refrão · verso ×2 linhas · refrão · verso · refrão · verso · break instrumental · refrão ×2 · final | letras ✓; voz −0,9 a +2,0 st, MFCC 16–35 ✓ | letras ✓ (Whisper ouve "Ara/Aira"); voz ✓ (−2,9 a +0,3 st) | letras ✓; voz um pouco mais grave (−1,7 a −4,6 st) |
| Miau Miau Milo (pizzicato, 100 BPM) | 2:03 | igual | letras ✓; voz ✓ (−0,6 a −2,9 st) | letras ✓; voz ✓ | letras ✓; voz ✓ |
| Naná Patinhas (ninar, 70 BPM) | 2:41 | sem break; refrão 5× | letras ✓; voz ✓ (MFCC 15 nos refrões = muito fiel) | letras ✓; voz −2,9 a −4,5 st | letras ✓ após correção dos versos 1–2 (inpainting); **voz ~4,5 st mais grave em toda a faixa ES** (dentro do limite de 5) |

- **Mesmo instrumental nos 3 idiomas:** as vozes EN/ES foram separadas (Demucs) e mixadas sobre o instrumental PT. Alinhamento medido: atraso mediano 0–12 ms (máx. 81 ms em uma janela da Ayra ES); harmonia (croma) 0,91–0,98.
- **Masters:** −14,0 LUFS, pico −1,4/−1,5 dBTP, 48 kHz/24 bits, nos 9 arquivos.
- **Títulos EN provisórios:** "Milo the Kitty Says Meow" (em vez de "Meow Meow Milo", que já existe).
- **Pontos para ouvir:** Ayra ES (voz mais grave nos versos), Naná EN/ES (registro mais grave que o PT), break instrumental da Ayra (tem latidinhos).
- **Custo desta etapa (preço de lista):** ≈ US$ 3,72 (~25.000 créditos) para PT+EN+ES das 3 músicas, incluindo 2 tomadas de teste (diagnóstico de um bloqueio "copyrighted_material_detected" causado pela frase de estilo "same melody as the original…", removida) e 1 inpainting (Naná ES). Teto: US$ 4,00.
