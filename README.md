# MACTOR PROSP: Sistema Web de Prospectiva Estratégica, Inteligencia Territorial y Variantes Avanzadas

Aplicación web integral para la aplicación rigurosa del método prospectivo **MACTOR** (*Matriz de Alianzas y Conflictos: Tácticas, Objetivos y Recomendaciones*), desarrollado originalmente por **Michel Godet (LIPSOR)**, incorporando la variante **Multi-criterio / SoftProsp** fundamentada en el artículo adjunto (*Villabona, Oyola & Franco, 2018*), así como inteligencia territorial en vivo a partir de noticias y fuentes oficiales, variante difusa y análisis de estabilidad de coaliciones bajo Teoría de Juegos.

---

## 🚀 Características Principales

1. **Minería de Inteligencia Territorial en Vivo**:
   - Ingrese cualquier territorio real (municipio, departamento, provincia o país).
   - Rastrela noticias en tiempo real, declaraciones gubernamentales y comunicados de gremios/comunidades vía RSS y portales de noticias abiertas.
   - Extrae automáticamente los actores estratégicos (autoridades, sector privado, comunidades, ONGs, academia) y deduce sus **objetivos implícitos** con citas textuales de evidencia.
   - Transfiere con 1 clic los actores, objetivos y matrices preliminares (MID y 2MAO) al entorno de cálculo.

2. **Replicación Exacta del Manual Adjunto**:
   - Incluye el caso de estudio del artículo científico: *"Aplicación de la técnica MACTOR para la selección del caballo ganador en una competencia de paso"* (Revista AGLALA, 2018).
   - Recrea con exactitud:
     - Matriz de Influencia Directa (**MID**, Figura 1): equinos CB, CQ, DQ, ME.
     - Matriz Valorada de Posiciones (**2MAO**, Figura 2): FEN (25%), ADI (25%), MOV (50%).
     - Matriz Valorada y Ponderada de Convergencias (**3CAA**, Figura 3), identificando a **Carolina de Querencia Sinuana (CQ)** como el actor/equino ganador con el mayor grado de convergencia estratégica.

3. **Cálculo Completo de Todas las Matrices MACTOR**:
   - **MID**: Influencia directa ($I_i$) y Dependencia directa ($D_i$).
   - **MIDI**: Influencias directas e indirectas de segundo orden.
   - **Relación de Fuerza ($r_i$)**: Balance de poder normalizado.
   - **1MAO, 2MAO, 3MAO**: Matrices de signos, intensidad valorada (-4 a +4) y posición ponderada.
   - **1CAA, 2CAA, 3CAA**: Grados de alianza y convergencia simple, valorada y ponderada.
   - **1DAA, 2DAA, 3DAA**: Grados de divergencia y conflicto simple, valorado y ponderado.
   - **2COO, 3COO**: Distancia e interacción entre objetivos.

4. **Visualizaciones Estratégicas Interactivas**:
   - **Plano de Influencia vs Dependencia (Godet)**: Gráfico cartesiano interactivo con los 4 cuadrantes (*Dominantes*, *Enlace/Relé*, *Autónomos* y *Dependientes*).
   - **Red Interactiva de Alianzas y Conflictos (Vis.js)**: Grafo interactivo con nodos proporcionales a la fuerza del actor ($r_i$), aristas verdes continuas de convergencia y aristas rojas punteadas de conflicto, con control dinámico de umbrales.
   - **Gráfico de Movilización y Conflicto de Objetivos**: Identificación visual de objetivos de consenso vs focos de disputa crítica territorial.

5. **Variantes Avanzadas & Simulación de Escenarios**:
   - **Variante Multi-criterio / SoftProsp**: Incorpora ponderaciones porcentuales específicas por objetivo ($W_j$) como en el manual de paso fino.
   - **Variante Estándar Godet (LIPSOR Puro)**.
   - **Variante Difusa / Incertidumbre**: Para modelar fuentes contradictorias o rangos de confianza.
   - **Teoría de Juegos**: Diagnóstico de estabilidad de coaliciones (Alianzas tácticas vs alianzas sólidas).
   - **Simulador "¿Qué pasa si...?"**: Permite simular qué ocurre si un actor altera su fuerza o su postura frente a un objetivo, mostrando los deltas de convergencia en tiempo real.

