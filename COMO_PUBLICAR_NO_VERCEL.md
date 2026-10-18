# 🚀 Como Publicar a Tua Aplicação no Vercel

A aplicação foi configurada e estruturada para ser **100% compatível com a plataforma Vercel**:
* **Frontend**: React + Vite + Tailwind CSS (Deploy estático com CDN mundial ultrarrápida).
* **Backend**: Python Serverless Functions (`api/index.py` com FastAPI).
* **Base de Dados/Conhecimento**: O catálogo mestre com 3.355 recursos de avaliação (`api/data/catalogo_7ano_quiz_index.json`) já está embutido na pasta do backend.

---

## 🌟 Opção 1: Publicação com 1 Comando via Vercel CLI (Mais Rápida)

1. Abre o terminal (PowerShell ou Linha de Comandos) dentro da pasta:
   ```powershell
   cd c:\Users\Miguel\Documents\ESCOLA\app_estudo_7ano
   ```

2. Executa o comando da Vercel:
   ```powershell
   npx vercel
   ```

3. O terminal vai perguntar se queres fazer login (podes escolher com o teu email ou conta GitHub).
4. Aceita as opções padrão pressionando `Enter`:
   * *Set up and deploy?* **Y**
   * *Which scope?* (o teu utilizador)
   * *Link to existing project?* **N**
   * *Project name?* **escola-virtual-7ano**
   * *In which directory is your code located?* **./**
5. Em cerca de 30 segundos, o Vercel dá-te o link público da tua aplicação (ex: `https://escola-virtual-7ano.vercel.app`)!

---

## 🐙 Opção 2: Publicação via GitHub (Recomendada para Deploy Automático)

1. Cria um repositório no teu GitHub (ex.: `escola-virtual-7ano`).
2. No teu computador, envia o código já preparado para o GitHub:
   ```powershell
   cd c:\Users\Miguel\Documents\ESCOLA\app_estudo_7ano
   git remote add origin https://github.com/<O-TEU-UTILIZADOR>/escola-virtual-7ano.git
   git branch -M main
   git push -u origin main
   ```
3. Acede a **[vercel.com/new](https://vercel.com/new)**.
4. Clica em **«Import»** no repositório `escola-virtual-7ano`.
5. Clica em **«Deploy»**.
6. A partir desse momento, qualquer alteração que faças é atualizada automaticamente na nuvem!

---

## 📌 Configuração Técnica que já foi Aplicada
* ✅ `vercel.json` configurado com rotas rewrites para `/api/(.*)` -> `/api/index.py`.
* ✅ `requirements.txt` com todas as dependências serverless (`fastapi`, `pydantic`, `reportlab`, etc.).
* ✅ `package.json` raiz com comando de build unificado (`cd frontend && npm install && npm run build`).
* ✅ Todos os caminhos da API no Frontend ajustados para rotas relativas (`/api/...`).
