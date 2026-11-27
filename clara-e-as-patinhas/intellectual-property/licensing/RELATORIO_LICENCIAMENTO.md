# Relatório de licenciamento (v1, 2026-11-27)

Registro detalhado por ativo: `licensing/REGISTRO.md`. Aqui, o resumo por ferramenta. Nada aqui é parecer jurídico.

| Ferramenta / ativo | Uso | Licença / termos | O que permite | Atenção |
|---|---|---|---|---|
| **ElevenLabs Eleven Music** (`music_v2_5`) | todas as músicas e vozes | Termos de Música da ElevenLabs (Exhibit A, por plano) | No plano pago **Starter**: uso comercial online/offline e sincronização em audiovisual (vídeo do YouTube parece coberto) | **Distribuição em streaming de música (Spotify, YouTube Music, Apple Music) proibida no Starter** — exige Creator ou superior. "Film, TV, radio" excluídos no Starter; não está claro se o YouTube conta como TV → **confirmar com a ElevenLabs antes de monetizar**. Licença de uso ≠ titularidade exclusiva; obras geradas por IA têm proteção autoral incerta. Plano real da conta não verificável pela API (chave sem `user_read`). |
| **OpenAI Whisper** (`whisper-1`) | conferência de palavras e tempos | Termos da API OpenAI | uso das transcrições sem restrição relevante | — |
| **Demucs** (htdemucs, Meta, MIT) | separar voz/instrumental | MIT (código e pesos publicados para uso) | uso comercial | separação imperfeita (pode haver resíduo) |
| **Blender 4.0.2** | modelos, cenários, render | GPL-2.0-or-later | os renders pertencem ao usuário | — |
| **Fredoka** | logo e títulos | SIL OFL 1.1 | uso comercial, inclusive em logos | não vender a fonte sozinha |
| **RunPod** (GPU alugada) | render na nuvem (preparado) | Termos RunPod | aluguel de máquina; saídas são do usuário | **uso não autorizado ainda** nesta etapa (bloqueado pela checagem de permissão) |
| **Modelos open source de imagem→3D** (ex.: TRELLIS) | avaliação para personagens premium | verificar código **e** pesos | — | não usados ainda; ver `reports/PERSONAGENS_ROTA.md` |
| Personagens, cenários, coreografias | criação do projeto | originais | propriedade do proprietário | ver `../authorship/CONTRIBUICOES_HUMANAS.md` |

## Pendências antes de monetizar / distribuir
1. Confirmar o plano ElevenLabs da conta (Starter × Creator/Pro) e a cobertura para YouTube monetizado.
2. Se houver distribuição em plataformas de streaming de música: plano Creator ou superior.
3. Decidir o título/gancho por causa do risco "Patati Patatá" (relatório de originalidade).
