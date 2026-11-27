# Arquitetura multilíngue (Aditivos 01 §34, 02 e 03)

**Vigente: Aditivo 03.** Um canal global "Clara & Paws – Kids Songs"; um vídeo público por música com **faixas de áudio multilíngues** do YouTube. **Faixa original: pt-BR** (decisão do proprietário em 2026-11-27, substitui a preferência do Aditivo 03 por inglês; configurável); en-US e es-LATAM entram como faixas adicionais. Sem dublagem automática do YouTube: cada idioma é cantado, adaptado e mixado por nós. Vídeos completos por idioma continuam exportáveis como contingência.

## Regras
1. **Uma composição, um instrumental, uma animação.** Mesma melodia, harmonia, BPM, compasso, **duração**, estrutura de refrões, entradas de personagem, pausas, coreografia e instrumentação em todos os idiomas.
2. **Mapa de tempos compartilhado** por música (`music/compositions/pilot/timing_map.json`): seções, entradas vocais, ações de coreografia, sons de animais, final. As faixas de todos os idiomas têm exatamente a duração do vídeo.
3. **Letras adaptadas, não traduzidas:** palavras equivalentes nas mesmas posições musicais (Pula, pula, pula / Jump, jump, jump / Salta, salta, salta); onomatopeias localizadas.
4. **Nomes nunca traduzidos:** Clara, Ayra, Pandora, Toby, Milo.
5. **Animação universal (Aditivo 03):** uma só renderização; lip-sync musical estilizado guiado pela voz PT (principal) e aberto o suficiente para EN/ES (abre/fecha + vogais largas, sem formas fonéticas específicas), expressividade facial preservada, enquadramento para esconder diferenças. Substitui o lip-sync por idioma do Aditivo 02.
6. **Nada de texto "queimado" na imagem:** textos como camadas substituíveis; miniaturas por idioma + 1 miniatura universal sem texto.
7. Separar por idioma: vozes, mixes, textos, metadados, miniaturas. Compartilhado: instrumental, efeitos, animação corporal e facial, logo global.

## Como o áudio multilíngue é produzido (testado em 2026-11-27)
1. Gerar a versão de referência completa (PT, porque é a voz travada) com os chunks do plano de composição.
2. Gerar EN e ES **com as mesmas durações de chunk** (refrão gerado uma vez e reutilizado por referência de inpainting; intro instrumental da PT reaproveitada por referência).
3. Demucs separa voz/instrumental de todas. **Medido:** a grade rítmica de EN e ES ficou a ≤ 12 ms da PT (mediana 0–12 ms, máx. 35 ms) e a harmonia bate (cosseno de croma 0,97–0,98). Por isso **as vozes EN e ES foram mixadas sobre o instrumental da PT**, o que dá instrumental idêntico nas três faixas.
4. Master igual (−14 LUFS, −1,5 dBTP, 48 kHz/24 bits) e conferência da duração (144,56 s nas três).
Limites: separação Demucs pode deixar resíduo; uma janela da versão EN (verso do Milo, 90–100 s) teve harmonia menos parecida (0,85) → ponto de escuta. As mixagens "originais" EN/ES (com o próprio instrumental gerado) ficam como alternativa.

## Configuração de idiomas
`clara-kids-studios/config/languages.json` — novos idiomas (fr, de, it, ja, ko, hi, ar, id, tr, zh) entram adicionando uma entrada (só infraestrutura por enquanto).
