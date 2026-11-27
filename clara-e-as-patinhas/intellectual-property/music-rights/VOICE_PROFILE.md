# Perfil de voz da marca (travado) — v1, 2026-11-27

> Pedido do proprietário: **"Precisamos manter a voz e os personagens ao longo dos episódios."**

## Política vigente (decisão do proprietário, 2026-11-27)
- A voz é gerada **somente com o ElevenLabs Eleven Music**. **Sem** cantora humana por enquanto, **sem** RVC/conversão de voz, **sem** treinar modelos em saídas do ElevenLabs, **sem** clonagem de vozes reais.
- Máxima fidelidade à cantora de **"Cadê? Achou!"** (referência principal, aprovada pelo proprietário: "essa última que você fez está ótima") e de **"A Dança das Patinhas"** (ep. 001).
- Como o Eleven Music **não tem um "ID de voz" fixo**, a consistência depende de: (1) descritores travados abaixo, copiados palavra por palavra; (2) tom/tessitura parecidos; (3) **verificação automática** em toda tomada e seção (`scripts/voice_match.py`); (4) **inpainting** das seções que desviarem, mantendo as partes boas; (5) escuta final do proprietário.
- **Opção futura (adiada pelo proprietário):** contratar uma cantora e, com consentimento por contrato, criar um modelo de voz próprio da marca. Daria uma voz realmente fixa em todos os idiomas. Não fazer nada disso sem nova autorização.

## Referências aprovadas
| Ref | Música | song_id | Trecho de referência | Tom | BPM | Status |
|---|---|---|---|---|---|---|
| **principal** | Cadê? Achou! (ep. 002, `music/masters/cade_achou_final.*`) | `qF8M4uoLJDxZImEDIrIZ` | refrão 4,0–24,0 s | Dó maior (medido) | ~100 | aprovada pelo proprietário 2026-11-27 |
| secundária | A Dança das Patinhas (ep. 001, `music/masters/danca_das_patinhas_final.*`) | `ao9quB5WWogkhSuGxTuH` (+ inpainting da intro) | refrão 25,0–41,7 s; verso 45,9–62,6 s | Ré maior | 115 | piloto aprovado |

Características medidas (stem de voz isolado com Demucs; `voice_reference/*.json`):
- **Altura mediana:** ~295–345 Hz (Ré4–Fá4), faixa típica p10–p90 ~260–400 Hz; no refrão mais agudo da Dança chega a ~390 Hz.
- **Brilho (centroide espectral 300–5000 Hz):** ~1.700–2.000 Hz.
- **Melodias:** poucas notas (4 a 6), saltos pequenos, tessitura de 5 a 8 semitons na maior parte.
- **Produção de "Cadê? Achou!":** xilofone, ukulele, percussão suave, latidinhos; mix limpo, voz à frente, levemente mais grave nos médios (EQ do master: −1,5 dB em 400 Hz, +1 dB em 3,5 kHz; `scripts/ep2/master.sh`), −14 LUFS, pico ≤ −1,5 dBTP.

## Descritores travados (copiar exatamente em todo chunk cantado)
**Voz (pt-BR):**
`the same warm young adult female lead singer throughout the whole song, identical voice, timbre and vocal register in every section, sweet and clear, natural Brazilian Portuguese`

Em seções regeradas por inpainting, acrescentar:
`warm young adult female lead singer, same voice, timbre and register as the rest of the song` · `same tempo and key as the surrounding song`

**Voz (en-US / es-LATAM, mesma "família" de cantora):** a mesma frase, trocando só o final por `natural American English` ou `natural neutral Latin American Spanish`.

**Estilos negativos travados:**
`male lead vocal`, `different singer`, `voice change between sections`, `child lead voice`, `high-pitched chipmunk vocal`, `pitched-up vocal`, `falsetto`, `shrill`, `autotune`, `aggressive vocals`, `rap`, `reverb wash`, `muddy mix`, sotaques errados (`European Portuguese accent`, `Spanish accent` etc.).

**Hábitos de tom e andamento:** tons maiores claros (Dó ou Ré maior), 90–115 BPM, melodia na região Dó4–Sol4. Evitar tons que empurrem a voz acima de Lá4 por muito tempo (é aí que o modelo tende a trocar de "cantora").

## Verificação obrigatória (`scripts/voice_match.py`)
```
python3 scripts/voice_match.py check <música.wav> --win 10 --json <saída.json>
```
- Isola a voz (Demucs) e mede, por janela de 10 s: altura mediana, brilho e "impressão digital" de timbre (MFCC).
- **FAIL (duro):** altura > ±5 semitons da referência (salto de oitava, voz de criança/esquilo, voz masculina); brilho fora de 0,75–1,25× a referência; MFCC > 1,6× a distância entre as duas referências aprovadas.
- **WARN:** seção com brilho > 8% diferente do resto da própria música → ouvir com atenção.
- **Calibração honesta (testada em 2026-11-27):**
  - Pega desvios grosseiros: oitava, voz de criança, voz masculina, vazamento de instrumento em trechos curtos (o final da Dança, com latidos e glockenspiel, aparece como FAIL e é falso positivo).
  - **Não** separa bem a diferença sutil de timbre que o proprietário ouviu na intro original da Dança (v1: altura +1,6 st, brilho +9%, MFCC um pouco mais distante, mas dentro dos limites). Ou seja, ela **ajuda, mas não substitui o ouvido do proprietário**.
  - Arranjos com sanfona (xote) dão leitura geral ~15–20% mais "escura" que as referências (vazamento de sanfona no stem de voz). Por isso, na prática, vale mais a **consistência dentro da própria música** (WARN) do que o valor absoluto.
- Referências: `intellectual-property/music-rights/voice_reference/` (só os números; o áudio fica em `music/masters/`, fora do git).

## Resultado no piloto "Pata Pata Patatá" (pt-BR, `music/analysis/pata/voice_pt_v3.json`)
13 de 14 janelas PASS, 0 WARN; 1 janela (40–50 s, verso da Pandora com xilofone) marginal (brilho 0,77× a referência; dentro do padrão da própria música). Altura mediana 295 Hz (igual a "Cadê? Achou!"). **Ponto de escuta para o proprietário: verso da Pandora.**
