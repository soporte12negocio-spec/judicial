import sqlite3
import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "consultas.db"
TXT_PATH = BASE_DIR / "base_ciudadanos.txt"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Tabla de Informes completos generados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial_consultas (
            id_informe TEXT PRIMARY KEY,
            fecha_emision TEXT,
            tipo_documento TEXT,
            numero_documento TEXT,
            nombre_completo TEXT,
            semaforo_global TEXT,
            score_riesgo INTEGER,
            resumen_ejecutivo TEXT,
            datos_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Base de datos de ciudadanos consultados (Cédula, Nombre, Apellido)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS base_ciudadanos (
            cedula TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

    # Inicializar archivo TXT con cabecera si no existe
    if not TXT_PATH.exists():
        with open(TXT_PATH, "w", encoding="utf-8") as f:
            f.write("CEDULA,NOMBRE,APELLIDO,FECHA_REGISTRO\n")

def guardar_ciudadano_base(cedula: str, nombre: str, apellido: str):
    """Guarda cédula, nombre y apellido en SQLite y en el archivo TXT."""
    cedula = str(cedula).strip()
    nombre = str(nombre).strip().upper()
    apellido = str(apellido).strip().upper()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Guardar en SQLite (UPSERT)
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO base_ciudadanos (cedula, nombre, apellido, fecha_registro)
            VALUES (?, ?, ?, ?)
        """, (cedula, nombre, apellido, now_str))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error guardando ciudadano en BD: {e}")

    # Guardar / Anexar en TXT
    try:
        linea = f"{cedula},{nombre},{apellido},{now_str}\n"
        with open(TXT_PATH, "a", encoding="utf-8") as f:
            f.write(linea)
    except Exception as e:
        print(f"Error guardando ciudadano en TXT: {e}")

def obtener_base_ciudadanos() -> List[Dict[str, Any]]:
    """Obtiene el listado consolidado de cédula, nombre y apellido."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cedula, nombre, apellido, fecha_registro
        FROM base_ciudadanos
        ORDER BY fecha_registro DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def guardar_informe(informe_dict: Dict[str, Any]):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO historial_consultas 
        (id_informe, fecha_emision, tipo_documento, numero_documento, nombre_completo, semaforo_global, score_riesgo, resumen_ejecutivo, datos_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        informe_dict["id_informe"],
        informe_dict["fecha_emision"],
        informe_dict["tipo_documento"],
        informe_dict["numero_documento"],
        informe_dict["nombre_completo"],
        informe_dict["semaforo_global"],
        informe_dict["score_riesgo"],
        informe_dict["resumen_ejecutivo"],
        json.dumps(informe_dict, ensure_ascii=False)
    ))
    conn.commit()
    conn.close()

def obtener_historial(limit: int = 15) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_informe, fecha_emision, tipo_documento, numero_documento, nombre_completo, semaforo_global, score_riesgo, resumen_ejecutivo
        FROM historial_consultas
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def obtener_informe_por_id(id_informe: str) -> Optional[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT datos_json FROM historial_consultas WHERE id_informe = ?
    """, (id_informe,))
    row = cursor.fetchone()
    conn.close()
    if row and row["datos_json"]:
        return json.loads(row["datos_json"])
    return None

# Inicializar BD y archivo TXT automáticamente al importar
init_db()
