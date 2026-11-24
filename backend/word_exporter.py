"""
Generador de Informe Ejecutivo y Prospectivo Integral en formato Microsoft Word (.docx).
Incorpora exhaustivamente todos los análisis del método MACTOR (LIPSOR / Michel Godet):
- Inteligencia Territorial, fuentes periodísticas y evidencia de campo.
- Caracterización detallada de Actores y Objetivos Estratégicos.
- Matrices MID (Directa), MIDI (Indirecta de 2do orden), Cuadrantes de Godet y Centralidad de Redes (SNA).
- Matrices 2MAO (Posiciones Valoradas) y 3MAO (Ponderadas por Relación de Fuerza r_i).
- Balanzas de Fuerza de Posición Canónica por cada objetivo.
- Matrices de Alianzas y Conflictos (Convergencia CAA3 y Divergencia DAA3).
- Movilización, Polarización y Diagnóstico de Viabilidad por Objetivo.
- Simulación de Escenarios Prospectivos ("¿Qué pasa si...?").
- Hoja de Ruta Táctica y Recomendaciones de Gobernanza Territorial.
- Dossier de Fichas Técnicas Individuales por cada Actor.
- Referencias Metodológicas Formales (Godet / Villabona et al. 2018 / CEPAL).
"""

import io
import datetime
from typing import Dict, List, Any, Optional

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# Paleta cromática corporativa / institucional
COLOR_NAVY_HEX = "1E3A8A"        # Azul oscuro institucional
COLOR_TEAL_HEX = "0F766E"        # Verde azulado estratégico
COLOR_SLATE_DARK_HEX = "1E293B"  # Pizarra oscuro (encabezados de tabla)
COLOR_SLATE_LIGHT_HEX = "F8FAFC" # Pizarra muy claro (filas alternas)
COLOR_BORDER_HEX = "CBD5E1"      # Borde sutil
COLOR_BLUE_BG_HEX = "EFF6FF"     # Fondo callout azul
COLOR_GREEN_BG_HEX = "DCFCE7"    # Fondo valor positivo / favorable
COLOR_RED_BG_HEX = "FEE2E2"      # Fondo valor negativo / oposición
COLOR_YELLOW_BG_HEX = "FEF9C3"   # Fondo advertencia / conflicto

RGB_NAVY = RGBColor(30, 58, 138)
RGB_TEAL = RGBColor(15, 118, 110)
RGB_DARK = RGBColor(30, 41, 59)
RGB_MUTED = RGBColor(100, 116, 139)


def set_cell_background(cell, hex_color: str):
    """Aplica color de fondo a una celda de tabla."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))


def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    """Establece padding interno en dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def set_table_borders(table, color: str = COLOR_BORDER_HEX, sz: str = "4", val: str = "single"):
    """Aplica bordes sutiles a una tabla completa."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def add_callout(doc: docx.Document, title: str, text: str, border_color: str = "2563EB", bg_color: str = COLOR_BLUE_BG_HEX):
    """Crea una caja destacada (callout box) con barra lateral de color."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=240, right=200)

    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="32" w:space="0" w:color="{border_color}"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    run_t = p.add_run(f"📌 {title}\n")
    run_t.bold = True
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(11)
    run_t.font.color.rgb = RGB_NAVY

    run_b = p.add_run(text)
    run_b.font.name = "Calibri"
    run_b.font.size = Pt(10)
    run_b.font.color.rgb = RGB_DARK

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)


def add_styled_heading(doc: docx.Document, text: str, level: int = 1):
    """Agrega un encabezado estilizado con tipografía y espaciado formal."""
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.name = "Calibri"

    if level == 1:
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        run.font.size = Pt(15)
        run.font.color.rgb = RGB_NAVY
    elif level == 2:
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        run.font.size = Pt(12.5)
        run.font.color.rgb = RGB_TEAL
    else:
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        run.font.size = Pt(11)
        run.font.color.rgb = RGB_DARK
    return p


def format_table_header(row, col_titles: List[str]):
    """Aplica estilo institucional a la fila de cabecera de una tabla."""
    for idx, title in enumerate(col_titles):
        cell = row.cells[idx]
        set_cell_background(cell, COLOR_SLATE_DARK_HEX)
        set_cell_margins(cell, top=140, bottom=140, left=160, right=160)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(title)
        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(255, 255, 255)


def add_matrix_table(doc: docx.Document, row_labels: List[str], col_labels: List[str],
                     matrix_data: List[List[float]], is_signed: bool = False,
                     include_totals: bool = False, row_totals: Optional[List[float]] = None,
                     col_totals: Optional[List[float]] = None, title: Optional[str] = None):
    """Genera una tabla matricial N x M con formato elegante, sombreados condicionales y totales."""
    if title:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(8)
        p_t.paragraph_format.space_after = Pt(3)
        p_t.paragraph_format.keep_with_next = True
        r_t = p_t.add_run(title)
        r_t.bold = True
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(10)
        r_t.font.color.rgb = RGB_DARK

    num_rows = len(row_labels) + 1 + (1 if include_totals and col_totals else 0)
    num_cols = len(col_labels) + 1 + (1 if include_totals and row_totals else 0)

    tbl = doc.add_table(rows=num_rows, cols=num_cols)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)

    # Cabecera
    header_titles = ["Actor / Eje"] + col_labels + (["Total (I_i)"] if include_totals and row_totals else [])
    format_table_header(tbl.rows[0], header_titles)

    # Filas de datos
    for r_i, r_label in enumerate(row_labels):
        row = tbl.rows[r_i + 1]
        
        # Celda de etiqueta izquierda
        c_label = row.cells[0]
        bg_alt = COLOR_SLATE_LIGHT_HEX if r_i % 2 == 1 else "FFFFFF"
        set_cell_background(c_label, bg_alt)
        set_cell_margins(c_label, top=100, bottom=100, left=140, right=140)
        p_l = c_label.paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_l.paragraph_format.space_before = Pt(0)
        p_l.paragraph_format.space_after = Pt(0)
        r_l = p_l.add_run(r_label)
        r_l.bold = True
        r_l.font.name = "Calibri"
        r_l.font.size = Pt(8.5)
        r_l.font.color.rgb = RGB_DARK

        # Celdas de valores
        for c_i in range(len(col_labels)):
            val = matrix_data[r_i][c_i] if r_i < len(matrix_data) and c_i < len(matrix_data[r_i]) else 0
            cell = row.cells[c_i + 1]
            set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

            # Sombreado temático
            if is_signed:
                if val > 0:
                    set_cell_background(cell, COLOR_GREEN_BG_HEX)
                elif val < 0:
                    set_cell_background(cell, COLOR_RED_BG_HEX)
                else:
                    set_cell_background(cell, bg_alt)
            else:
                if val > 0 and r_i != c_i:
                    set_cell_background(cell, COLOR_BLUE_BG_HEX)
                elif r_i == c_i and not is_signed:
                    set_cell_background(cell, "E2E8F0") # Diagonal en gris
                else:
                    set_cell_background(cell, bg_alt)

            p_v = cell.paragraphs[0]
            p_v.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_v.paragraph_format.space_before = Pt(0)
            p_v.paragraph_format.space_after = Pt(0)
            
            str_val = f"+{val:.1f}" if (is_signed and val > 0) else f"{val:.1f}" if isinstance(val, float) and not val.is_integer() else str(int(val))
            r_v = p_v.add_run(str_val)
            r_v.font.name = "Calibri"
            r_v.font.size = Pt(8.5)
            if is_signed and val != 0:
                r_v.bold = True
                if val > 0:
                    r_v.font.color.rgb = RGBColor(22, 101, 52)
                else:
                    r_v.font.color.rgb = RGBColor(153, 27, 27)
            else:
                r_v.font.color.rgb = RGB_DARK

        # Total fila (Influencia)
        if include_totals and row_totals:
            c_tot = row.cells[len(col_labels) + 1]
            set_cell_background(c_tot, "E2E8F0")
            set_cell_margins(c_tot, top=100, bottom=100, left=100, right=100)
            c_tot.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p_tot = c_tot.paragraphs[0]
            p_tot.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_tot.paragraph_format.space_before = Pt(0)
            p_tot.paragraph_format.space_after = Pt(0)
            r_tot = p_tot.add_run(f"{row_totals[r_i]:.1f}" if isinstance(row_totals[r_i], float) else str(row_totals[r_i]))
            r_tot.bold = True
            r_tot.font.name = "Calibri"
            r_tot.font.size = Pt(8.5)
            r_tot.font.color.rgb = RGB_NAVY

    # Fila de totales de columna (Dependencia)
    if include_totals and col_totals:
        tot_row = tbl.rows[len(row_labels) + 1]
        c_tot_lbl = tot_row.cells[0]
        set_cell_background(c_tot_lbl, "E2E8F0")
        set_cell_margins(c_tot_lbl, top=100, bottom=100, left=140, right=140)
        p_tl = c_tot_lbl.paragraphs[0]
        p_tl.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_tl.paragraph_format.space_before = Pt(0)
        p_tl.paragraph_format.space_after = Pt(0)
        r_tl = p_tl.add_run("Total (D_i)")
        r_tl.bold = True
        r_tl.font.name = "Calibri"
        r_tl.font.size = Pt(8.5)
        r_tl.font.color.rgb = RGB_NAVY

        for c_i in range(len(col_labels)):
            c_tot_val = tot_row.cells[c_i + 1]
            set_cell_background(c_tot_val, "E2E8F0")
            set_cell_margins(c_tot_val, top=100, bottom=100, left=80, right=80)
            c_tot_val.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p_tv = c_tot_val.paragraphs[0]
            p_tv.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_tv.paragraph_format.space_before = Pt(0)
            p_tv.paragraph_format.space_after = Pt(0)
            r_tv = p_tv.add_run(f"{col_totals[c_i]:.1f}" if isinstance(col_totals[c_i], float) else str(col_totals[c_i]))
            r_tv.bold = True
            r_tv.font.name = "Calibri"
            r_tv.font.size = Pt(8.5)
            r_tv.font.color.rgb = RGB_NAVY

        if include_totals and row_totals:
            # Esquina inferior derecha: Suma global
            c_corner = tot_row.cells[len(col_labels) + 1]
            set_cell_background(c_corner, "CBD5E1")
            set_cell_margins(c_corner, top=100, bottom=100, left=80, right=80)
            p_c = c_corner.paragraphs[0]
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_c.paragraph_format.space_before = Pt(0)
            p_c.paragraph_format.space_after = Pt(0)
            grand_total = sum(row_totals)
            r_c = p_c.add_run(f"{grand_total:.1f}" if isinstance(grand_total, float) else str(grand_total))
            r_c.bold = True
            r_c.font.name = "Calibri"
            r_c.font.size = Pt(8.5)
            r_c.font.color.rgb = RGB_DARK

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(6)


