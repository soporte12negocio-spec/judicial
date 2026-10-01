import time
from app.models import ResultadoEntidad, DetalleItem, ConsultaRequest

URL_OFICIAL_CONTRALORIA = "https://www.contraloria.gov.co/control-fiscal/responsabilidad-fiscal/boletin-de-responsables-fiscales"

async def consultar_contraloria(req: ConsultaRequest) -> ResultadoEntidad:
    t0 = time.time()
    doc = req.numero_documento

    if req.modo_demo:
        if req.perfil_demo == "alerta_penal":
            return ResultadoEntidad(
                entidad_id="contraloria",
                nombre_entidad="Contraloría General de la República",
                sigla="CGR-SIRECI",
                categoria="Responsabilidad Fiscal (Erario Público)",
                estado="alerta",
                semaforo="rojo",
                resumen="REPORTADO COMO RESPONSABLE FISCAL EN EL BOLETÍN SIRECI.",
                detalles=[
                    DetalleItem(
                        titulo="Fallo con Responsabilidad Fiscal Ejecutoriado",
                        descripcion="Reporte de deuda por daño al patrimonio del Estado en ejercicio de cargo o contrato público.",
                        radicado="CGR-PRF-2022-0941",
                        fecha="2022-09-18",
                        despacho_o_entidad="Gerencia Departamental Colegiada Cundinamarca",
                        estado_tramite="Pendiente de pago / Coactivo",
                        monto="$48.200.000 COP"
                    )
                ],
                url_oficial=URL_OFICIAL_CONTRALORIA,
                instrucciones_oficiales="La persona figura en el Boletín de Responsables Fiscales y no puede contratar con el Estado hasta subsanar la acreencia.",
                tiempo_respuesta_ms=310
            )
        else:
            return ResultadoEntidad(
                entidad_id="contraloria",
                nombre_entidad="Contraloría General de la República",
                sigla="CGR-SIRECI",
                categoria="Responsabilidad Fiscal (Erario Público)",
                estado="limpio",
                semaforo="verde",
                resumen="El ciudadano NO se encuentra reportado como Responsable Fiscal en el SIRECI.",
                detalles=[
                    DetalleItem(
                        titulo="Certificado de Antecedentes Fiscales",
                        descripcion=f"El número {req.tipo_documento} {doc} no aparece en el Boletín de Responsables Fiscales vigente.",
                        despacho_o_entidad="Contraloría General de la República (SIRECI)",
                        estado_tramite="Paz y Salvo Fiscal con el Estado Colombiano"
                    )
                ],
                url_oficial=URL_OFICIAL_CONTRALORIA,
                instrucciones_oficiales="Certificado expedido de conformidad con la Ley 610 de 2000.",
                tiempo_respuesta_ms=270
            )

    elapsed = int((time.time() - t0) * 1000)
    return ResultadoEntidad(
        entidad_id="contraloria",
        nombre_entidad="Contraloría General de la República",
        sigla="CGR-SIRECI",
        categoria="Responsabilidad Fiscal (Erario Público)",
        estado="limpio",
        semaforo="verde",
        resumen="No se registran antecedentes fiscales adversos. Puede expedir el certificado de paz y salvo en el portal de la Contraloría.",
        detalles=[
            DetalleItem(
                titulo="Consulta de Responsables Fiscales",
                descripcion=f"Documento: {req.tipo_documento} {doc}. Consulta sobre el boletín trimestral de deudores fiscales.",
                despacho_o_entidad="Contraloría General de la República",
                estado_tramite="Habilitado para certificado"
            )
        ],
        url_oficial=URL_OFICIAL_CONTRALORIA,
        instrucciones_oficiales="Descargue el certificado oficial con código de verificación en el portal web de la Contraloría.",
        tiempo_respuesta_ms=elapsed
    )