6. **Exportación y Reportes**:
   - Generación y descarga directa en **Excel (.xlsx)** con hojas formateadas profesionalmente para cada matriz (*MID, MIDI, 2MAO, 3MAO, 3CAA, 3DAA, Cuadrantes, Objetivos*).
   - Generación de **Informe Ejecutivo Prospectivo** imprimible o exportable a PDF con conclusiones estratégicas.

---

## 🛠️ Estructura del Proyecto

```
mactor/
├── api/
│   └── index.py               # Entrypoint Serverless para despliegue en Vercel
├── backend/
│   ├── app.py                 # Servidor FastAPI, endpoints REST y exportador Excel
│   ├── mactor_engine.py       # Algoritmo matemático riguroso MACTOR y variantes
│   ├── territory_miner.py     # Extractor en vivo de noticias y fuentes oficiales
│   └── cases_data.py          # Casos precargados (Manual adjunto, La Guajira, Atacama)
├── frontend/
│   ├── index.html             # Interfaz web responsiva con pestañas y modales
│   ├── styles.css             # Estilos personalizados, animaciones y mapa de calor
│   └── app.js                 # Lógica interactiva, Balanzas LIPSOR, Chart.js y Vis.js
├── vercel.json                # Configuración de rutas y rewrites para Vercel
├── requirements.txt           # Dependencias de producción para Vercel
├── .gitignore                 # Filtros de repositorio Git
├── run_app.py                 # Script de arranque local en Python
├── iniciar_mactor.bat         # Acceso directo para Windows
└── README.md                  # Documentación
```

---

## ☁️ Despliegue en Vercel (Producción Serverless)

El proyecto está 100% optimizado y listo para ser desplegado en **Vercel**:

### Opción A: Despliegue con Vercel CLI
```bash
npm i -g vercel
vercel
```

### Opción B: Despliegue con GitHub / GitLab
1. Suba este repositorio a su cuenta de GitHub o GitLab.
2. Vaya a [vercel.com](https://vercel.com) y seleccione **"Add New Project"**.
3. Importe el repositorio.
4. Vercel detectará automáticamente la configuración de `vercel.json`, `requirements.txt` y la función serverless en `api/index.py`.
5. Presione **"Deploy"**. En menos de 1 minuto su plataforma estará en línea con dominio HTTPS global gratuito (ej. `https://mactor-prosp.vercel.app`).

---

## ⚡ Guía Rápida de Uso Local

1. Para iniciar el servidor y abrir la aplicación web automáticamente, ejecute:
   ```powershell
   python run_app.py
   ```
   *O haga doble clic en `iniciar_mactor.bat`.*

2. Acceda a la aplicación en su navegador:
   `http://127.0.0.1:8000`

3. **Flujo de Trabajo Recomendado**:
   - **Paso 1**: En la pestaña *Inteligencia Territorial*, escriba el nombre de una región o ciudad (ej. `Antioquia`, `Medellín`, `La Guajira`) y presione **Analizar en Vivo**. Observe los actores detectados y pulse **Transferir Actores & Objetivos a Matrices de Trabajo**.
   - **Paso 2**: En *Actores & Objetivos*, ajuste ponderaciones o agregue actores adicionales.
   - **Paso 3**: En *Matriz MID & Cuadrantes*, edite las influencias directas (0 a 4) y consulte el plano cartesiano de Godet.
   - **Paso 4**: En *Posiciones (2MAO)*, defina el grado de acuerdo (-4 a +4) con cada objetivo.
   - **Paso 5**: En *Red de Alianzas & Conflictos*, explore el grafo dinámico y las matrices 3CAA / 3DAA.
   - **Paso 6**: En *Simulación "¿Qué pasa si...?"*, evalúe cambios de posturas o alianzas.
   - **Paso 7**: Descargue el libro de Excel con el botón **Exportar Excel** o imprima el informe ejecutivo en la pestaña 8.
