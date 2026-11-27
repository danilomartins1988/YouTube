# Registro de autoria e contribuições humanas (v1, 2026-11-27)

Princípio (Aditivo 01 §31): não atribuir autoria humana fictícia a material gerado por IA. Proteção autoral de obras geradas só por IA é juridicamente incerta; licença comercial de uso não equivale a titularidade exclusiva.

## Contribuições humanas efetivas (proprietário)
| Data | Contribuição | Onde |
|---|---|---|
| 2026-11 | Conceito da marca "Clara e as Patinhas", slogan, elenco, personalidades e aparência dos personagens (brief mestre) | `documentation/BRIEF.md` (histórico) |
| 2026-11 | Nomes Ayra, Pandora (e Tifa, depois Toby) | idem |
| 2026-11 | Letra original de "A Dança das Patinhas" (ajustes de métrica pelo assistente) | `music/lyrics/a-danca-das-patinhas.md` |
| 2026-11-27 | Aditivo 01 completo: posicionamento, 5 personagens, Milo, filosofia musical, **letra experimental de "Pata Pata Patatá"**, lista de 30 temas | `documentation/ADITIVO_01.md` |
| 2026-11-27 | Decisões criativas: estilo **forró/xote**, Toby macho, nomes cantados, voz fiel a "Cadê? Achou!", aprovação de músicas | `documentation/BRIEF.md` |
| 2026-11-27 | Aditivos 02 e 03: estratégia multilíngue e canal global | `documentation/ADITIVO_02.md`, `ADITIVO_03.md` |

## Contribuições do assistente de IA (Claude, sob direção do proprietário)
Adaptação de métrica das letras; letras "Cadê? Achou!" (original do assistente sob briefing do proprietário) e adaptações EN/ES de "Pata Pata Patatá"; planos de composição (prompts) para o Eleven Music; código dos modelos 3D procedurais, cenários, coreografia, câmera, render e verificação; documentação.

## Conteúdo gerado por IA de terceiros
| Item | Gerado por | Registro |
|---|---|---|
| Gravações (melodias, arranjos, vozes) de todas as músicas | ElevenLabs Eleven Music | song_ids e planos em `music/compositions/` e `music/masters/*.response.json` |
| Separação voz/instrumental | Demucs (ferramenta, não criativa) | `music/stems/` |

**Leitura honesta:** as melodias e as performances vocais são geradas pela IA da ElevenLabs a partir dos planos; a contribuição humana criativa está na letra (proprietário), nas decisões de estilo, na seleção/aprovação das tomadas e na direção. Os personagens 3D atuais são gerados por código escrito pelo assistente a partir das especificações do proprietário.
