let perfilesDemo = [];
let filtroActual = "todas";

document.addEventListener("DOMContentLoaded", async () => {
    await cargarPerfilesDemo();
    configurarEventos();
});

async function cargarPerfilesDemo() {
    try {
        const res = await fetch("/api/perfiles-demo");
        if (res.ok) {
            perfilesDemo = await res.json();
            const container = document.getElementById("demo-pills-container");
            if (container) {
                container.innerHTML = "";
                perfilesDemo.forEach(p => {
                    const btn = document.createElement("button");
                    btn.type = "button";
                    btn.className = "demo-btn";
                    btn.innerHTML = p.titulo;
                    btn.onclick = () => aplicarPerfilDemo(p);
                    container.appendChild(btn);
                });
            }
        }
    } catch (e) {
        console.error("Error cargando perfiles demo:", e);
    }
}

function aplicarPerfilDemo(p) {
    document.getElementById("tipo_documento").value = p.tipo_doc;
    document.getElementById("numero_documento").value = p.numero_doc;
    document.getElementById("primer_nombre").value = p.primer_nombre;
    document.getElementById("segundo_nombre").value = p.segundo_nombre || "";
    document.getElementById("primer_apellido").value = p.primer_apellido;
    document.getElementById("segundo_apellido").value = p.segundo_apellido || "";
    document.getElementById("fecha_expedicion").value = p.fecha_exp || "";
    document.getElementById("modo_demo").checked = true;
    document.getElementById("perfil_demo_val").value = p.id;

    // Feedback visual
    const submitBtn = document.getElementById("btn-consultar");
    submitBtn.scrollIntoView({ behavior: "smooth", block: "center" });
}

function configurarEventos() {
    const form = document.getElementById("form-consulta");
    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            await realizarConsulta();
        });
    }

    const btnHistorial = document.getElementById("btn-ver-historial");
    if (btnHistorial) {
        btnHistorial.addEventListener("click", abrirHistorial);
    }

    const btnVerBase = document.getElementById("btn-ver-base");
    if (btnVerBase) {
        btnVerBase.addEventListener("click", abrirBaseCiudadanos);
    }

    const btnCloseModal = document.getElementById("btn-close-modal");
    if (btnCloseModal) {
        btnCloseModal.addEventListener("click", cerrarModal);
    }

    const btnCloseBaseModal = document.getElementById("btn-close-base-modal");
    if (btnCloseBaseModal) {
        btnCloseBaseModal.addEventListener("click", cerrarBaseModal);
    }

    const modal = document.getElementById("history-modal");
    if (modal) {
        modal.addEventListener("click", (e) => {
            if (e.target === modal) cerrarModal();
        });
    }

    const baseModal = document.getElementById("base-modal");
    if (baseModal) {
        baseModal.addEventListener("click", (e) => {
            if (e.target === baseModal) cerrarBaseModal();
        });
    }

    // Toggle de modo demo manual
    const modoDemoCheck = document.getElementById("modo_demo");
    if (modoDemoCheck) {
        modoDemoCheck.addEventListener("change", (e) => {
            if (!e.target.checked) {
                document.getElementById("perfil_demo_val").value = "";
            }
        });
    }

    // Si el usuario escribe manualmente en cualquier campo, pasar a consulta en vivo
    ["numero_documento", "primer_nombre", "primer_apellido"].forEach(fieldId => {
        const input = document.getElementById(fieldId);
        if (input) {
            input.addEventListener("input", () => {
                if (modoDemoCheck) modoDemoCheck.checked = false;
                const demoVal = document.getElementById("perfil_demo_val");
                if (demoVal) demoVal.value = "";
            });
        }
    });
}

