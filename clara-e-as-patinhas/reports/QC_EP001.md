# QC — Episódio 001 "A Dança das Patinhas" (piloto)

Avaliado em 2026-11-27 a partir dos arquivos reais:
- `output/danca_das_patinhas_1080p.mp4`
- `output/danca_das_patinhas_light.mp4`
- `output/teste_3d_light.mp4`
- as sheets e os logos

> A cópia do brief que recebi **não trazia os pesos exatos da rubrica do proprietário**. Usei a rubrica abaixo, que segue as prioridades do brief (música/canto, qualidade 3D premium, sincronia, consistência, cenário, técnica, entregáveis). Se os pesos originais forem outros, basta recalcular com as mesmas notas.

| Critério | Peso | Nota (0–10) | Evidência |
|---|---|---|---|
| Música e voz cantada (pt-BR natural, gancho, refrão) | 25% | **3** | Melodia, estrutura e assinatura originais prontas, com gancho nos 0–4 s. **Não há voz**: o vídeo usa o instrumental-guia General MIDI. O Eleven Music foi bloqueado pelas permissões |
| Qualidade visual dos personagens (premium, fofos, anatomia) | 20% | **5** | Fofos, legíveis e com paleta correta. Formas primitivas, rig rígido, pelo aproximado com shells. Bem abaixo de "premium cinematográfico" |
| Animação, coreografia e sincronia com a música | 15% | **5** | Coreografia ligada às deixas da letra, palmas no tempo, contagem da Tifa no tempo e câmeras trocando nas seções. Movimento procedural, sem atuação nem pesos. Lip-sync básico pela melodia-guia |
| Consistência dos personagens | 10% | **8** | Merle da Ayra fixo, Pandora branca, Tifa castanho/cinza-aço, Clara com cabelo e macacão iguais em todos os frames verificados |
| Cenário e iluminação | 10% | **6,5** | Todos os elementos do brief estão presentes: jardim, colinas, árvores, flores, borboletas, lago, ponte, caminho de pedras, balanço, brinquedos, casinhas e casa com varanda/janelas/vasos. Luz suave e agradável. Sem GI nem reflexos no lago |
| Integridade técnica (duração, áudio, MP4, pés no chão, deformações) | 10% | **9** | 167,4 s; 0 erros de decodificação; pico de áudio -1,3 dBFS (sem clipping); 1080p; light de 53 MB. Pés no chão OK. Nenhuma deformação de malha (rig rígido). 1 segmento com frame corrompido foi refeito |
| Entregáveis e marca (logo, thumb, sheets, metadados, docs) | 10% | **8** | Logos em 5 versões, paleta, thumbnail 1280×720, sheets de 4 personagens, grupo, storyboard, metadados e relatórios. A guia de identidade é simples |
| **Total ponderado** | 100% | **5,7 / 10** | |

## Checklist de QC
- [x] Duração 2:47 (dentro de 2:30–3:00)
- [x] Resolução final 1920×1080 (ampliada de 720p, como está documentado)
- [x] Light ≤ 60 MB (53 MB)
- [x] Áudio sem clipping
- [x] MP4 íntegro (ffmpeg sem erros)
- [x] Personagens consistentes em todas as cenas amostradas (34 frames, 1 a cada ~5 s)
- [x] Logo na abertura (0:00–0:04) e no encerramento (2:39–fim), sem cobrir os personagens
- [ ] **Voz cantada**: bloqueada (Eleven Music)
- [ ] Lip-sync por palavra (Whisper): depende da voz
- [ ] Qualidade "premium cinematográfica": não atingida nesta infraestrutura (veja `reports/TESTE_3D.md`)
