"""
Casos de estudio pre-cargados para la aplicación MACTOR.
Incluye la replicación exacta del manual/artículo adjunto de Villabona, Oyola & Franco (2018)
así como casos reales territoriales latinoamericanos.
"""

from typing import Dict, Any

PRELOADED_CASES: Dict[str, Dict[str, Any]] = {
    "manual_caballos_monteria": {
        "id": "manual_caballos_monteria",
        "title": "Caso Manual Adjunto: Selección de Caballo Ganador en Competencia de Paso (Montería)",
        "territory": "Montería (Córdoba)",
        "country": "Colombia",
        "sector": "Competencia Equina de Paso & Selección",
        "description": "Aplicación de la técnica MACTOR para evaluar y seleccionar al equino ganador en competencia de paso (modalidad trocha), disminuyendo el sesgo y confabulación de jueces mediante matrices de influencia y convergencia (Villabona, Oyola & Franco, 2018).",
        "source": "Artículo de Investigación - Revista AGLALA 2018; 9 (1): 309-318. DOI: 10.22519/22157360.1206",
        "variant": "softprosp",
        "actors": [
            {
                "id": "CB",
                "name": "Candela de la Barqueña (CB)",
                "short_name": "CB - Candela",
                "category": "Criadero Querencia Sinuana",
                "base_power": 3,
                "evidence": "Equino competidor en la modalidad trocha, Montería. Puntuación obtenida: Fenotipo 20, Adiestramiento 20, Movimiento 50."
            },
            {
                "id": "CQ",
                "name": "Carolina de Querencia Sinuana (CQ)",
                "short_name": "CQ - Carolina",
                "category": "Criadero Querencia Sinuana",
                "base_power": 4,
                "evidence": "Equino competidor en la modalidad trocha, Montería. Puntuación obtenida: Fenotipo 25, Adiestramiento 22.5, Movimiento 50. Mayor influencia ejercida."
            },
            {
                "id": "DQ",
                "name": "Dinastía de Querencia Sinuana (DQ)",
                "short_name": "DQ - Dinastía",
                "category": "Criadero Alejandría",
                "base_power": 2,
                "evidence": "Equino competidor en la modalidad trocha, Montería. Puntuación obtenida: Fenotipo 20, Adiestramiento 25, Movimiento 40."
            },
            {
                "id": "ME",
                "name": "María Espejo de Alejandría (ME)",
                "short_name": "ME - María Espejo",
                "category": "Criadero Alejandría",
                "base_power": 1,
                "evidence": "Equino competidor en la modalidad trocha, Montería. Puntuación obtenida: Fenotipo 20, Adiestramiento 19, Movimiento 42.5."
            }
        ],
        "objectives": [
            {
                "id": "FEN",
                "name": "Evaluación del Fenotipo (FEN)",
                "short_name": "FEN (25%)",
                "description": "Fase 1: Cabeza, cuello, dorso, grupa, pecho, vientre, color (15%), aplomos (8%) y cola (2%).",
                "weight": 25.0
            },
            {
                "id": "ADI",
                "name": "Evaluación del Adiestramiento (ADI)",
                "short_name": "ADI (25%)",
                "description": "Fase 2: Sostenimiento (15%), rienda (7%) y posición de cabeza (3%).",
                "weight": 25.0
            },
            {
                "id": "MOV",
                "name": "Evaluación de los Movimientos (MOV)",
                "short_name": "MOV (50%)",
                "description": "Fase 3: Armonía (25%), cabeza y ritmo (15%), brío y temperamento (10%). Fase de mayor ponderación reglamentaria.",
                "weight": 50.0
            }
        ],
        # Matriz de Influencia Directa (Figura 1 del artículo adjunto)
        "mid": [
            [0, 1, 3, 4],  # CB
            [3, 0, 4, 4],  # CQ
            [1, 0, 0, 3],  # DQ
            [0, 0, 1, 0]   # ME
        ],
        # Matriz Valorada de Posiciones 2MAO (Figura 2 del artículo adjunto)
        "mao2": [
            [3, 3, 4],     # CB
            [4, 3, 4],     # CQ
            [3, 4, 3],     # DQ
            [3, 2, 3]      # ME
        ]
    },
    "guajira_transicion_energetica": {
        "id": "guajira_transicion_energetica",
        "title": "Territorio La Guajira: Parques Eólicos, Comunidades Wayúu y Transición Justa",
        "territory": "La Guajira",
        "country": "Colombia",
        "sector": "Transición Energética Justa & Eólica",
        "description": "Análisis prospectivo de juegos de actores en torno a la instalación de megaparques eólicos, consulta previa comunitaria, compensaciones hídricas y regalías.",
        "source": "Análisis de prensa territorial, resoluciones MinEnergía y pronunciamientos ONIC/Wayúu 2024-2026.",
        "variant": "softprosp",
        "actors": [
            {
                "id": "A1",
                "name": "Ministerio de Minas y Energía & UPME",
                "short_name": "MinEnergía / UPME",
                "category": "Gobierno Central",
                "base_power": 4,
                "evidence": "Rector de la política pública de transición energética y convocante del Pacto por La Guajira."
            },
            {
                "id": "A2",
                "name": "Empresas Generadoras y Gremios Eólicos (SER Colombia / Enel)",
                "short_name": "Generadoras Eólicas",
                "category": "Sector Privado",
                "base_power": 3,
                "evidence": "Inversionistas de parques eólicos Costa Norte, reclaman seguridad jurídica y licencias."
            },
            {
                "id": "A3",
                "name": "Autoridades Tradicionales y Comunidades Wayúu",
                "short_name": "Pueblo Wayúu",
                "category": "Comunidades Étnicas",
                "base_power": 3,
                "evidence": "Exigen consulta previa vinculante, agua potable, compensación territorial y respeto a cementerios ancestrales."
            },
            {
                "id": "A4",
                "name": "Gobernación de La Guajira & Corpoguajira",
                "short_name": "Gobernación / Corpoguajira",
                "category": "Autoridad Territorial",
                "base_power": 3,
                "evidence": "Reclaman mayores regalías locales para acueductos y hospitales en Uribia y Maicao."
            },
            {
                "id": "A5",
                "name": "Organizaciones de Derechos Humanos y Veedurías",
                "short_name": "Veedurías y DDHH",
                "category": "ONGs",
                "base_power": 2,
                "evidence": "Monitorean cumplimiento de sentencias T-302 de la Corte Constitucional sobre niñez Wayúu."
            }
        ],
        "objectives": [
            {
                "id": "O1",
                "name": "Aceleración de Capacidad Eólica y Conexión al SIN",
                "short_name": "Megaproyectos Eólicos (25%)",
                "description": "Construcción rápida de líneas Colectora y parques de generación renovable.",
                "weight": 25.0
            },
            {
                "id": "O2",
                "name": "Garantía de Consulta Previa y Consentimiento Libre e Informado",
                "short_name": "Consulta Previa (25%)",
                "description": "Procesos genuinos de consulta clan por clan respetando tiempos y usos ancestrales.",
                "weight": 25.0
            },
            {
                "id": "O3",
                "name": "Solución Estructural al Agua Potable y Seguridad Alimentaria",
                "short_name": "Agua y Alimento (25%)",
                "description": "Destinación de recursos de proyectos a acueductos sostenibles y desalinización.",
                "weight": 25.0
            },
            {
                "id": "O4",
                "name": "Transferencia de Rentas y Regalías Directas al Territorio",
                "short_name": "Regalías Territoriales (25%)",
                "description": "Participación accionaria o porcentaje de venta de energía en beneficio de los municipios locales.",
                "weight": 25.0
            }
        ],
        "mid": [
            [0, 3, 3, 4, 2],
            [2, 0, 3, 2, 1],
            [3, 3, 0, 3, 2],
            [2, 2, 2, 0, 1],
            [2, 1, 3, 2, 0]
        ],
        "mao2": [
            [4, 3, 3, 2],
            [4, -1, 1, -2],
            [-2, 4, 4, 3],
            [2, 2, 4, 4],
            [0, 4, 4, 3]
        ]
    },
    "atacama_litio_agua": {
        "id": "atacama_litio_agua",
        "title": "Salar de Atacama: Estrategia Nacional del Litio, Salmuera y Pueblos Atacameños",
        "territory": "Salar de Atacama",
        "country": "Chile",
        "sector": "Minería de Litio & Protección Hídrica",
        "description": "Juego de alianzas y conflictos por el control de la cuenca hídrica, la alianza público-privada Codelco-SQM y la gobernanza del pueblo Lickanantay.",
        "source": "Diario Financiero, Comunicados Consejo de Pueblos Atacameños y Estrategia Nacional del Litio 2024-2026.",
        "variant": "softprosp",
        "actors": [
            {
                "id": "A1",
                "name": "Gobierno de Chile & Codelco",
                "short_name": "Estado / Codelco",
                "category": "Estado y Empresa Pública",
                "base_power": 4,
                "evidence": "Impulsa la Estrategia Nacional del Litio y la asociación de mayoría estatal en el Salar."
            },
            {
                "id": "A2",
                "name": "SQM & Albemarle (Operadores Privados)",
                "short_name": "Empresas del Litio",
                "category": "Sector Privado",
                "base_power": 4,
                "evidence": "Operan la extracción de salmuera y buscan extender contratos hasta 2060."
            },
            {
                "id": "A3",
                "name": "Consejo de Pueblos Atacameños (CPA)",
                "short_name": "Pueblos Atacameños",
                "category": "Comunidades Originarias",
                "base_power": 3,
                "evidence": "Exigen protección del balance hidrológico del Salar y veto ambiental comunitario."
            },
            {
                "id": "A4",
                "name": "Comunidad Científica y Veedores Hídricos",
                "short_name": "Científicos Ambientales",
                "category": "Academia",
                "base_power": 2,
                "evidence": "Alertan sobre la fragilidad del acuífero y necesidad de tecnología de Extracción Directa (DLE)."
            }
        ],
        "objectives": [
            {
                "id": "O1",
                "name": "Maximización de Producción y Rentas Fiscales del Litio",
                "short_name": "Producción Litio (30%)",
                "description": "Incrementar las cuotas de exportación de carbonato e hidróxido de litio para baterías.",
                "weight": 30.0
            },
            {
                "id": "O2",
                "name": "Protección Estricta del Acuífero y Salmuera del Salar",
                "short_name": "Protección Acuífero (35%)",
                "description": "Monitoreo independiente en línea y detención de faenas si bajan los niveles freáticos.",
                "weight": 35.0
            },
            {
                "id": "O3",
                "name": "Reconversión a Tecnologías de Extracción Directa sin Evaporación",
                "short_name": "Tecnología DLE (20%)",
                "description": "Reemplazo de pozas de evaporación solar por reinyección de salmuera para salvar el agua.",
                "weight": 20.0
            },
            {
                "id": "O4",
                "name": "Co-decisión y Regalías Directas para Pueblos Originarios",
                "short_name": "Co-decisión Pueblos (15%)",
                "description": "Gobierno compartido del territorio con poder de veto comunitario.",
                "weight": 15.0
            }
        ],
        "mid": [
            [0, 4, 3, 2],
            [3, 0, 3, 2],
            [3, 3, 0, 3],
            [2, 2, 2, 0]
        ],
        "mao2": [
            [4, 2, 4, 2],
            [4, -2, 1, -2],
            [-3, 4, 3, 4],
            [0, 4, 4, 2]
        ]
    }
}
