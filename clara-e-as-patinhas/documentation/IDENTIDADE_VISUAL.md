# Guia de identidade visual — Clara e as Patinhas

**Slogan:** "Pequenas patinhas, grandes aventuras!"
**Tom:** alegre, acolhedor, simples e seguro para crianças de 1 a 5 anos. Cores vivas, formas redondas, sem nada pontiagudo nem assustador.

## Paleta (`assets/branding/paleta.png`)
| Cor | HEX | Uso |
|---|---|---|
| Amarelo-sol | `#FFC81A` | Macacão da Clara, palavra "Clara" no logo, títulos |
| Azul-céu | `#5CB0F5` | "e as Patinhas", céu, bandana da Ayra (variação `#2E7AF2`) |
| Verde natural | `#6CB848` | Gramado, árvores, bandana da Tifa |
| Rosa suave | `#FA8CB4` | Laço da Pandora, tênis, patinhas decorativas |
| Branco | `#FFFFFF` | Contornos internos, camiseta, telhado das casinhas |
| Madeira quente | `#B27542` | Ponte, balanço, varanda |
| Terracota | `#D66B42` | Telhado da casa, vasos |
| Castanho (contorno) | `#5C331A` | Contorno do logo, cabelo da Clara |

## Tipografia
- **Fredoka** 700/600 (SIL OFL 1.1, `assets/branding/fonts/`): logo, títulos e thumbnails. Arredondada e fácil de ler.
- Contorno grosso castanho `#5C331A` (títulos) ou branco (subtítulos) e sombra suave.

## Logos (`assets/branding/`)
| Arquivo | Uso |
|---|---|
| `logo_color.png` | Versão principal sobre cartão branco com borda amarela |
| `logo_transparent.png` | Wordmark empilhado com slogan, PNG transparente (abertura e encerramento dos vídeos) |
| `logo_horizontal.png` | Selo de patinha + nome em uma linha (thumbnails, banner) |
| `logo_compact.png` | Círculo azul com patinha e nome (marca-d'água, avatar alternativo) |
| `youtube_icon.png` | 800×800 com o rosto da Clara (funciona recortado em círculo) |

Regras:
- Manter área livre de pelo menos a altura do "C" em volta do logo.
- Não distorcer nem mudar as cores do logo.
- Sobre fundos movimentados, usar a versão com contorno.

## Personagens
As model sheets ficam em `assets/characters/<nome>/sheet_*.png`, as proporções em `assets/characters/proporcoes.png` e o grupo em `assets/characters/grupo.png`.

Elementos de identidade que **nunca mudam**:
- **Clara:** macacão amarelo, camiseta branca, cabelo castanho na altura dos ombros com franja lateral e presilha de flor amarela.
- **Ayra:** padrão merle fixo na textura, olhos azul-claros, bandana azul.
- **Pandora:** branca e fofa, laço rosa.
- **Tifa:** castanho-dourado com dorso cinza-aço, bandana verde, a menor.

## Som da marca
Assinatura de 2 compassos (Lá-Fá#-Lá-Si | Ré — Lá | Si-Dó#-Ré — Lá), em xilofone e glockenspiel com dois latidinhos. Abre e fecha todos os episódios (`music/compositions/estrutura.json` → `assinatura_marca`).
