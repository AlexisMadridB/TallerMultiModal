"""Genera las 5 imágenes sintéticas del dominio (MySQL) con valores reales conocidos.

Son capturas simuladas de un cliente MySQL, como las que usaría un estudiante de
Bases de Datos. Como las dibujamos nosotros, el 'valor real' de cada campo se conoce
con certeza (ver ground_truth.json). Si prefieren usar capturas propias de MySQL
Workbench, reemplacen los PNG y actualicen ground_truth.json.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent / "imagenes"
OUT.mkdir(exist_ok=True)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def terminal(nombre, lineas, ancho=1000):
    f = font(MONO, 22)
    alto = 40 + 32 * len(lineas)
    img = Image.new("RGB", (ancho, alto), (30, 30, 36))
    d = ImageDraw.Draw(img)
    y = 20
    for ln in lineas:
        color = (255, 120, 120) if ln.startswith("ERROR") else (220, 220, 220)
        if ln.startswith("mysql>") or ln.startswith("    ->"):
            color = (140, 220, 140)
        d.text((24, y), ln, font=f, fill=color)
        y += 32
    img.save(OUT / nombre)


# 1. SELECT con WHERE y resultado de 4 filas
terminal("img1_select_where.png", [
    "mysql> SELECT nombre, correo FROM estudiantes WHERE semestre = 5;",
    "+----------------+---------------------------+",
    "| nombre         | correo                    |",
    "+----------------+---------------------------+",
    "| Laura Gomez    | laura.gomez@unikl.edu     |",
    "| Mateo Rojas    | mateo.rojas@unikl.edu     |",
    "| Sofia Herrera  | sofia.herrera@unikl.edu   |",
    "| Daniel Pardo   | daniel.pardo@unikl.edu    |",
    "+----------------+---------------------------+",
    "4 rows in set (0.00 sec)",
])

# 2. CREATE TABLE con 5 columnas
terminal("img2_create_table.png", [
    "mysql> CREATE TABLE cursos (",
    "    ->   id_curso INT PRIMARY KEY AUTO_INCREMENT,",
    "    ->   nombre VARCHAR(80) NOT NULL,",
    "    ->   creditos TINYINT NOT NULL,",
    "    ->   semestre TINYINT,",
    "    ->   docente VARCHAR(60)",
    "    -> ) ENGINE=InnoDB;",
    "Query OK, 0 rows affected (0.03 sec)",
])

# 3. JOIN + GROUP BY con 3 filas de resultado
terminal("img3_join_group.png", [
    "mysql> SELECT c.nombre, COUNT(*) AS total",
    "    -> FROM cursos c JOIN inscripciones i ON c.id_curso = i.id_curso",
    "    -> GROUP BY c.nombre;",
    "+------------------------+-------+",
    "| nombre                 | total |",
    "+------------------------+-------+",
    "| Bases de Datos         |    32 |",
    "| Programacion Web       |    27 |",
    "| Estructuras de Datos   |    19 |",
    "+------------------------+-------+",
    "3 rows in set (0.01 sec)",
])

# 4. Diagrama entidad-relación
W, H = 1000, 460
img = Image.new("RGB", (W, H), (250, 250, 252))
d = ImageDraw.Draw(img)
fb, fs = font(SANSB, 22), font(SANS, 19)


def caja(x, titulo, campos):
    d.rectangle([x, 60, x + 260, 60 + 40 + 34 * len(campos)], outline=(40, 60, 120), width=3, fill=(235, 240, 255))
    d.rectangle([x, 60, x + 260, 100], fill=(40, 60, 120))
    d.text((x + 12, 68), titulo, font=fb, fill="white")
    for i, c in enumerate(campos):
        d.text((x + 12, 110 + 34 * i), c, font=fs, fill=(20, 20, 20))


caja(30, "estudiantes", ["PK id_estudiante", "nombre", "correo", "semestre"])
caja(370, "inscripciones", ["PK id_inscripcion", "FK id_estudiante", "FK id_curso", "nota"])
caja(710, "cursos", ["PK id_curso", "nombre", "creditos", "semestre", "docente"])
d.line([290, 180, 370, 180], fill=(40, 60, 120), width=3)
d.line([630, 180, 710, 180], fill=(40, 60, 120), width=3)
d.text((300, 150), "1", font=fb, fill=(180, 30, 30)); d.text((345, 150), "N", font=fb, fill=(180, 30, 30))
d.text((640, 150), "N", font=fb, fill=(180, 30, 30)); d.text((685, 150), "1", font=fb, fill=(180, 30, 30))
d.text((30, 400), "Modelo de la base 'universidad' (relaciones uno a muchos)", font=fs, fill=(80, 80, 80))
img.save(OUT / "img4_diagrama_er.png")

# 5. Error de sintaxis 1064
terminal("img5_error_sintaxis.png", [
    "mysql> SELCT * FROM estudiantes;",
    "ERROR 1064 (42000): You have an error in your SQL syntax; check the manual",
    "that corresponds to your MySQL server version for the right syntax to use",
    "near 'SELCT * FROM estudiantes' at line 1",
], ancho=1250)
print("Imagenes generadas en", OUT)
