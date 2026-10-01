import time
from app.models import ResultadoEntidad, DetalleItem, ConsultaRequest

URL_OFICIAL_SNR = "https://www.supernotariado.gov.co/servicios-al-ciudadano/consulta-de-indice-de-propietarios/"

async def consultar_snr_inmuebles(req: ConsultaRequest) -> ResultadoEntidad:
    t0 = time.time()
    doc = req.numero_documento
    nombre = req.nombre_completo

    if req.modo_demo:
        if req.perfil_demo == "alerta_penal":
            return ResultadoEntidad(
                entidad_id="snr_inmuebles",
                nombre_entidad="Superintendencia de Notariado y Registro",
                sigla="SNR-VUR",
                categoria="Bienes Inmuebles e Instrumentos Públicos",
                estado="alerta",
                semaforo="rojo",
                resumen="REGISTRA 1 INMUEBLE CON MEDIDA CAUTELAR DE EMBARGO JUDICIAL REGISTRADA.",
                total_propiedades=1,
                detalles=[
                    DetalleItem(
                        titulo="Inmueble con Medida Cautelar de Embargo Ejecutivo",
                        descripcion="Apartamento en Conjunto Residencial. Anotación No. 5: EMBARGO EJECUTIVO ordenado por juzgado civil.",
                        radicado="Matrícula Inmobiliaria 50C-1849201",
                        fecha="2023-09-05",
                        despacho_o_entidad="ORIP Bogotá Zona Centro / Juzgado 15 Civil Municipal",
                        estado_tramite="EMBARGADO / Fuera del comercio",
                        monto="Avalúo Catastral: $240.000.000 COP"
                    )
                ],
                url_oficial=URL_OFICIAL_SNR,
                instrucciones_oficiales="ALERTA: El predio tiene inscripción de embargo judicial que impide su venta o traspaso en notaría.",
                tiempo_respuesta_ms=360
            )
        elif req.perfil_demo == "proceso_civil_simit":
            return ResultadoEntidad(
                entidad_id="snr_inmuebles",
                nombre_entidad="Superintendencia de Notariado y Registro",
                sigla="SNR-VUR",
                categoria="Bienes Inmuebles e Instrumentos Públicos",
                estado="observacion",
                semaforo="amarillo",
                resumen="Registra 1 inmueble a su nombre con Hipoteca Bancaria de primer grado vigente (Crédito de vivienda).",
                total_propiedades=1,
                detalles=[
                    DetalleItem(
                        titulo="Predio Urbano con Gravamen Hipotecario Normal",
                        descripcion="Casa de Habitación de 2 niveles. Anotación No. 3: Hipoteca Abierta de Primer Grado a favor de entidad bancaria.",
                        radicado="Matrícula Inmobiliaria 001-928174",
                        fecha="2020-06-18",
                        despacho_o_entidad="ORIP Medellín Zona Sur (Envigado)",
                        estado_tramite="Activo / Gravamen hipotecario al día",
                        monto="Crédito Hipotecario: $180.000.000 COP"
                    )
                ],
                url_oficial=URL_OFICIAL_SNR,
                instrucciones_oficiales="Inmueble sujeto a hipoteca financiera por crédito hipotecario tradicional.",
                tiempo_respuesta_ms=320
            )
        else: # limpio
            return ResultadoEntidad(
                entidad_id="snr_inmuebles",
                nombre_entidad="Superintendencia de Notariado y Registro",
                sigla="SNR-VUR",
                categoria="Bienes Inmuebles e Instrumentos Públicos",
                estado="limpio",
                semaforo="verde",
                resumen=f"Registra 2 inmuebles a su nombre en Instrumentos Públicos. LIBRES de embargos y gravámenes.",
                total_propiedades=2,
                detalles=[
                    DetalleItem(
                        titulo="Inmueble Principal: Apartamento Residencial (100% Propiedad)",
                        descripcion="Apartamento ubicado en Bogotá D.C. Sin limitaciones al dominio, sin pleitos ni embargos inscritos.",
                        radicado="Matrícula Inmobiliaria 50N-2049182",
                        fecha="2018-11-22",
                        despacho_o_entidad="ORIP Bogotá Zona Norte",
                        estado_tramite="Paz y Salvo Registral / Plena Propiedad",
                        monto="Avalúo Comercial Est.: $380.000.000 COP"
                    ),
                    DetalleItem(
                        titulo="Inmueble Accesorio: Garaje Privado Cubierto",
                        descripcion="Parqueadero en servidumbre de uso exclusivo. Libre de pleitos judiciales o medidas cautelares.",
                        radicado="Matrícula Inmobiliaria 50N-2049183",
                        fecha="2018-11-22",
                        despacho_o_entidad="ORIP Bogotá Zona Norte",
                        estado_tramite="Pleno Dominio Registrado"
                    )
                ],
                url_oficial=URL_OFICIAL_SNR,
                instrucciones_oficiales="Consulta concordante con el Índice Nacional de Propietarios de la SNR.",
                tiempo_respuesta_ms=310
            )

    elapsed = int((time.time() - t0) * 1000)
    return ResultadoEntidad(
        entidad_id="snr_inmuebles",
        nombre_entidad="Superintendencia de Notariado y Registro",
        sigla="SNR-VUR",
        categoria="Bienes Inmuebles e Instrumentos Públicos",
        estado="limpio",
        semaforo="verde",
        resumen=f"Verificación preparada para el titular {nombre} ({req.tipo_documento} {doc}). Enlace al VUR listo para expedir el Certificado de Tradición.",
        total_propiedades=0,
        detalles=[
            DetalleItem(
                titulo="Consulta por Índice de Propietarios (SNR / VUR)",
                descripcion=f"Identificación: {req.tipo_documento} {doc}. Permite identificar todos los folios de matrícula inmobiliaria vinculados a nivel nacional.",
                despacho_o_entidad="Superintendencia de Notariado y Registro",
                estado_tramite="Listo para verificación en ventanilla VUR"
            )
        ],
        url_oficial=URL_OFICIAL_SNR,
        instrucciones_oficiales="En el portal oficial de la SNR puede solicitar el Certificado de Tradición y Libertad en PDF con PIN de verificación.",
        tiempo_respuesta_ms=elapsed
    )
