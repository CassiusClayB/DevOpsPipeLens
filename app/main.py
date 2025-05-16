from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import yaml
import random
from collections import Counter
from .analyze import analyze_pipeline
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import matplotlib.pyplot as plt
import os 
from fpdf import FPDF
import matplotlib.pyplot as plt
import os
from datetime import datetime


# Armazenamento em memória
pipeline_history = []
last_jobs_details = {}

app = FastAPI(title="DevOpsPipeLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "DevOpsPipeLens API está no ar! 🚀"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.filename.endswith((".yml", ".yaml")):
        return JSONResponse(status_code=400, content={"error": "Arquivo deve ser YAML (.yml ou .yaml)"})
    
    content = await file.read()
    try:
        pipeline_data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        return JSONResponse(status_code=400, content={"error": f"Erro ao processar YAML: {str(e)}"})

    result = analyze_pipeline(pipeline_data)

    # Armazenar dados
    pipeline_history.append({
        "score": result['score'],
        "warnings": result['warnings'],
        "suggestions": result['suggestions'],
    })

    global last_jobs_details
    last_jobs_details = pipeline_data.get("jobs") or pipeline_data  # guarda os últimos jobs analisados

    return result

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/history")
async def get_history():
    return {"history": pipeline_history}

@app.get("/metrics")
async def get_metrics():
    if not pipeline_history:
        raise HTTPException(status_code=404, detail="Nenhum dado de métricas encontrado.")
    metrics = [{"timestamp": idx + 1, "score": entry["score"], "warnings": entry["warnings"], "suggestions": entry["suggestions"]} for idx, entry in enumerate(pipeline_history)]
    return {"metrics": metrics}

@app.get("/jobs/details")
async def get_jobs_details():
    if not last_jobs_details:
        raise HTTPException(status_code=404, detail="Nenhum job analisado ainda.")
    return {"jobs": last_jobs_details}

@app.get("/score/average")
async def get_average_score():
    if not pipeline_history:
        raise HTTPException(status_code=404, detail="Nenhuma análise feita ainda.")
    average = sum(entry["score"] for entry in pipeline_history) / len(pipeline_history)
    return {"average_score": round(average, 2)}

@app.get("/warnings/frequent")
async def get_frequent_warnings():
    warnings_list = [warn for entry in pipeline_history for warn in entry["warnings"]]
    counter = Counter(warnings_list)
    return {"frequent_warnings": counter.most_common(5)}

@app.get("/suggestions/random")
async def get_random_suggestion():
    all_suggestions = [s for entry in pipeline_history for s in entry["suggestions"]]
    if not all_suggestions:
        raise HTTPException(status_code=404, detail="Nenhuma sugestão disponível ainda.")
    return {"suggestion": random.choice(all_suggestions)}


@app.get("/report")
async def generate_report():
    if not pipeline_history:
        raise HTTPException(status_code=404, detail="Nenhum dado disponível para gerar relatório.")

    # Gera o gráfico e salva como imagem
    scores = [entry["score"] for entry in pipeline_history]
    labels = [f"Execução {i+1}" for i in range(len(pipeline_history))]

    plt.figure(figsize=(8, 4))
    plt.bar(labels, scores, color='skyblue')
    plt.title("Scores das Análises")
    plt.xlabel("Execuções")
    plt.ylabel("Score")
    plt.ylim(0, 100)
    chart_path = "chart.png"
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    # Cria o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Relatório DevOpsPipeLens", ln=True, align='C')
    pdf.ln(10)

    # Score médio
    average = round(sum(scores) / len(scores), 2)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Score Médio: {average}", ln=True)
    pdf.ln(5)

    # Warnings frequentes
    warnings_list = [w for entry in pipeline_history for w in entry["warnings"]]
    counter = Counter(warnings_list)
    pdf.cell(0, 10, "Warnings Frequentes:", ln=True)
    for warning, count in counter.most_common(5):
        pdf.cell(0, 10, f"- {warning} (x{count})", ln=True)
    pdf.ln(5)

    # Adiciona gráfico
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Gráfico de Scores:", ln=True)
    pdf.image(chart_path, x=30, y=None, w=150)
    pdf.ln(10)

    # Detalhes das execuções
    pdf.set_font("Arial", '', 11)
    for i, entry in enumerate(pipeline_history, 1):
        pdf.multi_cell(0, 10, f"Execução {i} - Score: {entry['score']}")
        pdf.cell(0, 10, f"Warnings: {len(entry['warnings'])}", ln=True)
        pdf.cell(0, 10, f"Sugestões: {len(entry['suggestions'])}", ln=True)
        pdf.ln(5)

    # Salva o PDF
    output_path = "relatorio_devops.pdf"
    pdf.output(output_path)

    # Remove imagem temporária
    if os.path.exists(chart_path):
        os.remove(chart_path)

    return FileResponse(output_path, media_type='application/pdf', filename=output_path)
