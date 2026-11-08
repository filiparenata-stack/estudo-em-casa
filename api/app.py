import os
import sys
import io
import time
import urllib.request
import urllib.parse
import subprocess

DIR_BACKEND = os.path.dirname(os.path.abspath(__file__))
if DIR_BACKEND not in sys.path:
    sys.path.insert(0, DIR_BACKEND)

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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
        periodo=req.periodo,
        tema=req.topicos or "",
        quantidade=req.quantidade or 8
    )

    return {
        "disciplina_id": req.disciplina_id,
        "periodo": req.periodo,
        "topicos": req.topicos,
        "total_questoes": len(questoes),
        "questoes": questoes
    }

# Cache em memória para URLs assinados de GitHub Releases (evita 302 extra em cada chunk Range)
_GITHUB_ASSET_CACHE = {}
_MAX_CHUNK_BYTES = 1024 * 1024  # Máximo 1 MB por resposta Range (seguro para Vercel Serverless)


def _resolver_caminho_local_pdf(file_name: Optional[str], caminho: Optional[str]) -> Optional[str]:
    if caminho and os.path.isfile(caminho):
        return caminho
    if file_name:
        safe_name = os.path.basename(file_name)
        dir_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        candidatos = [
            os.path.join(dir_raiz, "public", "books", safe_name),
            os.path.join(dir_raiz, "frontend", "public", "books", safe_name),
            os.path.join(dir_raiz, "frontend", "dist", "books", safe_name),
        ]
        for c in candidatos:
            if os.path.isfile(c) and os.path.getsize(c) > 1024:
                return c
    return None


def _obter_url_github_manual(file_name: Optional[str], url: Optional[str]) -> Optional[str]:
    if file_name:
        safe_name = os.path.basename(file_name)
        info = getattr(motor, "urls_github", {}).get(safe_name)
        if isinstance(info, dict) and info.get("url"):
            return info["url"]
        if isinstance(info, str) and info.startswith("http"):
            return info
        # Fallback direto para a release oficial v1.0-manuais-7ano
        return f"https://github.com/filiparenata-stack/estudo-em-casa/releases/download/v1.0-manuais-7ano/{urllib.parse.quote(safe_name)}"
    if url and url.startswith("https://github.com/filiparenata-stack/estudo-em-casa/releases/download/"):
        return url
    return None


def _parse_range_header(range_header: Optional[str], total_size: Optional[int] = None):
    if not range_header or not range_header.startswith("bytes="):
        return 0, _MAX_CHUNK_BYTES - 1, False
    try:
        spec = range_header.replace("bytes=", "").split(",")[0].strip()
        parts = spec.split("-")
        start = int(parts[0]) if parts[0] else 0
        if len(parts) > 1 and parts[1]:
            end = int(parts[1])
        else:
            end = start + _MAX_CHUNK_BYTES - 1
        if end - start + 1 > _MAX_CHUNK_BYTES:
            end = start + _MAX_CHUNK_BYTES - 1
        if total_size is not None and total_size > 0:
            end = min(end, total_size - 1)
        return max(0, start), max(start, end), True
    except Exception:
        return 0, _MAX_CHUNK_BYTES - 1, False


