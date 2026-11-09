"""Utilidades compartidas por los scripts del taller."""
import base64
import json
import mimetypes
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

BASE = Path(__file__).parent
IMG_DIR = BASE / "imagenes"
AUDIO_DIR = BASE / "audios"
OUT_DIR = BASE / "resultados"
OUT_DIR.mkdir(exist_ok=True)

load_dotenv(BASE / ".env")

MODELO_VISION = os.getenv("MODELO_VISION", "qwen/qwen3.8-27b")
MODELO_AUDIO = os.getenv("MODELO_AUDIO", "whisper-large-v3-turbo")
MODELO_TEXTO = os.getenv("MODELO_TEXTO", "openai/gpt-oss-120b")


def get_client() -> Groq:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        sys.exit("Falta GROQ_API_KEY. Copia .env.example a .env y agrega tu clave.")
    return Groq(api_key=key)


def imagen_a_data_url(ruta: Path, mime: str | None = None) -> str:
    """Lee una imagen local y la devuelve como data URL base64."""
    mime = mime or mimetypes.guess_type(str(ruta))[0] or "image/png"
    b64 = base64.b64encode(Path(ruta).read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def parte_imagen(ruta: Path, mime: str | None = None) -> dict:
    return {"type": "image_url", "image_url": {"url": imagen_a_data_url(ruta, mime)}}


def limpiar_respuesta(texto: str) -> str:
    """Quita bloques <think>...</think> y cercas ```json ... ``` si el modelo los agrega."""
    texto = re.sub(r"<think>.*?</think>", "", texto or "", flags=re.DOTALL).strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", texto, flags=re.DOTALL)
    return (m.group(1) if m else texto).strip()

def limpiar_think(texto: str) -> str:
    return re.sub(r"<think>.*?</think>", "", texto or "", flags=re.DOTALL).strip()


def guardar_json(nombre: str, datos) -> Path:
    ruta = OUT_DIR / nombre
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    return ruta
