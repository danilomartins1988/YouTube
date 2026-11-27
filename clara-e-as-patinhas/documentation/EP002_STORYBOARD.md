# Episódio 002 — "Cadê? Achou!" · roteiro de cenas, storyboard e plano de qualidade

> Arquivo **interno de produção**. Os nomes internos dos rigs aparecem entre parênteses só para orientar a produção.
> Nada disso vai para tela, título, descrição, tags ou thumbnail. No vídeo, as personagens são só "a menina de macacão amarelo",
> "a cachorrinha de bandana azul" (rig `ayra`), "a branquinha de laço rosa" (rig `pandora`) e "a pequenina de bandana verde" (rig `tifa`).

- Música: `music/masters/cade_achou_final.wav` (2:04,8, 99,9 BPM, compasso de 2,4 s). Letra: `music/lyrics/cade-achou.md`.
- Cena: `scripts/blender/ep2_scene.py` cria `rendering/ep002.blend` a partir do jardim do ep. 001. O `ep001.blend` nunca é salvo por esse script.
- Stills de teste: `reports/ep002_stills/` (folha de contato: `contact_sheet.jpg`).
- **Status:** a música está pronta e esperando a aprovação do proprietário. **O render completo não começou.**

## 1. Mudanças no cenário em relação ao ep. 001
| Item | O que muda | Por quê |
|---|---|---|
| Placas das casinhas | Os letreiros com os nomes foram **removidos** e trocados por uma **patinha branca** em relevo | Regra do proprietário: nenhum nome na tela |
| Balde azul pequeno do ep. 001 | Removido da cena | Não pode haver dois baldes na história |
| **Flor gigante** (nova) | Flor coral de 11 pétalas, miolo amarelo e duas folhas grandes, em (-1,05; 0,55) | Esconderijo 1: atrás da flor |
| **Balde de brinquedo** (novo) | Balde azul-céu aberto (r 0,19→0,22 m, 0,24 m de altura), aro branco e alça amarela, em (0,05; 1,0) | Esconderijo 2: dentro do balde |
| **Chapéu de palha** (novo) | Aba de 0,29 m, copa em cúpula, fita amarela e textura de palha procedural, em (1,1; 0,5) | Esconderijo 3: embaixo do chapéu. No final, vira o objeto com que a menina tapa o rosto |
| Luz (níveis L1+) | Sol principal mais quente e mais macio (ângulo de 14°), **luz de recorte** quente por trás, **preenchimento** azulado de área do lado da câmera | Volume e separação do fundo |

Todos os esconderijos ficam no gramado central, a até 1,2 m da menina, para que o plano geral mostre os três ao mesmo tempo (still 02/03).

