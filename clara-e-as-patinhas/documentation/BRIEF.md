# Clara e as Patinhas — Brief (resumo fiel)

> Resumo do brief do proprietário tal como chegou a esta sessão, com as atualizações posteriores dele.
> Projeto **independente** de The Hidden Economics (sem arquivos compartilhados).

## Marca
- **Nome:** Clara e as Patinhas
- **Slogan:** "Pequenas patinhas, grandes aventuras!"
- **Idioma:** português do Brasil
- **Público:** crianças de 1 a 5 anos
- **Formato:** videoclipes musicais animados de 2 a 3 min
- **Ambição de qualidade:** "série infantil 3D premium e cinematográfica"

## Personagens
> **Atualização do proprietário:** as três cachorrinhas foram renomeadas e são todas **fêmeas** ("cachorrinha", "pequena" etc.):
> Theo → **Ayra**, Luna → **Pandora**, Toby → **Tifa**. Raças, visual, acessórios e personalidades continuam iguais.

| Personagem | Descrição |
|---|---|
| **Clara** | Menina de ~4 anos. Pele clara, cabelo castanho liso e brilhante na altura dos ombros, franja lateral delicada, olhos castanhos grandes, bochechas rosadas, rosto redondo e nariz pequeno. Usa **macacão amarelo** (o principal elemento de identidade), camiseta branca de manga curta, tênis coloridos e um pequeno acessório de cabelo. |
| **Ayra** | Border Collie Red Merle. Base castanho-avermelhada com manchas merle em marrom, bege e branco, peito branco, orelhas semieretas, olhos azul-claros, cauda longa e fofa e **bandana azul**. O desenho das manchas fica fixo na textura e nunca muda. |
| **Pandora** | Lulu da Pomerânia branca, muito fofa e arredondada, mas com anatomia clara: focinho, orelhinhas triangulares, olhos escuros, nariz preto, patas curtas e cauda em pluma enrolada sobre as costas. Usa **laço rosa**. |
| **Tifa** | Yorkshire Terrier. Rosto e patas castanho-dourados, dorso cinza-aço escuro, orelhas pequenas e eretas, olhos escuros, corpo compacto e **bandana verde**. É a menor e a mais engraçada. |

**Escala:** Clara é a mais alta. Ayra chega mais ou menos ao joelho da Clara, Pandora é bem menor que Ayra e Tifa é um pouco menor que Pandora. As cachorrinhas são quadrúpedes e só fazem movimentos de dança curtos e estilizados.

## Música — "A Dança das Patinhas" (ep. 001)
- Melodia **original**, 110–120 BPM, tom maior, 4/4, gancho principal nos primeiros 5 s, refrão memorável e uma **assinatura de marca** original de 2 a 4 compassos que possa ser reutilizada nos próximos episódios. Não copiar nenhuma música existente. Duração de 2:30 a 3:00.
- Estrutura: Intro → Refrão → Verso da cachorrinha 1 → Refrão curto (6 primeiras linhas) → Verso 2 → Verso 3 → Ponte → Refrão final → Final. A letra final está em `music/lyrics/a-danca-das-patinhas.md`; a letra original era do proprietário e só recebeu ajustes de métrica, rima e gênero.
- **Vozes:** voz feminina jovem e calorosa, pronúncia natural do pt-BR e backing vocals leves. O proprietário **recusou TTS falado** como substituto do canto e **autorizou a API Eleven Music (ElevenLabs)** para vozes cantadas reais. A chave ainda não está disponível.
- **Instrumentação:** violão/ukulele, piano, xilofone/marimba, palmas, percussão leve, baixo acústico, sininhos suaves e latidinhos rítmicos discretos.

## Visual / 3D
- Personagens estilizados, fofos, arredondados e com aparência premium, construídos no Blender e salvos como assets reutilizáveis.
- **Rig:** cabeça, orelhas, cauda, patas, braços, boca e pálpebras da Clara (piscar). **Ações:** respirar parada, piscar, abanar a cauda, mexer a orelha, andar/correr, pulinho, giro e bater palmas (Clara).
- **Pelagem:** aproximação procedural adequada a renderização em CPU.
- **Model sheets:** frente, lado, costas, 3/4, 5 expressões (feliz, curiosa, surpresa, concentrada, carinhosa), pose de dança, paleta e proporções. Mais uma imagem do grupo.
- **Cenário:** jardim com grama verde macia, colinas arredondadas, árvores de copa fofa, flores coloridas, borboletas, laguinho, ponte de madeira, caminho de pedras, balanço, brinquedos coloridos, casinhas de cachorro, céu azul com nuvens suaves e colinas ao longe. Casa da Clara com paredes claras, telhado de terracota, janelas grandes, varandinha e vasos de flores.
- **Paleta:** amarelo-sol, azul-céu, verde natural, rosa suave, branco, madeira quente e terracota.
- **Luz:** sol suave com preenchimento do céu, sombras suaves e brilho nos olhos.
- **Coreografia do refrão:** "Patinha pra frente" = Clara põe um pé à frente e as cachorrinhas levantam uma pata dianteira; "pra trás" = passinho para trás; "voltinha" = giro pequeno; palmas no tempo; caudas abanando, orelhas mexendo, piscadas e respiração.

## Etapas (escopo desta fase: 1, 2 até a composição, 3, 4, 6 e 7)
1. Diagnóstico técnico (`reports/DIAGNOSTICO.md`).
2. Composição: letra, melodia, estrutura, instrumental-guia e plano para o Eleven Music. **As vozes ficam bloqueadas até a chave existir.**
3. Personagens 3D, rigs, ações e model sheets.
4. Cenário.
6. Teste animado de 10 a 15 s, 1920×1080 a 30 fps, sincronizado com o instrumental-guia, com medição do tempo de render e estimativa para o episódio inteiro.
7. Autoavaliação honesta (`reports/TESTE_3D.md`).

## Regras
- Não publicar nem enviar nada. Não chamar serviços pagos. Nunca expor chaves.
- Registrar a origem e a licença de todo asset (`licensing/REGISTRO.md`) e os custos (`reports/CUSTOS.md`; gasto externo até agora: US$ 0).
- Mídia grande vai para `output/` ou `rendering/` e fica no git-ignore.


## Regra adicional do proprietário (2026-11-27)

"Evite citar os nomes dos personagens nos vídeos." Letras, falas, letreiros, títulos, descrições, tags e thumbnails não citam os nomes das personagens. Elas são identificadas pelo visual (a menina de macacão amarelo, a cachorrinha de bandana azul, a branquinha de laço rosa, a pequenina de bandana verde). Os nomes continuam apenas nos arquivos internos de produção.

Exceção decidida pelo proprietário (2026-11-27): o piloto "A Dança das Patinhas" fica como está, com os nomes cantados. A regra vale do episódio 2 em diante.