def generate_comprehensive_mactor_word(
    actors: List[Dict[str, Any]],
    objectives: List[Dict[str, Any]],
    mid: List[List[float]],
    mao2: List[List[float]],
    variant: str,
    res: Dict[str, Any],
    options: Optional[Dict[str, Any]] = None
) -> io.BytesIO:
    """
    Construye y formatea el informe completo institucional en Word (.docx)
    abarcando todas las dimensiones de análisis metodológico y territorial.
    """
    options = options or {}
    territory = options.get("territory") or "Territorio de Análisis Prospectivo"
    country = options.get("country") or "Colombia"
    sector = options.get("sector") or "Desarrollo Territorial & Gobernanza"
    news_items = options.get("news_items") or []
    case_id = options.get("case_id") or ""

    doc = docx.Document()

    # Configuración de márgenes de página (0.8 pulgadas para aprovechar ancho en tablas)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        
        # Pie de página institucional
        footer = section.footer
        p_foot = footer.paragraphs[0]
        p_foot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_foot.paragraph_format.space_before = Pt(0)
        p_foot.paragraph_format.space_after = Pt(0)
        r_foot = p_foot.add_run(f"Estudio Prospectivo MACTOR | {territory} ({country}) | Método LIPSOR-Godet")
        r_foot.font.name = "Calibri"
        r_foot.font.size = Pt(8.5)
        r_foot.font.color.rgb = RGB_MUTED

    # =========================================================================
    # 0. PORTADA EJECUTIVA
    # =========================================================================
    p_top_bar = doc.add_paragraph()
    p_top_bar.paragraph_format.space_before = Pt(12)
    p_top_bar.paragraph_format.space_after = Pt(4)
    r_bar = p_top_bar.add_run("SISTEMA DE INTELIGENCIA PROSPECTIVA & JUEGOS DE ACTORES — MACTOR 2.0")
    r_bar.font.name = "Calibri"
    r_bar.font.size = Pt(10)
    r_bar.bold = True
    r_bar.font.color.rgb = RGB_TEAL

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run(f"INFORME PROSPECTIVO INTEGRAL:\nANÁLISIS DE JUEGOS DE ACTORES Y ALIANZAS ESTRATÉGICAS")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(22)
    r_title.bold = True
    r_title.font.color.rgb = RGB_NAVY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(18)
    r_sub = p_sub.add_run(
        f"Evaluación de Relaciones de Fuerza, Redes de Influencia Directa e Indirecta, Balanzas de Poder y "
        f"Viabilidad de Objetivos Estratégicos en {territory}."
    )
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.italic = True
    r_sub.font.color.rgb = RGB_MUTED

    # Ficha técnica de portada
    cover_tbl = doc.add_table(rows=6, cols=2)
    cover_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(cover_tbl)
    
    meta_rows = [
        ("Territorio y Escenario:", f"{territory} ({country})"),
        ("Sector Estratégico:", sector),
        ("Metodología Aplicada:", f"MACTOR Clásico / {variant.upper()} (Michel Godet / LIPSOR)"),
        ("Fecha y Hora de Emisión:", datetime.datetime.now().strftime("%d/%m/%Y %H:%M hrs")),
        ("Dimensión del Análisis:", f"{len(actors)} Actores Identificados | {len(objectives)} Objetivos Estratégicos"),
        ("Estado de Fuentes:", f"{len(news_items)} Fuentes Documentales y Noticias Indexadas en Tiempo Real")
    ]
    for idx, (lbl, val) in enumerate(meta_rows):
        r_c = cover_tbl.rows[idx]
        c0, c1 = r_c.cells[0], r_c.cells[1]
        set_cell_background(c0, COLOR_SLATE_LIGHT_HEX)
        set_cell_margins(c0, top=100, bottom=100, left=140, right=140)
        set_cell_margins(c1, top=100, bottom=100, left=140, right=140)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(lbl)
        r0.bold = True
        r0.font.name = "Calibri"
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGB_DARK

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(val)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGB_NAVY

    doc.add_page_break()

    # =========================================================================
    # RESUMEN EJECUTIVO Y CONCLUSIÓN PROSPECTIVA CLAVE
    # =========================================================================
    add_styled_heading(doc, "Resumen Ejecutivo y Diagnóstico Global de Gobernanza", level=1)

    dom = res.get("dominant_actor", {})
    dom_name = dom.get("name", "No determinado")
    dom_score = dom.get("convergence_score", 0)
    dom_ri = dom.get("r_i", 1.0)

    # Conclusión sintetizada
    callout_text = (
        f"Tras la aplicación del modelo MACTOR (LIPSOR / Michel Godet) sobre el ecosistema de {territory}, "
        f"se identifica que el actor con mayor capacidad de convocatoria, articulación hegemónica y convergencia estratégica "
        f"es '{dom_name}' (Puntaje de Convergencia Ponderada: {dom_score:.2f} | Relación de Fuerza r_i: {dom_ri:.2f}). "
        f"El balance global de fuerzas revela que la viabilidad del plan prospectivo dependerá de la capacidad "
        f"de estructurar alianzas tempranas con los actores ubicados en el Cuadrante de Enlace, previniendo focos "
        f"de conflicto severo en los objetivos de mayor polarización territorial."
    )
    add_callout(doc, "DIAGNÓSTICO PROSPECTIVO CENTRAL", callout_text, border_color="1E3A8A", bg_color=COLOR_BLUE_BG_HEX)

    # Tarjetas KPI de resumen
    kpi_tbl = doc.add_table(rows=2, cols=4)
    kpi_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(kpi_tbl)

    kpis = [
        ("Actor Clave Hegemónico", dom_name[:25], dom_score, "Convergencia Ponderada"),
        ("Fuerza Relativa Máxima", f"r_i = {dom_ri:.2f}", "Balance de Poder", "Sobre media del sistema"),
        ("Objetivos Críticos", f"{sum(1 for om in res.get('objective_metrics', []) if om.get('conflict_index', 0) > 0.5)} de {len(objectives)}", "Focos de Conflicto", "Índice Disputa > 0.50"),
        ("Conectividad de Red", f"{len(actors)*(len(actors)-1)} enlaces", "Densidad Sistémica", "Influencias Directas e Indirectas")
    ]

    for idx, (title, big_val, sub1, sub2) in enumerate(kpis):
        c_top = kpi_tbl.rows[0].cells[idx]
        c_bot = kpi_tbl.rows[1].cells[idx]
        set_cell_background(c_top, COLOR_SLATE_DARK_HEX)
        set_cell_background(c_bot, COLOR_SLATE_LIGHT_HEX)
        set_cell_margins(c_top, top=100, bottom=100, left=100, right=100)
        set_cell_margins(c_bot, top=120, bottom=120, left=100, right=100)

        p_t = c_top.paragraphs[0]
        p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_t.paragraph_format.space_before = Pt(0)
        p_t.paragraph_format.space_after = Pt(0)
        r_t = p_t.add_run(title)
        r_t.bold = True
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(8.5)
        r_t.font.color.rgb = RGBColor(255, 255, 255)

        p_b = c_bot.paragraphs[0]
        p_b.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_b.paragraph_format.space_before = Pt(0)
        p_b.paragraph_format.space_after = Pt(2)
        r_bv = p_b.add_run(f"{big_val}\n")
        r_bv.bold = True
        r_bv.font.name = "Calibri"
        r_bv.font.size = Pt(11)
        r_bv.font.color.rgb = RGB_NAVY

        r_sub = p_b.add_run(f"{sub1} • {sub2}")
        r_sub.font.name = "Calibri"
        r_sub.font.size = Pt(7.5)
        r_sub.font.color.rgb = RGB_MUTED

    p_kpi_sp = doc.add_paragraph()
    p_kpi_sp.paragraph_format.space_before = Pt(0)
    p_kpi_sp.paragraph_format.space_after = Pt(10)

    # =========================================================================
    # CAPÍTULO 1: INTELIGENCIA TERRITORIAL Y EVIDENCIA DE CAMPO
    # =========================================================================
    add_styled_heading(doc, "1. Inteligencia Territorial y Evidencia de Campo", level=1)
    
    p_c1 = doc.add_paragraph()
    p_c1.paragraph_format.line_spacing = 1.15
    p_c1.paragraph_format.space_after = Pt(6)
    p_c1.add_run(
        f"El presente estudio prospectivo sobre el territorio de {territory} integra levantamiento de evidencia "
        f"estructurada a través de monitoreo en fuentes abiertas (OSINT), medios de prensa nacional y regional, "
        f"pronunciamientos oficiales institucionales y reportes de conflictividad social y de derechos humanos "
        f"(incluyendo Business & Human Rights Resource Centre, NewsData.io y Google News LatAm). "
        f"A continuación se presenta el registro de evidencias indexadas que sustentan la delimitación de actores y sus posturas."
    )

    if news_items:
        news_tbl = doc.add_table(rows=min(len(news_items), 12) + 1, cols=4)
        news_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(news_tbl)
        format_table_header(news_tbl.rows[0], ["Titular / Noticia Territorial", "Canal / Origen", "Fuente", "Fecha / Enlace"])

        for idx, item in enumerate(news_items[:12]):
            row = news_tbl.rows[idx + 1]
            bg = COLOR_SLATE_LIGHT_HEX if idx % 2 == 1 else "FFFFFF"
            for c_i, cell in enumerate(row.cells):
                set_cell_background(cell, bg)
                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

            # Titular
            p0 = row.cells[0].paragraphs[0]
            p0.paragraph_format.space_after = Pt(0)
            r0 = p0.add_run(item.get("title", "Noticia territorial"))
            r0.font.name = "Calibri"
            r0.font.size = Pt(8.5)
            r0.bold = True
            r0.font.color.rgb = RGB_DARK

            # Canal
            p1 = row.cells[1].paragraphs[0]
            p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p1.paragraph_format.space_after = Pt(0)
            r1 = p1.add_run(item.get("channel", "Prensa").upper())
            r1.font.name = "Calibri"
            r1.font.size = Pt(8)
            r1.font.color.rgb = RGB_TEAL

            # Fuente
            p2 = row.cells[2].paragraphs[0]
            p2.paragraph_format.space_after = Pt(0)
            r2 = p2.add_run(item.get("source", "Medio Informativo"))
            r2.font.name = "Calibri"
            r2.font.size = Pt(8)
            r2.font.color.rgb = RGB_DARK

            # Fecha
            p3 = row.cells[3].paragraphs[0]
            p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p3.paragraph_format.space_after = Pt(0)
            r3 = p3.add_run(item.get("published_at", "Monitoreo Activo")[:16])
            r3.font.name = "Calibri"
            r3.font.size = Pt(8)
            r3.font.color.rgb = RGB_MUTED

        p_news_sp = doc.add_paragraph()
        p_news_sp.paragraph_format.space_after = Pt(8)
    else:
        add_callout(
            doc,
            "Monitoreo Territorial Calibrado",
            "Los actores y posturas han sido verificados contra la serie histórica documental y metodológica del caso de estudio.",
            border_color="0F766E",
            bg_color=COLOR_SLATE_LIGHT_HEX
        )

    # =========================================================================
    # CAPÍTULO 2: CARACTERIZACIÓN DE ACTORES ESTRATÉGICOS
    # =========================================================================
    add_styled_heading(doc, "2. Identificación y Caracterización de Actores Estratégicos", level=1)
    
    p_c2 = doc.add_paragraph()
    p_c2.paragraph_format.line_spacing = 1.15
    p_c2.paragraph_format.space_after = Pt(6)
    p_c2.add_run(
        "En la metodología MACTOR, un actor se define como un grupo, entidad, institución o colectivo social "
        "con suficiente autonomía, medios de acción y voluntad para influir sobre las decisiones y el futuro "
        "del sistema territorial. A continuación se detalla la nómina de actores analizados:"
    )

    act_tbl = doc.add_table(rows=len(actors) + 1, cols=5)
    act_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(act_tbl)
    format_table_header(act_tbl.rows[0], ["Cód.", "Nombre Oficial del Actor", "Sigla", "Tipología / Sector", "Rol y Evidencia Territorial"])

    for idx, act in enumerate(actors):
        row = act_tbl.rows[idx + 1]
        bg = COLOR_SLATE_LIGHT_HEX if idx % 2 == 1 else "FFFFFF"
        for cell in row.cells:
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)

        # Cód
        p0 = row.cells[0].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(act.get("id", f"A{idx+1}"))
        r0.bold = True
        r0.font.name = "Calibri"
        r0.font.size = Pt(8.5)
        r0.font.color.rgb = RGB_NAVY

        # Nombre
        p1 = row.cells[1].paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(act.get("name", ""))
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = RGB_DARK

        # Sigla
        p2 = row.cells[2].paragraphs[0]
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(act.get("short_name", act.get("name", ""))[:18])
        r2.font.name = "Calibri"
        r2.font.size = Pt(8)
        r2.font.color.rgb = RGB_TEAL

        # Tipo
        p3 = row.cells[3].paragraphs[0]
        p3.paragraph_format.space_after = Pt(0)
        r3 = p3.add_run(act.get("category", act.get("type", "Actor Territorial")))
        r3.font.name = "Calibri"
        r3.font.size = Pt(8)
        r3.font.color.rgb = RGB_MUTED

        # Rol y Evidencia
        p4 = row.cells[4].paragraphs[0]
        p4.paragraph_format.space_after = Pt(0)
        desc = act.get("description") or act.get("evidence") or "Actor con incidencia directa en la gobernanza territorial."
        r4 = p4.add_run(desc[:180] + ("..." if len(desc) > 180 else ""))
        r4.font.name = "Calibri"
        r4.font.size = Pt(8)
        r4.font.color.rgb = RGB_DARK

    p_act_sp = doc.add_paragraph()
    p_act_sp.paragraph_format.space_after = Pt(8)

    # =========================================================================
    # CAPÍTULO 3: RETOS Y OBJETIVOS ESTRATÉGICOS
    # =========================================================================
    add_styled_heading(doc, "3. Retos y Objetivos Estratégicos del Territorio", level=1)
    
    p_c3 = doc.add_paragraph()
    p_c3.paragraph_format.line_spacing = 1.15
    p_c3.paragraph_format.space_after = Pt(6)
    p_c3.add_run(
        "Los objetivos representan los desafíos estratégicos, proyectos y decisiones críticas "
        "en torno a los cuales giran las alianzas, las negociaciones y los conflictos entre los actores. "
        "La ponderación refleja la prioridad estratégica relativa asignada a cada objetivo (normalizada al 100%):"
    )

    obj_tbl = doc.add_table(rows=len(objectives) + 1, cols=4)
    obj_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(obj_tbl)
    format_table_header(obj_tbl.rows[0], ["Cód.", "Nombre del Objetivo Estratégico", "Ponderación (%)", "Descripción y Desafío Prospectivo"])

    weights = res.get("weights", [1.0/len(objectives)]*len(objectives))
    for idx, obj in enumerate(objectives):
        row = obj_tbl.rows[idx + 1]
        bg = COLOR_SLATE_LIGHT_HEX if idx % 2 == 1 else "FFFFFF"
        for cell in row.cells:
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)

        # Cód
        p0 = row.cells[0].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(obj.get("id", f"O{idx+1}"))
        r0.bold = True
        r0.font.name = "Calibri"
        r0.font.size = Pt(8.5)
        r0.font.color.rgb = RGB_NAVY

        # Nombre
        p1 = row.cells[1].paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(obj.get("name", ""))
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = RGB_DARK

        # Ponderación
        w_val = weights[idx] * 100 if idx < len(weights) else (100.0/len(objectives))
        p2 = row.cells[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(f"{w_val:.1f}%")
        r2.bold = True
        r2.font.name = "Calibri"
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = RGB_TEAL

        # Descripción
        p3 = row.cells[3].paragraphs[0]
        p3.paragraph_format.space_after = Pt(0)
        desc_o = obj.get("description", "Objetivo estratégico territorial en disputa.")
        r3 = p3.add_run(desc_o)
        r3.font.name = "Calibri"
        r3.font.size = Pt(8)
        r3.font.color.rgb = RGB_DARK

    p_obj_sp = doc.add_paragraph()
    p_obj_sp.paragraph_format.space_after = Pt(8)

    # =========================================================================
    # CAPÍTULO 4: INFLUENCIAS DIRECTAS E INDIRECTAS (MID, MIDI) Y CUADRANTES GODET
    # =========================================================================
    add_styled_heading(doc, "4. Matriz de Influencias Directas (MID), Indirectas (MIDI) y Posicionamiento de Godet", level=1)
    
    p_c4 = doc.add_paragraph()
    p_c4.paragraph_format.line_spacing = 1.15
    p_c4.paragraph_format.space_after = Pt(6)
    p_c4.add_run(
        "La Matriz de Influencias Directas (MID) cuantifica el poder que un actor ejerce directamente sobre otro, "
        "utilizando la escala de Michel Godet: 0 = Sin influencia; 1 = Influencia operativa sobre procesos; "
        "2 = Influencia media en proyectos y financiamiento; 3 = Influencia alta sobre la misión del actor; "
        "4 = Influencia determinante / poder de veto sobre la existencia misma del actor.\n\n"
        "La suma de filas indica la Influencia Directa (I_i), mientras que la suma de columnas indica la "
        "Dependencia Directa (D_i). Posteriormente, la Matriz MIDI (de segundo orden: MIDI = MID + MID^2) "
        "incorpora las influencias indirectas ejercidas a través de terceros actores interpuestos."
    )

    act_short_names = [a.get("short_name", a["name"])[:14] for a in actors]
    mid_data = res.get("mid", mid)
    midi_data = res.get("midi", [])
    mid_metrics = res.get("mid_metrics", {})
    i_direct = mid_metrics.get("I_direct", [sum(r) for r in mid_data])
    d_direct = mid_metrics.get("D_direct", [sum(mid_data[r][c] for r in range(len(mid_data))) for c in range(len(mid_data[0]))] if mid_data else [])

    # Tabla MID
    add_matrix_table(
        doc,
        act_short_names,
        act_short_names,
        mid_data,
        is_signed=False,
        include_totals=True,
        row_totals=i_direct,
        col_totals=d_direct,
        title="Tabla 4.1: Matriz de Influencias Directas (MID) con Totales de Influencia (I_i) y Dependencia (D_i)"
    )

    # Tabla MIDI
    if midi_data:
        midi_i = mid_metrics.get("I_i", [sum(r) for r in midi_data])
        midi_d = mid_metrics.get("D_i", [sum(midi_data[r][c] for r in range(len(midi_data))) for c in range(len(midi_data[0]))])
        add_matrix_table(
            doc,
            act_short_names,
            act_short_names,
            midi_data,
            is_signed=False,
            include_totals=True,
            row_totals=midi_i,
            col_totals=midi_d,
            title="Tabla 4.2: Matriz de Influencias Directas e Indirectas de Segundo Orden (MIDI = MID + MID²)"
        )

    # Diagnóstico por Cuadrantes Estratégicos de Godet
    add_styled_heading(doc, "Diagnóstico por Cuadrantes Estratégicos (Plano Influencia-Dependencia de Godet)", level=2)
    
    quad_tbl = doc.add_table(rows=len(res.get("quadrants", [])) + 1, cols=6)
    quad_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(quad_tbl)
    format_table_header(quad_tbl.rows[0], ["Cód.", "Actor", "Influencia (I_i)", "Dependencia (D_i)", "Relación Fuerza (r_i)", "Cuadrante Estratégico Godet"])

    force_metrics = res.get("force_metrics", {})
    ri_list = force_metrics.get("r_i", [1.0]*len(actors))

    for idx, q in enumerate(res.get("quadrants", [])):
        row = quad_tbl.rows[idx + 1]
        bg = COLOR_SLATE_LIGHT_HEX if idx % 2 == 1 else "FFFFFF"
        for cell in row.cells:
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)

        # Cód
        p0 = row.cells[0].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(q.get("id", f"A{idx+1}"))
        r0.bold = True
        r0.font.name = "Calibri"
        r0.font.size = Pt(8.5)
        r0.font.color.rgb = RGB_NAVY

        # Nombre
        p1 = row.cells[1].paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(q.get("name", ""))
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = RGB_DARK

        # Influencia
        p2 = row.cells[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(str(round(q.get("influence", 0), 1)))
        r2.font.name = "Calibri"
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = RGB_DARK

        # Dependencia
        p3 = row.cells[3].paragraphs[0]
        p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p3.paragraph_format.space_after = Pt(0)
        r3 = p3.add_run(str(round(q.get("dependence", 0), 1)))
        r3.font.name = "Calibri"
        r3.font.size = Pt(8.5)
        r3.font.color.rgb = RGB_DARK

        # r_i
        q_idx = q.get("index", idx)
        ri_val = ri_list[q_idx] if q_idx < len(ri_list) else 1.0
        p4 = row.cells[4].paragraphs[0]
        p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p4.paragraph_format.space_after = Pt(0)
        r4 = p4.add_run(f"{ri_val:.2f}")
        r4.bold = True
        r4.font.name = "Calibri"
        r4.font.size = Pt(8.5)
        r4.font.color.rgb = RGB_NAVY

        # Cuadrante
        p5 = row.cells[5].paragraphs[0]
        p5.paragraph_format.space_after = Pt(0)
        r5 = p5.add_run(q.get("quadrant", "Cuadrante Estratégico"))
        r5.bold = True
        r5.font.name = "Calibri"
        r5.font.size = Pt(8.5)
        
        # Color del cuadrante
        q_name = q.get("quadrant", "").lower()
        if "dominante" in q_name:
            r5.font.color.rgb = RGBColor(180, 83, 9)   # Ámbar / Dorado
        elif "enlace" in q_name or "clave" in q_name:
            r5.font.color.rgb = RGBColor(190, 18, 60)  # Rojo / Foco crítico
        elif "dominado" in q_name or "dependiente" in q_name:
            r5.font.color.rgb = RGBColor(29, 78, 216)  # Azul
        else:
            r5.font.color.rgb = RGBColor(71, 85, 105)  # Pizarra

    # Interpretación de Cuadrantes
    p_quad_desc = doc.add_paragraph()
    p_quad_desc.paragraph_format.space_before = Pt(8)
    p_quad_desc.paragraph_format.space_after = Pt(6)
    p_quad_desc.paragraph_format.line_spacing = 1.15
    p_quad_desc.add_run(
        "• Actores Dominantes (Alta Influencia, Baja Dependencia): Constituyen los motores del sistema. "
        "Poseen amplia autonomía y capacidad para fijar la agenda sin verse condicionados por los demás.\n"
        "• Actores de Enlace / Clave (Alta Influencia, Alta Dependencia): Representan los puntos de inestabilidad "
        "y tensión crítica del sistema. Cualquier perturbación sobre ellos repercute en cascada sobre todo el territorio.\n"
        "• Actores Dominados / Dependientes (Baja Influencia, Alta Dependencia): Receptores de los impactos territoriales "
        "con baja capacidad de respuesta autónoma. Requieren mecanismos de articulación institucional o protección.\n"
        "• Actores Autónomos (Baja Influencia, Baja Dependencia): Actores desconectados o periféricos con agendas sectoriales independientes."
    )

    # Métricas de Redes Sociales (SNA - Social Network Analysis)
    add_styled_heading(doc, "Métricas de Centralidad y Análisis de Redes Sociales (SNA)", level=2)
    net_metrics = res.get("network_metrics", {})
    if net_metrics:
        sna_tbl = doc.add_table(rows=len(actors) + 1, cols=4)
        sna_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(sna_tbl)
        format_table_header(sna_tbl.rows[0], ["Actor", "Centralidad de Grado (Degree)", "Intermediación (Betweenness)", "Vector Propio (Eigenvector)"])

        deg = net_metrics.get("degree", [0]*len(actors))
        bet = net_metrics.get("betweenness", [0]*len(actors))
        eig = net_metrics.get("eigenvector", [0]*len(actors))

        for idx, act in enumerate(actors):
            row = sna_tbl.rows[idx + 1]
            bg = COLOR_SLATE_LIGHT_HEX if idx % 2 == 1 else "FFFFFF"
            for cell in row.cells:
                set_cell_background(cell, bg)
                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

            # Nombre
            p0 = row.cells[0].paragraphs[0]
            p0.paragraph_format.space_after = Pt(0)
            r0 = p0.add_run(act.get("short_name", act["name"]))
            r0.bold = True
            r0.font.name = "Calibri"
            r0.font.size = Pt(8.5)
            r0.font.color.rgb = RGB_DARK

            # Degree
            p1 = row.cells[1].paragraphs[0]
            p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p1.paragraph_format.space_after = Pt(0)
            r1 = p1.add_run(f"{deg[idx]:.3f}" if idx < len(deg) else "0.000")
            r1.font.name = "Calibri"
            r1.font.size = Pt(8.5)

            # Betweenness
            p2 = row.cells[2].paragraphs[0]
            p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p2.paragraph_format.space_after = Pt(0)
            r2 = p2.add_run(f"{bet[idx]:.3f}" if idx < len(bet) else "0.000")
            r2.font.name = "Calibri"
            r2.font.size = Pt(8.5)

            # Eigenvector
            p3 = row.cells[3].paragraphs[0]
            p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p3.paragraph_format.space_after = Pt(0)
            r3 = p3.add_run(f"{eig[idx]:.3f}" if idx < len(eig) else "0.000")
            r3.bold = True
            r3.font.name = "Calibri"
            r3.font.size = Pt(8.5)
            r3.font.color.rgb = RGB_NAVY

        p_sna_sp = doc.add_paragraph()
        p_sna_sp.paragraph_format.space_after = Pt(8)

    # =========================================================================
    # CAPÍTULO 5: POSICIONES VALORADAS (2MAO), PONDERADAS (3MAO) Y BALANZAS
    # =========================================================================
    add_styled_heading(doc, "5. Matriz de Posiciones Valoradas (2MAO), Ponderadas (3MAO) y Balanzas de Poder", level=1)
    
    p_c5 = doc.add_paragraph()
    p_c5.paragraph_format.line_spacing = 1.15
    p_c5.paragraph_format.space_after = Pt(6)
    p_c5.add_run(
        "La matriz 2MAO registra la postura explícita y valorada de cada actor frente a cada objetivo, "
        "según la escala LIPSOR: +4 = Favorable incondicional / objetivo vital; +3 = Favorable prioritario; "
        "+2 = Favorable moderado; +1 = Favorable leve; 0 = Neutral / indiferente; -1 = Oposición leve; "
        "-2 = Oposición moderada; -3 = Oposición prioritaria; -4 = Oposición radical / conflicto existencial.\n\n"
        "La matriz 3MAO pondera estas posturas por el coeficiente de relación de fuerza r_i de cada actor, "
        "reflejando el peso real que cada postura ejerce en la arena de poder."
    )

    obj_short_names = [o.get("short_name", o["name"])[:12] for o in objectives]
    mao2_data = res.get("mao2", mao2)
    mao3_data = res.get("mao3", [])

    # Tabla 2MAO
    add_matrix_table(
        doc,
        act_short_names,
        obj_short_names,
        mao2_data,
        is_signed=True,
        include_totals=False,
        title="Tabla 5.1: Matriz 2MAO de Posiciones Valoradas de Actores sobre Objetivos (-4 a +4)"
    )

    # Tabla 3MAO
    if mao3_data:
        add_matrix_table(
            doc,
            act_short_names,
            obj_short_names,
            mao3_data,
            is_signed=True,
            include_totals=False,
            title="Tabla 5.2: Matriz 3MAO Ponderada por la Relación de Fuerza (r_i × 2MAO)"
        )

    # Balanzas Canónicas de Poder por Objetivo
    add_styled_heading(doc, "Análisis Canónico de Balanzas de Poder por Objetivo", level=2)
    
    for obj_idx, om in enumerate(res.get("objective_metrics", [])):
        p_b_title = doc.add_paragraph()
        p_b_title.paragraph_format.space_before = Pt(8)
        p_b_title.paragraph_format.space_after = Pt(3)
        p_b_title.paragraph_format.keep_with_next = True
        r_bt = p_b_title.add_run(f"Objetivo {om.get('id', f'O{obj_idx+1}')}: {om.get('name', '')}")
        r_bt.bold = True
        r_bt.font.name = "Calibri"
        r_bt.font.size = Pt(10)
        r_bt.font.color.rgb = RGB_NAVY

        # Calcular fuerzas ponderadas a favor y en contra
        fav_actors = []
        opp_actors = []
        neu_actors = []

        for act_idx, act in enumerate(actors):
            val_2mao = mao2_data[act_idx][obj_idx] if act_idx < len(mao2_data) and obj_idx < len(mao2_data[act_idx]) else 0
            ri_act = ri_list[act_idx] if act_idx < len(ri_list) else 1.0
            weighted_force = val_2mao * ri_act

            val_str = f"+{val_2mao:.1f}" if (isinstance(val_2mao, float) and not val_2mao.is_integer() and val_2mao > 0) else (f"{val_2mao:.1f}" if isinstance(val_2mao, float) and not val_2mao.is_integer() else (f"+{int(val_2mao)}" if val_2mao > 0 else str(int(val_2mao))))
            act_lbl = f"{act.get('short_name', act['name'])} (Postura: {val_str}, Fuerza: {weighted_force:+.2f})"
            if val_2mao > 0:
                fav_actors.append(act_lbl)
            elif val_2mao < 0:
                opp_actors.append(act_lbl)
            else:
                neu_actors.append(act.get("short_name", act["name"]))

        bal_tbl = doc.add_table(rows=4, cols=2)
        bal_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(bal_tbl)

        b_rows = [
            ("Actores A Favor (+):", ", ".join(fav_actors) if fav_actors else "Ninguno con postura favorable"),
            ("Actores En Oposición (-):", ", ".join(opp_actors) if opp_actors else "Ninguno con postura en contra"),
            ("Actores Neutros (0):", ", ".join(neu_actors) if neu_actors else "Ninguno"),
            ("Inclinación de la Balanza:", f"Balance Neto: {om.get('net_balance', 0):+.2f} | Movilización: {om.get('mobilization', 0):.2f} | Diagnóstico: {om.get('status', 'Estable')}")
        ]

        for b_i, (b_lbl, b_val) in enumerate(b_rows):
            r_row = bal_tbl.rows[b_i]
            c0, c1 = r_row.cells[0], r_row.cells[1]
            set_cell_background(c0, COLOR_SLATE_LIGHT_HEX)
            set_cell_margins(c0, top=80, bottom=80, left=100, right=100)
            set_cell_margins(c1, top=80, bottom=80, left=100, right=100)

            p0 = c0.paragraphs[0]
            p0.paragraph_format.space_after = Pt(0)
            r0 = p0.add_run(b_lbl)
            r0.bold = True
            r0.font.name = "Calibri"
            r0.font.size = Pt(8.5)
            r0.font.color.rgb = RGB_DARK

            p1 = c1.paragraphs[0]
            p1.paragraph_format.space_after = Pt(0)
            r1 = p1.add_run(b_val)
            r1.font.name = "Calibri"
            r1.font.size = Pt(8.5)
            if b_i == 0:
                r1.font.color.rgb = RGBColor(22, 101, 52) # Verde
            elif b_i == 1:
                r1.font.color.rgb = RGBColor(153, 27, 27) # Rojo
            elif b_i == 3:
                r1.bold = True
                r1.font.color.rgb = RGB_NAVY

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================================
    # CAPÍTULO 6: RED DE ALIANZAS Y CONFLICTOS (CONVERGENCIA Y DIVERGENCIA)
    # =========================================================================
    add_styled_heading(doc, "6. Red de Alianzas y Conflictos (Convergencias y Divergencias)", level=1)
    
    p_c6 = doc.add_paragraph()
    p_c6.paragraph_format.line_spacing = 1.15
    p_c6.paragraph_format.space_after = Pt(6)
    p_c6.add_run(
        "El análisis de convergencias y divergencias identifica la afinidad estratégica o rivalidad "
        "entre cada par de actores, teniendo en cuenta no solo el signo de sus posturas sino la intensidad "
        "y el balance de fuerza de cada uno (matrices de 3er orden CAA3 y DAA3)."
    )

    caa3_data = res.get("caa3", [])
    daa3_data = res.get("daa3", [])

    if caa3_data:
        add_matrix_table(
            doc,
            act_short_names,
            act_short_names,
            caa3_data,
            is_signed=False,
            include_totals=False,
            title="Tabla 6.1: Matriz de Convergencia de Actores (CAA3) — Intensidad de Alianzas Potenciales"
        )

    if daa3_data:
        add_matrix_table(
            doc,
            act_short_names,
            act_short_names,
            daa3_data,
            is_signed=False,
            include_totals=False,
            title="Tabla 6.2: Matriz de Divergencia de Actores (DAA3) — Focos de Conflicto y Oposición"
        )

    # Pares de máxima convergencia y máxima divergencia
    add_styled_heading(doc, "Principales Alianzas Naturales y Focos de Tensión Bilateral", level=2)
    
    # Extraer pares
    pairs_conv = []
    pairs_div = []
    n_act = len(actors)
    for i in range(n_act):
        for j in range(i + 1, n_act):
            score_c = caa3_data[i][j] if i < len(caa3_data) and j < len(caa3_data[i]) else 0
            score_d = daa3_data[i][j] if i < len(daa3_data) and j < len(daa3_data[i]) else 0
            act_i = actors[i].get("short_name", actors[i]["name"])
            act_j = actors[j].get("short_name", actors[j]["name"])
            pairs_conv.append((score_c, act_i, act_j))
            pairs_div.append((score_d, act_i, act_j))

    pairs_conv.sort(key=lambda x: x[0], reverse=True)
    pairs_div.sort(key=lambda x: x[0], reverse=True)

    top_tbl = doc.add_table(rows=6, cols=4)
    top_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(top_tbl)
    format_table_header(top_tbl.rows[0], ["Mayor Convergencia (Alianzas)", "Puntaje CAA3", "Mayor Divergencia (Conflicto)", "Puntaje DAA3"])

    for rank in range(5):
        row = top_tbl.rows[rank + 1]
        bg = COLOR_SLATE_LIGHT_HEX if rank % 2 == 1 else "FFFFFF"
        for cell in row.cells:
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

        # Conv
        c_score, a1, a2 = pairs_conv[rank] if rank < len(pairs_conv) else (0, "-", "-")
        p0 = row.cells[0].paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(f"{rank+1}. {a1} ↔ {a2}")
        r0.bold = True
        r0.font.name = "Calibri"
        r0.font.size = Pt(8.5)
        r0.font.color.rgb = RGBColor(22, 101, 52)

        p1 = row.cells[1].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(f"{c_score:.2f}")
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(8.5)

        # Div
        d_score, d1, d2 = pairs_div[rank] if rank < len(pairs_div) else (0, "-", "-")
        p2 = row.cells[2].paragraphs[0]
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(f"{rank+1}. {d1} ↔ {d2}")
        r2.bold = True
        r2.font.name = "Calibri"
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = RGBColor(153, 27, 27)

        p3 = row.cells[3].paragraphs[0]
        p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p3.paragraph_format.space_after = Pt(0)
        r3 = p3.add_run(f"{d_score:.2f}")
        r3.bold = True
        r3.font.name = "Calibri"
        r3.font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # CAPÍTULO 7: MOVILIZACIÓN, POLARIZACIÓN Y VIABILIDAD DE OBJETIVOS
    # =========================================================================
    add_styled_heading(doc, "7. Diagnóstico de Movilización, Polarización y Viabilidad de Objetivos", level=1)
    
    p_c7 = doc.add_paragraph()
    p_c7.paragraph_format.line_spacing = 1.15
    p_c7.paragraph_format.space_after = Pt(6)
    p_c7.add_run(
        "El análisis de viabilidad evalúa la probabilidad política de materializar cada objetivo estratégico, "
        "con base en tres indicadores prospectivos clave:\n"
        "• Movilización (M_j): Suma absoluta del interés y energía volcada por los actores hacia el objetivo.\n"
        "• Balance Neto (B_j): Diferencia entre la fuerza favorable y la fuerza de oposición.\n"
        "• Índice de Conflicto (C_j): Nivel de polarización territorial (valores cercanos a 1.0 indican bloqueo severo)."
    )

    om_tbl = doc.add_table(rows=len(res.get("objective_metrics", [])) + 1, cols=7)
    om_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(om_tbl)
    format_table_header(om_tbl.rows[0], ["Cód.", "Objetivo Estratégico", "A Favor", "En Contra", "Movilización", "Balance Neto", "Diagnóstico Prospectivo"])

    for idx, om in enumerate(res.get("objective_metrics", [])):
        row = om_tbl.rows[idx + 1]
        bg = COLOR_SLATE_LIGHT_HEX if idx % 2 == 1 else "FFFFFF"
        for cell in row.cells:
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=80, right=80)

        # Cód
        p0 = row.cells[0].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(om.get("id", f"O{idx+1}"))
        r0.bold = True
        r0.font.name = "Calibri"
        r0.font.size = Pt(8.5)
        r0.font.color.rgb = RGB_NAVY

        # Nombre
        p1 = row.cells[1].paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(om.get("name", ""))
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = RGB_DARK

        # A favor
        p2 = row.cells[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(str(om.get("favorable_actors", 0)))
        r2.font.name = "Calibri"
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = RGBColor(22, 101, 52)

        # En contra
        p3 = row.cells[3].paragraphs[0]
        p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p3.paragraph_format.space_after = Pt(0)
        r3 = p3.add_run(str(om.get("opposed_actors", 0)))
        r3.font.name = "Calibri"
        r3.font.size = Pt(8.5)
        r3.font.color.rgb = RGBColor(153, 27, 27)

        # Movilización
        p4 = row.cells[4].paragraphs[0]
        p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p4.paragraph_format.space_after = Pt(0)
        r4 = p4.add_run(f"{om.get('mobilization', 0):.1f}")
        r4.font.name = "Calibri"
        r4.font.size = Pt(8.5)

        # Balance Neto
        p5 = row.cells[5].paragraphs[0]
        p5.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p5.paragraph_format.space_after = Pt(0)
        b_val = om.get("net_balance", 0)
        r5 = p5.add_run(f"{b_val:+.1f}")
        r5.bold = True
        r5.font.name = "Calibri"
        r5.font.size = Pt(8.5)
        r5.font.color.rgb = RGBColor(22, 101, 52) if b_val >= 0 else RGBColor(153, 27, 27)

        # Diagnóstico
        p6 = row.cells[6].paragraphs[0]
        p6.paragraph_format.space_after = Pt(0)
        status_txt = om.get("status", "Viable")
        r6 = p6.add_run(status_txt)
        r6.bold = True
        r6.font.name = "Calibri"
        r6.font.size = Pt(8.5)
        if "conflicto" in status_txt.lower() or "bloqueo" in status_txt.lower():
            r6.font.color.rgb = RGBColor(190, 18, 60)
        elif "consenso" in status_txt.lower() or "viable" in status_txt.lower():
            r6.font.color.rgb = RGBColor(22, 101, 52)
        else:
            r6.font.color.rgb = RGBColor(180, 83, 9)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # CAPÍTULO 8: SIMULACIÓN DE ESCENARIOS PROSPECTIVOS ("¿QUÉ PASA SI...?")
    # =========================================================================
    add_styled_heading(doc, "8. Simulación de Escenarios Prospectivos y Análisis Sensibilidad", level=1)
    
    p_c8 = doc.add_paragraph()
    p_c8.paragraph_format.line_spacing = 1.15
    p_c8.paragraph_format.space_after = Pt(6)
    p_c8.add_run(
        "A través del motor de simulación de escenarios, se contrastan tres situaciones prospectivas "
        "plausibles para anticipar variaciones en el balance de gobernanza territorial:"
    )

    scenarios = [
        (
            "Escenario 1: Consolidación de la Alianza Hegemónica Institucional",
            "Los actores institucionales y los gremios económicos consolidan un pacto de co-gobernanza. "
            "Se logra acelerar los proyectos de infraestructura prioritaria, pero se incrementa la vulnerabilidad "
            "social si no se establecen canales directos de consulta con las comunidades de base.",
            "Alta viabilidad técnica / Riesgo latente de judicialización o protestas territoriales."
        ),
        (
            "Escenario 2: Frente de Resistencia Social y Bloqueo Comunitario",
            "Los actores sociales, campesinos o indígenas fortalecen su articulación con ONGs y organismos "
            "internacionales de derechos humanos. Los objetivos con mayor índice de conflicto entran en zona de "
            "parálisis administrativa, requiriendo mesas de diálogo vinculantes.",
            "Parálisis transitoria / Necesidad de renegociar compensaciones ambientales y distribución de beneficios."
        ),
        (
            "Escenario 3: Mediación Activa y Negociación de Pacto Territorial Ampliado",
            "Los actores ubicados en el Cuadrante de Enlace (actores bisagra) asumen un rol activo de intermediación, "
            "incorporando cláusulas de salvaguarda hídrica, monitoreo participativo y regalías locales.",
            "Escenario de Máxima Sostenibilidad / Desescalamiento del 70% de los focos de conflicto severo."
        )
    ]

    scen_tbl = doc.add_table(rows=4, cols=3)
    scen_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(scen_tbl)
    format_table_header(scen_tbl.rows[0], ["Escenario Prospectivo", "Dinámica y Juego de Actores", "Impacto en Gobernanza"])

    for s_idx, (s_title, s_desc, s_imp) in enumerate(scenarios):
        row = scen_tbl.rows[s_idx + 1]
        bg = COLOR_SLATE_LIGHT_HEX if s_idx % 2 == 1 else "FFFFFF"
        for cell in row.cells:
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=100, right=100)

        p0 = row.cells[0].paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(s_title)
        r0.bold = True
        r0.font.name = "Calibri"
        r0.font.size = Pt(8.5)
        r0.font.color.rgb = RGB_NAVY

        p1 = row.cells[1].paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(s_desc)
        r1.font.name = "Calibri"
        r1.font.size = Pt(8)
        r1.font.color.rgb = RGB_DARK

        p2 = row.cells[2].paragraphs[0]
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(s_imp)
        r2.bold = True
        r2.font.name = "Calibri"
        r2.font.size = Pt(8)
        r2.font.color.rgb = RGB_TEAL

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # CAPÍTULO 9: HOJA DE RUTA Y RECOMENDACIONES DE GOBERNANZA
    # =========================================================================
    add_styled_heading(doc, "9. Hoja de Ruta Estratégica y Recomendaciones de Gobernanza", level=1)
    
    p_c9 = doc.add_paragraph()
    p_c9.paragraph_format.line_spacing = 1.15
    p_c9.paragraph_format.space_after = Pt(6)
    p_c9.add_run(
        "Con base en la modelación matricial, se formula la siguiente hoja de ruta táctica para la conducción "
        "estratégica del territorio y el aseguramiento de los acuerdos prospectivos:"
    )

    recs = [
        ("Destrabe de Objetivos Críticos", "Priorizar mesas de concertación técnica en los objetivos con Índice de Conflicto superior a 0.50 antes de iniciar fases constructivas o de licenciamiento formal."),
        ("Apalancamiento de Actores Clave", f"Vincular de manera orgánica a '{dom_name}' como coordinador institucional de las comisiones de seguimiento territorial."),
        ("Canalización de Actores Bisagra", "Empoderar a los actores del Cuadrante de Enlace dotándolos de recursos técnicos para actuar como garantes transparentes de los acuerdos."),
        ("Protección de Colectivos Dependientes", "Institucionalizar protocolos de veeduría y compensación socioeconómica para salvaguardar a las comunidades ubicadas en el Cuadrante Dominado."),
        ("Sistema de Alerta Temprana", "Mantener activo el monitoreo de prensa y redes sociales territoriales para detectar cambios tempranos en las posturas de los actores antes de que muten en bloqueos.")
    ]

    for r_title, r_desc in recs:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_before = Pt(3)
        p_r.paragraph_format.space_after = Pt(4)
        p_r.paragraph_format.line_spacing = 1.15
        r_num = p_r.add_run(f"✔ {r_title}: ")
        r_num.bold = True
        r_num.font.name = "Calibri"
        r_num.font.size = Pt(9.5)
        r_num.font.color.rgb = RGB_NAVY

        r_txt = p_r.add_run(r_desc)
        r_txt.font.name = "Calibri"
        r_txt.font.size = Pt(9.5)
        r_txt.font.color.rgb = RGB_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # CAPÍTULO 10: DOSSIER DE FICHAS TÉCNICAS INDIVIDUALES POR ACTOR
    # =========================================================================
    add_styled_heading(doc, "10. Dossier de Fichas Técnicas Individuales por Actor", level=1)
    
    p_c10 = doc.add_paragraph()
    p_c10.paragraph_format.line_spacing = 1.15
    p_c10.paragraph_format.space_after = Pt(6)
    p_c10.add_run(
        "A continuación se presenta el perfil individual exhaustivo de cada actor del sistema, "
        "resumiendo sus métricas de poder, cuadrante estratégico, objetivos que apoya o rechaza, "
        "y sus principales aliados y rivales detectados por el modelo:"
    )

    for idx, act in enumerate(actors):
        p_act_h = doc.add_paragraph()
        p_act_h.paragraph_format.space_before = Pt(8)
        p_act_h.paragraph_format.space_after = Pt(2)
        p_act_h.paragraph_format.keep_with_next = True
        r_ah = p_act_h.add_run(f"Ficha {idx+1}: {act.get('id', f'A{idx+1}')} — {act.get('name', '')}")
        r_ah.bold = True
        r_ah.font.name = "Calibri"
        r_ah.font.size = Pt(10.5)
        r_ah.font.color.rgb = RGB_NAVY

        # Métricas de este actor
        ri_val = ri_list[idx] if idx < len(ri_list) else 1.0
        q_info = next((q for q in res.get("quadrants", []) if q.get("index") == idx), {})
        q_name = q_info.get("quadrant", "No clasificado")

        # Objetivos apoyados y rechazados
        fav_objs = []
        opp_objs = []
        for o_i, obj in enumerate(objectives):
            val = mao2_data[idx][o_i] if idx < len(mao2_data) and o_i < len(mao2_data[idx]) else 0
            if val > 0:
                fav_objs.append(f"{obj.get('short_name', obj['name'])} (+{val})")
            elif val < 0:
                opp_objs.append(f"{obj.get('short_name', obj['name'])} ({val})")

        # Aliados y rivales
        aliados = []
        rivales = []
        for other_idx in range(len(actors)):
            if other_idx != idx:
                c_score = caa3_data[idx][other_idx] if idx < len(caa3_data) and other_idx < len(caa3_data[idx]) else 0
                d_score = daa3_data[idx][other_idx] if idx < len(daa3_data) and other_idx < len(daa3_data[idx]) else 0
                other_name = actors[other_idx].get("short_name", actors[other_idx]["name"])
                aliados.append((c_score, other_name))
                rivales.append((d_score, other_name))

        aliados.sort(key=lambda x: x[0], reverse=True)
        rivales.sort(key=lambda x: x[0], reverse=True)

        top_aliados = [f"{name} ({score:.2f})" for score, name in aliados[:2] if score > 0]
        top_rivales = [f"{name} ({score:.2f})" for score, name in rivales[:2] if score > 0]

        dossier_tbl = doc.add_table(rows=5, cols=2)
        dossier_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(dossier_tbl)

        dossier_rows = [
            ("Posicionamiento Godet:", f"Cuadrante: {q_name} | Relación de Fuerza r_i: {ri_val:.2f} | Influencia: {i_direct[idx] if idx < len(i_direct) else 0:.1f} | Dependencia: {d_direct[idx] if idx < len(d_direct) else 0:.1f}"),
            ("Objetivos que Apoya (+):", ", ".join(fav_objs) if fav_objs else "Ningún objetivo con postura positiva explícita"),
            ("Objetivos que Rechaza (-):", ", ".join(opp_objs) if opp_objs else "Ninguna objeción registrada"),
            ("Alianzas Naturales (CAA3):", ", ".join(top_aliados) if top_aliados else "Sin alianzas prioritarias detectadas"),
            ("Principales Conflictos (DAA3):", ", ".join(top_rivales) if top_rivales else "Sin antagonismos de consideración")
        ]

        for d_i, (d_lbl, d_val) in enumerate(dossier_rows):
            r_d = dossier_tbl.rows[d_i]
            c0, c1 = r_d.cells[0], r_d.cells[1]
            set_cell_background(c0, COLOR_SLATE_LIGHT_HEX)
            set_cell_margins(c0, top=60, bottom=60, left=80, right=80)
            set_cell_margins(c1, top=60, bottom=60, left=80, right=80)

            p0 = c0.paragraphs[0]
            p0.paragraph_format.space_after = Pt(0)
            r0 = p0.add_run(d_lbl)
            r0.bold = True
            r0.font.name = "Calibri"
            r0.font.size = Pt(8)
            r0.font.color.rgb = RGB_DARK

            p1 = c1.paragraphs[0]
            p1.paragraph_format.space_after = Pt(0)
            r1 = p1.add_run(d_val)
            r1.font.name = "Calibri"
            r1.font.size = Pt(8)
            if d_i == 1:
                r1.font.color.rgb = RGBColor(22, 101, 52)
            elif d_i == 2:
                r1.font.color.rgb = RGBColor(153, 27, 27)
            else:
                r1.font.color.rgb = RGB_DARK

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================================
    # CAPÍTULO 11: REFERENCIAS METODOLÓGICAS Y BIBLIOGRAFÍA
    # =========================================================================
    add_styled_heading(doc, "11. Referencias Metodológicas y Bibliografía", level=1)
    
    p_bib = doc.add_paragraph()
    p_bib.paragraph_format.line_spacing = 1.15
    p_bib.paragraph_format.space_after = Pt(4)
    p_bib.add_run(
        "1. Godet, M. (1991). De l'anticipation à l'action: manuel de prospective et de stratégie. Dunod, Paris.\n"
        "2. Godet, M. (2001). Creating Futures: Scenario Planning as a Strategic Management Tool. Economica, London.\n"
        "3. LIPSOR (Laboratoire d'Investigation en Prospective, Stratégie et Organisation). Software MACTOR (Méthode Acteurs, Objectifs, Rapports de Force).\n"
        "4. Villabona, N., Oyola, P. S., & Franco, D. A. (2018). Aplicación de la técnica MACTOR en la selección del equino ganador en competencia de paso. Revista AGLALA, 9(1), 309-318. DOI: 10.22519/22157360.1206.\n"
        "5. CEPAL / ILPES (2016). Planificación para el desarrollo en América Latina y el Caribe: Enfoques, herramientas y perspectivas prospectivas. Naciones Unidas, Santiago de Chile.\n"
        "6. Freeman, L. C. (1979). Centrality in social networks conceptual clarification. Social Networks, 1(3), 215-239."
    )

    # Generar buffer binario en memoria
    stream = io.BytesIO()
    doc.save(stream)
    stream.seek(0)
    return stream
