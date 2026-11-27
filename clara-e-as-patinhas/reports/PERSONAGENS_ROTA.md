# Personagens avançados com IA open source — teste real (2026-11-27)

Pedido do proprietário: "eu gostaria de ter personagens avançados" → **"Testar IA primeiro"** (GPU RunPod autorizada; teto US$ 3 para personagens).

## O que foi feito (tudo real, arquivos conferidos)
1. **Imagens de referência** dos 5 personagens a partir da Bíblia: **SDXL base 1.0** (licença CreativeML Open RAIL++-M: uso comercial permitido com restrições de uso). O FLUX.1-schnell (Apache-2.0) foi tentado primeiro, mas o repositório exige login/aceite no Hugging Face (conta do proprietário) — não usado.
   - 4 variações por personagem; escolhidas: Clara s7 (macacão recolorido para amarelo e camiseta para branco por pós-processamento, porque o SDXL insistiu em jeans azul), Ayra2 s7, Pandora s6, Toby s8, Milo s44.
2. **Imagem → 3D:** **TRELLIS-image-large** (Microsoft; código e pesos MIT). **O nvdiffrast não foi instalado de propósito** (licença NVIDIA não comercial); a malha foi exportada com cores por vértice em vez do "bake" de textura que depende dele.
3. **Limpeza no Blender:** rotação, escala, decimação de 400–900 mil para 60 mil faces, remoção de fragmentos soltos.
4. **Turntables** (EEVEE na CPU) dos 5 e **teste de rig** no Milo (esqueleto quadrúpede simples + pesos automáticos, 4 poses).

Arquivos: `reports/chars_ai_test/` (folhas de contato) e no scratchpad `chars_*_turntable.mp4`, `chars_refs_sheet*.jpg`, `chars_milo_rig_test.jpg`, malhas `*_trellis.ply` (fora do git).

## Resultado honesto
| Personagem | Aparência (turntable) | Problemas |
|---|---|---|
| **Milo** | **muito bom**: proporções fofas, listras, olhos verdes, coleira roxa | bigodes viraram fragmentos pretos espetados (precisa apagar e refazer bigodes como curvas) |
| **Toby** | bom: Yorkshire reconhecível, bandana verde | dorso ficou preto (deveria ser cinza-aço) — recolorir |
| **Pandora** | boa silhueta branca e fofa | sem laço rosa visível; a "pluma" do rabo virou uma bola com manchas rosadas; pelagem é volume liso, não pelo |
| **Ayra** | Border Collie reconhecível, olhos azuis, bandana | **sentada** (a referência estava sentada); padrão merle aproximado e **não controlado** (não dá para "travar" manchas idênticas sem pintar à mão); textura borrada |
| **Clara** | frente boa e fofa | **costas inventadas** (macacão ficou preto atrás); cabelo em bloco; sem rosto animável |

**Nota estimada (aparência estática):** 7,5–8/10 — bem acima dos modelos procedurais atuais (≈ 6,9) em carisma e forma.

## Onde fica aquém (o mais importante)
- **Topologia para animação:** a malha é um "molde" único (triângulos irregulares, sem laços de borda em articulações). O teste de rig no Milo funcionou para **inclinar a cabeça** e **balançar o rabo**, mas a **pata não levantou** direito (pesos automáticos ruins nas pernas) — exigiria retopologia/pesos à mão.
- **Animação facial e canto:** não há pálpebras, boca separada nem olhos móveis — **a Clara não consegue cantar/abrir a boca** sem trabalho manual (shape keys esculpidas ou cabeça refeita). Isso é crítico para videoclipe.
- **Pelo:** as cores estão "pintadas" na superfície; não há pelagem 3D. Dá para adicionar pelo de partículas por cima, mas é trabalho manual.
- **Consistência e marcas fixas:** as manchas da Ayra e as listras do Milo vêm da IA e não são editáveis com precisão; congelar o canon exige pintar/limpar uma textura definitiva à mão.
- **Licenças:** TRELLIS MIT (ok); SDXL OpenRAIL++ (ok com restrições de uso); Hunyuan3D-2 **evitado** (licença exclui UE/Reino Unido/Coreia do Sul). As saídas de modelos generativos têm proteção autoral incerta (ver `intellectual-property/authorship/`).

## Recomendação
**Caminho híbrido (melhor custo × qualidade):** usar estas malhas de IA como **base/modelo de escultura** e contratar um artista 3D para **retopologia + rig + rosto (boca/olhos para canto) + pelo + texturas finais com marcações travadas** dos 5 personagens. A IA economiza a fase de modelagem inicial; o artista entrega personagens animáveis de verdade (estimativa de mercado, não cotação: ~US$ 150–600 por personagem por esse escopo, contra US$ 300–1.500 do zero). Sem isso, as malhas de IA servem para **planos estáticos, miniaturas e turntables**, mas não para o videoclipe cantado.

Alternativa sem artista: manter os personagens procedurais (animáveis, boca funciona) e só melhorar materiais/pelo — fica abaixo do nível "avançado" pedido.

**Canon:** nada foi congelado. Congelar só após a escolha do proprietário.

## Custo do teste
RunPod (RTX 4090, Secure Cloud US$ 0,89/h, Community estava sem disponibilidade): **0,30 h ≈ US$ 0,27**. Pod **encerrado**. Saldo RunPod após o teste: ~US$ 9,58 (inclui o pod de render do ep. 2, que não é deste teste).
