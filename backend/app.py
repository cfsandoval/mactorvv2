"""
Servidor Web FastAPI para la Aplicación Prospectiva MACTOR.
Integra análisis en vivo de territorios reales con minería de noticias y fuentes oficiales,
cálculo completo del algoritmo MACTOR clásico de Michel Godet (LIPSOR) y sus variantes avanzadas
(Multi-criterio/SoftProsp, Difusa, Teoría de Juegos y Simulación de Escenarios),
así como exportación en Excel estructurado y reportes ejecutivos.
"""

import io
import os
import sys
from pathlib import Path

# Ensure backend directory is in python sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from mactor_engine import MactorEngine
from territory_miner import fetch_multi_angle_news, extract_detailed_actors_and_postures
from cases_data import PRELOADED_CASES

app = FastAPI(
    title="Plataforma Prospectiva MACTOR & Variantes Avanzadas",
    description="Sistema web para análisis de juegos de actores prospectivos, inteligencia territorial y simulación estratégica",
    version="2.0.0"
)

# Enable CORS for flexible local development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class TerritoryRequest(BaseModel):
    territory: str
    country: Optional[str] = "Colombia"
    sector: Optional[str] = None
    newsapi_key: Optional[str] = None
    custom_keywords: Optional[str] = None
    max_news: Optional[int] = 40
    target_actors: Optional[int] = 8

class MactorCalculationRequest(BaseModel):
    actors: List[Dict[str, Any]]
    objectives: List[Dict[str, Any]]
    mid: List[List[float]]
    mao2: List[List[float]]
    variant: Optional[str] = "softprosp"
    options: Optional[Dict[str, Any]] = None

class ScenarioSimRequest(BaseModel):
    base_data: MactorCalculationRequest
    modifications: Dict[str, Any] # e.g. modified_mid, modified_mao2, power_boost

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "MACTOR Prospectiva Territorial", "version": "2.0.0"}

