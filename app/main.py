import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models import ConsultaRequest, InformeUnificado
from app.services.engine import ejecutar_consulta_unificada
from app.db import init_db, obtener_historial, obtener_informe_por_id, obtener_base_ciudadanos, TXT_PATH

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="VerificaCO - Sistema Unificado de Antecedentes y Procesos Judiciales",
    description="Plataforma de consulta unificada para antecedentes penales, judiciales, disciplinarios, fiscales, comparendos, Sisbén, ADRES y subsidios en Colombia.",
    version="1.2.0"
)

# Inicializar Base de Datos SQLite
init_db()

# Directorios estáticos y plantillas
templates_dir = BASE_DIR / "templates"
static_dir = BASE_DIR / "static"

os.makedirs(templates_dir, exist_ok=True)
os.makedirs(static_dir / "css", exist_ok=True)
os.makedirs(static_dir / "js", exist_ok=True)

templates = Jinja2Templates(directory=str(templates_dir))
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/consultar", response_model=InformeUnificado)
async def api_consultar(req: ConsultaRequest):
    try:
        informe = await ejecutar_consulta_unificada(req)
        return informe
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la consulta: {str(e)}")

@app.get("/api/base-ciudadanos")
async def api_base_ciudadanos():
    """Retorna la lista de ciudadanos guardados (cédula, nombre, apellido, fecha)."""
    return obtener_base_ciudadanos()

@app.get("/api/descargar-base-txt")
async def api_descargar_base_txt():
    """Permite descargar el archivo base_ciudadanos.txt con cédula, nombre y apellido."""
    if not TXT_PATH.exists():
        with open(TXT_PATH, "w", encoding="utf-8") as f:
            f.write("CEDULA,NOMBRE,APELLIDO,FECHA_REGISTRO\n")
    return FileResponse(
        path=str(TXT_PATH),
        filename="base_ciudadanos.txt",
        media_type="text/plain"
    )

@app.get("/api/historial")
async def api_historial():
    return obtener_historial(limit=15)

@app.get("/api/informe/{id_informe}")
async def api_obtener_informe(id_informe: str):
    informe = obtener_informe_por_id(id_informe)
    if not informe:
        raise HTTPException(status_code=404, detail="Informe no encontrado")
    return informe

@app.get("/api/perfiles-demo")
async def api_perfiles_demo():
    return [
        {
            "id": "limpio",
            "titulo": "👤 Favorable (Sin Pendientes + Inmuebles Libres + Score AAA)",
            "descripcion": "Sin antecedentes, 2 inmuebles libres de embargos en SNR, Score Datacrédito 820 y CIFIN A.",
            "tipo_doc": "CC",
            "numero_doc": "1018452930",
            "primer_nombre": "JUAN",
            "segundo_nombre": "CARLOS",
            "primer_apellido": "PÉREZ",
            "segundo_apellido": "GÓMEZ",
            "fecha_exp": "2015-04-12"
        },
        {
            "id": "proceso_civil_simit",
            "titulo": "⚠️ Observación (Proceso Civil + SIMIT + Accidente Leve + Hipoteca)",
            "descripcion": "Demanda civil, 1 comparendo, choque simple en RUNT, hipoteca bancaria en SNR y Score 635.",
            "tipo_doc": "CC",
            "numero_doc": "80234519",
            "primer_nombre": "CARLOS",
            "segundo_nombre": "ALBERTO",
            "primer_apellido": "GÓMEZ",
            "segundo_apellido": "RODRÍGUEZ",
            "fecha_exp": "2008-09-24"
        },
        {
            "id": "alerta_penal",
            "titulo": "🚨 Alerta Crítica (Penal + REDAM + Embargo Inmueble + Mora Datacrédito)",
            "descripcion": "Requerimiento judicial, reporte REDAM, inmueble embargado en SNR, Datacrédito 380 y CIFIN D.",
            "tipo_doc": "CC",
            "numero_doc": "79812455",
            "primer_nombre": "JORGE",
            "segundo_nombre": "ENRIQUE",
            "primer_apellido": "MARTÍNEZ",
            "segundo_apellido": "TORRES",
            "fecha_exp": "2001-11-05"
        }
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
