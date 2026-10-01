import asyncio
from datetime import datetime
from typing import List
from app.models import ConsultaRequest, ResultadoEntidad, InformeUnificado
from app.services.rama_judicial import consultar_rama_judicial
from app.services.policia_nacional import consultar_policia_nacional
from app.services.procuraduria import consultar_procuraduria
from app.services.contraloria import consultar_contraloria
from app.services.rnmc_convivencia import consultar_rnmc
from app.services.simit import consultar_simit
from app.services.redam import consultar_redam
from app.services.runt_accidentes import consultar_runt_accidentes
from app.services.snr_inmuebles import consultar_snr_inmuebles
from app.services.datacredito import consultar_datacredito
from app.services.cifin import consultar_cifin
from app.services.sisben import consultar_sisben
from app.services.adres_eps import consultar_adres_eps
from app.services.subsidios_dps import consultar_subsidios_dps
from app.db import guardar_informe, guardar_ciudadano_base

async def ejecutar_consulta_unificada(req: ConsultaRequest) -> InformeUnificado:
    # 1. Guardar automáticamente en la base de datos y archivo TXT (Cédula, Nombre, Apellido)
    try:
        guardar_ciudadano_base(
            cedula=req.numero_documento,
            nombre=req.primer_nombre,
            apellido=req.primer_apellido
        )
    except Exception as e:
        print(f"Aviso guardando en base de ciudadanos: {e}")

    # 2. Ejecución paralela concurrente de las 14 entidades y bases de datos oficiales
    tasks = [
        consultar_policia_nacional(req),
        consultar_rama_judicial(req),
        consultar_procuraduria(req),
        consultar_contraloria(req),
        consultar_redam(req),
        consultar_simit(req),
        consultar_rnmc(req),
        consultar_runt_accidentes(req),
        consultar_snr_inmuebles(req),
        consultar_datacredito(req),
        consultar_cifin(req),
        consultar_sisben(req),
        consultar_adres_eps(req),
        consultar_subsidios_dps(req)
    ]

    resultados_raw = await asyncio.gather(*tasks, return_exceptions=True)
    resultados: List[ResultadoEntidad] = []

    for r in resultados_raw:
        if isinstance(r, ResultadoEntidad):
            resultados.append(r)
        else:
            resultados.append(ResultadoEntidad(
                entidad_id="desconocido",
                nombre_entidad="Entidad en Proceso",
                sigla="ERR",
                categoria="General",
                estado="error",
                semaforo="gris",
                resumen=f"Error durante la consulta: {str(r)}",
                detalles=[],
                url_oficial="#",
                instrucciones_oficiales="Reintente la consulta individual.",
                tiempo_respuesta_ms=0
            ))

    # Cálculo ponderado del score de riesgo y semáforo global
    score = 0
    total_alertas = 0
    total_observaciones = 0

    for r in resultados:
        if r.semaforo == "rojo":
            total_alertas += 1
            if r.entidad_id in ["policia", "procuraduria"]:
                score += 35
            elif r.entidad_id in ["simit"]:
                score += 25  # Multas en cobro coactivo
            elif r.entidad_id == "rama_judicial":
                score += 25
            elif r.entidad_id in ["datacredito", "cifin"]:
                score += 20
            elif r.entidad_id in ["contraloria", "redam", "snr_inmuebles"]:
                score += 18
            else:
                score += 15
        elif r.semaforo == "amarillo":
            total_observaciones += 1
            if r.entidad_id == "rama_judicial":
                score += 10
            elif r.entidad_id in ["datacredito", "cifin"]:
                score += 8
            elif r.entidad_id in ["simit", "rnmc", "runt_accidentes"]:
                score += 6
            elif r.entidad_id == "snr_inmuebles":
                score += 3
            else:
                score += 2

    score = min(max(score, 0), 100)

    # Determinar semáforo global y dictamen
    if score >= 30 or total_alertas > 0:
        semaforo_global = "rojo"
        resumen_ejecutivo = (
            f"ALERTA ALTA: Se detectaron {total_alertas} novedad(es) crítica(s) en antecedentes legales, comparendos coactivos, "
            f"patrimoniales o crediticios (Índice de riesgo: {score}/100). Se recomienda auditar a fondo los mandamientos de pago, "
            f"procesos o reportes antes de cualquier vinculación o contrato."
        )
    elif score >= 10 or total_observaciones > 0:
        semaforo_global = "amarillo"
        resumen_ejecutivo = (
            f"OBSERVACIÓN MODERADA: El ciudadano no presenta antecedentes penales ni disciplinarios graves, pero registra "
            f"{total_observaciones} asunto(s) en observación (procesos civiles o tutelas ordinarias, comparendos de tránsito, "
            f"hipotecas bancarias o endeudamiento crediticio medio). Índice de riesgo: {score}/100."
        )
    else:
        semaforo_global = "verde"
        resumen_ejecutivo = (
            f"FAVORABLE / SIN PENDIENTES: El ciudadano presenta un récord óptimo en las 14 bases de datos consultadas: "
            f"sin antecedentes penales ni disciplinarios, paz y salvo de tránsito, afiliación a salud activa y solvencia financiera. "
            f"Índice de riesgo: {score}/100 (Bajo)."
        )

    informe = InformeUnificado(
        tipo_documento=req.tipo_documento,
        numero_documento=req.numero_documento,
        nombre_completo=req.nombre_completo,
        semaforo_global=semaforo_global,
        score_riesgo=score,
        resumen_ejecutivo=resumen_ejecutivo,
        total_entidades=len(resultados),
        total_alertas=total_alertas,
        total_observaciones=total_observaciones,
        resultados=resultados,
        es_simulado=req.modo_demo
    )

    # Guardar en base de datos local SQLite para auditoría
    try:
        guardar_informe(informe.model_dump())
    except Exception as e:
        print(f"Error guardando en historial: {e}")

    return informe
