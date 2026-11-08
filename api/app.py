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
from motor_quizzes import MotorQuizzes

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
motor_quiz = MotorQuizzes()

class ResumoRequest(BaseModel):
    disciplina_id: str
    periodo: str = "Todos"
    conteudos: str
    nivel: str = "completo"

class AnkiRequest(BaseModel):
    disciplina_id: str
    periodo: str = "1_Periodo"

class QuizRequest(BaseModel):
    disciplina_id: str
    periodo: str = "Todos"
    topicos: str = ""
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
def get_disciplinas(ano: Optional[str] = None):
    return motor.listar_disciplinas(ano=ano)

@app.get("/api/manuais/{disc_id}")
def get_manuais(disc_id: str):
    return motor.obter_manuais(disc_id)

@app.get("/api/topicos/{disc_id}")
def get_topicos(disc_id: str, periodo: Optional[str] = "Todos"):
    return motor.listar_topicos_sugeridos(disc_id, periodo)

@app.get("/api/resumo/periodo")
def get_resumo_periodo(disciplina_id: str, periodo: Optional[str] = "1_Periodo"):
    try:
        dados = gerador.obter_resumo_periodo(disciplina_id, periodo)
        return dados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter resumo do período: {str(e)}")

@app.post("/api/exportar-pdf-periodo")
def post_exportar_pdf_periodo(dados: dict):
    try:
        pdf_bytes = exportador.gerar_pdf_resumo_periodo(dados)
        disc_id = dados.get("disciplina_id", "7ano")
        periodo = dados.get("periodo", "1_Periodo")
        nome_ficheiro = f"Dossie_Estudo_{disc_id}_{periodo}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{nome_ficheiro}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao compilar PDF do período: {str(e)}")

@app.post("/api/exportar-anki")
def post_exportar_anki(req: AnkiRequest):
    try:
        tsv_content = gerador.exportar_para_anki_tsv(req.disciplina_id, req.periodo)
        nome_ficheiro = f"Anki_Flashcards_{req.disciplina_id}_{req.periodo}.txt"
        return Response(
            content=tsv_content.encode("utf-8"),
            media_type="text/tab-separated-values; charset=utf-8",
            headers={"Content-Disposition": f'attachment; filename="{nome_ficheiro}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar baralho Anki: {str(e)}")

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
    # Gerar quiz pedagógico e rigoroso com questões curadas e conceitos reais do 7.º Ano
    questoes = motor_quiz.gerar_quiz_pedagogico(
        disciplina_id=req.disciplina_id,
        tema=req.topicos,
        quantidade=req.quantidade or 8
    )

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
