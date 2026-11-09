"""Parte 2.2 - Pasar la transcripción al LLM para que responda (flujo audio -> texto -> respuesta)."""
import json

from common import MODELO_TEXTO, OUT_DIR, get_client, guardar_json

SYSTEM = ("Eres TutorIA, un tutor académico de Bases de Datos y MySQL. Responde en español, de lo simple a "
          "lo complejo, en máximo 120 palabras. Si la pregunta no es de bases de datos, dilo brevemente.")

client = get_client()
ruta = OUT_DIR / "2_1_transcripciones.json"
if not ruta.exists():
    raise SystemExit("Primero ejecuten parte2_1_transcripcion.py")

salida = []
for a in json.loads(ruta.read_text(encoding="utf-8")):
    r = client.chat.completions.create(
        model=MODELO_TEXTO, temperature=0,
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": a["transcripcion"]}],
    )
    resp = (r.choices[0].message.content or "").strip()
    salida.append({"archivo": a["archivo"], "transcripcion": a["transcripcion"], "respuesta": resp})
    print(f"\n[{a['archivo']}] audio -> transcripción -> respuesta")
    print("  Transcripción:", a["transcripcion"])
    print("  Respuesta    :", resp)
guardar_json("2_2_respuestas.json", salida)
