# Escalabilidade e obstáculos técnicos

## O que dá para reaproveitar nos próximos episódios
- **Personagens** (`assets/characters/*.blend` e o código em `scripts/blender/cp_chars.py`): o design e a textura fixa da Ayra se regeneram iguais a cada build.
- **Ações reutilizáveis** em cada .blend: respirar, piscar, andar, correr, pulinho, giro, abanar a cauda, mexer a orelha, patinha, passinho para trás, sentar, bater palmas, acenar, cantar e as 5 expressões.
- **Biblioteca de movimento** `cp_motion.py`: as camadas se somam (balanço no tempo, palmas, pulos etc.).
- **Cenário** `cp_env.py`: o jardim inteiro em ~40 s de build.
- **Pipeline do episódio** `episode.py`:
  - lê um timeline JSON (seções, linhas e notas/sílabas);
  - a coreografia e as câmeras ficam numa função por cena;
  - o render é retomável em lotes (`scripts/render_driver.py`), com segmentos de 240 frames codificados e PNGs apagados para economizar disco.
- **Assinatura musical** (2 compassos) e **logos** prontos para vinheta.

Para um episódio novo é preciso:
1. letra e plano Eleven Music;
2. timeline;
3. reescrever `choreo()` e `plan_cameras()` para a nova história (horas de trabalho, não dias);
4. ~6 h de render nesta máquina.

## Custos de tempo por episódio (nesta máquina, sem GPU)
| Etapa | Tempo |
|---|---|
| Build da cena | ~40 s |
| Render a 720p/8 amostras/24 fps | ~5,3 s/frame, ≈6 h para 2:47 |
| Montagem e codificação (1080p + light) | ~8 min |

Com uma GPU dedicada, a mesma cena em EEVEE deve cair para menos de 1 s/frame (estimativa, não medida aqui), permitindo 1080p nativo e mais amostras.

## Obstáculos encontrados (e o que foi feito)
| Obstáculo | Solução / situação |
|---|---|
| Sem GPU | EEVEE por llvmpipe (EGL surfaceless) funciona em background. Escolhidos 720p, 8 amostras e LOD 0.6, com ampliação para 1080p |
| Blender do Ubuntu sem OpenImageDenoise | Cycles sem denoiser ficou inviável; usado EEVEE |
| Python do Blender (3.12) sem numpy | `apt install python3-numpy` |
| Cabelo por partículas no EEVEE/llvmpipe: fios escuros e comprimento errado | Trocado por *fur shells* com alpha-clip + deslocamento |
| `render()` frame a frame reinicializava o EEVEE (11 s/frame) | Render em modo animação com `use_overwrite=False` (retomável), ~5,3 s/frame |
| Timeout matando o Blender no meio da escrita de um PNG (frame corrompido) | Segmento refeito; o driver agora valida PNGs com PIL antes de codificar |
| Disco apertado (~3 GB) | Segmentos de 10 s codificados e PNGs apagados a cada lote; o .blend do episódio fica fora do git |
| **Geração Eleven Music negada pela camada de permissões da sessão** | **Não contornado.** Script e plano prontos; precisa de aprovação direta do usuário/proprietário |
| Fonte Fredoka: o GitHub não está acessível nesta sessão | Obtida pelo npm (`@fontsource/fredoka`, OFL) |
| A chave ElevenLabs não tem `user_read` | Plano e créditos não verificáveis pela API; registrado como "informado pelo proprietário" |
