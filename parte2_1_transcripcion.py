"""Parte 2.1 - Transcripción desde archivo con Whisper (Groq).

Lee audios/audios.json (archivo, hablante, condición, lo que se dijo) y transcribe cada audio.
"""
import json

from common import AUDIO_DIR, MODELO_AUDIO, get_client, guardar_json

client = get_client()
meta = json.loads((AUDIO_DIR / "audios.json").read_text(encoding="utf-8"))
salida = []
for a in meta:
    ruta = AUDIO_DIR / a["archivo"]
    if not ruta.exists():
        print(f"[!] Falta el archivo {ruta.name}; grábenlo y colóquenlo en audios/")
        continue
    with open(ruta, "rb") as f:
        r = client.audio.transcriptions.create(
            file=(ruta.name, f.read()), model=MODELO_AUDIO,
            language="es", response_format="verbose_json", temperature=0,
        )
    fila = {**a, "duracion_s": round(getattr(r, "duration", 0) or 0, 1), "transcripcion": r.text.strip()}
    salida.append(fila)
    print(f"\n[{a['archivo']}] {a['hablante']} · {a['condicion']} · {fila['duracion_s']} s")
    print("  Dicho        :", a["texto_dicho"])
    print("  Transcripción:", fila["transcripcion"])
guardar_json("2_1_transcripciones.json", salida)
