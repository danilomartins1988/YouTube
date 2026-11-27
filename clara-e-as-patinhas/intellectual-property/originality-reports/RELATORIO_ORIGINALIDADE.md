# Relatório de originalidade — 2026-11-27

**Aviso:** isto é uma pesquisa de anterioridade preliminar feita por automação, não um parecer jurídico. A ausência de resultados **não** garante originalidade nem disponibilidade de marca. Antes de publicar ou registrar, recomenda-se busca profissional (INPI, USPTO, IMPI, EUIPO/OEPM, WIPO Global Brand Database) por advogado de PI.

## Fontes consultadas e limitações
| Fonte | Acesso | Como |
|---|---|---|
| Web (buscador) | sim | buscas por frase exata (resultados em inglês/EUA) |
| YouTube | **parcial** | primeira página pública de resultados (BR), sem login, via `scripts/originality_search.py`; não cobre vídeos privados, buscas profundas, nem o YouTube Kids |
| Apple Music / iTunes | **parcial** | API pública de busca (lojas BR, US, MX); algumas consultas falharam por limite de requisições (marcadas `ERROR`) |
| Spotify | **não** | a busca do Spotify exige login/token de API; não consultado |
| INPI (BR) | **não** | o BuscaWeb exige sessão interativa; não consultado. Deve ser feito pelo proprietário/advogado em busca.inpi.gov.br |
| USPTO / IMPI / OEPM / EUIPO / WIPO | **não** | não consultados nesta etapa |
| Semelhança melódica | **parcial** | só verificação por análise do próprio material (melodia de 4 notas, Dó maior); sem base de dados de melodias. Prompts nunca citaram artistas ou músicas existentes |

Resultados brutos: `raw/2026-11-27_search_BR.json`, `_US.json`, `_MX.json`.

## Achados que exigem decisão do proprietário (ordem de risco)

### ALTO
1. **"Pata, pata, patatá" × "Patati Patatá".** Patati Patatá é uma marca brasileira de entretenimento infantil muito conhecida (dupla de palhaços, DVDs, desenhos, canal oficial no YouTube, produtos licenciados de brinquedos e alimentos encontrados no varejo). O gancho e o título soam muito próximos no mesmo mercado (música infantil no Brasil). Risco de confusão de marca e de alegação de aproveitamento. **Recomendação:** não registrar nem usar "Pata Pata Patatá" como título/marca sem parecer; considerar alternativas como "Pata, pata, pá!", "Patinha, patinha, olé!", "Pé de pata, patapá". A música atual pode ser regravada só no gancho (inpainting) se o proprietário decidir trocar.
2. **"Pata Pata" (Miriam Makeba, 1967).** Título muito famoso no mundo todo (relançado em 2020 pela UNICEF). Título idêntico a parte do nosso. A melodia e a letra não têm relação, mas o título "Pata Pata…" em plataformas internacionais vai disputar busca e pode confundir. Reforça a recomendação acima, sobretudo para a faixa em espanhol (que manteve "Pata, pata, patatá").
3. **Título EN "The Happy Paw Dance".** Já existem faixas e vídeos chamados **"Happy Paw Dance"** (ex.: "Happy Paw Dance — Flora Blaze" no Apple Music; "Happy Paw Dance Final — Ruby Ridpath" e o canal "Happy-Paws-Dance" no YouTube). **Recomendação:** trocar o título comercial EN (ex.: "Paw Paw Hooray! Puppy & Kitten Dance Song" — "Paw Paw Hooray" não teve resultado idêntico na busca).
4. **Título ES "El Baile de las Patitas".** Já existe vídeo infantil **"El baile de las patitas | Canción y baile infantil"** (MilMundos para Peques). **Recomendação:** trocar (ex.: "¡Guau, Miau, a Bailar!").

### MÉDIO
5. **Nome "Pandora".** Existe um canal infantil brasileiro **"Pandora e Amigos"** ("Dança Dança, Pandorinha"). Nome comum, mas no mesmo nicho. Uso como personagem é provavelmente aceitável; evitar "Pandora" sozinha como título/marca.
6. **Nome "Milo".** Existe série/canal infantil **"Milo" (Milo Português Brasil – Canal Oficial)**, inclusive com vídeo "Encontra o Milo!". O tema nº 8 "Milo Sumiu, Milo Apareceu" deve ser reavaliado no título.
7. **Tema nº 9 "Piuí Patatá".** "Piuí, piuí, piuí" e "Piuí Abacaxi" são músicas da Patati Patatá — **conflito direto**, descartar o título.
8. **Tema nº 11 "A Orquestra das Patinhas".** Patati Patatá tem "Orquestra dos Bichos". Conceito genérico, mas evitar título parecido.
9. **Tema nº 16 "Patinhas Coloridas".** Giramille tem vídeos "Patinhas Coloridas" (vol. 1 e 2) — **título já usado**, trocar.
10. **Tema nº 20 "Escova Chiqui Chiqui".** Já existem "Escova, Escova! Chiqui Chiqui Chá!" (Anto e Theo) e similares — **trocar o gancho**.
11. **Tema nº 6 "Clara Bate Palminha".** "Bate palminha bate" é cantiga tradicional/domínio popular com várias versões gravadas; usar só melodia e letra próprias.
12. **Marca "Clara & Paws".** Sem marca idêntica encontrada na web/YouTube/Apple Music; existem usos isolados ("Clara P.A.W.S. Rescue", "Clara The Cow" da Super Simple Songs). Requer busca USPTO/EUIPO.

### BAIXO / sem resultado idêntico encontrado
- "Clara e as Patinhas", "Clara y sus Patitas", "Jardim Mágico das Patinhas", "Pandora e as Borboletas", "Clara Kids Studios" (só homônimos com "Clara" e "Studios" separados), "Paw Paw Hooray" (só combinações soltas).
- Demais títulos da lista de 30: resultados genéricos (palavras comuns de música infantil). "Tio Patinhas" (Disney) aparece em buscas com "Patinhas", mas é outro uso; "Patinhas" sozinha é palavra comum.

## Estilo musical
O proprietário escolheu **forró pé-de-serra / xote** como estilo da casa. Estilos e gêneros não são protegidos; o risco está em melodias específicas. Os prompts nunca citaram artistas nem músicas (nada de nomes de compositores de forró ou títulos clássicos); a melodia gerada usa 4 notas (Ré–Mi–Dó–Fá em Dó maior) em padrão de pergunta e resposta. Não há como garantir por automação que nenhuma melodia existente seja parecida; recomenda-se escuta crítica do proprietário e, antes de monetizar, uma checagem por reconhecimento de áudio (ex.: o próprio Content ID após upload privado, ou serviço de identificação musical).

## Ferramentas e amostras
Nenhum sample de terceiros foi usado. Toda a música vem do Eleven Music (ElevenLabs) sob a conta do proprietário — ver `../licensing/RELATORIO_LICENCIAMENTO.md`.
