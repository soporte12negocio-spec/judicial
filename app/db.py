import sqlite3
import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any

DB_PATH = Path(__file__).resolve().parent.parent / "consultas.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()

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

# Inicializar tabla automáticamente
init_db()
