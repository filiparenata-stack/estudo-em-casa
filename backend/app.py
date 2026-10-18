import os
import sys
import io
import subprocess

DIR_BACKEND = os.path.dirname(os.path.abspath(__file__))
if DIR_BACKEND not in sys.path:
    sys.path.insert(0, DIR_BACKEND)

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List

from motor_busca import MotorBusca, REPO_7ANO
from extrator_questoes import ExtratorQuestoes
from gerador_resumos import GeradorResumos
from exportador_pdf import ExportadorPDF

app = FastAPI(
    title="Escola Virtual 7.º Ano - API de Estudo e Resumos",
    description="Backend para geração de resumos, quizzes interativos e flashcards a partir dos materiais da Escola Virtual.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

motor = MotorBusca()
extrator = ExtratorQuestoes()
gerador = GeradorResumos(motor, extrator)
exportador = ExportadorPDF()

class ResumoRequest(BaseModel):
    disciplina_id: str
    periodo: str = "Todos"
    conteudos: str
    nivel: str = "completo"

class QuizRequest(BaseModel):
    disciplina_id: str
    periodo: str = "Todos"
    topicos: str
    quantidade: int = 10

class AbrirFicheiroRequest(BaseModel):
    caminho: str

@app.get("/api/status")
def get_status():
    return {
        "status": "online",
        "repositorio": REPO_7ANO,
        "total_disciplinas": len(motor.listar_disciplinas()),
        "total_recursos_catalogo": len(motor.catalogo.get("recursos_descarregados", []))
    }

@app.get("/api/disciplinas")
def get_disciplinas():
    return motor.listar_disciplinas()

@app.get("/api/manuais/{disc_id}")
def get_manuais(disc_id: str):
    return motor.obter_manuais(disc_id)

@app.get("/api/topicos/{disc_id}")
def get_topicos(disc_id: str, periodo: Optional[str] = "Todos"):
    return motor.listar_topicos_sugeridos(disc_id, periodo)

@app.post("/api/resumo")
def post_gerar_resumo(req: ResumoRequest):
    if not req.conteudos.strip():
        raise HTTPException(status_code=400, detail="Por favor insere os conteúdos que o professor indicou.")
    
    resumo = gerador.gerar_resumo_estruturado(
        disc_id=req.disciplina_id,
        periodo=req.periodo,
        indicacao_professor=req.conteudos,
        nivel=req.nivel
    )
    return resumo

@app.post("/api/exportar-pdf")
def post_exportar_pdf(resumo: dict):
    try:
        pdf_bytes = exportador.gerar_pdf_resumo(resumo)
        nome_ficheiro = f"Resumo_{resumo.get('disciplina_id', '7ano')}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{nome_ficheiro}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao compilar PDF: {str(e)}")

@app.post("/api/quiz")
def post_gerar_quiz(req: QuizRequest):
    pasta_disc = os.path.join(REPO_7ANO, req.disciplina_id)
    if not os.path.exists(pasta_disc):
        raise HTTPException(status_code=404, detail="Pasta da disciplina não encontrada.")
    
    questoes = extrator.buscar_questoes_por_topico(pasta_disc, req.topicos, limite=req.quantidade)
    
    # Se não houver questões suficientes extraídas de docx, gerar questões estruturadas a partir dos conceitos
    if len(questoes) < 3:
        resumo = gerador.gerar_resumo_estruturado(req.disciplina_id, req.periodo, req.topicos)
        conceitos = resumo.get("conceitos_chave", [])
        for idx, c in enumerate(conceitos):
            questoes.append({
                "id": f"q_gen_{idx+1}",
                "numero": f"{idx+1}",
                "grupo": "Consolidação Conceitual",
                "enunciado": f"Considera o tema «{req.topicos}». Qual das seguintes afirmações define corretamente o conceito de {c['termo']}?",
                "tipo": "escolha_multipla",
                "opcoes": [
                    {"letra": "A", "texto": c["definicao"]},
                    {"letra": "B", "texto": f"É uma propriedade irrelevante no contexto de {c['termo']}."},
                    {"letra": "C", "texto": f"Aplica-se apenas em casos excecionais onde não ocorre {c['termo']}."},
                    {"letra": "D", "texto": "Nenhuma das opções anteriores está correta."}
                ],
                "resposta_correta": "A",
                "explicacao": f"Definição oficial do programa: {c['definicao']}",
                "ficheiro_origem": "Conceitos Oficiais do Manual 7.º Ano"
            })

    return {
        "disciplina_id": req.disciplina_id,
        "topicos": req.topicos,
        "total_questoes": len(questoes),
        "questoes": questoes
    }

@app.post("/api/abrir-ficheiro")
def post_abrir_ficheiro(req: AbrirFicheiroRequest):
    if not os.path.exists(req.caminho):
        raise HTTPException(status_code=404, detail="Ficheiro não encontrado.")
    try:
        os.startfile(req.caminho)
        return {"status": "ok", "mensagem": f"Ficheiro aberto: {os.path.basename(req.caminho)}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Servir Frontend compilado se existir
FRONTEND_DIST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")
if os.path.exists(FRONTEND_DIST):
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
