# Episódio 001: A Dança das Patinhas — storyboard e timeline

Os tempos seguem o **instrumental-guia** (`music/compositions/estrutura.json`, 115 BPM, 1 compasso = 2,087 s).
Quando a música cantada (Eleven Music) existir, `music/compositions/timeline_final.json` substitui o guia e `scripts/blender/episode.py` relê os tempos automaticamente. Aí é só refazer o render.

Tudo o que se move é calculado por frame a partir do timeline:
- **mudanças de câmera** nas trocas de seção ou de verso;
- **coreografia** nas deixas da letra;
- **palmas** da Clara nos tempos 2 e 4, junto com as palmas do áudio;
- **boca** da Clara pela envoltória das notas da melodia vocal;
- **latidos e boca das cachorrinhas** nas sílabas "AU".

| # | Cena | Tempo | Seção / letra | Ação | Câmera |
|---|---|---|---|---|---|
| 1 | **O convite** | 0:00–0:04 | Assinatura (vinheta + 2 latidos) | Plano geral do jardim, da casa, do lago e das casinhas. Logo sobreposto | Plano bem aberto com *push-in* lento |
| | | 0:04–0:08 | Gancho no xilofone | Clara sai pelo caminho de pedras e vai até o gramado | Dolly em direção à varanda |
| | | 0:08–0:12 | "Clara chamou as amiguinhas" | Clara canta e acena para as casinhas | Plano médio da Clara |
| | | 0:12–0:17 | "Vieram correndo três cachorrinhas!" | Ayra, Pandora e Tifa correm das casinhas até o gramado (ciclo de corrida) | Plano aberto acompanhando |
| | | 0:17–0:21 | "Ayra, Pandora e Tifa também" | Cada cachorrinha dá um pulinho quando o nome é cantado | Plano baixo das três |
| | | 0:21–0:25 | "Vamos dançar, vem, vem, vem!" | Clara acena com os dois braços e todas balançam | Plano de grupo |
| 2 | **Refrão 1** | 0:25–0:42 | Refrão completo | "pra frente": Clara pé à frente, cachorrinhas levantam a pata · "pra trás": passinho atrás · "voltinha": giro · "dança muito mais": braços para cima · "Au, au, au": pulinhos nos AU e palmas · "Bate palma, bate o pé": palmas nos tempos 2/4 e pisada · "Dança junto": balanço livre | Frontal baixa (compassos 1–4) e arco lateral (5–8) |
| | | 0:42–0:46 | Pausa de dança | Cachorrinhas pulam, Clara bate palmas | Travelling baixo |
| 3 | **Dança da Ayra** | 0:46–1:03 | Verso da Ayra | "corre pelo jardim": volta em círculo ao redor da Clara · "olha pra mim": vem até a câmera, abana o rabo, cabeça curiosa · "pula pra cá / pra lá": saltos laterais · fim: giro e volta ao lugar | Câmera acompanha a Ayra |
| | | 1:03–1:19 | Refrão curto + pausa | Mesma coreografia do refrão | Arco 3/4 e plano baixo |
| 4 | **Pandora entre flores e borboletas** | 1:19–1:36 | Verso da Pandora | Prado de flores com 3 borboletas · "branquinha, fofinha": close, expressão carinhosa · "voltinha e pede mais": giro e senta pedindo · "mexe as patinhas, começa a girar": patinhas alternadas e giro · "com a Clara ela vai dançar": Clara e Pandora giram juntas | Close baixo → travelling lateral pelo prado → plano a duas |
| 5 | **A dança engraçada da Tifa** | 1:36–1:53 | Verso da Tifa | "cheia de energia": corridinha em círculos · "sorrir de alegria": pulo com giro, as outras dão risada · "um, dois, três": **3 pulinhos exatamente nas sílabas** · "mais uma vez": giro grande, fica tonta e senta balançando a cabeça | Câmera na altura da Tifa |
| 6 | **Ponte sobre o lago** | 1:53–2:09 | Ponte | As quatro atravessam a ponte de madeira uma a uma. Revela o lago · "fazendo festinha": pulinhos · "voltinha, salto no ar": giro e salto · "pronto pra dançar": Clara com os braços para cima no alto da ponte | Grua subindo (revela o lago) → plano frontal |
| 7 | **Grande refrão final** | 2:09–2:30 | Refrão final | Coreografia completa · "Com os amigos é tão bom viver": balanço com braços abertos · "Dançando juntos, eu e você": giro e braços para cima, cachorrinhas pulando | Grua descendo e arco amplo |
| 8 | **Final** | 2:30–2:39 | "Clara e as Patinhas, que alegria! Juntos brincando, todo dia!" | Cachorrinhas se aproximam, Clara se inclina num abraço carinhoso | Plano 3/4 |
| | | 2:39–2:47 | Assinatura final | Todas viram para a câmera e a Clara dá tchau. **Logo** em fade-in | Afastamento e subida (plano geral) |

Arquivos ligados:
- `music/compositions/estrutura.json`: seções, compassos, linhas e notas.
- `scripts/blender/episode.py`: `plan_cameras()` e `choreo()` implementam esta tabela.
- `output/danca_das_patinhas_*.mp4`: os renders.
