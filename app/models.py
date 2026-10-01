from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class ConsultaRequest(BaseModel):
    tipo_documento: str = Field(default="CC", description="Tipo de documento (CC, CE, NIT, PAS)")
    numero_documento: str = Field(..., description="Número del documento de identidad")
    primer_nombre: str = Field(..., description="Primer nombre del ciudadano")
    segundo_nombre: Optional[str] = Field(default="", description="Segundo nombre (opcional)")
    primer_apellido: str = Field(..., description="Primer apellido")
    segundo_apellido: Optional[str] = Field(default="", description="Segundo apellido (opcional)")
    fecha_expedicion: Optional[str] = Field(default="", description="Fecha de expedición (YYYY-MM-DD)")
    autorizacion_financiera: bool = Field(default=True, description="Autorización expresa para consultar centrales de riesgo (Ley 1266 de 2008)")
    modo_demo: bool = Field(default=False, description="Activa perfiles de demostración")
    perfil_demo: Optional[str] = Field(default=None, description="Perfil de prueba: 'limpio', 'proceso_civil_simit', 'alerta_penal'")

    @property
    def nombre_completo(self) -> str:
        partes = [self.primer_nombre, self.segundo_nombre, self.primer_apellido, self.segundo_apellido]
        return " ".join(p.strip() for p in partes if p and p.strip()).upper()

class DetalleItem(BaseModel):
    titulo: str
    descripcion: str
    radicado: Optional[str] = None
    fecha: Optional[str] = None
    despacho_o_entidad: Optional[str] = None
    estado_tramite: Optional[str] = None
    monto: Optional[str] = None

class ResultadoEntidad(BaseModel):
    entidad_id: str
    nombre_entidad: str
    sigla: str
    categoria: str # Penal, Judicial, Disciplinario, Fiscal, Convivencia, Tránsito, Familia, Inmuebles, Financiero
    estado: str    # "limpio", "alerta", "observacion", "enlace_oficial", "error"
    semaforo: str  # "verde", "amarillo", "rojo", "gris"
    resumen: str
    detalles: List[DetalleItem] = []
    url_oficial: str
    instrucciones_oficiales: str
    tiempo_respuesta_ms: int = 0
    score_financiero: Optional[int] = None
    calificacion_bancaria: Optional[str] = None
    total_propiedades: Optional[int] = None
    fecha_consulta: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

class InformeUnificado(BaseModel):
    id_informe: str = Field(default_factory=lambda: f"VCO-{uuid.uuid4().hex[:8].upper()}")
    fecha_emision: str = Field(default_factory=lambda: datetime.now().strftime("%d/%m/%Y %I:%M %p"))
    tipo_documento: str
    numero_documento: str
    nombre_completo: str
    semaforo_global: str # "verde", "amarillo", "rojo"
    score_riesgo: int    # 0 a 100
    resumen_ejecutivo: str
    total_entidades: int = 11
    total_alertas: int = 0
    total_observaciones: int = 0
    resultados: List[ResultadoEntidad] = []
    es_simulado: bool = False