## 2. Mapa música → cenas (tempos reais da faixa)
| Tempo | Seção | Plano / ação | Detalhe de animação |
|---|---|---|---|
| 0:00–0:04,8 | Intro instrumental | Plano geral do jardim (still 02). Câmera desce devagar do céu até o gramado. A menina está no centro e não há nenhuma cachorrinha à vista | Borboletas. Dois latidinhos fora de quadro (pista sonora: "onde estão?") |
| 0:04,8–0:24 | Refrão "Cadê, cadê…" | A menina gira devagar e procura com a mão na testa (pose de busca). Cortes curtos para cada esconderijo, sem revelar nada | A cada "cadê" ela vira a cabeça para um lado. No "Vem procurar" acena para a câmera |
| 0:24–0:33,8 | Estrofe 1 "Atrás da flor…" | Aproximação da flor gigante (still 04). Em "Uma orelhinha" **só a orelha** aparece atrás das pétalas e balança. Em "Bandana azul…" a pontinha da bandana aparece | Suspense de ~1,7 s com zoom lento na flor |
| **0:33,8** | **ACHOU!** (au, au!) | A cachorrinha de bandana azul **pula para fora** da flor (squash-and-stretch na saída e no pouso), e as pétalas balançam | "Au, au!" com a boca no tempo. A cauda abana com atraso (overlap) |
| 0:38,4–0:48 | Refrão curto | Plano médio: as duas dançam juntas e procuram a próxima | |
| 0:48–0:58,7 | Estrofe 2 "Dentro do balde…" | Aproximação do balde (still 05). Em "Um rabinho branco" **só a cauda-pluma** aparece acima do aro e balança. Em "Laço cor-de-rosa…" o laço aparece | O balde treme levemente |
| **0:58,7** | **ACHOU!** | A branquinha **salta do balde**, o balde balança e quase cai | Squash ao sair; as orelhas acompanham |
| 1:02,4–1:12 | Refrão curto | As três procuram juntas | |
| 1:12–1:22,2 | Estrofe 3 "Embaixo do chapéu…" | Aproximação do chapéu (still 06). Em "Um narizinho" **só o focinho** aparece embaixo da aba e cheira o ar. Em "Bandana verde…" a bandana aparece | O chapéu se mexe sozinho (a cachorrinha anda embaixo dele) |
| **1:22,2** | **ACHOU!** | A pequenina **levanta o chapéu com a cabeça**, e ele sai rolando | Momento engraçado: ela fica com o chapéu na cabeça por um instante |
| 1:26,4–1:38,3 | Ponte "E a menina? Cadê?" | As três cachorrinhas viram para a câmera. A menina pega o chapéu e **tapa o rostinho com ele** (still 07) | As cachorrinhas inclinam a cabeça (expressão curiosa). Pausa longa de ~3 s |
| **1:38,3** | **ACHOU!** | A menina abaixa o chapéu, **põe na cabeça** e abre os braços (still 08). As três pulam | Sorriso e piscada |
| 1:40,8–1:51,9 | Final "E você? Cadê você?" | **Plano frontal de olho na câmera**: a menina olha para o espectador. Em "Tapa o rostinho" ela tapa de novo, convidando a criança a imitar | Câmera parada (bebês acompanham melhor), fundo desfocado |
| **1:51,9** | **ACHOU!** (convite) | A menina e as três aparecem juntas para o espectador | Comemoração simples, sem pedido de inscrição nem CTA |
| 1:55,2–2:04,8 | Encerramento "Achou, achou, que alegria!" | Plano geral: todas pulam em roda. A câmera sobe e mostra o jardim | Fim em plano aberto. Sem logo de marca (o canal ainda não tem nome definido) |

**Por que a menina tapa o rosto com o chapéu e não com as mãos:** testei 12 poses de mãos sobre os olhos (`EP2_HIDE`/`EP2_HEAD` em `ep2_scene.py`). O rig rígido de proporções chibi (cabeça grande, braços de 0,23 m) **não alcança os olhos**: as mãos param nas bochechas ou atrás da cabeça. O chapéu resolve na história ("tapou o rostinho") e liga o final ao terceiro esconderijo. Para tapar com as mãos seria preciso refazer os braços (mais longos ou com IK e ombro), o que fica como melhoria opcional.

## 3. Stills de teste (`reports/ep002_stills/`)
| Arquivo | Nível | O que mostra |
|---|---|---|
| `01_plano_geral_L0_ep1.jpg` | L0 | Configuração do ep. 001 (720p, 8 amostras), para comparar |
| `02_plano_geral_L1M.jpg` | L1M | 1080p nativo, luz de 3 pontos, gradação, DOF e motion blur |
| `03_plano_geral_L2.jpg` | L2 | L1M + 32 amostras + SSR |
| `04`–`08` | L2 | Flor com orelhinha, balde com rabinho, chapéu com focinho, menina tapando o rosto, ACHOU |
| `09_teste_pelo_L3_rejeitado.jpg` | L3 | Pelo por partículas: ficou espetado ("ouriço"), precisaria de grooming manual, e é 3× mais lento. **Rejeitado** |

Observação: os stills 04–06 mostram a pose de esconderijo, ou seja, o primeiro "peek". Na animação, cada parte (orelha, cauda, focinho) entra no tempo da palavra.

## 4. Upgrades de qualidade: tempo medido nesta CPU (4 núcleos, sem GPU, EEVEE do Blender 4.0.2)
Tempos por frame medidos no plano geral (`still wide`; "quente" = segundo frame, com os shaders já compilados). Os close-ups L2 levaram de 89 a 106 s.

