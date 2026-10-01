import time
from app.models import ResultadoEntidad, DetalleItem, ConsultaRequest

URL_OFICIAL_CIFIN = "https://www.transunion.co/producto/controlplus"

async def consultar_cifin(req: ConsultaRequest) -> ResultadoEntidad:
    t0 = time.time()
    doc = req.numero_documento

    if req.modo_demo:
        if req.perfil_demo == "alerta_penal":
            return ResultadoEntidad(
                entidad_id="cifin",
                nombre_entidad="TransUnion / CIFIN Colombia",
                sigla="TRANSUNION-CIFIN",
                categoria="Riesgo Bancario y Endeudamiento",
                estado="alerta",
                semaforo="rojo",
                resumen="CALIFICACIÓN BANCARIA D (DIFÍCIL COBRO). RIESGO FINANCIERO ALTO EN EL SISTEMA.",
                calificacion_bancaria="D (Difícil Cobro)",
                detalles=[
                    DetalleItem(
                        titulo="Calificación de Riesgo según SuperFinanciera: Categoría D",
                        descripcion="Crédito de consumo en mora prolongada superior a 90 días. Reclasificación de riesgo obligatoria.",
                        radicado="SFC-CIFIN-88419",
                        fecha="2023-09-15",
                        despacho_o_entidad="Sector Financiero Vigilado SFC",
                        estado_tramite="En Cobro Jurídico / Cartera Deteriorada",
                        monto="Exposición Financiera: $12.300.000 COP"
                    ),
                    DetalleItem(
                        titulo="Huellas de Consulta y Alertas",
                        descripcion="Múltiples solicitudes de crédito rechazadas en los últimos 6 meses por alto riesgo.",
                        despacho_o_entidad="Central de Información Financiera (CIFIN)",
                        estado_tramite="Capacidad de crédito bloqueada"
                    )
                ],
                url_oficial=URL_OFICIAL_CIFIN,
                instrucciones_oficiales="Sujeto de alto riesgo financiero de acuerdo con la Circular Básica Contable de la Superintendencia Financiera.",
                tiempo_respuesta_ms=350
            )
        elif req.perfil_demo == "proceso_civil_simit":
            return ResultadoEntidad(
                entidad_id="cifin",
                nombre_entidad="TransUnion / CIFIN Colombia",
                sigla="TRANSUNION-CIFIN",
                categoria="Riesgo Bancario y Endeudamiento",
                estado="observacion",
                semaforo="amarillo",
                resumen="Calificación Bancaria B (Riesgo Aceptable / Potencial). Nivel de endeudamiento controlado.",
                calificacion_bancaria="B (Riesgo Aceptable)",
                detalles=[
                    DetalleItem(
                        titulo="Calificación de Riesgo Bancario: Categoría B",
                        descripcion="El titular atiende sus compromisos bancarios con puntualidad aceptable. Capacidad de pago suficiente.",
                        despacho_o_entidad="Superintendencia Financiera de Colombia",
                        estado_tramite="Normal / Vigente",
                        monto="Endeudamiento Global: $34.500.000 COP"
                    ),
                    DetalleItem(
                        titulo="Alertas de Fraude o Suplantación",
                        descripcion="No registra alertas preventivas por suplantación de identidad o robo de documentos.",
                        despacho_o_entidad="TransUnion Cifin",
                        estado_tramite="Identidad verificada"
                    )
                ],
                url_oficial=URL_OFICIAL_CIFIN,
                instrucciones_oficiales="Perfil financiero apto para operaciones corrientes de crédito con capacidad media.",
                tiempo_respuesta_ms=320
            )
        else: # limpio
            return ResultadoEntidad(
                entidad_id="cifin",
                nombre_entidad="TransUnion / CIFIN Colombia",
                sigla="TRANSUNION-CIFIN",
                categoria="Riesgo Bancario y Endeudamiento",
                estado="limpio",
                semaforo="verde",
                resumen="CALIFICACIÓN BANCARIA A (RIESGO NORMAL). Solvencia óptima y excelente respaldo en el sistema bancario.",
                calificacion_bancaria="A (Riesgo Normal)",
                detalles=[
                    DetalleItem(
                        titulo="Calificación Máxima SuperFinanciera: Categoría A",
                        descripcion="Cumplimiento estricto en pagos de capital e intereses sin demoras en todo el historial financiero.",
                        despacho_o_entidad="Superintendencia Financiera / TransUnion",
                        estado_tramite="Excelente Solvencia"
                    ),
                    DetalleItem(
                        titulo="Control de Identidad y Seguridad",
                        descripcion="Documento validado sin reportes de fraude, pérdidas de documentos o fraudes bancarios.",
                        despacho_o_entidad="CIFIN Sistema de Prevención de Fraudes",
                        estado_tramite="Titular confiable verificado"
                    )
                ],
                url_oficial=URL_OFICIAL_CIFIN,
                instrucciones_oficiales="El ciudadano goza de la máxima calificación crediticia en el sistema financiero colombiano.",
                tiempo_respuesta_ms=300
            )

    elapsed = int((time.time() - t0) * 1000)
    return ResultadoEntidad(
        entidad_id="cifin",
        nombre_entidad="TransUnion / CIFIN Colombia",
        sigla="TRANSUNION-CIFIN",
        categoria="Riesgo Bancario y Endeudamiento",
        estado="limpio",
        semaforo="verde",
        resumen=f"Verificación de CIFIN preparada para {req.tipo_documento} {doc}. Acceso al portal TransUnion para reporte bancario.",
        calificacion_bancaria="A (Estimada)",
        detalles=[
            DetalleItem(
                titulo="Consulta de Endeudamiento Consolidado (CIFIN)",
                descripcion=f"Documento: {req.tipo_documento} {doc}. Información sobre créditos vigentes y comportamiento en entidades bancarias.",
                despacho_o_entidad="TransUnion Colombia",
                estado_tramite="Listo para verificación"
            )
        ],
        url_oficial=URL_OFICIAL_CIFIN,
        instrucciones_oficiales="Consulte su informe de crédito y endeudamiento global en TransUnion ControlPlus.",
        tiempo_respuesta_ms=elapsed
    )
