# Taller: Entrada multimodal y audio (TutorIA - MySQL)

Dominio: tutor académico de Bases de Datos / MySQL. Modelos en Groq: `qwen/qwen3.8-27b` (visión),
`whisper-large-v3-turbo` (audio) y `openai/gpt-oss-120b` (respuesta de texto).

## Preparación
```bash
cd taller_multimodal
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                  # y editar GROQ_API_KEY
```
**Variable de entorno requerida:** `GROQ_API_KEY` (en `.env`, ignorado por git).
Opcionales: `MODELO_VISION`, `MODELO_AUDIO`, `MODELO_TEXTO`.

## Parte 1 - Visión
Las 5 imágenes están en `imagenes/` (se regeneran con `python generar_imagenes.py`; los valores reales están en `ground_truth.json`).
| Punto | Comando |
|---|---|
| 1.1 Pregunta sobre una imagen | `python parte1_1_pregunta.py` |
| 1.2 Extracción estructurada + % de aciertos | `python parte1_2_extraccion.py` |
| 1.3 Varias imágenes en una solicitud | `python parte1_3_varias_imagenes.py` |
| 1.4 Error provocado | `python parte1_4_error.py [modelo_sin_vision\|cuatro_imagenes\|imagen_grande]` |

## Parte 2 - Audio
Los audios van en `audios/` (guiones en `audios/GUIONES.md`, metadatos en `audios/audios.json`).
| Punto | Comando |
|---|---|
| 2.1 Transcripción desde archivo | `python parte2_1_transcripcion.py` |
| 2.2 Respuesta a partir de la transcripción | `python parte2_2_respuesta.py` (requiere haber corrido 2.1) |

Las salidas quedan en `resultados/` (JSON/CSV). Ninguna clave de API se guarda en el código.