@app.post("/api/territory/analyze")
def analyze_territory(req: TerritoryRequest):
    """
    Crawls live news across:
    1. Google News CL & LatAm (https://news.google.com/home?hl=es-419&gl=CL&ceid=CL:es-419)
    2. Business & Human Rights Resource Centre (https://www.business-humanrights.org/es/feeds/latest-news/3/)
    3. NewsAPI (https://newsapi.org/docs) when API key is provided
    4. Official government gazettes (.gov/.gob) and Social Networks (X/Twitter/YouTube)
    """
    territory = req.territory.strip()
    sector = (req.sector or "").strip()
    newsapi_key = (req.newsapi_key or "").strip()
    if not territory:
        raise HTTPException(status_code=400, detail="Debe ingresar el nombre de un territorio real.")
        
    try:
        news_items = fetch_multi_angle_news(
            territory, 
            sector=sector, 
            country=req.country or "Colombia", 
            newsapi_key=newsapi_key
        )
        analysis = extract_detailed_actors_and_postures(
            territory, 
            news_items, 
            sector=sector, 
            target_actors=req.target_actors or 8
        )
        return {
            "status": "success",
            "data": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando territorio: {str(e)}")

@app.post("/api/mactor/calculate")
def calculate_mactor(req: MactorCalculationRequest):
    """
    Executes the complete MACTOR mathematical model:
    MID -> MIDI -> r_i -> 1MAO -> 2MAO -> 3MAO -> 1CAA, 2CAA, 3CAA -> 1DAA, 2DAA, 3DAA -> 2COO, 3COO -> Cuadrantes.
    """
    try:
        engine = MactorEngine(
            actors=req.actors,
            objectives=req.objectives,
            mid=req.mid,
            mao2=req.mao2,
            variant=req.variant or "softprosp",
            options=req.options
        )
        results = engine.run_all()
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en el cálculo MACTOR: {str(e)}")

@app.get("/api/mactor/cases")
def list_cases():
    """Lists preloaded real territorial cases and benchmark studies (including the manual case)."""
    summary = []
    for k, v in PRELOADED_CASES.items():
        summary.append({
            "id": v["id"],
            "title": v["title"],
            "territory": v["territory"],
            "description": v["description"],
            "source": v["source"],
            "actors_count": len(v["actors"]),
            "objectives_count": len(v["objectives"])
        })
    return {"cases": summary}

@app.get("/api/mactor/cases/{case_id}")
def get_case(case_id: str):
    """Returns full dataset for a specific preloaded case."""
    if case_id not in PRELOADED_CASES:
        raise HTTPException(status_code=404, detail="Caso de estudio no encontrado.")
    return {"case": PRELOADED_CASES[case_id]}

@app.post("/api/mactor/simulate")
def simulate_scenario(req: ScenarioSimRequest):
    """
    Evaluates 'What-If' scenarios:
    Compares baseline calculation vs modified matrices (e.g., actor alliances, policy shifts).
    """
    try:
        # Base engine
        base_engine = MactorEngine(
            actors=req.base_data.actors,
            objectives=req.base_data.objectives,
            mid=req.base_data.mid,
            mao2=req.base_data.mao2,
            variant=req.base_data.variant or "softprosp"
        )
        base_res = base_engine.run_all()

        # Modified engine
        sim_mid = req.modifications.get("mid", req.base_data.mid)
        sim_mao2 = req.modifications.get("mao2", req.base_data.mao2)
        
        sim_engine = MactorEngine(
            actors=req.base_data.actors,
            objectives=req.base_data.objectives,
            mid=sim_mid,
            mao2=sim_mao2,
            variant=req.base_data.variant or "softprosp"
        )
        sim_res = sim_engine.run_all()

        # Delta comparison
        convergence_delta = [
            round(s - b, 2) for s, b in zip(sim_res["actor_convergence"], base_res["actor_convergence"])
        ]
        
        return {
            "status": "success",
            "base_dominant": base_res["dominant_actor"],
            "sim_dominant": sim_res["dominant_actor"],
            "convergence_delta": convergence_delta,
            "base_results": base_res,
            "sim_results": sim_res
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en simulación: {str(e)}")

@app.post("/api/mactor/export/excel")
def export_excel(req: MactorCalculationRequest):
    """
    Generates a beautifully formatted multi-sheet Excel file (.xlsx) with all MACTOR matrices,
    indicators, quadrants, and formulas.
    """
    try:
        engine = MactorEngine(
            actors=req.actors,
            objectives=req.objectives,
            mid=req.mid,
            mao2=req.mao2,
            variant=req.variant or "softprosp"
        )
        res = engine.run_all()

        wb = openpyxl.Workbook()
        wb.remove(wb.active) # Remove default sheet

        # Styles
        header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid") # Navy
        sub_fill = PatternFill(start_color="3B82F6", end_color="3B82F6", fill_type="solid") # Blue
        accent_fill = PatternFill(start_color="10B981", end_color="10B981", fill_type="solid") # Emerald
        header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
        title_font = Font(name="Segoe UI", size=14, bold=True, color="1E3A8A")
        bold_font = Font(name="Segoe UI", size=10, bold=True)
        normal_font = Font(name="Segoe UI", size=10)
        thin_border = Border(
            left=Side(style="thin", color="D1D5DB"),
            right=Side(style="thin", color="D1D5DB"),
            top=Side(style="thin", color="D1D5DB"),
            bottom=Side(style="thin", color="D1D5DB")
        )
        center_align = Alignment(horizontal="center", vertical="center")

        def style_matrix_sheet(sheet, title, row_names, col_names, matrix_data, col_header="Actores", is_signed=False):
            sheet.views.sheetView[0].showGridLines = True
            sheet.cell(row=1, column=1, value=title).font = title_font
            
            # Headers
            sheet.cell(row=3, column=1, value=col_header).font = header_font
            sheet.cell(row=3, column=1).fill = header_fill
            sheet.cell(row=3, column=1).alignment = center_align
            sheet.cell(row=3, column=1).border = thin_border
            
            for c_idx, c_name in enumerate(col_names):
                cell = sheet.cell(row=3, column=c_idx + 2, value=c_name)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = center_align
                cell.border = thin_border

            # Data rows
            for r_idx, r_name in enumerate(row_names):
                row_num = r_idx + 4
                r_cell = sheet.cell(row=row_num, column=1, value=r_name)
                r_cell.font = bold_font
                r_cell.fill = PatternFill(start_color="F3F4F6", fill_type="solid")
                r_cell.border = thin_border
                
                for c_idx in range(len(col_names)):
                    val = matrix_data[r_idx][c_idx]
                    cell = sheet.cell(row=row_num, column=c_idx + 2, value=val)
                    cell.font = normal_font
                    cell.alignment = center_align
                    cell.border = thin_border
                    
                    # Highlight colors
                    if is_signed:
                        if val > 0:
                            cell.fill = PatternFill(start_color="DCFCE7", fill_type="solid") # light green
                        elif val < 0:
                            cell.fill = PatternFill(start_color="FEE2E2", fill_type="solid") # light red
                    elif val > 0 and r_idx != c_idx:
                        cell.fill = PatternFill(start_color="EFF6FF", fill_type="solid") # soft blue

            # Auto column width
            for col in sheet.columns:
                max_len = max(len(str(cell.value or '')) for cell in col)
                col_letter = get_column_letter(col[0].column)
                sheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

        # 1. Sheet: Resumen Ejecutivo
        ws_sum = wb.create_sheet(title="Resumen Ejecutivo")
        ws_sum.views.sheetView[0].showGridLines = True
        ws_sum.cell(row=1, column=1, value="INFORME PROSPECTIVO MACTOR - RESULTADOS").font = title_font
        ws_sum.cell(row=2, column=1, value=f"Variante Utilizada: {res['variant'].upper()}").font = Font(italic=True, size=10)
        
        ws_sum.cell(row=4, column=1, value="Actor Ganador / Máxima Convergencia:").font = bold_font
        ws_sum.cell(row=4, column=2, value=res["dominant_actor"]["name"]).font = Font(bold=True, size=11, color="1E3A8A")
        ws_sum.cell(row=5, column=1, value="Puntaje de Convergencia Total:").font = bold_font
        ws_sum.cell(row=5, column=2, value=res["dominant_actor"]["convergence_score"])

        ws_sum.cell(row=7, column=1, value="Clasificación en Cuadrantes Estratégicos (Godet):").font = title_font
        q_headers = ["Código", "Nombre del Actor", "Influencia", "Dependencia", "Cuadrante Estratégico"]
        for c_i, qh in enumerate(q_headers):
            c = ws_sum.cell(row=8, column=c_i+1, value=qh)
            c.font = header_font
            c.fill = header_fill
            c.alignment = center_align
            c.border = thin_border
            
        for r_i, q in enumerate(res["quadrants"]):
            ws_sum.cell(row=9+r_i, column=1, value=q["id"]).alignment = center_align
            ws_sum.cell(row=9+r_i, column=2, value=q["name"])
            ws_sum.cell(row=9+r_i, column=3, value=q["influence"]).alignment = center_align
            ws_sum.cell(row=9+r_i, column=4, value=q["dependence"]).alignment = center_align
            ws_sum.cell(row=9+r_i, column=5, value=q["quadrant"]).font = bold_font

        # 2. Sheet: MID
        act_names = [a.get("short_name", a["name"]) for a in req.actors]
        obj_names = [o.get("short_name", o["name"]) for o in req.objectives]
        
        ws_mid = wb.create_sheet(title="Matriz MID")
        style_matrix_sheet(ws_mid, "Matriz de Influencias Directas (MID)", act_names, act_names, res["mid"])

        # 3. Sheet: MIDI
        ws_midi = wb.create_sheet(title="Matriz MIDI")
        style_matrix_sheet(ws_midi, "Matriz de Influencias Directas e Indirectas (MIDI)", act_names, act_names, res["midi"])

        # 4. Sheet: 2MAO
        ws_mao2 = wb.create_sheet(title="Matriz 2MAO")
        style_matrix_sheet(ws_mao2, "Matriz Valorada de Posiciones (2MAO)", act_names, obj_names, res["mao2"], col_header="Actores \\ Objetivos", is_signed=True)

        # 5. Sheet: 3MAO
        ws_mao3 = wb.create_sheet(title="Matriz 3MAO Ponderada")
        style_matrix_sheet(ws_mao3, "Matriz Ponderada de Posiciones (3MAO)", act_names, obj_names, res["mao3"], col_header="Actores \\ Objetivos", is_signed=True)

        # 6. Sheet: 3CAA
        ws_caa = wb.create_sheet(title="Matriz 3CAA Alianzas")
        style_matrix_sheet(ws_caa, "Matriz Ponderada de Convergencias (3CAA - Grados de Alianza)", act_names, act_names, res["caa3"])

        # 7. Sheet: 3DAA
        ws_daa = wb.create_sheet(title="Matriz 3DAA Conflictos")
        style_matrix_sheet(ws_daa, "Matriz Ponderada de Divergencias (3DAA - Grados de Conflicto)", act_names, act_names, res["daa3"])

        # 8. Sheet: Movilización de Objetivos
        ws_obj = wb.create_sheet(title="Movilización Objetivos")
        ws_obj.views.sheetView[0].showGridLines = True
        ws_obj.cell(row=1, column=1, value="Métricas de Movilización y Conflicto por Objetivo").font = title_font
        obj_head = ["ID", "Objetivo", "Ponderación (%)", "A Favor", "En Contra", "Neutros", "Movilización", "Balance Neto", "Índice Conflicto", "Diagnóstico"]
        for c_i, oh in enumerate(obj_head):
            c = ws_obj.cell(row=3, column=c_i+1, value=oh)
            c.font = header_font
            c.fill = header_fill
            c.alignment = center_align
            c.border = thin_border
            
        for r_i, om in enumerate(res["objective_metrics"]):
            row_idx = 4 + r_i
            ws_obj.cell(row=row_idx, column=1, value=om["id"]).alignment = center_align
            ws_obj.cell(row=row_idx, column=2, value=om["name"])
            ws_obj.cell(row=row_idx, column=3, value=round(om["weight"] * 100, 1)).alignment = center_align
            ws_obj.cell(row=row_idx, column=4, value=om["favorable_actors"]).alignment = center_align
            ws_obj.cell(row=row_idx, column=5, value=om["opposed_actors"]).alignment = center_align
            ws_obj.cell(row=row_idx, column=6, value=om["neutral_actors"]).alignment = center_align
            ws_obj.cell(row=row_idx, column=7, value=om["mobilization"]).alignment = center_align
            ws_obj.cell(row=row_idx, column=8, value=om["net_balance"]).alignment = center_align
            ws_obj.cell(row=row_idx, column=9, value=om["conflict_index"]).alignment = center_align
            ws_obj.cell(row=row_idx, column=10, value=om["status"]).font = bold_font

        # Output to buffer
        stream = io.BytesIO()
        wb.save(stream)
        stream.seek(0)

        filename = "Estudio_Prospectivo_MACTOR.xlsx"
        return StreamingResponse(
            stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando Excel: {str(e)}")

# Mount static frontend files
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
