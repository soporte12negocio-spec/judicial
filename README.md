# VerificaCO - Sistema Unificado de Antecedentes, Tránsito, Inmuebles y Centrales de Riesgo (Colombia)

Plataforma unificada para la consulta, consolidación y emisión de informes integrales de seguridad, antecedentes judiciales, tránsito, siniestralidad, titularidad de bienes raíces y solvencia crediticia en la República de Colombia.

---

## 🏛️ Las 11 Entidades y Bases de Datos Integradas (11 en 1)

### ⚖️ 1. Módulo Penal y Judicial
1. **Rama Judicial de Colombia (Justicia XXI / Siglo XXI)**:
   - Demandas activas en juzgados civiles, laborales, de familia, administrativos y penales en todo el territorio nacional.
2. **Policía Nacional de Colombia (DIJIN)**:
   - Órdenes de captura activas, antecedentes penales y requerimientos judiciales vigentes (Art. 248 Constitución Política).
3. **Procuraduría General de la Nación (SIRI)**:
   - Sanciones disciplinarias e inhabilidades para contratar con el Estado o ejercer cargos públicos (Ley 1952 de 2019).
4. **Contraloría General de la República (SIRECI)**:
   - Boletín de Responsables Fiscales por daño patrimonial al erario público (Ley 610 de 2000).
5. **REDAM (Registro de Deudores Alimentarios Morosos)**:
   - Reportes judiciales por inasistencia alimentaria y mora en cuotas alimentarias (Ley 2097 de 2021).
6. **Policía Nacional - RNMC (Registro Nacional de Medidas Correctivas)**:
   - Comparendos y sanciones del Código Nacional de Seguridad y Convivencia Ciudadana (Ley 1801 de 2016).

### 🚗 2. Módulo de Tránsito, Licencias y Accidentes
7. **SIMIT (Federación Colombiana de Municipios)**:
   - Multas, comparendos pendientes y fotomultas de tránsito a nivel municipal y departamental.
8. **RUNT (Registro Único Nacional de Tránsito)**:
   - Estado de la licencia de conducción (Vigente / Suspendida / Cancelada), categorías autorizadas e **historial de accidentes de tránsito / siniestros viales** reportados (IPAT).

### 🏠 3. Módulo de Bienes Inmuebles y Patrimonio
9. **Superintendencia de Notariado y Registro (SNR / VUR - Instrumentos Públicos)**:
   - Consulta del Índice de Propietarios, número de matrículas inmobiliarias a su nombre, círculos registrales, porcentaje de titularidad, gravámenes (hipotecas bancarias) y **medidas cautelares de embargo judicial**.

### 💳 4. Módulo Financiero y Centrales de Riesgo (Habeas Data)
10. **Datacrédito Experian Colombia**:
    - Score crediticio (escala 150 a 950 puntos), hábito de pago, obligaciones financieras activas y reportes en mora (Ley 1266 de 2008 y Ley 2157 de 2021).
11. **TransUnion / CIFIN**:
    - Calificación bancaria según la Superintendencia Financiera (Categorías A, B, C, D, E), nivel de endeudamiento consolidado y alertas preventivas de fraude o suplantación.

---

## 🚀 Características Principales

- **Filtros por Categoría**: Pestañas interactivas para visualizar: *Todas las Entidades (11)*, *Penal y Judicial*, *Tránsito y Accidentes*, *Inmuebles (SNR)* y *Datacrédito / CIFIN*.
- **Semáforo de Riesgo Ponderado**: Evaluación global automatizada con semáforo verde, amarillo o rojo.
- **Badges Especiales**: Medidores visuales de Score Crediticio, Calificación Bancaria y Conteo de Bienes Raíces.
- **Informe Imprimible / PDF**: Formato listo para impresión oficial con estilos `@media print`.
- **Exportación en JSON**: Descarga estructurada para auditorías o integraciones con otros sistemas.
- **Historial Local SQLite**: Consulta y reabre auditorías previas sin salir de la plataforma.
- **Casos Demo con 1 Clic**: Tres perfiles preconfigurados para validar todos los escenarios de inmediato.

---

## 📦 Ejecución en Windows

### Con el lanzador rápido:
Doble clic sobre el archivo `run.bat`.

### Desde PowerShell:
```powershell
cd C:\Users\Juan\.gemini\antigravity\scratch\consulta-antecedentes-colombia
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Acceso en navegador: **`http://127.0.0.1:8000`**