async function realizarConsulta() {
    const submitBtn = document.getElementById("btn-consultar");
    const progressCard = document.getElementById("progress-card");
    const reportSection = document.getElementById("report-section");
    const progressBar = document.getElementById("progress-fill");

    const payload = {
        tipo_documento: document.getElementById("tipo_documento").value,
        numero_documento: document.getElementById("numero_documento").value.trim(),
        primer_nombre: document.getElementById("primer_nombre").value.trim(),
        segundo_nombre: document.getElementById("segundo_nombre").value.trim(),
        primer_apellido: document.getElementById("primer_apellido").value.trim(),
        segundo_apellido: document.getElementById("segundo_apellido").value.trim(),
        fecha_expedicion: document.getElementById("fecha_expedicion").value,
        autorizacion_financiera: document.getElementById("autorizacion_financiera") ? document.getElementById("autorizacion_financiera").checked : true,
        modo_demo: document.getElementById("modo_demo").checked,
        perfil_demo: document.getElementById("perfil_demo_val").value || null
    };

    if (!payload.numero_documento || !payload.primer_nombre || !payload.primer_apellido) {
        alert("Por favor diligencie como mínimo el Número de Documento, Primer Nombre y Primer Apellido.");
        return;
    }

    // UI Loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<span>⏳ Consultando 14 Bases de Datos...</span>`;
    progressCard.style.display = "block";
    reportSection.style.display = "none";
    progressBar.style.width = "6%";

    // Simular progreso visual de chips
    const chips = document.querySelectorAll(".entity-chips .chip");
    chips.forEach(c => {
        c.className = "chip";
        const icon = c.querySelector(".chip-icon");
        if (icon) icon.textContent = "⚪";
    });

    let chipIdx = 0;
    const interval = setInterval(() => {
        if (chipIdx < chips.length) {
            chips[chipIdx].className = "chip active";
            const icon = chips[chipIdx].querySelector(".chip-icon");
            if (icon) icon.textContent = "🔄";
            progressBar.style.width = `${Math.min(10 + (chipIdx * 7), 92)}%`;
            chipIdx++;
        }
    }, 110);

    try {
        const res = await fetch("/api/consultar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        clearInterval(interval);
        progressBar.style.width = "100%";

        chips.forEach(c => {
            c.className = "chip done";
            const icon = c.querySelector(".chip-icon");
            if (icon) icon.textContent = "✅";
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Error en la consulta");
        }

        const informe = await res.json();
        setTimeout(() => {
            progressCard.style.display = "none";
            renderizarInforme(informe);
            submitBtn.disabled = false;
            submitBtn.innerHTML = `<span>🔍 Consultar Expediente Completo (14 en 1)</span>`;
            reportSection.scrollIntoView({ behavior: "smooth", block: "start" });
        }, 500);

    } catch (e) {
        clearInterval(interval);
        alert("Error ejecutando la consulta: " + e.message);
        submitBtn.disabled = false;
        submitBtn.innerHTML = `<span>🔍 Consultar Expediente Completo (14 en 1)</span>`;
        progressCard.style.display = "none";
    }
}

function renderizarInforme(informe) {
    const reportSection = document.getElementById("report-section");
    reportSection.style.display = "block";

    // Guardar referencia actual para exportación JSON y filtros
    window.currentInforme = informe;

    // Metadata
    document.getElementById("rep-id").textContent = informe.id_informe;
    document.getElementById("rep-fecha").textContent = informe.fecha_emision;
    document.getElementById("rep-ciudadano").textContent = informe.nombre_completo;
    document.getElementById("rep-documento").textContent = `${informe.tipo_documento} ${informe.numero_documento}`;

    // Semáforo Banner
    const semaforoBanner = document.getElementById("rep-semaforo-banner");
    semaforoBanner.className = `semaforo-banner ${informe.semaforo_global}`;
    
    let icono = "🟢";
    let titulo = "ESTADO FAVORABLE / SIN NOVEDADES ADVERSAS";
    if (informe.semaforo_global === "amarillo") {
        icono = "🟡";
        titulo = "OBSERVACIÓN MODERADA / ASUNTOS INFORMATIVOS";
    } else if (informe.semaforo_global === "rojo") {
        icono = "🚨";
        titulo = "ALERTA CRÍTICA / PENDIENTES CON LA JUSTICIA O CONTROL";
    }

    document.getElementById("semaforo-icon").textContent = icono;
    document.getElementById("semaforo-title").textContent = titulo;
    document.getElementById("semaforo-desc").textContent = informe.resumen_ejecutivo;

    // Metrics
    document.getElementById("metric-total").textContent = informe.total_entidades;
    document.getElementById("metric-alertas").textContent = informe.total_alertas;
    document.getElementById("metric-observaciones").textContent = informe.total_observaciones;
    document.getElementById("metric-score").textContent = `${informe.score_riesgo}/100`;

    // Renderizar tarjetas con filtro actual
    filtrarEntidades(filtroActual || "todas");
}

function filtrarEntidades(categoria) {
    filtroActual = categoria;
    const btns = document.querySelectorAll(".category-tabs .tab-btn");
    btns.forEach(b => b.classList.remove("active"));
    
    const activeBtn = Array.from(btns).find(b => b.getAttribute("onclick") && b.getAttribute("onclick").includes(categoria));
    if (activeBtn) activeBtn.classList.add("active");

    const cardsContainer = document.getElementById("entity-cards-container");
    cardsContainer.innerHTML = "";

    if (!window.currentInforme || !window.currentInforme.resultados) return;

    const entidades = window.currentInforme.resultados.filter(ent => {
        if (categoria === "todas") return true;
        if (categoria === "penal_judicial") {
            return ["policia", "rama_judicial", "procuraduria", "contraloria", "redam", "rnmc"].includes(ent.entidad_id);
        }
        if (categoria === "transito_runt") {
            return ["simit", "runt_accidentes"].includes(ent.entidad_id);
        }
        if (categoria === "inmuebles") {
            return ["snr_inmuebles"].includes(ent.entidad_id);
        }
        if (categoria === "financiero") {
            return ["datacredito", "cifin"].includes(ent.entidad_id);
        }
        if (categoria === "salud_subsidios") {
            return ["sisben", "adres_eps", "subsidios_dps"].includes(ent.entidad_id);
        }
        return true;
    });

    entidades.forEach(ent => {
        const card = document.createElement("div");
        card.className = `entity-card ${ent.estado}`;

        let statusText = "Sin Pendientes";
        if (ent.semaforo === "rojo") statusText = "Alerta Crítica";
        else if (ent.semaforo === "amarillo") statusText = "Con Observaciones";
        else if (ent.estado === "enlace_oficial") statusText = "Verificado / Enlace Oficial";

        // Badges especiales (Score crediticio, Calificación bancaria, Bienes raíces, Sisbén, EPS, Subsidios)
        let badgesEspeciales = "";
        if (ent.score_financiero) {
            let colorScore = ent.score_financiero >= 700 ? "#10b981" : ent.score_financiero >= 550 ? "#f59e0b" : "#ef4444";
            badgesEspeciales += `<span style="background: rgba(255,255,255,0.06); border: 1px solid ${colorScore}; color: ${colorScore}; padding: 3px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; margin-left: 8px;">Score: ${ent.score_financiero}/950</span>`;
        }
        if (ent.calificacion_bancaria) {
            badgesEspeciales += `<span style="background: rgba(6, 182, 212, 0.12); border: 1px solid rgba(6, 182, 212, 0.4); color: #06b6d4; padding: 3px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; margin-left: 8px;">Calificación: ${ent.calificacion_bancaria}</span>`;
        }
        if (ent.total_propiedades !== undefined && ent.total_propiedades !== null) {
            badgesEspeciales += `<span style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.4); color: #10b981; padding: 3px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; margin-left: 8px;">Inmuebles: ${ent.total_propiedades}</span>`;
        }
        if (ent.grupo_sisben) {
            badgesEspeciales += `<span style="background: rgba(56, 189, 248, 0.15); border: 1px solid #38bdf8; color: #38bdf8; padding: 3px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; margin-left: 8px;">Grupo Sisbén: ${ent.grupo_sisben}</span>`;
        }
        if (ent.eps_nombre) {
            let colorEps = (ent.estado_afiliacion && ent.estado_afiliacion.toUpperCase() === "ACTIVO") ? "#10b981" : "#f59e0b";
            badgesEspeciales += `<span style="background: rgba(16, 185, 129, 0.12); border: 1px solid ${colorEps}; color: #e2e8f0; padding: 3px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; margin-left: 8px;">EPS: ${ent.eps_nombre} (${ent.regimen_salud || 'BDUA'}) • <strong style="color: ${colorEps};">${ent.estado_afiliacion || 'ACTIVO'}</strong></span>`;
        }
        if (ent.municipio_afiliacion) {
            badgesEspeciales += `<span style="background: rgba(148, 163, 184, 0.15); border: 1px solid #64748b; color: #cbd5e1; padding: 3px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; margin-left: 8px;">📍 ${ent.municipio_afiliacion}</span>`;
        }
        if (ent.subsidios_activos && ent.subsidios_activos.length > 0) {
            badgesEspeciales += `<span style="background: rgba(245, 158, 11, 0.15); border: 1px solid #f59e0b; color: #fbbf24; padding: 3px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; margin-left: 8px;">🎁 Beneficiario: ${ent.subsidios_activos.join(', ')}</span>`;
        }

        let detallesHtml = "";
        if (ent.detalles && ent.detalles.length > 0) {
            detallesHtml = `<div class="detalles-list">`;
            ent.detalles.forEach(d => {
                detallesHtml += `
                    <div class="detalle-card">
                        <div class="detalle-title">${d.titulo}</div>
                        <div class="detalle-desc">${d.descripcion}</div>
                        <div class="detalle-meta">
                            ${d.radicado ? `<span><strong>Radicado/Matrícula:</strong> ${d.radicado}</span>` : ""}
                            ${d.fecha ? `<span><strong>Fecha:</strong> ${d.fecha}</span>` : ""}
                            ${d.despacho_o_entidad ? `<span><strong>Despacho/ORIP:</strong> ${d.despacho_o_entidad}</span>` : ""}
                            ${d.estado_tramite ? `<span><strong>Estado:</strong> ${d.estado_tramite}</span>` : ""}
                            ${d.monto ? `<span><strong>Monto/Avalúo:</strong> ${d.monto}</span>` : ""}
                        </div>
                    </div>
                `;
            });
            detallesHtml += `</div>`;
        }

        card.innerHTML = `
            <div class="entity-header">
                <div class="entity-info-group">
                    <span class="entity-badge">${ent.sigla}</span>
                    <div>
                        <div class="entity-name">${ent.nombre_entidad} ${badgesEspeciales}</div>
                        <div class="entity-category">${ent.categoria}</div>
                    </div>
                </div>
                <span class="status-pill ${ent.semaforo}">${statusText}</span>
            </div>
            <div class="entity-body">
                <p class="entity-resumen">${ent.resumen}</p>
                ${detallesHtml}
                <div class="entity-footer">
                    <span>⏱️ Tiempo de respuesta: ${ent.tiempo_respuesta_ms} ms</span>
                    <a href="${ent.url_oficial}" target="_blank" rel="noopener noreferrer" class="btn-link-oficial">
                        🔗 Abrir Portal Oficial para Certificado con Firma Legal ↗
                    </a>
                </div>
            </div>
        `;
        cardsContainer.appendChild(card);
    });
}

function imprimirInforme() {
    window.print();
}

function exportarJSON() {
    if (!window.currentInforme) return;
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(window.currentInforme, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `expediente_${window.currentInforme.id_informe}_${window.currentInforme.numero_documento}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
}

async function abrirHistorial() {
    const modal = document.getElementById("history-modal");
    const container = document.getElementById("history-list");
    modal.style.display = "flex";
    container.innerHTML = "<p>Cargando historial...</p>";

    try {
        const res = await fetch("/api/historial");
        if (res.ok) {
            const list = await res.json();
            if (list.length === 0) {
                container.innerHTML = "<p style='color: var(--text-secondary);'>No hay consultas guardadas aún.</p>";
                return;
            }
            container.innerHTML = "";
            list.forEach(item => {
                const div = document.createElement("div");
                div.className = "history-item";
                div.onclick = () => cargarInformeGuardado(item.id_informe);

                let badgeColor = item.semaforo_global === "rojo" ? "var(--status-red)" : item.semaforo_global === "amarillo" ? "var(--status-yellow)" : "var(--status-green)";

                div.innerHTML = `
                    <div>
                        <div style="font-weight: 600; color: #ffffff;">${item.nombre_completo}</div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">${item.tipo_documento} ${item.numero_documento} • ${item.fecha_emision}</div>
                    </div>
                    <span style="display: inline-block; width: 12px; height: 12px; border-radius: 50%; background: ${badgeColor};"></span>
                `;
                container.appendChild(div);
            });
        }
    } catch (e) {
        container.innerHTML = "<p style='color: red;'>Error cargando el historial.</p>";
    }
}

async function cargarInformeGuardado(idInforme) {
    try {
        const res = await fetch(`/api/informe/${idInforme}`);
        if (res.ok) {
            const informe = await res.json();
            cerrarModal();
            renderizarInforme(informe);
            document.getElementById("report-section").scrollIntoView({ behavior: "smooth", block: "start" });
        }
    } catch (e) {
        alert("No se pudo cargar el informe: " + e.message);
    }
}

function cerrarModal() {
    const modal = document.getElementById("history-modal");
    modal.style.display = "none";
}

async function abrirBaseCiudadanos() {
    const modal = document.getElementById("base-modal");
    const container = document.getElementById("base-list");
    const contador = document.getElementById("base-contador");
    modal.style.display = "flex";
    container.innerHTML = "<p style='color: var(--text-secondary); padding: 10px;'>Cargando base de ciudadanos...</p>";

    try {
        const res = await fetch("/api/base-ciudadanos");
        if (res.ok) {
            const list = await res.json();
            contador.textContent = `Total: ${list.length} ciudadano${list.length === 1 ? '' : 's'} registrado${list.length === 1 ? '' : 's'}`;
            
            if (list.length === 0) {
                container.innerHTML = "<p style='color: var(--text-secondary); padding: 10px;'>No hay ciudadanos registrados en la base aún. Realice una consulta para registrar el primero.</p>";
                return;
            }

            let tablaHtml = `
                <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem; text-align: left;">
                    <thead>
                        <tr style="border-bottom: 1px solid var(--border-color); color: #94a3b8;">
                            <th style="padding: 10px 8px;">Cédula</th>
                            <th style="padding: 10px 8px;">Nombre(s)</th>
                            <th style="padding: 10px 8px;">Apellido(s)</th>
                            <th style="padding: 10px 8px;">Fecha Registro</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            list.forEach(c => {
                tablaHtml += `
                    <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.05); color: #e2e8f0;">
                        <td style="padding: 10px 8px; font-weight: 700; color: #38bdf8;">${c.cedula}</td>
                        <td style="padding: 10px 8px;">${c.nombre}</td>
                        <td style="padding: 10px 8px;">${c.apellido}</td>
                        <td style="padding: 10px 8px; color: #94a3b8; font-size: 0.78rem;">${c.fecha_registro}</td>
                    </tr>
                `;
            });

            tablaHtml += `</tbody></table>`;
            container.innerHTML = tablaHtml;
        }
    } catch (e) {
        container.innerHTML = "<p style='color: #ef4444; padding: 10px;'>Error cargando la base de datos de ciudadanos.</p>";
    }
}

function cerrarBaseModal() {
    const modal = document.getElementById("base-modal");
    modal.style.display = "none";
}

