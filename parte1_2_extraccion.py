"""Parte 1.2 - Extracción estructurada (JSON) + validación + comparación con valor real."""
import csv
import json

from jsonschema import Draft202012Validator

from common import (BASE, IMG_DIR, MODELO_VISION, OUT_DIR, get_client, guardar_json,
                    limpiar_respuesta, parte_imagen)

# --- Esquema (6 campos) ------------------------------------------------------
ESQUEMA = {
    "type": "object",
    "properties": {
        "sentencia": {"type": "string", "description": "Tipo de sentencia SQL (SELECT, CREATE TABLE, INSERT...)"},
        "tabla_principal": {"type": "string", "description": "Tabla principal sobre la que opera la sentencia"},
        "num_columnas": {"type": "integer", "description": "Columnas devueltas (SELECT) o definidas (CREATE TABLE)"},
        "clausula_where": {"type": ["string", "null"], "description": "Condición del WHERE sin la palabra WHERE; null si no hay"},
        "num_filas_resultado": {"type": ["integer", "null"], "description": "Filas devueltas ('N rows in set'); null si no es consulta"},
        "tiempo_s": {"type": "number", "description": "Tiempo de ejecución en segundos que muestra el cliente"},
    },
    "required": ["sentencia", "tabla_principal", "num_columnas", "clausula_where",
                 "num_filas_resultado", "tiempo_s"],
    "additionalProperties": False,
}
VALIDADOR = Draft202012Validator(ESQUEMA)
CAMPOS = list(ESQUEMA["properties"])
VERDAD = json.loads((BASE / "ground_truth.json").read_text(encoding="utf-8"))

PROMPT = (
    "Eres un extractor de datos. La imagen es una captura de un cliente MySQL. "
    "Extrae los campos descritos y responde SOLO con un objeto JSON válido, sin texto adicional.\n"
    "Campos:\n" + "\n".join(f"- {k} ({v['type']}): {v['description']}" for k, v in ESQUEMA["properties"].items())
    + "\nUsa null cuando el dato no aparezca en la imagen."
)


def validar(texto: str):
    """Devuelve (datos | None, [errores]). Nunca lanza excepción."""
    try:
        datos = json.loads(texto)
    except json.JSONDecodeError as e:
        return None, [f"JSON mal formado: {e}"]
    errores = [f"{'/'.join(map(str, e.path)) or '(raíz)'}: {e.message}" for e in VALIDADOR.iter_errors(datos)]
    return (datos if not errores else None), errores


def normalizar(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).lower().strip().rstrip(";")
    if s.startswith("where "):
        s = s[6:]
    return "".join(ch for ch in s if ch not in " `'\"")


def main():
    client = get_client()
    filas, detalle = [], {}
    for nombre, real in VERDAD.items():
        resp = client.chat.completions.create(
            model=MODELO_VISION,
            messages=[{"role": "user", "content": [{"type": "text", "text": PROMPT}, parte_imagen(IMG_DIR / nombre)]}],
            temperature=0,
            response_format={"type": "json_object"},
        )
        bruto = limpiar_respuesta(resp.choices[0].message.content)
        datos, errores = validar(bruto)
        detalle[nombre] = {"respuesta_cruda": bruto, "valido": datos is not None, "errores_esquema": errores}
        print(f"\n== {nombre} ==\n{bruto}")
        if datos is None:
            print("  [!] El JSON NO cumple el esquema:", *errores, sep="\n   - ")
        for campo in CAMPOS:
            extraido = datos.get(campo) if datos else "(sin JSON válido)"
            ok = datos is not None and normalizar(extraido) == normalizar(real[campo])
            filas.append([nombre, campo, real[campo], extraido, "Sí" if ok else "No"])

    aciertos = sum(f[4] == "Sí" for f in filas)
    total = len(filas)
    print(f"\nPorcentaje de aciertos: {aciertos} de {total} campos = {100 * aciertos / total:.1f} %")
    print("(La comparación es automática; revísenla a mano antes de reportarla.)")

    with open(OUT_DIR / "1_2_aciertos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["imagen", "campo", "valor_real", "valor_extraido", "correcto"])
        w.writerows(filas)
    guardar_json("1_2_detalle.json", {"detalle": detalle, "aciertos": aciertos, "total": total})


if __name__ == "__main__":
    main()
