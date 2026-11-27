# Guia de identidade musical — Clara e as Patinhas / Clara & Paws (v1, 2026-11-27)

## Princípios (Aditivo 01, §13–§19)
- Simplicidade extrema na letra, qualidade na composição, voz, produção e animação.
- Repetição é a arte central: regra **80/20** (80% familiar, 20% novidade em cada música).
- 2 a 3 min; intro ≤ 3 s; gancho imediato; refrão 5 a 8 vezes; frases de 2 a 6 palavras; melodia de 3 a 5 notas principais; intervalos pequenos; ritmo constante; pausas para interação; final natural.
- Sempre cantada (nunca narração substituindo o canto). Voz: ver `VOICE_PROFILE.md`.

## Estilos da casa (aprovados)
| Estilo | Status | Uso |
|---|---|---|
| Pop infantil acústico (ukulele, xilofone, palmas) | aprovado (ep. 001, ep. 002) | dança, brincadeira |
| **Forró pé-de-serra / xote suave** | **aprovado pelo proprietário em 2026-11-27** | estilo do piloto "Pata Pata Patatá"; pode ser usado no catálogo |
| Canção de ninar | previsto (10% do catálogo) | rotina de sono |

**Xote da casa:** 85–100 BPM, dinâmica suave, **sanfona** como instrumento principal e portadora do gancho, triângulo constante, zabumba bem leve, baixo leve. As cores dos personagens entram só como pequenos preenchimentos. Nunca citar artistas reais ou músicas existentes nos prompts; evitar melodias de forró conhecidas (melodia sempre original).

## Instrumento de cada personagem (§19)
| Personagem | Instrumento | Uso no arranjo |
|---|---|---|
| Clara | ukulele | batida que entra no verso dela e no final |
| Ayra | tambor suave | preenchimentos no verso dela |
| Pandora | xilofone | preenchimentos no verso dela |
| Toby | trompete suave (surdina) | preenchimentos no verso dele |
| Milo | pizzicato de violino | preenchimentos no verso dele |

## Assinatura sonora (§17) — proposta
- **Proposta atual:** o gancho do refrão do piloto, "Pata, pata, patatá!" (PT/ES) / "Paw paw, paw paw, paw hooray!" (EN), cantado em 4 notas (Ré–Mi–Dó–Fá, Dó maior) e dobrado pela sanfona.
- **Conflito encontrado (ver `../originality-reports/RELATORIO_ORIGINALIDADE.md`):** "Pata, pata, patatá" soa muito próximo de **"Patati Patatá"** (marca infantil brasileira conhecida) e de **"Pata Pata"** (Miriam Makeba). **Não consolidar** como assinatura antes da decisão do proprietário.
- **Alternativas propostas** (mesma métrica de 7 sílabas, funcionam nos 3 idiomas com pequenas adaptações):
  1. "Pa-ta-pá, pa-ta-pá, hey!" — EN "Pat-a-pat, pat-a-pat, hey!" — ES "¡Pa-ta-pá, pa-ta-pá, hey!"
  2. "Patinha, patinha, olé!" — EN "Little paws, little paws, olé!" — ES "¡Patita, patita, olé!"
  3. Assinatura só instrumental: 5 notas de sanfona + "au-au" + "miau" (sem palavra; funciona em qualquer idioma e não tem risco de título).
- Uso: integrada às músicas (na intro de ≤ 3 s ou no final), sem vinheta institucional longa.

## Onomatopeias por idioma (§16 + Aditivo 02/03)
| Som | pt-BR | en-US | es-LATAM |
|---|---|---|---|
| cachorro | au, au | woof, woof | guau, guau |
| gato | miau | meow | miau |
| pato | quá, quá | quack, quack | cuac, cuac |
| vaca | muuu | moo | muuu |
| pintinho | piu, piu | peep, peep | pío, pío |
| sapo | croac | ribbit | croac |
| palmas | pá, pá / palma | clap, clap | palmas / plas, plas |
Cada som tem uma ação visual clara (`../../documentation/GUIA_COREOGRAFIAS.md`).

## Produção (padrão técnico)
- Master: −14 LUFS integrado, pico ≤ −1,5 dBTP, 48 kHz / 24 bits estéreo (`scripts/ep2/master.sh`). Mesma loudness em todos os idiomas.
- Instrumental: separado com Demucs (htdemucs, MIT) da versão PT; serve de base comum para EN e ES.
- Todas as versões de idioma têm **exatamente a mesma duração** e o mesmo mapa de tempos (`music/compositions/pilot/timing_map.json`).
