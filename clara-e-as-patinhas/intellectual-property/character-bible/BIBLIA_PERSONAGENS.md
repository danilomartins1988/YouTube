# Bíblia dos Personagens — Clara e as Patinhas (v1, 2026-11-27)

Fonte: Aditivo 01, §4–§10, e decisões do proprietário de 2026-11-27 (Toby macho). Este documento é a referência de texto. A referência visual é a imagem oficial da turma e os assets canônicos (abaixo).

## Regra de consistência (proprietário: "Precisamos manter a voz e os personagens ao longo dos episódios")

1. Cada personagem tem **um asset canônico versionado**: `assets/characters/canon/<nome>_v<N>.blend`, com turnaround renderizado (`<nome>_v<N>_turnaround.png`), paleta e mapa de marcações (`<nome>_v<N>_markings.png`, ex.: manchas merle da Ayra, listras do Milo).
2. **Os episódios importam (link/append) o asset canônico e nunca o reconstroem nem o modificam.** Poses, ações e expressões ficam no arquivo do episódio ou na biblioteca de ações; malha, materiais, texturas, marcações e acessórios ficam no canon.
3. Qualquer mudança no canon exige **autorização do proprietário** e gera uma **nova versão** (`_v2`), com changelog em `assets/characters/canon/CHANGELOG.md`. Episódios antigos continuam apontando para a versão com que foram feitos.
4. Um script de verificação (`scripts/canon_check.py`) compara o hash do canon usado pelo episódio com `assets/characters/canon/MANIFEST.json` antes de cada render.
5. **Estado atual:** o canon v1 só é congelado quando os cinco modelos finais forem escolhidos (após o teste de personagens; ver `reports/PERSONAGENS_ROTA.md`). Até lá, os arquivos em `assets/characters/<nome>/` são a versão do ep. 001 e **não** são canon.

## Escala comparativa
Clara é a mais alta (referência = 1,00). Ayra ≈ altura do joelho/quadril da Clara (0,45). Pandora ≈ 0,30. Toby ≈ 0,27 (o menor dos cães). Milo ≈ 0,28 (sentado ≈ 0,32 com orelhas).

## 1. Clara — a líder criativa (menina, ~4 anos)
- **Aparência:** pele branca; cabelo castanho liso na altura dos ombros com franja lateral delicada; olhos castanhos grandes; bochechas levemente rosadas; rosto redondo; nariz pequeno; sorriso acolhedor; **jardineira amarela**, camiseta branca, tênis coloridos, pequeno acessório no cabelo (presilha de flor amarela no ep. 001; manter).
- **Personalidade:** alegre, inteligente, curiosa, carinhosa, musical, criativa. Conduz as músicas, demonstra os movimentos, interage com os animais.
- **Cor** amarelo · **símbolo** estrela · **instrumento** ukulele · **movimento** bater palmas e girar · **expressão** sorriso com leve inclinação da cabeça.
- **Animação:** cabelo, roupa e mãos com movimento secundário; expressões faciais; lip-sync em pt-BR (por visemas).

## 2. Ayra — a aventureira (Border Collie red merle, fêmea)
- **Aparência:** marrom avermelhado com manchas merle mescladas (marrom, bege, branco), padrão red merle reconhecível; peito predominantemente branco; pelo médio, macio e volumoso; orelhas semieretas; **olhos azul-claros**; focinho delicado; cauda longa e peluda; **bandana azul**.
- **Marcações fixas:** o mapa de manchas é uma textura única do canon (`ayra_v1_markings.png`) e nunca é gerado de novo (sem ruído procedural com semente variável).
- **Personalidade:** inteligente, aventureira, atlética, curiosa, corajosa, protetora.
- **Cor** azul · **símbolo** bússola · **instrumento** tambor suave · **movimento** saltinhos e corridas · **som** au, au, au.
- **Animação:** corridas fluidas, saltos, orelhas independentes, cabeça inclinada, cauda balançando, pelagem secundária, passos de dança com as patas dianteiras.

## 3. Pandora — a encantadora (Lulu da Pomerânia, fêmea)
- **Aparência:** totalmente branca; pelo longo, macio e muito volumoso; silhueta arredondada; olhos grandes, escuros e brilhantes; nariz pequeno preto; orelhas triangulares; patinhas curtas; cauda volumosa curvada sobre o dorso; **laço rosa**.
- **Personalidade:** carinhosa, delicada, alegre, musical, afetuosa, apaixonada por dança. Forte potencial de pelúcia.
- **Cor** rosa · **símbolo** coração · **instrumento** xilofone · **movimento** pulinhos e giros · **som** au, au (delicado, estilizado).
- **Animação:** saltinhos ritmados, giros, patas delicadas, piscadas, pelagem suave, aproximação carinhosa da Clara.

