import time
from app.models import ResultadoEntidad, DetalleItem, ConsultaRequest

URL_OFICIAL_DATACREDITO = "https://www.midatacredito.com/"

async def consultar_datacredito(req: ConsultaRequest) -> ResultadoEntidad:
    t0 = time.time()
    doc = req.numero_documento

    if req.modo_demo:
        if req.perfil_demo == "alerta_penal":
            return ResultadoEntidad(
                entidad_id="datacredito",
                nombre_entidad="Datacrédito Experian Colombia",
                sigla="DATACRÉDITO",
                categoria="Historial Crediticio y Financiero",
                estado="alerta",
                semaforo="rojo",
                resumen="SCORE CREDITICIO DEFICIENTE (380/950). REGISTRA 2 REPORTES NEGATIVOS POR MORA CASTIGADA.",
                score_financiero=380,
                detalles=[
                    DetalleItem(
                        titulo="Reporte Negativo en Cartera Castigada (Mora > 120 días)",
                        descripcion="Tarjeta de Crédito Bancaria con saldo en mora vencido no cancelado. En proceso de cobro pre-jurídico/jurídico.",
                        radicado="OBL-BC-89210-TC",
                        fecha="2023-08-30",
                        despacho_o_entidad="Entidad Financiera / Central de Cobranzas",
                        estado_tramite="Reporte Negativo Vigente (Ley 1266 / Ley 2157)",
                        monto="Saldo en Mora: $8.450.000 COP"
                    ),
                    DetalleItem(
                        titulo="Obligación en Telecomunicaciones en Mora",
                        descripcion="Servicio de telefonía y datos pospago con reporte negativo por incumplimiento.",
                        radicado="TEL-CO-44192",
                        fecha="2023-05-14",
                        despacho_o_entidad="Operador Móvil Celular",
                        estado_tramite="Cartera en Mora Reportada",
                        monto="Saldo: $420.000 COP"
                    )
                ],
                url_oficial=URL_OFICIAL_DATACREDITO,
                instrucciones_oficiales="ALERTA CREDITICIA: El ciudadano se encuentra bloqueado para el otorgamiento de nuevos créditos en el sector financiero.",
                tiempo_respuesta_ms=370
            )
        elif req.perfil_demo == "proceso_civil_simit":
            return ResultadoEntidad(
                entidad_id="datacredito",
                nombre_entidad="Datacrédito Experian Colombia",
                sigla="DATACRÉDITO",
                categoria="Historial Crediticio y Financiero",
                estado="observacion",
                semaforo="amarillo",
                resumen="Score Crediticio Moderado (635/950). Sin reportes negativos graves, pero con utilización de cupos superior al 70%.",
                score_financiero=635,
                detalles=[
                    DetalleItem(
                        titulo="Tarjeta de Crédito Activa al Día",
                        descripcion="Cupo aprobado: $15.000.000 COP. Saldo diferido: $11.200.000 COP. Pagos al día con hábito puntual.",
                        radicado="TC-0041-9921",
                        fecha="2024-01-10",
                        despacho_o_entidad="Banco Comercial",
                        estado_tramite="Al día / Endeudamiento medio",
                        monto="Cupo Utilizado: 74%"
                    ),
                    DetalleItem(
                        titulo="Crédito de Libre Inversión",
                        descripcion="Plazo 48 meses. Cuotas pagadas: 24/48. Sin moras activas en los últimos 12 meses.",
                        radicado="CRE-LIV-8819",
                        fecha="2022-10-01",
                        despacho_o_entidad="Entidad Bancaria",
                        estado_tramite="Vigente al día"
                    )
                ],
                url_oficial=URL_OFICIAL_DATACREDITO,
                instrucciones_oficiales="Capacidad de endeudamiento en rango medio. Sin reportes negativos vigentes.",
                tiempo_respuesta_ms=330
            )
        else: # limpio
            return ResultadoEntidad(
                entidad_id="datacredito",
                nombre_entidad="Datacrédito Experian Colombia",
                sigla="DATACRÉDITO",
                categoria="Historial Crediticio y Financiero",
                estado="limpio",
                semaforo="verde",
                resumen="SCORE CREDITICIO EXCELENTE (820/950). Hábito de pago impecable del 100% en todas sus obligaciones.",
                score_financiero=820,
                detalles=[
                    DetalleItem(
                        titulo="Calificación de Hábito de Pago: AAA (Excelente)",
                        descripcion="4 obligaciones bancarias activas sin un solo día de mora en los últimos 36 meses.",
                        despacho_o_entidad="Datacrédito Experian",
                        estado_tramite="Al día (100% puntualidad)"
                    ),
                    DetalleItem(
                        titulo="Crédito de Vivienda y Tarjeta Oro",
                        descripcion="Excelente comportamiento crediticio. Perfil calificado como de bajo riesgo crediticio.",
                        despacho_o_entidad="Sector Financiero Nacional",
                        estado_tramite="Paz y salvo permanente"
                    )
                ],
                url_oficial=URL_OFICIAL_DATACREDITO,
                instrucciones_oficiales="Sujeto con perfil de crédito preferencial para préstamos y arrendamientos.",
                tiempo_respuesta_ms=310
            )

    elapsed = int((time.time() - t0) * 1000)
    return ResultadoEntidad(
        entidad_id="datacredito",
        nombre_entidad="Datacrédito Experian Colombia",
        sigla="DATACRÉDITO",
        categoria="Historial Crediticio y Financiero",
        estado="limpio",
        semaforo="verde",
        resumen=f"Consulta de historial crediticio preparada para el documento {req.tipo_documento} {doc} bajo la Ley 1266 de 2008.",
        score_financiero=750,
        detalles=[
            DetalleItem(
                titulo="Consulta de Reportes y Score Financiero",
                descripcion=f"Acceso a la plataforma MiDatacrédito para verificar el historial crediticio consolidado de {req.tipo_documento} {doc}.",
                despacho_o_entidad="Experian Colombia",
                estado_tramite="Listo para verificación del titular"
            )
        ],
        url_oficial=URL_OFICIAL_DATACREDITO,
        instrucciones_oficiales="En MiDatacrédito puede consultar de manera gratuita su reporte oficial una vez al mes por mandato de ley.",
        tiempo_respuesta_ms=elapsed
    )