| Nível | O que inclui | s/frame | Episódio (≈3.020 frames) | Nota visual honesta* |
|---|---|---|---|---|
| **L0** (= ep. 001) | 720p ampliado, 8 amostras, sol + céu | ~10–13 (no lote do ep. 001: ~5,5) | **~5–8 h** | 5,0 personagens · 6,5 cenário/luz |
| L1 | 1080p nativo, 16 amostras, luz de 3 pontos, gradação + vinheta, DOF | ~36 | ~30 h | 5,5 · 7,3 |
| **L1M (recomendado)** | L1 + motion blur, sombras de contato, sombras 2048 | **~40** | **~34 h** (≈215 lotes de 9,5 min) | 5,5 · 7,5 |
| L2 | L1M + 32 amostras + reflexos SSR | ~85–106 | ~75–90 h | 5,6 · 7,6 (pouca diferença visível sobre L1M) |
| L3 | L2 + 64 amostras + pelo por partículas | ~267 | ~225 h | Rejeitado (pelo espetado, exige grooming) |

\* Na mesma rubrica ponderada do QC do ep. 001 (personagens 20%, cenário/luz 10%).

**Upgrades de animação: custo de render ≈ 0, só código** (são o maior ganho por hora):
| Upgrade | Como | Ganho esperado |
|---|---|---|
| **Visemas pelo Whisper** | O Whisper dá o tempo de cada palavra. Divido em sílabas pt-BR e mapeio vogais para formas: A/E → `mouth_open` largo, O/U → `mouth_o`, M/B/P → boca fechada (`mouth_smile`), F/V → aberta estreita (escala x 0,7). Coarticulação com suavização de 60 ms | Boca deixa de ser "abre/fecha" (problema do ep. 001) |
| Squash-and-stretch | Escala no eixo do movimento nos pulos do "ACHOU!" (estica 1,15 na subida, achata 0,85 no pouso, volume preservado) | Pulos mais vivos |
| Overlapping action | Orelhas e cauda seguem o corpo com atraso de 2–4 frames e mola amortecida (ζ ≈ 0,4) | Menos "boneco" |
| Piscadas + sobrancelhas | Piscadas aleatórias com dupla piscada ocasional. Sobrancelhas da menina sobem na pausa de suspense e no "ACHOU!" (os bones `brow_L/R` já existem) | Atuação legível |
| Câmera | Curvas com ease in/out de 1–2 s, sem cortes bruscos. Dolly lento na pausa de suspense. Câmera estática no convite ao espectador | Ritmo para bebês |
| Cenário | Mais flores e tufos em volta dos esconderijos, borboleta pousando na flor gigante, folhas balançando | Riqueza |

**Estimativa honesta do episódio 002 com L1M + upgrades de animação:** ≈ **7,5/10** na rubrica (era 6,9). Música ≈ 8,5; personagens 5,5; animação 7,5–8; consistência 8; cenário/luz 7,5; técnica 9; entregáveis 8.

### O que falta para 9–10 (não dá com este setup)
1. **Personagens refeitos por um artista 3D**: modelos esculpidos com topologia de animação, malha que deforma (pele e roupa contínuas em vez de peças rígidas), rosto com blendshapes (boca, bochechas, pálpebras) e pelo com grooming de verdade. **É o maior limitador (personagens = 20% da nota).** Na prática são algumas semanas de um modelador/rigger profissional.
2. **Animador** para as atuações-chave (os 5 "ACHOU!"). O procedural não substitui atuação feita à mão.
3. **GPU**: com uma GPU moderna, o mesmo L2 em EEVEE sairia em ~1–3 s/frame, e o Cycles com GI real em ~20–60 s/frame (estimativa). Com isso dá para usar GI, pelo e motion blur reais num prazo viável. Nesta CPU, o Cycles a 1080p levaria vários minutos por frame (dias de render).
4. Blender mais novo (EEVEE Next, 4.2+), com sombras e GI melhores. Mas o apt oferece só o 4.0.2, e atualizar pode quebrar o pipeline.

## 5. Plano de render (só depois da aprovação da música)
1. `episode2.py` (novo, sem alterar o `episode.py` do ep. 001): handler por frame com o timeline real da faixa (Whisper + batidas em `music/analysis/ep2/`), visemas, squash/overlap e as câmeras da tabela 2.
2. Teste animado de 10 s (estrofe 1 + ACHOU) em L1M, para aprovação do movimento.
3. Render completo em L1M com o `render_driver.py` (lotes de 9,5 min; ~34 h de CPU), segmentos codificados e PNGs apagados a cada segmento (há ~1,6 GB livres no disco).
4. QC: frames a cada 5 s, sincronia de cada "ACHOU!", loudness do MP4 e conferência de que não há nenhum nome na tela.