## 4. Toby — o brincalhão (Yorkshire Terrier, macho)
- **Aparência:** castanho-dourado no rosto e nas patas; cinza-escuro no dorso; pelo sedoso; orelhas pequenas e eretas; olhos escuros grandes; focinho pequeno; corpo compacto; patinhas curtas; **bandana verde**. Visual masculino discreto (sem laço; topete curto em vez do "rabinho de cabelo" típico de fêmea).
- **Histórico:** substitui "Tifa" (fêmea) do ep. 001 por decisão do proprietário em 2026-11-27.
- **Personalidade:** engraçado, energético, curioso, corajoso, um pouco atrapalhado. Humor gentil, sem violência, sustos ou humilhação.
- **Cor** verde · **símbolo** raio · **instrumento** trompete suave · **movimento** passos rápidos e giros engraçados · **som** latidinhos ritmados.
- **Animação:** corridinhas, pulinhos, cabeça engraçada, passos curtos, surpresa, tentativas de acompanhar os outros, pequenas comemorações.

## 5. Milo — o explorador curioso (gato laranja, macho)
- **Aparência:** laranja com listras suaves (rajado); barriga e focinho creme; **olhos verdes** grandes; nariz rosado; orelhas triangulares; bigodes delicados; cauda longa e flexível; patinhas arredondadas; **coleira roxa**.
- **Marcações fixas:** mapa de listras único do canon (`milo_v1_markings.png`).
- **Personalidade:** curioso, inteligente, independente, observador, criativo, brincalhão; encontra soluções e objetos escondidos.
- **Cor** roxo · **símbolo** lua · **instrumento** pizzicato de violino · **movimento** saltos felinos e brincadeiras com a cauda · **som** miau, miau, miau.
- **Animação:** caminhada felina, saltinhos, orelhas independentes, cauda expressiva, piscadas lentas, esconder/aparecer, cabeça curiosa, surpresa, interação com bola, folhas e brinquedos.

## Paleta oficial dos personagens
| Personagem | Cores principais (HEX) |
|---|---|
| Clara | jardineira `#FFC81A`, camiseta `#FFFFFF`, cabelo `#5C331A`, pele `#F6D2BC`, bochecha `#F4A4A0` |
| Ayra | base `#9A4A2C`, merle `#C98A63`/`#E8D2B6`, peito `#FFFFFF`, olhos `#8FD3F5`, bandana `#2E7AF2` |
| Pandora | pelo `#FFFFFF` (sombra `#EDE7F0`), olhos/nariz `#1E1418`, laço `#FA8CB4` |
| Toby | dourado `#C68A3E`, dorso `#4A4F5A`, olhos `#1E1418`, bandana `#6CB848` |
| Milo | laranja `#F08A2C`, listras `#C9601C`, creme `#F7E3C0`, olhos `#5FBF4A`, nariz `#F2A0A8`, coleira `#8E5CC8` |

## Assinaturas sonoras
Ayra "au, au, au" (médio, alegre) · Pandora "au, au" (agudo e delicado) · Toby latidinhos curtos ritmados · Milo "miau, miau, miau" · Clara canta (voz principal = voz da marca, ver `music-rights/VOICE_PROFILE.md`).

## Situação dos entregáveis visuais (honesta)
| Item | Situação |
|---|---|
| Especificação em texto (este documento) | feito |
| Model sheets frente/lado/costas/3/4 e 5 expressões | existem para Clara, Ayra, Pandora e Tifa (versão ep. 001, procedural). **Faltam:** Toby (macho) e Milo; nova versão premium dos cinco |
| Imagem oficial da turma com os cinco | ver `reports/PERSONAGENS_ROTA.md` (Fase C) |
| Mapas de marcações fixos (Ayra, Milo) | a criar com o canon v1 |
| Rigs | ep. 001: rig simples (cabeça, orelhas, cauda, patas, boca, pálpebras). Premium: a definir |
| Biblioteca de animações | ações do ep. 001 (respirar, piscar, abanar, pulinho, giro, palmas); faltam corrida, salto felino, miado, trompete etc. |
| Canon congelado `assets/characters/canon/` | **ainda não** (só após escolha dos modelos finais e aprovação) |
