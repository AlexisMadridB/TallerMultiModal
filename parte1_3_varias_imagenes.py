"""Parte 1.3 - Varias imágenes relacionadas en una sola solicitud (máx. 3 con qwen)."""
from common import IMG_DIR, MODELO_VISION, get_client, guardar_json, limpiar_respuesta, parte_imagen

IMAGENES = ["img4_diagrama_er.png", "img2_create_table.png", "img3_join_group.png"]
PREGUNTA = ("Las tres imágenes pertenecen a la misma base de datos. La 1ª es el diagrama entidad-relación, "
            "la 2ª la creación de la tabla cursos y la 3ª una consulta. Indica si la tabla cursos coincide con "
            "el diagrama, si el JOIN de la consulta es coherente con las relaciones del modelo y resume en "
            "3 frases qué calcula la consulta.")

client = get_client()
contenido = [{"type": "text", "text": PREGUNTA}] + [parte_imagen(IMG_DIR / n) for n in IMAGENES]
resp = client.chat.completions.create(
    model=MODELO_VISION, messages=[{"role": "user", "content": contenido}], temperature=0)
texto = limpiar_respuesta(resp.choices[0].message.content)

print("IMÁGENES:", IMAGENES)
print("PREGUNTA:", PREGUNTA)
print("RESPUESTA:\n", texto)
guardar_json("1_3_varias.json", {"imagenes": IMAGENES, "pregunta": PREGUNTA, "respuesta": texto})
