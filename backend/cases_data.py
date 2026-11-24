"""
Casos de estudio pre-cargados para la aplicación MACTOR.
Incluye la replicación exacta del manual/artículo adjunto de Villabona, Oyola & Franco (2018)
así como casos territoriales estratégicos de Colombia, Chile, Argentina, Perú, México y España.
"""

from typing import Dict, Any

PRELOADED_CASES: Dict[str, Dict[str, Any]] = {
    # -------------------------------------------------------------
    # 1. CASO MANUAL ADJUNTO: VILLABONA, OYOLA & FRANCO (2018)
    # -------------------------------------------------------------
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
                "evidence": "Equino competidor en la modalidad trocha, Montería. Puntuación obtenida: Fenotipo 20, Adiestramiento 20, Movimiento 50.",
                "explicit_objective": "Alcanzar el puntaje óptimo reglamentario en movimientos y sostenimiento.",
                "implicit_objective": "Posicionar la genética del criadero en el circuito nacional."
            },
            {
                "id": "CQ",
                "name": "Carolina de Querencia Sinuana (CQ)",
                "short_name": "CQ - Carolina",
                "category": "Criadero Querencia Sinuana",
                "base_power": 4,
                "evidence": "Equino competidor en la modalidad trocha, Montería. Puntuación obtenida: Fenotipo 25, Adiestramiento 22.5, Movimiento 50. Mayor influencia ejercida.",
                "explicit_objective": "Liderar la tabla general de calificación morfológica y cadencia.",
                "implicit_objective": "Consolidar hegemonía en pista y valoración económica de crías."
            },
            {
                "id": "DQ",
                "name": "Dinastía de Querencia Sinuana (DQ)",
                "short_name": "DQ - Dinastía",
                "category": "Criadero Alejandría",
                "base_power": 2,
                "evidence": "Equino competidor en la modalidad trocha, Montería. Puntuación obtenida: Fenotipo 20, Adiestramiento 25, Movimiento 40.",
                "explicit_objective": "Destacar en adiestramiento y suavidad de rienda.",
                "implicit_objective": "Disputar podio y presionar a los ejemplares favoritos."
            },
            {
                "id": "ME",
                "name": "María Espejo de Alejandría (ME)",
                "short_name": "ME - María Espejo",
                "category": "Criadero Alejandría",
                "base_power": 1,
                "evidence": "Equino competidor en la modalidad trocha, Montería. Puntuación obtenida: Fenotipo 20, Adiestramiento 19, Movimiento 42.5.",
                "explicit_objective": "Completar las pruebas de pista sin penalizaciones técnicas.",
                "implicit_objective": "Obtener cinta de premiación y mejorar cotización de pesebrera."
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
        "mid": [
            [0, 1, 3, 4],
            [3, 0, 4, 4],
            [1, 0, 0, 3],
            [0, 0, 1, 0]
        ],
        "mao2": [
            [3, 3, 4],
            [4, 3, 4],
            [3, 4, 3],
            [3, 2, 3]
        ]
    },

    # -------------------------------------------------------------
    # 2. COLOMBIA: LA GUAJIRA - ENERGÍA EÓLICA Y PUEBLO WAYÚU
    # -------------------------------------------------------------
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

    # -------------------------------------------------------------
    # 3. COLOMBIA: MEDELLÍN - EPM, METRO DE LA 80 Y POT DISTRITAL
    # -------------------------------------------------------------
    "medellin_servicios_metro": {
        "id": "medellin_servicios_metro",
        "title": "Medellín: Gobernanza de EPM, Metro de la 80 y Ordenamiento Territorial",
        "territory": "Medellín",
        "country": "Colombia",
        "sector": "Servicios Públicos, Movilidad Eléctrica y POT",
        "description": "Juego estratégico entre la administración distrital, el Grupo EPM, gremios empresariales, veedurías ciudadanas y el Metro de Medellín en torno a la financiación de grandes obras y tarifas de servicios.",
        "source": "Plan de Desarrollo de Medellín, Informes Financieros EPM y Acuerdos del Concejo Distrital 2024-2026.",
        "variant": "softprosp",
        "actors": [
            {
                "id": "A1",
                "name": "Alcaldía Distrital de Medellín",
                "short_name": "Alcaldía de Medellín",
                "category": "Gobierno Local",
                "base_power": 4,
                "evidence": "Máxima autoridad distrital, accionista única de EPM y líder de la ejecución del Metro de la 80."
            },
            {
                "id": "A2",
                "name": "Grupo EPM (Empresas Públicas de Medellín)",
                "short_name": "Grupo EPM",
                "category": "Empresa Pública",
                "base_power": 4,
                "evidence": "Generador de hidroelectricidad (Hidroituango) y transferencias billonarias al presupuesto distrital."
            },
            {
                "id": "A3",
                "name": "Empresa de Transporte Masivo del Valle de Aburrá (Metro)",
                "short_name": "Metro de Medellín",
                "category": "Empresa de Transporte",
                "base_power": 3,
                "evidence": "Operador del sistema férreo y ejecutor técnico del corredor de tranvía y tren ligero de la 80."
            },
            {
                "id": "A4",
                "name": "Sector Empresarial e Industrial (Proantioquia / ANDI)",
                "short_name": "Gremios & Proantioquia",
                "category": "Sector Privado",
                "base_power": 3,
                "evidence": "Defienden el gobierno corporativo de EPM, estabilidad jurídica y clima de inversión privada."
            },
            {
                "id": "A5",
                "name": "Concejo Distrital de Medellín",
                "short_name": "Concejo Distrital",
                "category": "Órgano de Control Político",
                "base_power": 3,
                "evidence": "Aprueba presupuesto, transferencias extraordinarias de EPM y reformas al POT."
            },
            {
                "id": "A6",
                "name": "Colectivos Comunitarios, Usuarios de Servicios y Veedurías",
                "short_name": "Comunidades & Usuarios",
                "category": "Sociedad Civil",
                "base_power": 2,
                "evidence": "Exigen contención de tarifas de energía, agua mínima vital y mitigación de gentrificación urbana."
            }
        ],
        "objectives": [
            {
                "id": "O1",
                "name": "Culminación y Financiación del Metro de la 80",
                "short_name": "Metro de la 80 (30%)",
                "description": "Garantizar cofinanciación 70/30 de la Nación y el Distrito para el tercer corredor férreo.",
                "weight": 30.0
            },
            {
                "id": "O2",
                "name": "Blindaje del Gobierno Corporativo y Finanzas de EPM",
                "short_name": "Blindaje de EPM (25%)",
                "description": "Proteger la calificación crediticia de EPM y mantener transferencias sostenibles sin descapitalizar.",
                "weight": 25.0
            },
            {
                "id": "O3",
                "name": "Tarifas Justas y Mínimo Vital de Servicios Públicos",
                "short_name": "Tarifas y Agua Vital (25%)",
                "description": "Subsidios focalizados para estratos 1, 2 y 3 y estabilización de la fórmula tarifaria de energía.",
                "weight": 25.0
            },
            {
                "id": "O4",
                "name": "Revisión Concertada del Plan de Ordenamiento Territorial (POT)",
                "short_name": "POT Concertado (20%)",
                "description": "Renovación urbana en el corredor del río con equilibrio entre densificación y espacio verde.",
                "weight": 20.0
            }
        ],
        "mid": [
            [0, 4, 3, 2, 3, 2],
            [3, 0, 2, 2, 3, 2],
            [3, 2, 0, 1, 2, 1],
            [2, 3, 1, 0, 2, 1],
            [3, 3, 2, 2, 0, 2],
            [2, 2, 1, 1, 2, 0]
        ],
        "mao2": [
            [4, 3, 2, 3],
            [2, 4, -1, 2],
            [4, 2, 1, 3],
            [3, 4, -2, 3],
            [3, 2, 3, 2],
            [2, -1, 4, 2]
        ]
    },

    # -------------------------------------------------------------
    # 4. COLOMBIA: BOGOTÁ Y SABANA - REGIÓN METROPOLITANA Y AMBIENTE
    # -------------------------------------------------------------
    "bogota_sabana_vanderhammen": {
        "id": "bogota_sabana_vanderhammen",
        "title": "Bogotá y Sabana: Región Metropolitana, Movilidad y Reserva Thomas van der Hammen",
        "territory": "Bogotá y Sabana",
        "country": "Colombia",
        "sector": "Ordenamiento Territorial, Movilidad & Reserva Forestal",
        "description": "Disputa sobre la gobernanza regional, integración de trenes de cercanías (RegioTram), urbanización de la Sabana y preservación estricta de la Reserva Forestal Van der Hammen.",
        "source": "Sentencias Consejo de Estado, Ley de Región Metropolitana y acuerdos CAR Cundinamarca.",
        "variant": "softprosp",
        "actors": [
            {
                "id": "A1",
                "name": "Alcaldía Mayor de Bogotá D.C.",
                "short_name": "Alcaldía Mayor",
                "category": "Gobierno Distrital",
                "base_power": 4,
                "evidence": "Lidera la primera y segunda línea del Metro y la integración de transporte de la capital."
            },
            {
                "id": "A2",
                "name": "Gobernación de Cundinamarca & Municipios de la Sabana",
                "short_name": "Cundinamarca & Municipios",
                "category": "Gobierno Departamental",
                "base_power": 3,
                "evidence": "Promueven RegioTram de Occidente y Norte y defienden autonomía municipal frente a Bogotá."
            },
            {
                "id": "A3",
                "name": "Ministerio de Ambiente & CAR Cundinamarca",
                "short_name": "MinAmbiente & CAR",
                "category": "Autoridad Ambiental",
                "base_power": 4,
                "evidence": "Custodios del régimen de usos del suelo de la Reserva Van der Hammen y cuenca del Río Bogotá."
            },
            {
                "id": "A4",
                "name": "Gremio Inmobiliario y Constructor (CAMACOL)",
                "short_name": "Constructores (CAMACOL)",
                "category": "Sector Privado",
                "base_power": 3,
                "evidence": "Demandan habilitación de suelo urbanizable en el borde norte y municipios conurbados."
            },
            {
                "id": "A5",
                "name": "Veedurías Ciudadanas y Colectivos Ambientales de la Sabana",
                "short_name": "Colectivos Ambientales",
                "category": "Sociedad Civil",
                "base_power": 2,
                "evidence": "Exigen restauración integral de la reserva y respeto a la estructura ecológica principal."
            },
            {
                "id": "A6",
                "name": "Empresa de Acueducto y Alcantarillado de Bogotá (EAAB)",
                "short_name": "Acueducto Bogotá (EAAB)",
                "category": "Empresa de Servicios",
                "base_power": 3,
                "evidence": "Garantiza el suministro hídrico de Chingaza y Tibitoc para más de 10 millones de habitantes."
            }
        ],
        "objectives": [
            {
                "id": "O1",
                "name": "Consolidación de la Región Metropolitana y Trenes Eléctricos (RegioTram)",
                "short_name": "RegioTram & Región (30%)",
                "description": "Integración tarifaria y física del transporte masivo entre Bogotá y los municipios satélite.",
                "weight": 30.0
            },
            {
                "id": "O2",
                "name": "Blindaje Ecológico y Restauración de la Reserva Van der Hammen",
                "short_name": "Reserva Van der Hammen (30%)",
                "description": "Prohibición de sustracciones viales de alto impacto y compra pública de predios para conectividad biológica.",
                "weight": 30.0
            },
            {
                "id": "O3",
                "name": "Seguridad Hídrica Estructural y Resiliencia de Embalses",
                "short_name": "Seguridad Hídrica (20%)",
                "description": "Modernización de plantas de tratamiento, reducción de pérdidas y protección de páramos Chingaza y Sumapaz.",
                "weight": 20.0
            },
            {
                "id": "O4",
                "name": "Expansión Sostenible de Vivienda de Interés Social (VIS)",
                "short_name": "Vivienda Asequible (20%)",
                "description": "Planificación de macroproyectos habitacionales con equipamientos sociales y servicios públicos asegurados.",
                "weight": 20.0
            }
        ],
        "mid": [
            [0, 3, 3, 2, 2, 3],
            [3, 0, 2, 3, 1, 2],
            [4, 3, 0, 3, 3, 3],
            [2, 3, 1, 0, 1, 2],
            [2, 2, 3, 1, 0, 2],
            [3, 2, 3, 1, 1, 0]
        ],
        "mao2": [
            [4, 2, 4, 3],
            [4, 0, 3, 4],
            [2, 4, 4, -2],
            [2, -3, 1, 4],
            [1, 4, 4, -1],
            [3, 3, 4, 2]
        ]
    },

    # -------------------------------------------------------------
    # 5. COLOMBIA: AMAZONÍA - DEFORESTACIÓN, COLONIZACIÓN Y MERCADOS DE CARBONO
    # -------------------------------------------------------------
    "amazonia_deforestacion_redd": {
        "id": "amazonia_deforestacion_redd",
        "title": "Amazonía Colombiana: Arco de Deforestación, Frontera Agrícola y Créditos de Carbono",
        "territory": "Caquetá y Guaviare",
        "country": "Colombia",
        "sector": "Conservación de Bosques, Paz Total y Bioeconomía",
        "description": "Dilema socioambiental en torno a la ganadería extensiva, acuerdos de conservación con campesinos, gobernanza de resguardos indígenas y transparencia en proyectos REDD+.",
        "source": "Monitoreo IDEAM, Parques Nacionales Naturales e investigaciones sobre gobernanza climática en la Amazonía.",
        "variant": "softprosp",
        "actors": [
            {
                "id": "A1",
                "name": "Ministerio de Ambiente y Parques Nacionales Naturales",
                "short_name": "MinAmbiente & PNN",
                "category": "Gobierno Central",
                "base_power": 4,
                "evidence": "Encabeza la estrategia de contención de la deforestación y delimitación de la frontera agrícola."
            },
            {
                "id": "A2",
                "name": "Pueblos Indígenas de la Amazonía (OPIAC)",
                "short_name": "Indígenas (OPIAC)",
                "category": "Pueblos Originarios",
                "base_power": 3,
                "evidence": "Administran resguardos que preservan el 80% de la biomasa boscosa y exigen autonomía de fondos verdes."
            },
            {
                "id": "A3",
                "name": "Asociaciones Campesinas y Colonos de Reserva Campesina",
                "short_name": "Campesinos & Colonos",
                "category": "Comunidades Rurales",
                "base_power": 3,
                "evidence": "Habitan zonas amortiguadoras, reclaman titulación de tierras, vías terciarias y proyectos productivos sostenibles."
            },
            {
                "id": "A4",
                "name": "Sector Ganadero y Agropecuario Regional",
                "short_name": "Gremios Ganaderos",
                "category": "Sector Productivo",
                "base_power": 3,
                "evidence": "Grandes tenedores de ganado bovino, impulsan la reconversión silvopastoril pero defienden sus títulos."
            },
            {
                "id": "A5",
                "name": "Desarrolladores Privados de Proyectos REDD+ y Carbono",
                "short_name": "Empresas Carbono REDD+",
                "category": "Sector Financiero Verde",
                "base_power": 2,
                "evidence": "Estructuran contratos de créditos de carbono con comunidades para su venta a multinacionales."
            },
            {
                "id": "A6",
                "name": "Cooperación Internacional y Fondo Amazonía (Alemania, Noruega, UK)",
                "short_name": "Cooperación Multilateral",
                "category": "Cooperación Internacional",
                "base_power": 3,
                "evidence": "Condicionan desembolsos financieros no reembolsables al cumplimiento verificable de metas de reducción de tala."
            }
        ],
        "objectives": [
            {
                "id": "O1",
                "name": "Meta de Cero Deforestación Neta y Cierre de Frontera Agrícola",
                "short_name": "Cero Deforestación (30%)",
                "description": "Operativos de control territorial, monitoreo satelital y prohibición de quemas.",
                "weight": 30.0
            },
            {
                "id": "O2",
                "name": "Autonomía Indígena y Gobierno Propio sobre Fondos Ambientales",
                "short_name": "Gobernanza Indígena (25%)",
                "description": "Manejo directo de recursos climáticos sin intermediación indebida de terceros.",
                "weight": 25.0
            },
            {
                "id": "O3",
                "name": "Formalización de Tierras y Pago por Servicios Ambientales Campesinos",
                "short_name": "Tierras y PSA (25%)",
                "description": "Contratos de concesión forestal campesina que permitan vivir del bosque en pie sin talar.",
                "weight": 25.0
            },
            {
                "id": "O4",
                "name": "Auditoría Estricta y Reparto Justo en Mercados Voluntarios de Carbono",
                "short_name": "Integridad REDD+ (20%)",
                "description": "Regulación estatal para evitar abusos contractuales y garantizar trazabilidad ecológica del crédito.",
                "weight": 20.0
            }
        ],
        "mid": [
            [0, 3, 3, 3, 3, 3],
            [3, 0, 2, 2, 3, 3],
            [2, 2, 0, 3, 2, 2],
            [2, 1, 3, 0, 1, 1],
            [2, 3, 2, 1, 0, 2],
            [3, 3, 2, 2, 2, 0]
        ],
        "mao2": [
            [4, 3, 3, 3],
            [3, 4, 1, 4],
            [1, 1, 4, 2],
            [-2, -1, 2, 1],
            [1, -2, 1, -3],
            [4, 3, 3, 4]
        ]
    },

    # -------------------------------------------------------------
    # 6. CHILE: SALAR DE ATACAMA - LITIO, CODELCO Y COMUNIDADES
    # -------------------------------------------------------------
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
    },

    # -------------------------------------------------------------
    # 7. ARGENTINA: VACA MUERTA - FRACKING, GNL Y COMUNIDADES MAPUCHE
    # -------------------------------------------------------------
    "vaca_muerta_neuquen": {
        "id": "vaca_muerta_neuquen",
        "title": "Vaca Muerta: Hidrocarburos No Convencionales, Exportación de GNL y Tierras Mapuche",
        "territory": "Cuenca Neuquina (Vaca Muerta)",
        "country": "Argentina",
        "sector": "Gas, Petróleo y Derechos Indígenas",
        "description": "Tensión estratégica entre la meta de autoabastecimiento energético y exportación de gas licuado frente a demandas territoriales mapuches, sismicidad inducida y uso intensivo de agua.",
        "source": "Secretaría de Energía de la Nación, Informes IAPG y declaraciones de la Confederación Mapuche de Neuquén.",
        "variant": "softprosp",
        "actors": [
            {
                "id": "A1",
                "name": "YPF & Secretaría de Energía de la Nación",
                "short_name": "YPF & Nación",
                "category": "Estado y Operadora Nacional",
                "base_power": 4,
                "evidence": "Lideran el proyecto de GNL en Río Negro y expansión de pozos horizontales en Añelo."
            },
            {
                "id": "A2",
                "name": "Gobierno de la Provincia del Neuquén",
                "short_name": "Provincia de Neuquén",
                "category": "Gobierno Provincial",
                "base_power": 3,
                "evidence": "Titular del dominio originario de los recursos, recauda regalías y regula el ordenamiento del suelo."
            },
            {
                "id": "A3",
                "name": "Operadoras Petroleras Internacionales (Chevron, Vista, Total)",
                "short_name": "Operadoras Multinacionales",
                "category": "Sector Privado",
                "base_power": 4,
                "evidence": "Invierten miles de millones de dólares en fracturación hidráulica y reclaman libre disponibilidad de divisas."
            },
            {
                "id": "A4",
                "name": "Confederación Mapuche de Neuquén",
                "short_name": "Confederación Mapuche",
                "category": "Comunidades Indígenas",
                "base_power": 3,
                "evidence": "Exigen relevamiento territorial (Ley 26.160), consulta previa y denuncian basureros petroleros ilegales."
            },
            {
                "id": "A5",
                "name": "Sindicato de Petróleo y Gas Privado de Río Negro y Neuquén",
                "short_name": "Sindicato Petrolero",
                "category": "Movimiento Sindical",
                "base_power": 3,
                "evidence": "Representa a 25.000 trabajadores; clave en productividad y convenios de paz social en yacimientos."
            },
            {
                "id": "A6",
                "name": "Asambleas Socioambientales del Agua del Comahue",
                "short_name": "Asambleas del Agua",
                "category": "ONGs Ambientalistas",
                "base_power": 2,
                "evidence": "Litigan judicialmente contra la sismicidad por pozos de inyección y contaminación de ríos Limay y Neuquén."
            }
        ],
        "objectives": [
            {
                "id": "O1",
                "name": "Aceleración de Oleoductos, Gasoductos y Planta de GNL",
                "short_name": "Megaproyecto GNL (30%)",
                "description": "Completar la infraestructura de transporte masivo para exportar energía al mercado global.",
                "weight": 30.0
            },
            {
                "id": "O2",
                "name": "Relevamiento Territorial y Consulta Previa a Comunidades",
                "short_name": "Consulta Mapuche (25%)",
                "description": "Delimitación formal de tierras ancestrales y participación en beneficios del subsuelo.",
                "weight": 25.0
            },
            {
                "id": "O3",
                "name": "Mitigación de Sismicidad Inducida y Tratamiento de Aguas Residuales",
                "short_name": "Control Ambiental Fracking (25%)",
                "description": "Auditorías geológicas a pozos sumideros y prohibición de vertidos tóxicos sin reciclar.",
                "weight": 25.0
            },
            {
                "id": "O4",
                "name": "Empleo Local, Seguridad Ocupacional y Renta Provincial",
                "short_name": "Empleo & Regalías (20%)",
                "description": "Prioridad en mano de obra neuquina, infraestructura urbana en Añelo y regalías coparticipables.",
                "weight": 20.0
            }
        ],
        "mid": [
            [0, 3, 3, 2, 3, 1],
            [3, 0, 2, 2, 2, 1],
            [3, 2, 0, 2, 3, 1],
            [2, 3, 2, 0, 1, 3],
            [3, 2, 3, 1, 0, 1],
            [1, 2, 2, 3, 1, 0]
        ],
        "mao2": [
            [4, 1, 2, 3],
            [3, 2, 2, 4],
            [4, -2, 1, 2],
            [-3, 4, 4, 1],
            [3, 0, 1, 4],
            [-2, 4, 4, 0]
        ]
    },

    # -------------------------------------------------------------
    # 8. PERÚ: CORREDOR MINERO DEL SUR - LAS BAMBAS Y COMUNIDADES
    # -------------------------------------------------------------
    "corredor_minero_peru": {
        "id": "corredor_minero_peru",
        "title": "Corredor Minero del Sur del Perú: Las Bambas, Carretera y Comunidades Campesinas",
        "territory": "Apurímac y Cusco",
        "country": "Perú",
        "sector": "Minería de Cobre & Conflictividad Social Vial",
        "description": "Disputa por el tránsito pesado de camiones concentrados de cobre a lo largo de 480 km de carretera andina no pavimentada que cruza decenas de comunidades quechuas.",
        "source": "Reportes de Conflictos Sociales de la Defensoría del Pueblo del Perú y comunicados de Minera Las Bambas.",
        "variant": "softprosp",
        "actors": [
            {
                "id": "A1",
                "name": "Presidencia del Consejo de Ministros (PCM) & Minem",
                "short_name": "Gobierno Central (PCM)",
                "category": "Poder Ejecutivo",
                "base_power": 4,
                "evidence": "Declara estados de emergencia viales y articula mesas de diálogo multisectoriales."
            },
            {
                "id": "A2",
                "name": "Minera Las Bambas (MMG Limited)",
                "short_name": "Minera Las Bambas",
                "category": "Sector Privado",
                "base_power": 4,
                "evidence": "Produce el 2% del cobre mundial; sufre paralizaciones periódicas por bloqueos comunales."
            },
            {
                "id": "A3",
                "name": "Comunidades Campesinas del Corredor (Chumbivilcas / Cotabambas)",
                "short_name": "Comunidades Campesinas",
                "category": "Comunidades Rurales",
                "base_power": 3,
                "evidence": "Exigen pago de servidumbres de paso, remediación del polvo y ruidos, e inclusión como proveedores comunales."
            },
            {
                "id": "A4",
                "name": "Gobierno Regional de Apurímac",
                "short_name": "Gobierno Regional",
                "category": "Gobierno Regional",
                "base_power": 3,
                "evidence": "Exige el pago efectivo de regalías contractuales e impuestos para cerrar brechas de pobreza extrema."
            },
            {
                "id": "A5",
                "name": "Defensoría del Pueblo del Perú",
                "short_name": "Defensoría del Pueblo",
                "category": "Órgano Autónomo Constitucional",
                "base_power": 3,
                "evidence": "Media en los conflictos, verifica el uso proporcional de la fuerza policial y vigila acuerdos firmados."
            },
            {
                "id": "A6",
                "name": "Gremios de Transportistas Locales de Carga",
                "short_name": "Transportistas Locales",
                "category": "Pequeña Empresa",
                "base_power": 2,
                "evidence": "Demandan cuotas reservadas para el transporte de insumos y concentrados frente a empresas foráneas."
            }
        ],
        "objectives": [
            {
                "id": "O1",
                "name": "Garantía de Tránsito Ininterrumpido de Concentrados de Cobre",
                "short_name": "Tránsito Libre Minero (30%)",
                "description": "Evitar bloqueos viales que fuercen la paralización de la mina y el puerto de Matarani.",
                "weight": 30.0
            },
            {
                "id": "O2",
                "name": "Pavimentación Integral y Proyecto del Ferrocarril Minero",
                "short_name": "Ferrocarril / Asfalto (25%)",
                "description": "Solución técnica definitiva que elimine la polución de polvo en las parcelas agrícolas.",
                "weight": 25.0
            },
            {
                "id": "O3",
                "name": "Convenios Marco y Participación Económica Comunal",
                "short_name": "Convenios Comunales (25%)",
                "description": "Aporte social directo, empleo comunal no calificado y compras locales prioritarias.",
                "weight": 25.0
            },
            {
                "id": "O4",
                "name": "Transferencia Efectiva de Canon Minero para Agua y Hospitales",
                "short_name": "Canon y Desarrollo (20%)",
                "description": "Inversión transparente de las rentas mineras en los pueblos de influencia directa.",
                "weight": 20.0
            }
        ],
        "mid": [
            [0, 3, 3, 3, 2, 2],
            [3, 0, 3, 2, 1, 2],
            [3, 3, 0, 2, 2, 2],
            [2, 3, 2, 0, 1, 1],
            [3, 2, 2, 2, 0, 1],
            [1, 2, 2, 1, 1, 0]
        ],
        "mao2": [
            [4, 3, 2, 3],
            [4, 2, -1, 2],
            [-3, 4, 4, 3],
            [2, 3, 3, 4],
            [1, 3, 3, 3],
            [1, 1, 3, 2]
        ]
    },

    # -------------------------------------------------------------
    # 9. MÉXICO: PENÍNSULA DE YUCATÁN - TREN MAYA Y ECOSISTEMA KÁRSTICO
    # -------------------------------------------------------------
    "tren_maya_yucatan": {
        "id": "tren_maya_yucatan",
        "title": "Península de Yucatán: Tren Maya, Turismo Sostenible y Acuífero Kárstico",
        "territory": "Quintana Roo y Yucatán",
        "country": "México",
        "sector": "Transporte Ferroviario, Turismo & Ecosistema de Cenotes",
        "description": "Impactos y tensiones entre la aceleración del Tren Maya por la selva tropical, la conservación de cenotes y cavernas subterráneas, y el desarrollo de comunidades mayas.",
        "source": "Manifiestos de Impacto Ambiental SEMARNAT, amparos judiciales y colectivos espeleológicos del Caribe.",
        "variant": "softprosp",
        "actors": [
            {
                "id": "A1",
                "name": "Gobierno Federal & SEDENA (Operadora Ferroviaria)",
                "short_name": "Gobierno Federal / SEDENA",
                "category": "Gobierno Federal",
                "base_power": 4,
                "evidence": "Ejecuta y administra el Tren Maya con declaratoria de obra de seguridad nacional."
            },
            {
                "id": "A2",
                "name": "Comunidades Mayas y Colectivos Ejidales",
                "short_name": "Comunidades Mayas",
                "category": "Pueblos Originarios",
                "base_power": 3,
                "evidence": "Demandan respeto a tierras comunales ejidales, freno a la gentrificación y reparto de polos de desarrollo."
            },
            {
                "id": "A3",
                "name": "Científicos, Espeleólogos y Colectivos 'Sélvame del Tren'",
                "short_name": "Científicos & Ambientalistas",
                "category": "Sociedad Civil",
                "base_power": 2,
                "evidence": "Documentan el colapso de cavernas por pilotes de acero y contaminación del agua dulce subterránea."
            },
            {
                "id": "A4",
                "name": "Cámaras Hoteleras y de Comercio (Cancún / Riviera Maya)",
                "short_name": "Sector Hotelero y Turismo",
                "category": "Sector Privado",
                "base_power": 3,
                "evidence": "Buscan capturar el flujo turístico de Cancún hacia el sur de Quintana Roo y zonas arqueológicas."
            },
            {
                "id": "A5",
                "name": "SEMARNAT & Procuraduría Federal de Protección al Ambiente (PROFEPA)",
                "short_name": "Autoridad Ambiental",
                "category": "Regulador Ambiental",
                "base_power": 3,
                "evidence": "Fiscaliza medidas de mitigación, pasos de fauna y reforestación de áreas impactadas."
            },
            {
                "id": "A6",
                "name": "Poder Judicial de la Federación (Jueces de Amparo)",
                "short_name": "Poder Judicial",
                "category": "Rama Judicial",
                "base_power": 3,
                "evidence": "Tramita suspensiones definitivas solicitadas por ambientalistas y comunidades indígenas."
            }
        ],
        "objectives": [
            {
                "id": "O1",
                "name": "Operación Plena de Pasajeros y Transporte de Carga Ferroviaria",
                "short_name": "Operación Tren Maya (30%)",
                "description": "Conectar los 1.554 km del circuito para detonar el turismo masivo y logística de carga.",
                "weight": 30.0
            },
            {
                "id": "O2",
                "name": "Protección Estricta del Sistema de Cenotes y Ríos Subterráneos",
                "short_name": "Protección Acuífero Cenotes (30%)",
                "description": "Blindar el manto freático contra corrosión de pilotes y derrames de combustibles.",
                "weight": 30.0
            },
            {
                "id": "O3",
                "name": "Inclusión Comunitaria en Polos de Desarrollo y Tenencia Ejidal",
                "short_name": "Desarrollo Ejidal Maya (20%)",
                "description": "Evitar el despojo de tierras y asegurar que las estaciones generen empleo local de calidad.",
                "weight": 20.0
            },
            {
                "id": "O4",
                "name": "Conectividad Biológica y Cumplimiento de Pasos de Fauna",
                "short_name": "Corredores Biológicos (20%)",
                "description": "Preservar el paso seguro del jaguar y fauna silvestre entre reservas de Calakmul y Sian Ka'an.",
                "weight": 20.0
            }
        ],
        "mid": [
            [0, 3, 2, 3, 3, 3],
            [2, 0, 3, 2, 2, 3],
            [1, 2, 0, 2, 2, 3],
            [2, 1, 1, 0, 2, 1],
            [3, 2, 2, 2, 0, 2],
            [3, 2, 3, 1, 3, 0]
        ],
        "mao2": [
            [4, 0, 2, 2],
            [2, 4, 4, 3],
            [-3, 4, 2, 4],
            [4, 1, 1, 1],
            [2, 3, 2, 4],
            [1, 3, 2, 3]
        ]
    },

    # -------------------------------------------------------------
    # 10. ESPAÑA: DOÑANA Y EL MAR MENOR - REGADÍOS Y HUMEDALES
    # -------------------------------------------------------------
    "donana_mar_menor_espana": {
        "id": "donana_mar_menor_espana",
        "title": "Doñana y Mar Menor: Agricultura Intensiva de Regadío vs Conservación de Humedales",
        "territory": "Andalucía y Murcia",
        "country": "España",
        "sector": "Agroindustria, Recursos Hídricos y Protección Europea",
        "description": "Pugna entre la agricultura intensiva de fresas y hortalizas bajo plástico frente a la desecación del acuífero de Doñana, la eutrofización del Mar Menor y las sanciones de la Unión Europea.",
        "source": "Marco de Actuaciones MITECO, Sentencias del Tribunal de Justicia de la UE y Ley de Personalidad Jurídica del Mar Menor.",
        "variant": "softprosp",
        "actors": [
            {
                "id": "A1",
                "name": "Ministerio para la Transición Ecológica (MITECO) & Comisión Europea",
                "short_name": "MITECO & UE",
                "category": "Gobierno Central y Europeo",
                "base_power": 4,
                "evidence": "Exige el cierre de pozos ilegales y financia planes millonarios de restauración ecológica."
            },
            {
                "id": "A2",
                "name": "Junta de Andalucía & Gobierno de la Región de Murcia",
                "short_name": "Gobiernos Autonómicos",
                "category": "Administración Autonómica",
                "base_power": 3,
                "evidence": "Tienen competencias de agricultura y ordenación del territorio; enfrentan presión de agricultores locales."
            },
            {
                "id": "A3",
                "name": "Asociaciones de Agricultores y Comunidades de Regantes",
                "short_name": "Regantes y Agroindustria",
                "category": "Sector Productivo",
                "base_power": 3,
                "evidence": "Generan miles de empleos en exportación de frutos rojos; reclaman trasvases de agua y regularizaciones."
            },
            {
                "id": "A4",
                "name": "Organizaciones Ecologistas (WWF España, SEO BirdLife, Greenpeace)",
                "short_name": "ONGs Ecologistas",
                "category": "Sociedad Civil",
                "base_power": 3,
                "evidence": "Denuncian el expolio del agua subterránea ante Bruselas y exigen medidas cautelares inmediatas."
            },
            {
                "id": "A5",
                "name": "Comunidad Científica (CSIC / Instituto Español de Oceanografía)",
                "short_name": "Comunidad Científica",
                "category": "Academia e Investigación",
                "base_power": 2,
                "evidence": "Monitorea la pérdida de lagunas permanentes en Doñana y la anoxia marina en el Mar Menor."
            },
            {
                "id": "A6",
                "name": "Sector Turístico, Hotelero y Vecinal Costero",
                "short_name": "Turismo & Vecinos",
                "category": "Sector Servicios",
                "base_power": 2,
                "evidence": "Afectados por la degradación del paisaje costero y la pérdida de valor de propiedades."
            }
        ],
        "objectives": [
            {
                "id": "O1",
                "name": "Clausura Definitiva de Pozos Ilegales y Reducción de Regadío",
                "short_name": "Cierre Pozos Ilegales (30%)",
                "description": "Ajustar las extracciones hídricas a la capacidad real de recarga de los acuíferos.",
                "weight": 30.0
            },
            {
                "id": "O2",
                "name": "Protección de la Renta y Reconversión de Cultivos Agrícolas",
                "short_name": "Transición Agrícola Justa (25%)",
                "description": "Fondos de compensación económica para agricultores que abandonen regadíos intensivos.",
                "weight": 25.0
            },
            {
                "id": "O3",
                "name": "Regeneración Ecológica de Humedales y Acuíferos",
                "short_name": "Regeneración Ecológica (25%)",
                "description": "Reforestación de riberas, eliminación de nitratos y restauración de la marisma.",
                "weight": 25.0
            },
            {
                "id": "O4",
                "name": "Seguridad Jurídica y Cumplimiento de Sentencias Europeas (TJUE)",
                "short_name": "Cumplimiento Directivas UE (20%)",
                "description": "Evitar multas millonarias de la UE y boicots comerciales internacionales a exportaciones españolas.",
                "weight": 20.0
            }
        ],
        "mid": [
            [0, 3, 3, 3, 3, 2],
            [3, 0, 3, 2, 2, 2],
            [2, 3, 0, 1, 1, 1],
            [3, 2, 2, 0, 3, 2],
            [3, 2, 1, 2, 0, 1],
            [2, 2, 2, 2, 1, 0]
        ],
        "mao2": [
            [4, 2, 4, 4],
            [2, 3, 2, 2],
            [-3, 4, -1, -2],
            [4, -1, 4, 4],
            [4, 0, 4, 3],
            [2, 0, 3, 2]
        ]
    },

    # -------------------------------------------------------------
    # 11. CONO SUR: HIDROVÍA PARANÁ-PARAGUAY - NAVEGACIÓN Y GEOPOLÍTICA
    # -------------------------------------------------------------
    "hidrovia_parana_paraguay": {
        "id": "hidrovia_parana_paraguay",
        "title": "Hidrovía Paraná-Paraguay: Soberanía Fluvial, Dragado a Gran Escala y Transporte de Granos",
        "territory": "Cuenca del Plata (Paraná-Paraguay)",
        "country": "Internacional",
        "sector": "Transporte Fluvial, Dragado y Comercio Exterior",
        "description": "Disputa multilateral por el calado y peaje de la principal arteria logística por donde sale el 80% de las exportaciones agroindustriales del Cono Sur hacia ultramar.",
        "source": "Comisión Intergubernamental de la Hidrovía (CIH), acuerdos de Cancillerías y cámaras exportadoras.",
        "variant": "softprosp",
        "actors": [
            {
                "id": "A1",
                "name": "Gobierno de Argentina & Administración General de Puertos (AGP)",
                "short_name": "Gobierno Argentino & AGP",
                "category": "Estado Ribereño Concesionario",
                "base_power": 4,
                "evidence": "Controla el tramo troncal del Río Paraná y cobra el peaje de navegación a buques internacionales."
            },
            {
                "id": "A2",
                "name": "Gobierno y Armadores Fluviales del Paraguay (CAFyM)",
                "short_name": "Paraguay & Armadores Fluviales",
                "category": "País Sin Litoral & Flota Fluvial",
                "base_power": 3,
                "evidence": "Opera la tercera flota de barcazas más grande del mundo y rechaza peajes unilaterales."
            },
            {
                "id": "A3",
                "name": "Cámaras Agroexportadoras Multinacionales (CIARA-CEC / Cargill / Bunge)",
                "short_name": "Agroexportadoras (CIARA-CEC)",
                "category": "Sector Privado Global",
                "base_power": 4,
                "evidence": "Exigen mayor profundidad de dragado (40 pies) para abaratar fletes de granos a China y Europa."
            },
            {
                "id": "A4",
                "name": "Provincias Ribereñas del Litoral Argentino (Santa Fe / Entre Ríos)",
                "short_name": "Provincias del Litoral",
                "category": "Gobiernos Subnacionales",
                "base_power": 3,
                "evidence": "Reclaman participación en la licitación del dragado y desarrollo de puertos públicos provinciales."
            },
            {
                "id": "A5",
                "name": "Colectivos Ambientales de los Humedales del Delta del Paraná",
                "short_name": "Defensores de Humedales",
                "category": "Sociedad Civil",
                "base_power": 2,
                "evidence": "Advierten sobre el impacto del sobre-dragado en la salinización de tomas de agua y erosión costera."
            }
        ],
        "objectives": [
            {
                "id": "O1",
                "name": "Dragado y Señalización de Calado Profundo para Buques Panamax",
                "short_name": "Mayor Calado (35%)",
                "description": "Llevar la vía a 36-40 pies para cargar buques al 100% sin depender de trasbordos caros.",
                "weight": 35.0
            },
            {
                "id": "O2",
                "name": "Tarifa Justa de Peaje y Libre Navegación Multilateral",
                "short_name": "Peaje Concertado (25%)",
                "description": "Acuerdo vinculante en el marco del Tratado de Las Leñas que asegure previsibilidad tarifaria.",
                "weight": 25.0
            },
            {
                "id": "O3",
                "name": "Protección Ambiental de los Humedales del Delta y Calidad del Agua",
                "short_name": "Protección del Delta (20%)",
                "description": "Límites al vertido de sedimentos de dragado y monitoreo de la dinámica hidrológica.",
                "weight": 20.0
            },
            {
                "id": "O4",
                "name": "Control Aduanero y Prevención del Contrabando y Narcotráfico Fluvial",
                "short_name": "Seguridad y Soberanía (20%)",
                "description": "Escáneres modernos y fiscalización estatal de barcazas en tránsito internacional.",
                "weight": 20.0
            }
        ],
        "mid": [
            [0, 3, 3, 3, 1],
            [3, 0, 3, 2, 1],
            [3, 3, 0, 2, 1],
            [3, 2, 2, 0, 1],
            [2, 1, 1, 2, 0]
        ],
        "mao2": [
            [3, 3, 2, 4],
            [3, -3, 1, 1],
            [4, -1, -2, 2],
            [3, 2, 2, 3],
            [-2, 1, 4, 1]
        ]
    }
}
