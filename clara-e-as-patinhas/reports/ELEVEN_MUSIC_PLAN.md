# Plano Eleven Music: "A Dança das Patinhas"

**Status em 2026-11-27:** o plano e o script estão prontos. **Nenhuma geração foi feita.**
O proprietário autorizou (pelo coordenador) **1 geração + no máximo 1 nova tentativa**, mas a camada de permissões desta sessão **bloqueou a chamada paga**. Uma mensagem de outro agente não conta como consentimento do usuário. Para gerar, o proprietário precisa aprovar a execução diretamente: rodar o comando abaixo ou liberar a permissão.

## Endpoint
- `POST https://api.elevenlabs.io/v1/music` (Compose music)
  Doc: https://elevenlabs.io/docs/api-reference/music/compose
- Autenticação: header `xi-api-key`. Neste ambiente, o proxy de rede injeta a chave para `api.elevenlabs.io`; o script manda um valor fictício e nunca imprime headers.
- Query `output_format`: o script tenta, em ordem, `pcm_48000` → `pcm_44100` → `mp3_48000_320` → `mp3_48000_192` → `mp3_44100_128` (o Starter lista "High-Quality Downloads: No", então é provável que caia em 128 kbps). Só passa para o próximo formato se o servidor recusar o anterior (4xx sobre formato ou plano), e nesse caso nada é gerado. Valores permitidos segundo a referência da API (o padrão `auto` escolhe `mp3_48000_192` para os modelos v2).
- O header de resposta traz o `song_id`, usado em inpainting e Audio Reference. O script salva os headers não sensíveis em `music/masters/*.response.json`.
- Outros endpoints oficiais: `POST /v1/music/plan` cria um plano a partir de um prompt e **não gasta créditos** (https://elevenlabs.io/docs/api-reference/music/create-composition-plan). `POST /v1/music/detailed` devolve o áudio junto com os metadados.
- **Stems:** existe o endpoint oficial `POST /v1/music/stem-separation` (multipart com `file`, opcional `stem_variation_id`), que devolve um ZIP de stems (https://elevenlabs.io/docs/api-reference/music/separate-stems). **O custo não está publicado na página de preços**, então **não está autorizado** e não foi usado. O instrumental separado também pode sair de uma segunda geração do mesmo plano com `negative_styles: ["vocals"]`, mas isso conta como geração extra, também não autorizada.

## Formato da requisição (`music_v2_5`, plano por chunks)
Arquivo: `music/compositions/eleven_music_plan.json`, gerado por `scripts/build_eleven_plan.py` a partir de `estrutura.json`. Os campos `_meta` são removidos antes do envio.
```json
{
  "model_id": "music_v2_5",
  "composition_plan": {
    "chunks": [
      {"text": "[Brand Jingle]\n{cheerful xylophone jingle}\n{two small cute dog barks}",
       "duration_ms": 4174,
       "positive_styles": ["cheerful Brazilian children's song", "warm young female lead vocal, ... Brazilian Portuguese pronunciation", "...", "115 BPM", "D major"],
       "negative_styles": ["electric guitar distortion", "...", "European Portuguese accent", "vocals", "lyrics"],
       "context_adherence": "high"},
      {"text": "[Intro]\nClara chamou as amiguinhas,\nVieram correndo três cachorrinhas!\n...", "duration_ms": 16695, "...": "..."}
    ]
  }
}
```
- **14 chunks**, total **164.870 ms (2:44,9)**, com as mesmas durações do instrumental-guia (115 BPM, 79 compassos).
- Regras seguidas, conforme o guia de planos de composição (https://elevenlabs.io/docs/eleven-api/guides/how-to/music/composition-plans):
  - tag de seção entre `[ ]`; direções inline entre `{ }`;
  - estilos em inglês e letra em pt-BR;
  - seções instrumentais sem letra e com `vocals` em `negative_styles`;
  - até 30 chunks, cada um com 3 a 120 s;
  - o primeiro chunk leva o estilo global (17 estilos).
- O prompt não cita nenhum artista nem título de música existente (Music Terms, §2.1).
- Prompt de estilo global (também guardado em `_meta.estilo_global_prompt`): *"Cheerful Brazilian children's song for ages 1-5, warm young female lead vocal with natural Brazilian Portuguese pronunciation, light backing vocals, ukulele and acoustic guitar, xylophone and marimba, hand claps, light percussion, acoustic bass, soft bells, 115 BPM, D major, small rhythmic dog barks."*
- **Risco de idioma:** a página de capacidades cita inglês, espanhol, alemão e japonês "and more", **sem confirmar o português** (https://elevenlabs.io/docs/overview/capabilities/music). O plano reforça "Brazilian Portuguese" e põe "European Portuguese accent" e "Spanish accent" em `negative_styles`. É preciso conferir com transcrição (Whisper) depois de gerar.

## Custo estimado (fontes oficiais)
| Item | Cálculo | Créditos | US$ |
|---|---|---|---|
| 1 geração de 2:44,9 | 2,748 min × US$ 0,15/min; 2,748 min × ~900 créditos/min | **~2.473** | **~US$ 0,41** |
| + 1 nova tentativa | o mesmo | ~2.473 | ~US$ 0,41 |
| **Máximo autorizado (2 gerações)** | | **~4.946** | **~US$ 0,82** |
| Plano de composição (`/v1/music/plan`) | gratuito | 0 | 0 |
| Verificação Whisper (opcional, por música) | 2,75 min × US$ 0,006 | n/a | ~US$ 0,02 |

Fontes:
- https://elevenlabs.io/pricing/api: "Via ElevenAPI, Eleven Music is $0.15 per minute plus $1.50 per finetune"; limite de 5 min por faixa; "Commercial use licensing on Starter+ plans".
- https://elevenlabs.io/pricing: Eleven Music "uses about 900 [credits] per minute", com custo exato por plano mostrado antes de gerar.

O consumo real depende do plano do proprietário. A chave **não tem permissão `user_read`**, então nem o plano nem o saldo de créditos podem ser lidos pela API.

## Termos de uso comercial (resumo)
Fonte: https://elevenlabs.io/music-terms (atualizado em 09/10/2026). Ver também https://elevenlabs.io/pricing.
- **Propriedade:** "you retain any and all rights in and to your Input and Output", sujeito ao contrato principal com a ElevenLabs (§2.2).
- **Por plano:**
  - **Free:** uso individual, sem download, sem distribuição em streaming e com atribuição obrigatória.
  - **Starter:** uso comercial, mas **distribuição em streaming proibida**.
  - **Creator e acima:** distribuição em streaming permitida e sem atribuição.
  - **Pro:** downloads em alta qualidade.
  - **Scale e Business:** limites por número de funcionários.
- **Exclusões em Free até Scale:** "All online and offline commercial use permitted, except film, TV, radio, and Studio Games". Não fica claro se YouTube conta como "TV"; **vale confirmar com a ElevenLabs.**
- **Proibido:** citar nomes reais de artistas, títulos de músicas ou trechos de letras nos prompts (§2.1), imitar artistas (§3.3) e criar bibliotecas de música ou revender (§4.2–4.3).
- **Obrigações:** o usuário revisa o resultado antes de publicar (§3.1) e segue as regras de cada plataforma sobre divulgação de IA (§4.4). No YouTube, isso significa marcar conteúdo sintético/alterado quando aplicável.
- **Conclusão para um canal no YouTube:** é preciso no mínimo o plano **Creator** (streaming permitido). **O proprietário precisa confirmar o plano.**

## Passos exatos para gerar (quando aprovado)
```bash
cd /home/user/YouTube/clara-e-as-patinhas
# 1) (re)gerar o plano a partir da estrutura, se a letra ou a estrutura mudarem
python3 scripts/build_eleven_plan.py
# 2) simulação: mostra a estimativa de custo e se recusa a chamar a API
python3 music/scripts/eleven_generate.py
# 3) geração real (gasta ~2.473 créditos ≈ US$ 0,41)
python3 music/scripts/eleven_generate.py --confirm --tag v1
# saída: music/masters/danca_das_patinhas_v1.wav (ou .mp3) + .response.json; uma linha é adicionada em reports/CUSTOS.md
# 4) só se houver defeito claro (idioma ou sotaque, letra ininteligível, sem voz, estrutura errada):
python3 music/scripts/eleven_generate.py --confirm --tag v2 --seed 7
```
Depois de gerar:
1. Medir duração e BPM (detecção de batidas).
2. Transcrever com Whisper para checar o pt-BR.
3. Montar `music/compositions/timeline_final.json` a partir do áudio real.
4. Re-sincronizar a animação com o novo timeline.
5. Exportar o MP3 de escuta.

## Conta ElevenLabs (informada pelo proprietário)
- O painel mostra o plano pago de **€5/mês (Starter)**. O proprietário diz ter assinado um plano superior e ter **~150.000 créditos** disponíveis. São dados **informados pelo proprietário**; a API não os confirma porque a chave não tem `user_read`.
- Linha do **Starter** na tabela de direitos comerciais (Exhibit A, https://elevenlabs.io/music-terms):
  - "For Individual Use Only"
  - limite de geração de **17 min/mês** e de download de 30 min/mês
  - **Music Streaming Distribution: "Prohibited"**
  - Media Rights: "All online and offline commercial use permitted, except film, TV, radio, and Studio Games"
  - High-Quality Downloads: "No"
  - API Access: "Yes"
- Interpretação (não é parecer jurídico):
  - "Media Rights" (§4.8(d)) inclui "the right to synchronize Output in timed relation to audiovisual content", então **sincronizar a música num vídeo** cabe no uso comercial do Starter.
  - "Music Streaming Distribution" (§4.8(g)) é "making Output available on a music streaming platform", ou seja, **publicar a faixa de áudio** no Spotify, Apple Music ou YouTube Music. Isso o Starter **proíbe**; exige Creator ou superior.
  - Os termos não dizem explicitamente se um vídeo no YouTube conta como "TV". **Confirme com a ElevenLabs antes de monetizar**, e prefira o plano Creator se a faixa também for para plataformas de streaming de música.
- Com ~150k créditos, as 2 gerações autorizadas (~4.946 créditos) cabem com folga. **Mas, se o plano for mesmo Starter, o limite de 17 min/mês de geração vale.** Cada geração de 2:45 consome ~2,75 min desse limite.
