# Guia de publicação multilíngue (YouTube) — v1, 2026-11-27

> **Decisão do proprietário (2026-11-27):** "o vídeo principal precisa ser feito em português e os outros idiomas serão carregados por áudio." A **faixa original é pt-BR**; inglês e espanhol entram como faixas de áudio adicionais. (Substitui a preferência do Aditivo 03 por inglês como original; continua configurável em `clara-kids-studios/config/languages.json`.)

**Importante:** não temos acesso ao canal do proprietário. Tudo abaixo vem da documentação pública do YouTube consultada em 2026-11-27 e **deve ser validado pelo proprietário no YouTube Studio**. Nada foi publicado.

## O que a documentação oficial diz (consultada em 2026-11-27)
- **Áudio multilíngue** ("Add Multi-language features to your videos", https://support.google.com/youtube/answer/13338784): permite enviar faixas de áudio dubladas próprias em outros idiomas, para vídeos novos ou existentes e Shorts. A página avisa que o recurso **pode não estar disponível para todos** ainda (implantação gradual) e tem uma seção de elegibilidade — **confirmar no Studio se aparece a opção de faixas de áudio**. Se houver dublagem automática para um idioma, ela precisa ser apagada antes de enviar a faixa própria. Dublagem automática: https://support.google.com/youtube/answer/15569972 (não usar, por decisão do proprietário).
- **Conteúdo "made for kids"** (https://support.google.com/youtube/answer/9527654 e https://support.google.com/youtube/answer/9632097): sem anúncios personalizados, sem comentários, sem sino de notificação, sem miniplayer, entre outros; a receita pode ser menor. Marcar o vídeo/canal como "feito para crianças" é obrigatório para este conteúdo (COPPA).
- **Monetização — conteúdo inautêntico e reutilizado** (https://support.google.com/youtube/answer/1311392): desde julho de 2025 a regra antes chamada de "conteúdo repetitivo" se chama "conteúdo inautêntico" (produção em massa / repetitiva, com pouca variação). Vale para o canal inteiro. "Conteúdo reutilizado" é outra regra (material de terceiros sem transformação). **Implicação:** cada música precisa ter identidade própria; não publicar versões quase idênticas; as faixas de idioma no mesmo vídeo não são uploads duplicados.
- Não verificado nesta etapa (o proprietário deve conferir no Studio/Ajuda): lista exata de idiomas aceitos para faixas extras, formatos de arquivo aceitos para faixas de áudio, miniaturas por idioma, métricas por faixa de áudio. Não inventamos esses dados.

## Passo a passo previsto no Studio (12 passos — validar)
1. Confirmar que o canal está marcado/configurado como "feito para crianças" e que o recurso de áudio multilíngue aparece (Configurações → Padrões de upload / Recursos avançados).
2. Enviar o vídeo principal com a **faixa original em português** (MP4 principal, áudio pt-BR).
3. Definir idioma do vídeo = português (Brasil); público = feito para crianças.
4. Título, descrição e tags em português (`metadata/pilot/pt-BR.md`).
5. Miniatura principal: a PT (ou a universal sem texto).
6. Em **Idiomas** (Legendas/Traduções), adicionar **inglês** e **espanhol (América Latina)**.
7. Para cada idioma: **adicionar faixa de áudio** e enviar o arquivo correspondente (mesma duração exata do vídeo).
8. Para cada idioma: título e descrição traduzidos (metadados localizados).
9. Se disponível, miniatura por idioma.
10. Conferir se não existe dublagem automática para EN/ES (apagar, se houver).
11. Publicar como **privado/não listado** primeiro e ouvir cada faixa no player (troca de idioma pelo menu de áudio).
12. Só então publicar (decisão do proprietário).

## Contingências
- **A. Começar só com o português** e adicionar as faixas quando o recurso aparecer (vídeos existentes aceitam faixas novas, segundo a ajuda).
- **B. Esperar o recurso** ser liberado para o canal.
- **C. Canais separados por idioma** — só com autorização do proprietário (vídeos completos por idioma já podem ser exportados, porque o áudio de cada idioma tem a duração exata).
