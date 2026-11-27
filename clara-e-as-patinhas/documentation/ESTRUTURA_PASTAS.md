# Estrutura de pastas (Aditivo 03 §18) — adaptada por necessidade técnica

O layout pedido (`clara-kids-studios/…`) foi criado **dentro** de `clara-e-as-patinhas/clara-kids-studios/`. O diretório `clara-e-as-patinhas/` **não** foi renomeado nem movido porque outro processo renderiza "Cadê? Achou!" a partir dele e os scripts usam esses caminhos. Cada pasta do layout tem um README que aponta para os arquivos reais (mídia pesada fica fora do git).

Configuração de idiomas: `clara-kids-studios/config/languages.json` (en-US original; pt-BR e es-LATAM extras; fr, de, it, ja, ko, hi, ar, id, tr, zh planejados).

| Pasta do layout | Onde está |
|---|---|
| `shared-assets/characters/` | Assets canônicos dos 5 personagens → `assets/characters/canon/` (a congelar; ver Bíblia). Versão ep. 001: `assets/characters/<nome>/`. |
| `shared-assets/environments/` | Jardim Mágico → `rendering/ep001.blend`, `rendering/ep002.blend`, `scripts/blender/cp_env.py`, `ep2_scene.py`; doc `documentation/JARDIM_MAGICO.md`. |
| `shared-assets/rigs/` | Rigs → dentro dos .blend dos personagens (`scripts/blender/cp_chars.py`). |
| `shared-assets/animations/` | Biblioteca de ações → `scripts/blender/cp_motion.py`. |
| `shared-assets/choreography/` | `documentation/GUIA_COREOGRAFIAS.md`. |
| `shared-assets/branding/` | `assets/branding/` (logos PT); logo global Clara & Paws: pendente. |
| `shared-assets/sound-effects/` | Sem SFX externos até agora (latidos/miados vêm do Eleven Music dentro das faixas). |
| `episodes/episode-001/composition/` | Planos de composição → `music/compositions/pilot/` (chorus_*.json, full_pt/en/es.json, inpaint_*.json). |
| `episodes/episode-001/lyrics/` | `music/lyrics/pata-pata-patata.md` (PT) e `music/lyrics/pata-pata-patata_en_es.md` (EN/ES). |
| `episodes/episode-001/instrumental/` | `music/masters/pata_pata_patata_instrumental.{wav,mp3}` (Demucs da versão PT). |
| `episodes/episode-001/master-animation/` | Pendente (render só após aprovação das músicas). |
| `episodes/episode-001/timing-map/` | `music/compositions/pilot/timing_map.json`. |
| `episodes/episode-001/audio/en-US/` | `music/masters/pata_pata_patata_en_final.{wav,mp3}` (vozes EN sobre o instrumental comum). Alternativa: `pata_pata_patata_en_v1.wav` (mix original). |
| `episodes/episode-001/audio/pt-BR/` | `music/masters/pata_pata_patata_pt_final.{wav,mp3}`. |
| `episodes/episode-001/audio/es-LATAM/` | `music/masters/pata_pata_patata_es_final.{wav,mp3}` (vozes ES sobre o instrumental comum). Alternativa: `pata_pata_patata_es_v4.wav`. |
| `episodes/episode-001/vocals/` | Vozes isoladas (uso interno) → `music/stems/pata_pata_patata_{pt_final,en_v1,es_v4}/vocals.wav`. |
| `episodes/episode-001/thumbnails/` | Pendente (3 localizadas + 1 universal sem texto). |
| `episodes/episode-001/metadata/` | `metadata/pilot/` (en-US, pt-BR, es-LATAM). |
| `episodes/episode-001/quality-control/` | `music/analysis/pata/` (voz, palavras, alinhamento) e relatórios em `reports/`. |
| `episodes/episode-001/exports/` | Pendente (vídeo). |
| `global-channel/` | Identidade do canal global Clara & Paws (logo, banner, descrição) — pendente; ver `documentation/ADITIVO_03.md`. |
| `intellectual-property/` | → `intellectual-property/` na raiz do projeto. |
| `licensing/` | → `licensing/REGISTRO.md` e `intellectual-property/licensing/`. |
| `analytics/` | Vazio até haver dados reais do YouTube (Fase 3). |
| `reports/` | → `reports/`. |
