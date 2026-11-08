import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  FolderOpen,
  Search,
  ExternalLink,
  FileText,
  CheckCircle,
  Sparkles,
  Download,
  GraduationCap,
  Filter,
  X,
  ArrowRight,
  DownloadCloud
} from 'lucide-react';
import { LIVROS_RENATA_3ANO } from '../data/booksCatalog';
import BookReaderModal from './BookReaderModal';

export default function BibliotecaView({ disciplina, onVerResumos, anoAtivo = '3' }) {
  const [manuais, setManuais] = useState([]);
  const [busca, setBusca] = useState('');
  const [abertoInfo, setAbertoInfo] = useState(null);
  const [filtroCategoria, setFiltroCategoria] = useState(anoAtivo === '3' ? 'renata' : 'todos');

  // Estado para o Leitor Online de PDFs
  const [leitorAberto, setLeitorAberto] = useState(false);
  const [livroSelecionado, setLivroSelecionado] = useState(null);
  const [paginaInicialLeitor, setPaginaInicialLeitor] = useState(1);

  // Estado para a Gaveta / Modal de Resumos Curriculares
  const [resumosModalLivro, setResumosModalLivro] = useState(null);

  useEffect(() => {
    if (anoAtivo === '3') {
      setFiltroCategoria('renata');
    } else if (anoAtivo === '7') {
      setFiltroCategoria('todos');
    }
  }, [anoAtivo]);

  useEffect(() => {
    if (!disciplina) return;
    fetch(`/api/manuais/${disciplina.id}`)
      .then((res) => res.json())
      .then((data) => setManuais(data || []))
      .catch(() => setManuais([]));
  }, [disciplina]);

  const abrirFicheiro = async (caminho) => {
    try {
      const resp = await fetch('/api/abrir-ficheiro', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ caminho })
      });
      if (resp.ok) {
        setAbertoInfo(caminho);
        setTimeout(() => setAbertoInfo(null), 3000);
      } else {
        alert('Este ficheiro PDF encontra-se guardado localmente no teu PC. Para o abrir com 1 clique, executa a aplicação no computador com o ficheiro iniciar_app.bat.');
      }
    } catch {
      alert('Para abrir PDFs diretamente do disco rígido, executa a app no computador através do ficheiro iniciar_app.bat.');
    }
  };

  // Abrir o Leitor Online Interativo
  const handleLerOnline = (livro, pagina = 1) => {
    setLivroSelecionado(livro);
    setPaginaInicialLeitor(pagina);
    setLeitorAberto(true);
  };

  // Abrir o Modal de Resumos e Estrutura Curricular
  const handleAbrirResumos = (livro) => {
    if (onVerResumos && typeof onVerResumos === 'function') {
      onVerResumos(livro.disciplinaId);
    } else {
      setResumosModalLivro(livro);
    }
  };

  // Filtragem dos Livros da Renata (3.º Ano)
  const livrosRenataFiltrados = LIVROS_RENATA_3ANO.filter((livro) => {
    const termo = busca.toLowerCase();
    const coincideBusca =
      livro.titulo.toLowerCase().includes(termo) ||
      livro.disciplina.toLowerCase().includes(termo) ||
      livro.descricao.toLowerCase().includes(termo) ||
      livro.unidades.some((u) =>
        u.titulo.toLowerCase().includes(termo) ||
        (u.descricao && u.descricao.toLowerCase().includes(termo)) ||
        (u.conceitos && u.conceitos.some((c) => c.toLowerCase().includes(termo)))
      );

    if (filtroCategoria === 'oficiais') return false;
    return coincideBusca;
  });

  // Filtragem dos Manuais do 7.º Ano
  const manuaisFiltrados = manuais.filter((m) => {
    const termo = busca.toLowerCase();
    const coincideBusca =
      (m.nome || '').toLowerCase().includes(termo) ||
      (m.projeto || '').toLowerCase().includes(termo) ||
      (m.nome_simples || '').toLowerCase().includes(termo);

    if (filtroCategoria === 'renata') return false;
    return coincideBusca;
  });

  return (
    <div className="flex-1 p-4 sm:p-6 max-w-6xl mx-auto flex flex-col gap-6">
      {/* Banner Informativo Global */}
      <div className="bg-gradient-to-r from-blue-50 via-indigo-50 to-purple-50 border border-blue-200/80 rounded-2xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs text-blue-900 shadow-sm">
        <div className="flex items-center gap-2.5">
          <Sparkles className="w-4 h-4 text-purple-600 shrink-0" />
          <span>
            <strong>Acervo Digital & Livros da Renata:</strong> Consulta os manuais escolares digitalizados em alta resolução (3.º Ano do 1.º Ciclo e 7.º Ano). Disponíveis para leitura online com leitor integrado e download direto de PDFs otimizados.
          </span>
        </div>
        <div className="flex items-center gap-1.5 text-slate-500 font-medium shrink-0">
          <DownloadCloud className="w-3.5 h-3.5 text-emerald-600" />
          <span>Fast Web View ⚡ • OCR Ativo</span>
        </div>
      </div>

      {/* Cabeçalho da Biblioteca com Pesquisa e Filtros */}
      <div className="bg-white rounded-2xl p-5 sm:p-6 border border-slate-200 shadow-sm flex flex-col gap-4">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs uppercase font-extrabold tracking-wider text-blue-600 bg-blue-50 px-2.5 py-0.5 rounded-md border border-blue-100">
                Biblioteca Digital
              </span>
              <span className="text-xs font-semibold text-purple-700 bg-purple-50 px-2.5 py-0.5 rounded-md border border-purple-100 flex items-center gap-1">
                <GraduationCap className="w-3 h-3" />
                3.º Ano & 7.º Ano
              </span>
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-slate-800 mt-1">
              Manuais Escolares e Livros de Estudo
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
              Acede aos livros escolares digitalizados da Renata e ao acervo completo de manuais com um clique.
            </p>
          </div>

          {/* Campo de Pesquisa */}
          <div className="relative w-full md:w-72">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
              placeholder="Pesquisar manual, livro ou unidade..."
              className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-300 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-all"
            />
            {busca && (
              <button
                onClick={() => setBusca('')}
                className="absolute right-2.5 top-2.5 text-slate-400 hover:text-slate-600"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </div>

        {/* Abas de Filtragem de Categoria */}
        <div className="flex items-center gap-2 pt-2 border-t border-slate-100 flex-wrap">
          <button
            onClick={() => setFiltroCategoria('todos')}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all cursor-pointer flex items-center gap-1.5 ${
              filtroCategoria === 'todos'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            <Filter className="w-3 h-3" />
            Todos os Manuais ({livrosRenataFiltrados.length + manuaisFiltrados.length})
          </button>
          <button
            onClick={() => setFiltroCategoria('renata')}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all cursor-pointer flex items-center gap-1.5 ${
              filtroCategoria === 'renata'
                ? 'bg-purple-600 text-white shadow-sm'
                : 'bg-purple-50 text-purple-700 hover:bg-purple-100 border border-purple-200'
            }`}
          >
            <span>📚 Livros da Renata (3.º Ano)</span>
            <span className="px-1.5 py-0.2 rounded-full text-[10px] bg-purple-200/60 font-bold">
              {livrosRenataFiltrados.length}
            </span>
          </button>
          <button
            onClick={() => setFiltroCategoria('oficiais')}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all cursor-pointer flex items-center gap-1.5 ${
              filtroCategoria === 'oficiais'
                ? 'bg-slate-800 text-white shadow-sm'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            <FolderOpen className="w-3 h-3" />
            Manuais Oficiais (7.º Ano) ({manuaisFiltrados.length})
          </button>
        </div>
      </div>

      {abertoInfo && (
        <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 px-4 py-2.5 rounded-xl text-xs flex items-center gap-2 animate-fadeIn shadow-sm">
          <CheckCircle className="w-4 h-4 text-emerald-600" />
          <span>Ficheiro aberto com sucesso no teu leitor de PDF predefinido!</span>
        </div>
      )}

      {/* ========================================================================= */}
      {/* SECÇÃO PROMINENTE: LIVROS DA RENATA (3.º ANO) */}
      {/* ========================================================================= */}
      {filtroCategoria !== 'oficiais' && (
        <section className="flex flex-col gap-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div className="flex items-center gap-2.5">
              <span className="text-xl">📚</span>
              <div>
                <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2">
                  Livros da Renata (3.º Ano)
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-sm">
                    4 Manuais Digitalizados
                  </span>
                </h3>
                <p className="text-xs text-slate-500">
                  Manuais oficiais digitalizados da Porto Editora com páginas alinhadas, OCR em português e visualizador interativo embutido.
                </p>
              </div>
            </div>
          </div>

          {livrosRenataFiltrados.length === 0 ? (
            <div className="bg-white rounded-2xl p-8 border border-slate-200 text-center text-slate-500 text-xs">
              Nenhum livro da Renata encontrado para a pesquisa "{busca}".
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {livrosRenataFiltrados.map((livro) => (
                <div
                  key={livro.id}
                  className={`bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-all flex flex-col justify-between overflow-hidden group ${
                    livro.corTema?.bordaHover || 'hover:border-blue-300'
                  }`}
                >
                  {/* Capa Ilustrada / Thumbnail */}
                  <div
                    className={`h-40 p-4 bg-gradient-to-br ${
                      livro.corTema?.gradienteCapa || 'from-indigo-600 to-purple-800'
                    } text-white flex flex-col justify-between relative overflow-hidden`}
                  >
                    {/* Efeito decorativo de fundo */}
                    <div className="absolute -right-4 -bottom-4 w-28 h-28 rounded-full bg-white/10 blur-xl pointer-events-none" />
                    <div className="absolute -left-4 -top-4 w-24 h-24 rounded-full bg-black/10 blur-md pointer-events-none" />

                    <div className="flex items-start justify-between relative z-10">
                      <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-white/20 backdrop-blur-md text-white border border-white/30">
                        {livro.ano}
                      </span>
                      <span className="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-emerald-500/90 text-white shadow-xs flex items-center gap-1">
                        Fast Web View ⚡
                      </span>
                    </div>

                    <div className="relative z-10">
                      <span className="text-[10px] font-medium uppercase tracking-wider text-white/80 block">
                        {livro.disciplina}
                      </span>
                      <h4 className="text-base font-extrabold leading-snug drop-shadow-sm line-clamp-2">
                        {livro.titulo}
                      </h4>
                    </div>

                    <div className="flex items-center justify-between text-[10px] text-white/80 border-t border-white/20 pt-1.5 relative z-10">
                      <span>{livro.editora}</span>
                      <span>{livro.paginas} págs • {livro.tamanhoFormatado}</span>
                    </div>
                  </div>

                  {/* Corpo do Card com Metadados e Descrição */}
                  <div className="p-4 flex-1 flex flex-col justify-between gap-3">
                    <div>
                      <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed">
                        {livro.descricao}
                      </p>

                      {/* Lista de Unidades / Tags de Tópicos */}
                      <div className="mt-2.5 pt-2 border-t border-slate-100 flex flex-wrap gap-1">
                        {livro.unidades?.slice(0, 2).map((u) => (
                          <button
                            key={u.numero}
                            onClick={() => handleLerOnline(livro, u.paginaInicio)}
                            className="text-[10px] font-medium px-2 py-0.5 rounded bg-slate-50 text-slate-600 hover:bg-blue-50 hover:text-blue-700 transition-colors cursor-pointer border border-slate-200/70"
                            title={`Saltar diretamente para ${u.titulo} (Pág. ${u.paginaInicio})`}
                          >
                            Pág. {u.paginaInicio}: {u.titulo.split(':')[1] || u.titulo}
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Botões de Ação Rápida */}
                    <div className="pt-3 border-t border-slate-100 flex flex-col gap-2">
                      <div className="flex items-center gap-1.5">
                        {/* Botão Ler Online (abre modal interativo) */}
                        <button
                          onClick={() => handleLerOnline(livro, 1)}
                          className={`flex-1 px-3 py-2 rounded-xl text-white text-xs font-bold flex items-center justify-center gap-1.5 transition-all shadow-sm cursor-pointer ${
                            livro.corTema?.botaoBg || 'bg-blue-600 hover:bg-blue-700'
                          }`}
                        >
                          <BookOpen className="w-3.5 h-3.5" />
                          <span>Ler Online</span>
                        </button>

                        {/* Botão Ver Resumos */}
                        <button
                          onClick={() => handleAbrirResumos(livro)}
                          className="px-2.5 py-2 rounded-xl bg-slate-100 hover:bg-purple-100 text-slate-700 hover:text-purple-800 text-xs font-semibold flex items-center gap-1 transition-colors cursor-pointer border border-slate-200"
                          title="Ver unidades curriculares e resumos pedagógicos"
                        >
                          <FileText className="w-3.5 h-3.5 text-purple-600" />
                          <span className="hidden sm:inline">Ver Resumos</span>
                        </button>
                      </div>

                      {/* Botão Descarregar PDF (link direto para /books/livro_<disciplina>_3ano.pdf) */}
                      <a
                        href={livro.pdfUrl}
                        download={livro.canonicalFilename}
                        className="w-full px-3 py-1.5 rounded-xl bg-slate-50 hover:bg-emerald-50 text-slate-600 hover:text-emerald-700 text-[11px] font-semibold flex items-center justify-center gap-1.5 transition-colors border border-slate-200 hover:border-emerald-200 cursor-pointer"
                        title="Descarregar ficheiro PDF completo para o teu dispositivo"
                      >
                        <Download className="w-3 h-3 text-emerald-600" />
                        <span>Descarregar PDF ({livro.tamanhoFormatado})</span>
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      )}

      {/* ========================================================================= */}
      {/* SECÇÃO OFICIAL: MANUAIS DO 7.º ANO */}
      {/* ========================================================================= */}
      {filtroCategoria !== 'renata' && (
        <section className="flex flex-col gap-4 pt-4 border-t border-slate-200">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div className="flex items-center gap-2.5">
              <span className="text-xl">📁</span>
              <div>
                <h3 className="text-lg font-bold text-slate-800">
                  Manuais e Dossiês do 7.º Ano {disciplina ? `— ${disciplina.nome}` : ''}
                </h3>
                <p className="text-xs text-slate-500">
                  Acervo oficial de 79 manuais e cadernos de atividades para o 7.º ano do Ensino Básico.
                </p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {manuaisFiltrados.map((m, idx) => (
              <div
                key={idx}
                className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm hover:shadow-md hover:border-blue-300 transition-all flex flex-col justify-between gap-4 group"
              >
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center font-bold shrink-0 group-hover:scale-105 transition-transform">
                    <BookOpen className="w-5 h-5" />
                  </div>
                  <div className="min-w-0">
                    <h3 className="text-sm font-bold text-slate-800 leading-snug line-clamp-2">
                      {m.nome_simples || m.nome}
                    </h3>
                    <p className="text-[11px] text-slate-500 truncate mt-0.5">
                      {m.projeto || 'Escola Virtual 7.º Ano'}
                    </p>
                    <div className="flex flex-wrap gap-1 mt-1.5">
                      {m.url_github && (
                        <span className="inline-block px-2 py-0.5 rounded-md text-[10px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                          PDF GitHub Cloud
                        </span>
                      )}
                      {m.tem_pdf_local && (
                        <span className="inline-block px-2 py-0.5 rounded-md text-[10px] font-semibold bg-blue-50 text-blue-700 border border-blue-200">
                          PDF Local (PC)
                        </span>
                      )}
                      {!m.url_github && !m.tem_pdf_local && (
                        <span className="inline-block px-2 py-0.5 rounded-md text-[10px] font-semibold bg-slate-100 text-slate-600 border border-slate-200">
                          Escola Virtual Digital
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-100 flex items-center justify-between gap-2 flex-wrap">
                  <span className="text-[11px] font-semibold text-slate-400">
                    {m.tamanho_mb ? `${m.tamanho_mb} MB` : '7.º Ano'}
                  </span>
                  <div className="flex items-center gap-1.5">
                    {m.url_github && (
                      <a
                        href={m.url_github}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-2.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold flex items-center gap-1 transition-all shadow-sm"
                        title="Ler ou descarregar o PDF original alojado no GitHub"
                      >
                        Ver PDF <ExternalLink className="w-3 h-3" />
                      </a>
                    )}
                    {m.tem_pdf_local && (
                      <button
                        onClick={() => abrirFicheiro(m.caminho)}
                        className="px-2.5 py-1.5 rounded-lg bg-blue-50 hover:bg-blue-600 text-blue-700 hover:text-white text-xs font-semibold flex items-center gap-1 transition-all cursor-pointer"
                        title="Abrir no leitor de PDF do teu computador"
                      >
                        PC <ExternalLink className="w-3 h-3" />
                      </button>
                    )}
                    <a
                      href={m.link_escolavirtual || 'https://app.escolavirtual.pt/'}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold flex items-center gap-1 transition-all"
                      title="Abrir na Escola Virtual"
                    >
                      Online <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* ========================================================================= */}
      {/* MODAL DO LEITOR ONLINE DE LIVROS EM PDF (BookReaderModal) */}
      {/* ========================================================================= */}
      <BookReaderModal
        isOpen={leitorAberto}
        onClose={() => setLeitorAberto(false)}
        book={livroSelecionado}
        initialPage={paginaInicialLeitor}
      />

      {/* ========================================================================= */}
      {/* MODAL / DRAWER INTERATIVO DE RESUMOS CURRICULARES DO LIVRO */}
      {/* ========================================================================= */}
      {resumosModalLivro && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/70 backdrop-blur-sm animate-fadeIn"
          onClick={(e) => {
            if (e.target === e.currentTarget) setResumosModalLivro(null);
          }}
        >
          <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] flex flex-col overflow-hidden shadow-2xl border border-slate-200">
            {/* Cabeçalho do Modal de Resumos */}
            <div className="p-4 sm:p-5 border-b border-slate-200 flex items-center justify-between gap-3 bg-slate-50">
              <div className="flex items-center gap-3 min-w-0">
                <div
                  className={`w-9 h-9 rounded-xl flex items-center justify-center text-white font-bold bg-gradient-to-br ${
                    resumosModalLivro.corTema?.primaria || 'from-purple-600 to-indigo-700'
                  }`}
                >
                  <FileText className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-800 truncate">
                    Resumos Curriculares: {resumosModalLivro.disciplina}
                  </h3>
                  <p className="text-xs text-slate-500">
                    {resumosModalLivro.titulo} • {resumosModalLivro.editora}
                  </p>
                </div>
              </div>
              <button
                onClick={() => setResumosModalLivro(null)}
                className="p-1.5 rounded-xl hover:bg-slate-200 text-slate-500 hover:text-slate-700 transition-colors cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Conteúdo com Unidades e Conceitos */}
            <div className="p-4 sm:p-6 overflow-y-auto space-y-4">
              <div className="bg-purple-50 border border-purple-200 rounded-xl p-3 text-xs text-purple-900">
                <strong>Programa Curricular do 3.º Ano:</strong> Cada unidade mapeia diretamente as páginas digitalizadas do manual com resumos teóricos, conceitos-chave, flashcards e testes modelo.
              </div>

              <div className="space-y-3">
                {resumosModalLivro.unidades?.map((u) => (
                  <div
                    key={u.numero}
                    className="p-3.5 rounded-xl border border-slate-200 bg-white hover:border-purple-300 transition-all flex flex-col gap-2"
                  >
                    <div className="flex items-center justify-between gap-2">
                      <h4 className="text-xs font-bold text-slate-800">
                        {u.titulo}
                      </h4>
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-purple-100 text-purple-800 shrink-0">
                        Páginas {u.paginaInicio}-{u.paginaFim}
                      </span>
                    </div>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      {u.descricao}
                    </p>
                    {u.conceitos && (
                      <div className="flex flex-wrap gap-1 mt-1">
                        {u.conceitos.map((c, ci) => (
                          <span
                            key={ci}
                            className="text-[10px] px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-medium"
                          >
                            {c}
                          </span>
                        ))}
                      </div>
                    )}
                    <div className="pt-2 border-t border-slate-100 flex items-center justify-end">
                      <button
                        onClick={() => {
                          const livro = resumosModalLivro;
                          const pag = u.paginaInicio;
                          setResumosModalLivro(null);
                          handleLerOnline(livro, pag);
                        }}
                        className="text-xs font-semibold text-blue-600 hover:text-blue-800 flex items-center gap-1 cursor-pointer"
                      >
                        <span>Abrir Leitor na Página {u.paginaInicio}</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Rodapé com Ação Principal */}
            <div className="p-4 border-t border-slate-200 bg-slate-50 flex items-center justify-between gap-2">
              <span className="text-xs text-slate-500">
                {resumosModalLivro.paginas} páginas digitalizadas
              </span>
              <button
                onClick={() => {
                  const livro = resumosModalLivro;
                  setResumosModalLivro(null);
                  handleLerOnline(livro, 1);
                }}
                className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white text-xs font-bold flex items-center gap-1.5 transition-colors cursor-pointer"
              >
                <BookOpen className="w-4 h-4" />
                <span>Ler Livro Online</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