@app.api_route("/api/pdf-proxy", methods=["GET", "HEAD"])
def proxy_pdf_inline(
    request: Request,
    file: Optional[str] = None,
    caminho: Optional[str] = None,
    url: Optional[str] = None
):
    """
    Serve ficheiros PDF (locais ou do GitHub Releases) com suporte a HTTP Range (206 Partial Content)
    e Content-Disposition: inline para o leitor PDF.js em Canvas, evitando downloads automáticos.
    """
    range_header = request.headers.get("range") or request.headers.get("Range")
    cors_headers = {
        "Accept-Ranges": "bytes",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Expose-Headers": "Accept-Ranges, Content-Range, Content-Length, Content-Type",
    }

    # 1. Tentar servir a partir do disco local (3.º Ano /public/books ou 7.º Ano local)
    local_path = _resolver_caminho_local_pdf(file, caminho)
    if local_path:
        total_size = os.path.getsize(local_path)
        nome_seguro = os.path.basename(local_path)
        headers_base = {
            **cors_headers,
            "Content-Disposition": f'inline; filename="{nome_seguro}"',
        }
        if request.method == "HEAD":
            return Response(
                status_code=200,
                media_type="application/pdf",
                headers={**headers_base, "Content-Length": str(total_size)},
            )
        start, end, is_ranged = _parse_range_header(range_header, total_size)
        if is_ranged or total_size > 4 * 1024 * 1024:
            with open(local_path, "rb") as f:
                f.seek(start)
                chunk = f.read(end - start + 1)
            return Response(
                content=chunk,
                status_code=206,
                media_type="application/pdf",
                headers={
                    **headers_base,
                    "Content-Range": f"bytes {start}-{start + len(chunk) - 1}/{total_size}",
                    "Content-Length": str(len(chunk)),
                },
            )
        return FileResponse(
            local_path,
            media_type="application/pdf",
            headers=headers_base,
        )

    # 2. Servir via proxy HTTP Range a partir do GitHub Releases
    gh_url = _obter_url_github_manual(file, url)
    if not gh_url:
        raise HTTPException(status_code=404, detail="Manual PDF não especificado ou não encontrado.")

    nome_seguro = os.path.basename(urllib.parse.unquote(gh_url.split("?")[0]))
    agora = time.time()
    cached = _GITHUB_ASSET_CACHE.get(gh_url)
    target_url = cached["signed_url"] if (cached and cached["expires_at"] > agora) else gh_url
    cached_total = cached.get("total_size") if cached else None

    start, end, _ = _parse_range_header(range_header, cached_total)
    if request.method == "HEAD":
        start, end = 0, 0

    for tentativa in range(2):
        try:
            req_upstream = urllib.request.Request(
                target_url,
                headers={
                    "User-Agent": "EstudoEmCasa-PDFReader/1.0",
                    "Range": f"bytes={start}-{end}",
                },
                method="GET",
            )
            with urllib.request.urlopen(req_upstream, timeout=20) as resp:
                final_url = resp.geturl()
                content_range = resp.headers.get("Content-Range") or ""
                data = resp.read()

                total_size = cached_total
                if "/" in content_range:
                    try:
                        total_size = int(content_range.split("/")[-1].strip())
                    except ValueError:
                        pass
                if not total_size:
                    cl = resp.headers.get("Content-Length")
                    total_size = int(cl) if cl and cl.isdigit() else len(data)

                if final_url and final_url != gh_url:
                    _GITHUB_ASSET_CACHE[gh_url] = {
                        "signed_url": final_url,
                        "total_size": total_size,
                        "expires_at": agora + 600,
                    }

                headers_resp = {
                    **cors_headers,
                    "Content-Disposition": f'inline; filename="{nome_seguro}"',
                }

                if request.method == "HEAD":
                    return Response(
                        status_code=200,
                        media_type="application/pdf",
                        headers={**headers_resp, "Content-Length": str(total_size)},
                    )

                actual_end = start + len(data) - 1
                return Response(
                    content=data,
                    status_code=206,
                    media_type="application/pdf",
                    headers={
                        **headers_resp,
                        "Content-Range": content_range or f"bytes {start}-{actual_end}/{total_size}",
                        "Content-Length": str(len(data)),
                    },
                )
        except Exception as e:
            if tentativa == 0 and gh_url in _GITHUB_ASSET_CACHE:
                _GITHUB_ASSET_CACHE.pop(gh_url, None)
                target_url = gh_url
                continue
            raise HTTPException(status_code=502, detail=f"Erro ao obter PDF remoto: {str(e)}")


@app.post("/api/abrir-ficheiro")
def post_abrir_ficheiro(req: AbrirFicheiroRequest):
    if not os.path.exists(req.caminho):
        raise HTTPException(status_code=404, detail="Ficheiro não encontrado.")
    try:
        os.startfile(req.caminho)
        return {"status": "ok", "mensagem": f"Ficheiro aberto: {os.path.basename(req.caminho)}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Servir pasta /books com os manuais digitalizados do 3.º Ano se existir
DIR_RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_BOOKS_DIR = os.path.join(DIR_RAIZ_PROJETO, "public", "books")
if os.path.isdir(PUBLIC_BOOKS_DIR):
    app.mount("/books", StaticFiles(directory=PUBLIC_BOOKS_DIR), name="books")

# Servir Frontend compilado se existir
FRONTEND_DIST = os.path.join(DIR_RAIZ_PROJETO, "frontend", "dist")
if os.path.exists(FRONTEND_DIST):
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
