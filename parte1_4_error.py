"""Parte 1.4 - Error provocado a propósito: enviar 4 imágenes en una sola solicitud."""
from common import IMG_DIR, MODELO_VISION, get_client, guardar_json, parte_imagen

client = get_client()
PREG = "¿Qué dice esta imagen?"

imagenes = [parte_imagen(IMG_DIR / f"img{i}_{n}.png") for i, n in
            [(1, "select_where"), (2, "create_table"), (3, "join_group"), (5, "error_sintaxis")]]

print("### Caso: cuatro_imagenes")
try:
    r = client.chat.completions.create(
        model=MODELO_VISION,
        messages=[{"role": "user", "content": [{"type": "text", "text": PREG}] + imagenes}],
        max_tokens=200,
    )
    msg = "SIN ERROR (la API aceptó la solicitud): " + (r.choices[0].message.content or "")[:200]
except Exception as e:  # mostramos el error tal cual lo devuelve la API
    msg = f"{type(e).__name__}: {e}"

print(msg)
guardar_json("1_4_errores.json", {"cuatro_imagenes": msg})