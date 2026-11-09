"""Parte 1.1 - Pregunta sobre una imagen local (base64)."""
from common import IMG_DIR, MODELO_VISION, get_client, guardar_json, limpiar_think, parte_imagen

IMAGEN = IMG_DIR / "img5_error_sintaxis.png"
PREGUNTA = ("Esta captura es de un cliente MySQL. ¿Qué error muestra, cuál es su causa "
            "y cómo se corrige la sentencia?")

client = get_client()
resp = client.chat.completions.create(
    model=MODELO_VISION,
    messages=[
        {"role": "system", "content": (
            "Eres un experto en MySQL. Analiza la imagen y responde en máximo 4 líneas, "
            "sin encabezados, sin emojis y sin repetir lo que ya se ve en la imagen. "
            "Formato: primero el error y su causa en una frase, luego la sentencia corregida con explicacion"
            "en un bloque de código."
        )},
        {"role": "user", "content": [
            {"type": "text", "text": PREGUNTA},
            parte_imagen(IMAGEN),
        ]},
    ],
    temperature=0,
    max_tokens=512,
)
texto = limpiar_think(resp.choices[0].message.content)

print("IMAGEN  :", IMAGEN.name)
print("PREGUNTA:", PREGUNTA)
print("RESPUESTA:\n", texto)
print("TOKENS  :", resp.usage.total_tokens if resp.usage else "n/d")
guardar_json("1_1_pregunta.json", {"imagen": IMAGEN.name, "pregunta": PREGUNTA, "respuesta": texto})
