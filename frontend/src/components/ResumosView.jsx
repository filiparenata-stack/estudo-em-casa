import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  Printer,
  HelpCircle,
  AlertTriangle,
  Lightbulb,
  FileCheck2,
  BookOpen,
  ArrowRight,
  BrainCircuit,
  Loader2,
  PlusCircle,
  Download,
  Layers,
  ChevronDown,
  ChevronUp,
  Maximize2,
  X,
  Target,
  CheckCircle2,
  Share2,
  Search
} from 'lucide-react';

import { LIVROS_RENATA_3ANO } from '../data/booksCatalog';

export default function ResumosView({
  disciplina,
  periodo,
  onMudarPeriodo,
  anoAtivo = '3',
  onIniciarQuiz,
  onIrParaFlashcards,
  onAbrirLivro,
  resumoAtual,
  setResumoAtual
}) {
  const is3Ano = anoAtivo === '3' || disciplina?.ano === 3 || disciplina?.id?.endsWith('_3ano');
  const [unidadeFiltro, setUnidadeFiltro] = useState('');

  // Estado do Período selecionado (1_Periodo, 2_Periodo, 3_Periodo)
  const [periodoAtivo, setPeriodoAtivo] = useState(
    periodo && periodo !== 'Todos' ? periodo : '1_Periodo'
  );

  // Sincronizar quando o período externo na Navbar muda
  useEffect(() => {
    if (periodo && periodo !== 'Todos') {
      setPeriodoAtivo(periodo);
    } else if (!periodoAtivo) {
      setPeriodoAtivo('1_Periodo');
    }
  }, [periodo]);

  // Dados do dossiê do período (com imagens e match de testes)
  const [dossiePeriodo, setDossiePeriodo] = useState(null);
  const [aCarregarPeriodo, setACarregarPeriodo] = useState(false);
  const [resolucoesAbertas, setResolucoesAbertas] = useState({});
  const [flashcardVirado, setFlashcardVirado] = useState({});
  const [imagemModal, setImagemModal] = useState(null);
  const [filtroPesquisa, setFiltroPesquisa] = useState('');

  // Estados da geração livre/personalizada
  const [modoPersonalizado, setModoPersonalizado] = useState(false);
  const [indicacaoProfessor, setIndicacaoProfessor] = useState('');
  const [topicosSugeridos, setTopicosSugeridos] = useState([]);
  const [aCarregarLivre, setACarregarLivre] = useState(false);
  const [aExportarPdf, setAExportarPdf] = useState(false);
  const [aExportarAnki, setAExportarAnki] = useState(false);
  const [erro, setErro] = useState(null);

  // Carregar Dossiê Oficial do Período quando muda a disciplina ou o período ativo
  useEffect(() => {
    if (!disciplina) return;
    setACarregarPeriodo(true);
    setErro(null);

    const fallbackLivro = LIVROS_RENATA_3ANO.find(
      (l) => l.disciplinaId === disciplina.id || (disciplina.id && disciplina.id.startsWith(l.disciplinaId.split('_')[0]))
    );

    fetch(`/api/resumo/periodo?disciplina_id=${disciplina.id}&periodo=${periodoAtivo}`)
      .then((res) => {
        if (!res.ok) throw new Error('Não foi possível carregar o dossiê do período.');
        return res.json();
      })
      .then((data) => {
        setDossiePeriodo(data);
      })
      .catch((err) => {
        console.error(err);
        if (fallbackLivro) {
          setDossiePeriodo({
            disciplina_id: disciplina.id,
            disciplina_nome: disciplina.nome,
            ano: 3,
            livro_referencia: fallbackLivro.tituloCompleto,
            titulo: `${disciplina.nome} 3.º Ano • ${fallbackLivro.titulo}`,
            metas: [
              `Compreender e consolidar os conteúdos de cada unidade do manual ${fallbackLivro.tituloCompleto}.`,
              'Reconhecer vocabulário, regras essenciais e conceitos práticos do 1.º Ciclo.',
              'Treinar com perguntas de autoavaliação e flashcards interativos.'
            ],
            topicos: fallbackLivro.unidades.map((u) => ({
              id: `${disciplina.id}_u${u.numero}`,
              titulo: u.titulo,
              subdominio: `Manual • Páginas ${u.paginaInicio}-${u.paginaFim}`,
              paginas_livro: `Páginas ${u.paginaInicio}-${u.paginaFim}`,
              pagina_inicio: u.paginaInicio,
              pagina_fim: u.paginaFim,
              resumo_pedagogico: u.descricao,
              conceitos_chave: (u.conceitos || []).map((c) => ({
                termo: c,
                definicao: `Conceito curricular fundamental abordado nas páginas ${u.paginaInicio}-${u.paginaFim}.`
              }))
            })),
            total_topicos: fallbackLivro.unidades.length
          });
        }
      })
      .finally(() => {
        setACarregarPeriodo(false);
      });
  }, [disciplina, periodoAtivo]);

  // Carregar tópicos sugeridos para a pesquisa rápida
  useEffect(() => {
    if (!disciplina) return;
    fetch(`/api/topicos/${disciplina.id}?periodo=${periodoAtivo}`)
      .then((res) => res.json())
      .then((data) => setTopicosSugeridos(data || []))
      .catch(() => setTopicosSugeridos([]));
  }, [disciplina, periodoAtivo]);

  const toggleResolucao = (topicoId) => {
    setResolucoesAbertas((prev) => ({
      ...prev,
      [topicoId]: !prev[topicoId]
    }));
  };

  const toggleFlashcard = (cardId) => {
    setFlashcardVirado((prev) => ({
      ...prev,
      [cardId]: !prev[cardId]
    }));
  };

  // Descarregar Sebenta em PDF do Resumo Livre Personalizado
  const descarregarPdf = async () => {
    if (!resumoAtual) return;
    setAExportarPdf(true);
    try {
      const resp = await fetch('/api/exportar-pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(resumoAtual)
      });
      if (!resp.ok) throw new Error('Falha ao compilar PDF do resumo.');
      const blob = await resp.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const nomeDisc = (resumoAtual.disciplina_nome || disciplina?.nome || 'Disciplina').replace(/\s+/g, '_');
      a.download = `Resumo_Livre_${nomeDisc}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      alert('Erro ao transferir PDF do resumo livre: ' + err.message);
    } finally {
      setAExportarPdf(false);
    }
  };

  // Descarregar Sebenta em PDF Ilustrado do Período
  const descarregarPdfPeriodo = async () => {
    if (!dossiePeriodo) return;
    setAExportarPdf(true);
    try {
      const resp = await fetch('/api/exportar-pdf-periodo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dossiePeriodo)
      });
      if (!resp.ok) throw new Error('Falha ao compilar PDF do período.');
      const blob = await resp.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Dossie_Estudo_${disciplina.nome.replace(/\s+/g, '_')}_${periodoAtivo}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      alert('Erro ao transferir PDF: ' + err.message);
    } finally {
      setAExportarPdf(false);
    }
  };

  // Descarregar Baralho Anki (.txt/.tsv)
  const descarregarAnki = async () => {
    if (!disciplina) return;
    setAExportarAnki(true);
    try {
      const resp = await fetch('/api/exportar-anki', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          disciplina_id: disciplina.id,
          periodo: periodoAtivo
        })
      });
      if (!resp.ok) throw new Error('Falha ao gerar flashcards Anki.');
      const blob = await resp.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Anki_${disciplina.nome.replace(/\s+/g, '_')}_${periodoAtivo}.txt`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      alert('Erro ao transferir baralho Anki: ' + err.message);
    } finally {
      setAExportarAnki(false);
    }
  };

  // Gerar resumo à medida (modo livre)
  const gerarResumoLivre = async () => {
    if (!indicacaoProfessor.trim()) {
      setErro('Por favor, escreve os tópicos ou conteúdos pretendidos.');
      return;
    }
    setErro(null);
    setACarregarLivre(true);

    try {
      const resp = await fetch('/api/resumo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          disciplina_id: disciplina.id,
          periodo: periodoAtivo,
          conteudos: indicacaoProfessor,
          nivel: 'completo'
        })
      });

      if (!resp.ok) throw new Error('Erro ao gerar resumo no servidor.');
      const data = await resp.json();
      setResumoAtual(data);
    } catch (err) {
      setErro('Não foi possível gerar o resumo. Verifica a ligação.');
    } finally {
      setACarregarLivre(false);
    }
  };

  const topicosFiltrados = dossiePeriodo?.topicos?.filter((t) => {
    if (unidadeFiltro && !t.titulo.toLowerCase().includes(unidadeFiltro.toLowerCase())) {
      return false;
    }
    if (!filtroPesquisa.trim()) return true;
    const q = filtroPesquisa.toLowerCase();
    return (
      t.titulo.toLowerCase().includes(q) ||
      t.subdominio?.toLowerCase().includes(q) ||
      t.resumo_pedagogico?.toLowerCase().includes(q) ||
      t.conceitos_chave?.some((c) => c.termo.toLowerCase().includes(q) || c.definicao.toLowerCase().includes(q)) ||
      t.foco_teste?.questao_exemplo?.toLowerCase().includes(q)
    );
  }) || [];

  return (
    <div className="flex-1 p-4 md:p-6 max-w-6xl mx-auto flex flex-col gap-6">
      {/* 1. Barra de Seleção de Períodos / Unidades e Ações Rápidas */}
      <div className="bg-white rounded-2xl p-4 md:p-5 border border-slate-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Abas dos Períodos (7.º Ano) ou Unidades do Manual (3.º Ano) */}
        {is3Ano ? (
          <div className="flex items-center gap-1.5 p-1.5 bg-purple-50/70 border border-purple-200/80 rounded-xl w-full md:w-auto overflow-x-auto">
            <span className="text-xs font-bold text-purple-900 px-2 py-1 shrink-0 flex items-center gap-1">
              <BookOpen className="w-3.5 h-3.5 text-purple-600" />
              <span>Unidades:</span>
            </span>
            {['Todas', 'Unidade 1', 'Unidade 2', 'Unidade 3', 'Unidade 4', 'Unidade 5'].map((uLabel, uIdx) => {
              const isSelected = (unidadeFiltro === uLabel) || (uLabel === 'Todas' && !unidadeFiltro);
              return (
                <button
                  key={uIdx}
                  onClick={() => setUnidadeFiltro(uLabel === 'Todas' ? '' : uLabel)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer whitespace-nowrap ${
                    isSelected
                      ? 'bg-purple-600 text-white shadow-sm'
                      : 'text-purple-800 hover:bg-purple-100/70'
                  }`}
                >
                  {uLabel}
                </button>
              );
            })}
          </div>
        ) : (
          <div className="flex items-center gap-2 p-1.5 bg-slate-100 rounded-xl w-full md:w-auto">
            {[
              { id: '1_Periodo', label: '1.º Período' },
              { id: '2_Periodo', label: '2.º Período' },
              { id: '3_Periodo', label: '3.º Período' }
            ].map((p) => {
              const isSelected = periodoAtivo === p.id && !modoPersonalizado;
              return (
                <button
                  key={p.id}
                  onClick={() => {
                    setPeriodoAtivo(p.id);
                    if (onMudarPeriodo) onMudarPeriodo(p.id);
                    setModoPersonalizado(false);
                  }}
                  className={`flex-1 md:flex-none px-4 py-2 rounded-lg text-xs md:text-sm font-bold transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
                  }`}
                >
                  {p.label}
                </button>
              );
            })}

            <button
              onClick={() => setModoPersonalizado(!modoPersonalizado)}
              className={`px-3 py-2 rounded-lg text-xs md:text-sm font-semibold transition-all cursor-pointer flex items-center gap-1.5 ${
                modoPersonalizado
                  ? 'bg-purple-600 text-white shadow-md'
                  : 'text-slate-500 hover:text-purple-600 hover:bg-white/60'
              }`}
              title="Pesquisar ou compilar tópicos específicos"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Tópicos Livres</span>
            </button>
          </div>
        )}

        {/* Botões de Exportação e Estudo */}
        <div className="flex items-center gap-2 w-full md:w-auto justify-end flex-wrap">
          {onAbrirLivro && (
            <button
              onClick={() => onAbrirLivro(disciplina, 1)}
              className="px-3.5 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white text-xs font-bold flex items-center gap-1.5 shadow-sm shadow-purple-600/20 transition-all cursor-pointer"
              title="Abrir o manual escolar no leitor online integrado no browser"
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span>Ler Manual Online</span>
            </button>
          )}

          <button
            onClick={descarregarPdfPeriodo}
            disabled={aExportarPdf || !dossiePeriodo}
            className="flex-1 md:flex-none px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 disabled:opacity-50 text-white text-xs font-semibold flex items-center justify-center gap-2 shadow-sm transition-all cursor-pointer"
            title="Descarregar a sebenta do período em PDF ilustrado com esquemas e testes"
          >
            {aExportarPdf ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
            ) : (
              <Download className="w-3.5 h-3.5 text-blue-400" />
            )}
            <span>Sebenta em PDF</span>
          </button>

          <button
            onClick={descarregarAnki}
            disabled={aExportarAnki || !dossiePeriodo}
            className="px-3.5 py-2 rounded-xl bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer"
            title="Descarregar baralho de cartões Anki para rever no telemóvel"
          >
            {aExportarAnki ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
            ) : (
              <Layers className="w-3.5 h-3.5 text-blue-600" />
            )}
            <span>Exportar Anki (.txt)</span>
          </button>

          <button
            onClick={() => onIniciarQuiz && onIniciarQuiz(dossiePeriodo?.titulo || 'Teste do Período')}
            className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold flex items-center gap-1.5 shadow-sm shadow-emerald-600/20 transition-all cursor-pointer"
            title="Fazer simulação de teste com cotação e avaliação oficial"
          >
            <BrainCircuit className="w-3.5 h-3.5" />
            <span>Simular Teste</span>
          </button>
        </div>
      </div>

      {/* Caixa Expansível de Tópicos Livres / Personalizados */}
      {modoPersonalizado && (
        <div className="bg-purple-50/60 border border-purple-200 rounded-2xl p-5 flex flex-col gap-3 transition-all animate-fadeIn">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="p-1.5 bg-purple-600 text-white rounded-lg text-xs font-bold">✨</span>
              <h3 className="text-sm font-bold text-purple-950">
                Criar Resumo Sob Medida para {disciplina?.nome}
              </h3>
            </div>
            <span className="text-xs text-purple-700 font-medium">
              Foco Personalizado
            </span>
          </div>

          <textarea
            value={indicacaoProfessor}
            onChange={(e) => setIndicacaoProfessor(e.target.value)}
            placeholder="Escreve os tópicos indicados pelo professor ou páginas do livro (ex.: Estrutura da Terra, Rochas Magmáticas, págs. 40 a 65)..."
            rows={2}
            className="w-full p-3 rounded-xl border border-purple-200 focus:border-purple-500 focus:ring-2 focus:ring-purple-100 text-sm text-slate-800 bg-white placeholder-slate-400 outline-none resize-none"
          />

          {erro && <p className="text-xs text-rose-600 font-semibold">{erro}</p>}

          <div className="flex items-center justify-between pt-1">
            <div className="flex flex-wrap gap-1.5 max-w-xl">
              {topicosSugeridos.slice(0, 6).map((top, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => setIndicacaoProfessor(top)}
                  className="text-[11px] bg-white text-purple-800 px-2.5 py-1 rounded-md border border-purple-200 hover:bg-purple-100 transition-colors"
                >
                  + {top}
                </button>
              ))}
            </div>

            <button
              onClick={gerarResumoLivre}
              disabled={aCarregarLivre}
              className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-semibold text-xs flex items-center gap-2 cursor-pointer transition-all"
            >
              {aCarregarLivre ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" /> A compilar...
                </>
              ) : (
                <>
                  <Sparkles className="w-3.5 h-3.5" /> Gerar Resumo Livre
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* 1.5. Resumo Personalizado Gerado (Tópicos Livres) */}
      {resumoAtual && (
        <div className="bg-white rounded-2xl border-2 border-purple-300 shadow-md overflow-hidden flex flex-col gap-6 p-5 md:p-6 animate-fadeIn">
          {/* Cabeçalho do Resumo Livre */}
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pb-4 border-b border-purple-100">
            <div>
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-0.5 rounded-full bg-purple-100 text-purple-800 text-[11px] font-extrabold uppercase tracking-wider">
                  Resumo Livre • {resumoAtual.disciplina_nome || disciplina?.nome}
                </span>
                {resumoAtual.indicacao_professor && (
                  <span className="text-xs text-slate-500 font-medium">
                    Tema: "{resumoAtual.indicacao_professor}"
                  </span>
                )}
              </div>
              <h2 className="text-xl md:text-2xl font-black text-slate-900 mt-1">
                {resumoAtual.titulo}
              </h2>
            </div>

            <div className="flex flex-wrap items-center gap-2">
              <button
                onClick={descarregarPdf}
                disabled={aExportarPdf}
                className="px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 disabled:opacity-50 text-white text-xs font-semibold flex items-center gap-1.5 cursor-pointer transition-all"
              >
                {aExportarPdf ? (
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                ) : (
                  <Printer className="w-3.5 h-3.5 text-purple-300" />
                )}
                <span>📄 Descarregar PDF deste Resumo</span>
              </button>

              {onIrParaFlashcards && (
                <button
                  onClick={onIrParaFlashcards}
                  className="px-3 py-2 rounded-xl bg-purple-50 hover:bg-purple-100 text-purple-800 border border-purple-200 text-xs font-semibold flex items-center gap-1.5 cursor-pointer transition-all"
                >
                  <Layers className="w-3.5 h-3.5 text-purple-600" />
                  <span>🎴 Treinar Flashcards</span>
                </button>
              )}

              {onIniciarQuiz && (
                <button
                  onClick={() => onIniciarQuiz(resumoAtual.indicacao_professor || resumoAtual.titulo)}
                  className="px-3 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold flex items-center gap-1.5 cursor-pointer transition-all"
                >
                  <BrainCircuit className="w-3.5 h-3.5" />
                  <span>🎯 Fazer Quiz sobre este Tema</span>
                </button>
              )}

              <button
                onClick={() => setResumoAtual(null)}
                className="px-2.5 py-2 rounded-xl bg-slate-100 hover:bg-rose-50 text-slate-500 hover:text-rose-600 text-xs font-bold cursor-pointer transition-all"
                title="Fechar Resumo Livre"
              >
                ✕ Fechar Resumo Livre
              </button>
            </div>
          </div>

          {/* Introdução */}
          {resumoAtual.introducao && (
            <div className="p-4 rounded-xl bg-purple-50/50 border border-purple-100 text-xs md:text-sm text-slate-700 leading-relaxed">
              {resumoAtual.introducao}
            </div>
          )}

          {/* Conceitos-Chave */}
          {resumoAtual.conceitos_chave?.length > 0 && (
            <div className="flex flex-col gap-3">
              <span className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-2">
                <Lightbulb className="w-4 h-4 text-purple-600" />
                Conceitos-Chave Essenciais
              </span>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {resumoAtual.conceitos_chave.map((c, i) => (
                  <div
                    key={i}
                    className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/90 flex flex-col gap-1"
                  >
                    <span className="text-xs font-bold text-purple-900">
                      {c.termo}
                    </span>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      {c.definicao}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Esquemas e Fórmulas */}
          {resumoAtual.esquemas_formulas?.length > 0 && (
            <div className="flex flex-col gap-3">
              <span className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-blue-600" />
                Esquemas, Relações e Fórmulas
              </span>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {resumoAtual.esquemas_formulas.map((ef, i) => (
                  <div
                    key={i}
                    className="p-3.5 rounded-xl bg-blue-50/50 border border-blue-200 flex flex-col gap-1"
                  >
                    <span className="text-xs font-bold text-blue-950">
                      {ef.titulo}
                    </span>
                    <p className="text-xs text-slate-700 font-mono whitespace-pre-line leading-relaxed">
                      {ef.conteudo}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Pontos Fundamentais */}
          {resumoAtual.pontos_fundamentais?.length > 0 && (
            <div className="flex flex-col gap-3">
              <span className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-emerald-600" />
                Síntese de Conteúdos por Tópico
              </span>
              <div className="flex flex-col gap-3">
                {resumoAtual.pontos_fundamentais.map((sec, i) => (
                  <div
                    key={i}
                    className="p-4 rounded-xl bg-white border border-slate-200 flex flex-col gap-2"
                  >
                    <h4 className="text-xs md:text-sm font-bold text-slate-800">
                      {sec.subtitulo}
                    </h4>
                    <ul className="list-disc list-inside flex flex-col gap-1 text-xs text-slate-600">
                      {sec.itens?.map((item, j) => (
                        <li key={j} className="leading-relaxed">
                          {item}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Atenção no Teste */}
          {resumoAtual.atencao_no_teste?.length > 0 && (
            <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 flex flex-col gap-2">
              <span className="text-xs font-bold text-amber-900 uppercase tracking-wider flex items-center gap-1.5">
                <AlertTriangle className="w-4 h-4 text-amber-600" />
                Atenção no Teste — O que os Professores Mais Descontam:
              </span>
              <ul className="list-disc list-inside flex flex-col gap-1 text-xs text-amber-900">
                {resumoAtual.atencao_no_teste.map((dica, i) => (
                  <li key={i} className="leading-relaxed">
                    {dica}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Documentos Consultados */}
          {resumoAtual.documentos_consultados?.length > 0 && (
            <div className="pt-3 border-t border-slate-100 flex flex-wrap items-center gap-2 text-[11px] text-slate-400">
              <FileCheck2 className="w-3.5 h-3.5 text-slate-400" />
              <span className="font-semibold">Fontes e Manuais Consultados:</span>
              {resumoAtual.documentos_consultados.map((doc, i) => (
                <span
                  key={i}
                  className="px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-medium"
                >
                  {doc}
                </span>
              ))}
            </div>
          )}
        </div>
      )}

      {/* 2. Dossiê Oficial do Período */}
      {aCarregarPeriodo ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 flex flex-col items-center justify-center gap-3 text-slate-500">
          <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
          <p className="text-sm font-semibold text-slate-700">
            A carregar o Dossiê de Exame com esquemas e questões oficiais do {periodoAtivo.replace('_', '.º ')}...
          </p>
        </div>
      ) : dossiePeriodo ? (
        <div className="flex flex-col gap-6">
          {/* Cabeçalho do Dossiê com Metas Curriculares */}
          <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-blue-950 text-white rounded-2xl p-6 shadow-sm border border-slate-800 flex flex-col gap-4">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-2">
              <div>
                <span className="text-xs uppercase font-extrabold tracking-wider text-blue-400">
                  {dossiePeriodo.disciplina_nome} • 7.º Ano de Escolaridade
                </span>
                <h2 className="text-xl md:text-2xl font-black text-white mt-0.5 tracking-tight">
                  {dossiePeriodo.titulo}
                </h2>
              </div>
              <div className="flex items-center gap-2">
                <span className="px-3 py-1 rounded-full bg-blue-500/20 border border-blue-400/30 text-blue-300 text-xs font-bold">
                  {dossiePeriodo.total_topicos || dossiePeriodo.topicos?.length} Unidades Essenciais
                </span>
              </div>
            </div>

            {/* Metas Curriculares Oficiais */}
            {dossiePeriodo.metas?.length > 0 && (
              <div className="bg-white/10 backdrop-blur-md rounded-xl p-4 border border-white/10 flex flex-col gap-2">
                <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
                  <Target className="w-3.5 h-3.5" /> O que é rigorosamente avaliado nos testes deste período:
                </span>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-slate-200">
                  {dossiePeriodo.metas.map((meta, i) => (
                    <div key={i} className="flex items-start gap-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                      <span className="leading-relaxed">{meta}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Filtro de Pesquisa rápida dentro do período */}
            <div className="relative w-full max-w-md mt-1">
              <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-400" />
              <input
                type="text"
                value={filtroPesquisa}
                onChange={(e) => setFiltroPesquisa(e.target.value)}
                placeholder="Filtrar temas deste período (ex.: escalas, equações, rochas, verbos)..."
                className="w-full pl-10 pr-4 py-2 bg-white/10 border border-white/20 rounded-xl text-xs text-white placeholder-slate-400 focus:outline-none focus:bg-white/20 focus:border-blue-400 transition-all"
              />
              {filtroPesquisa && (
                <button
                  onClick={() => setFiltroPesquisa('')}
                  className="absolute right-3 top-2.5 text-slate-400 hover:text-white text-xs"
                >
                  ✕
                </button>
              )}
            </div>
          </div>

          {/* Lista de Tópicos Curriculares Emparelhados */}
          <div className="flex flex-col gap-6">
            {topicosFiltrados.map((topico, idx) => {
              const resAberto = resolucoesAbertas[topico.id];
              const imgQuestao = topico.foco_teste?.imagem_questao || topico.imagem_questao;
              return (
                <div
                  key={topico.id}
                  className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden hover:border-slate-300 transition-all"
                >
                  {/* Cabeçalho do Tópico */}
                  <div className="p-5 border-b border-slate-100 bg-slate-50/50 flex flex-col md:flex-row justify-between items-start md:items-center gap-2">
                    <div>
                      <span className={`text-[11px] font-bold uppercase tracking-wider ${is3Ano ? 'text-purple-600' : 'text-blue-600'}`}>
                        {topico.subdominio || `Tópico ${idx + 1}`}
                      </span>
                      <h3 className="text-lg font-bold text-slate-900 mt-0.5">
                        {topico.titulo}
                      </h3>
                    </div>
                    <div className="flex items-center gap-2">
                      {topico.pagina_inicio && onAbrirLivro && (
                        <button
                          onClick={() => onAbrirLivro(disciplina, topico.pagina_inicio)}
                          className="px-3 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-700 text-white text-xs font-bold flex items-center gap-1.5 shadow-sm transition-all cursor-pointer"
                        >
                          <BookOpen className="w-3.5 h-3.5" />
                          <span>Pág. {topico.pagina_inicio}</span>
                        </button>
                      )}
                      <span className="text-xs px-2.5 py-1 rounded-md bg-white border border-slate-200 text-slate-600 font-semibold shadow-2xs">
                        {topico.paginas_livro || topico.paginas_manual || `Unidade ${idx + 1}`}
                      </span>
                    </div>
                  </div>

                  <div className="p-5 md:p-6 flex flex-col gap-6">
                    {/* Resumo Pedagógico da Unidade (3.º Ano) */}
                    {topico.resumo_pedagogico && (
                      <div className="bg-gradient-to-r from-purple-50/80 to-indigo-50/60 border border-purple-200/80 rounded-xl p-4 text-xs text-purple-950 leading-relaxed shadow-2xs">
                        <div className="font-bold text-purple-900 mb-1.5 flex items-center gap-1.5">
                          <Sparkles className="w-3.5 h-3.5 text-purple-600 shrink-0" />
                          <span>Síntese Curricular do Manual Escolar:</span>
                        </div>
                        <p>{topico.resumo_pedagogico}</p>
                      </div>
                    )}
                    {/* 1. Teoria e Conceitos-Chave */}
                    {topico.conceitos_chave?.length > 0 && (
                      <div className="flex flex-col gap-3">
                        <span className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-2">
                          <span className="w-2 h-2 rounded-full bg-blue-600" />
                          Conceitos Fundamentais que Tens de Saber
                        </span>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {topico.conceitos_chave.map((c, i) => (
                            <div
                              key={i}
                              className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/90 flex flex-col gap-1"
                            >
                              <span className="text-xs font-bold text-blue-900">
                                {c.termo}
                              </span>
                              <p className="text-xs text-slate-600 leading-relaxed">
                                {c.definicao}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* 2. Esquema / Imagem Visual do Manual */}
                    {topico.imagem_manual && (
                      <div className="flex flex-col gap-2 p-4 bg-slate-50 rounded-xl border border-slate-200/80">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                            <BookOpen className="w-3.5 h-3.5 text-blue-600" /> Esquema Conceitual do Manual
                          </span>
                          <button
                            onClick={() =>
                              setImagemModal({
                                src: topico.imagem_manual,
                                legenda: topico.imagem_legenda || topico.titulo
                              })
                            }
                            className="text-xs text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-1 cursor-pointer"
                          >
                            <Maximize2 className="w-3 h-3" /> Ampliar
                          </button>
                        </div>

                        <div
                          onClick={() =>
                            setImagemModal({
                              src: topico.imagem_manual,
                              legenda: topico.imagem_legenda || topico.titulo
                            })
                          }
                          className="w-full max-h-72 rounded-lg bg-white border border-slate-200 overflow-hidden flex items-center justify-center p-2 cursor-pointer hover:opacity-95 transition-opacity"
                        >
                          <img
                            src={topico.imagem_manual}
                            alt={topico.titulo}
                            className="max-h-64 object-contain rounded"
                            onError={(e) => {
                              e.target.style.display = 'none';
                            }}
                          />
                        </div>
                        {topico.imagem_legenda && (
                          <p className="text-[11px] text-slate-500 italic text-center">
                            {topico.imagem_legenda}
                          </p>
                        )}
                      </div>
                    )}

                    {/* 3. Bloco "COMO SAI NO TESTE" (Questão Real + Resolução Oficial) */}
                    {topico.foco_teste && (
                      <div className="rounded-xl border-2 border-blue-200 bg-blue-50/40 p-4 md:p-5 flex flex-col gap-3">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <span className="px-2 py-0.5 rounded bg-blue-600 text-white text-[10px] font-extrabold uppercase tracking-wider">
                              Foco no Teste
                            </span>
                            <span className="text-xs font-bold text-blue-950">
                              Questão Real de Avaliação Oficial
                            </span>
                          </div>
                          <span className="text-[11px] font-semibold text-blue-700 bg-blue-100 px-2 py-0.5 rounded">
                            Exame 7.º Ano
                          </span>
                        </div>

                        <div className="bg-white p-3.5 rounded-lg border border-blue-100 shadow-2xs text-xs font-medium text-slate-800 leading-relaxed">
                          <b>Enunciado:</b> {topico.foco_teste.questao_exemplo}
                        </div>

                        {/* Imagem da Questão de Teste (se existir) */}
                        {imgQuestao && imgQuestao !== topico.imagem_manual && (
                          <div
                            onClick={() =>
                              setImagemModal({
                                src: imgQuestao,
                                legenda: `Figura da Questão: ${topico.titulo}`
                              })
                            }
                            className="w-full max-h-56 rounded-lg bg-white border border-blue-100 p-2 flex items-center justify-center cursor-pointer hover:opacity-95"
                          >
                            <img
                              src={imgQuestao}
                              alt="Figura da Questão"
                              className="max-h-48 object-contain"
                              onError={(e) => {
                                e.target.style.display = 'none';
                              }}
                            />
                          </div>
                        )}

                        {/* Botão para Revelar Resolução & Critérios */}
                        <div className="flex flex-col gap-2 pt-1">
                          <button
                            onClick={() => toggleResolucao(topico.id)}
                            className="px-3 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold flex items-center justify-between transition-colors cursor-pointer"
                          >
                            <span className="flex items-center gap-1.5">
                              <CheckCircle2 className="w-3.5 h-3.5" />
                              {resAberto
                                ? 'Ocultar Proposta de Resolução e Critérios'
                                : 'Ver Proposta de Resolução Oficial e Dicas de Cotação'}
                            </span>
                            {resAberto ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                          </button>

                          {resAberto && (
                            <div className="bg-white rounded-lg p-4 border border-blue-200 flex flex-col gap-2.5 text-xs animate-fadeIn">
                              <div>
                                <span className="font-bold text-emerald-700 block mb-0.5">
                                  ✅ Resolução Esperada (Nota Máxima):
                                </span>
                                <p className="text-slate-700 leading-relaxed bg-emerald-50/60 p-2.5 rounded border border-emerald-100">
                                  {topico.foco_teste.proposta_resolucao}
                                </p>
                              </div>

                              <div>
                                <span className="font-bold text-blue-900 block mb-0.5">
                                  📋 Critério do Professor e Distribuição de Cotação:
                                </span>
                                <p className="text-slate-600 leading-relaxed bg-slate-50 p-2 rounded">
                                  {topico.foco_teste.criterio_cotacao}
                                </p>
                              </div>

                              {topico.foco_teste.erro_frequente && (
                                <div className="p-2.5 bg-amber-50 rounded border border-amber-200 text-amber-900">
                                  <span className="font-bold block mb-0.5">
                                    ⚠️ Onde a Maioria dos Alunos Perde Pontos:
                                  </span>
                                  <p>{topico.foco_teste.erro_frequente}</p>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* 4. Mini Flashcards Rápidos do Tópico */}
                    {topico.flashcards?.length > 0 && (
                      <div className="flex flex-col gap-2 pt-2 border-t border-slate-100">
                        <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
                          <Layers className="w-3 h-3 text-purple-600" /> Cartões Rápidos de Autoavaliação (Clica para virar):
                        </span>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
                          {topico.flashcards.map((fc, cardIdx) => {
                            const cKey = `${topico.id}_fc_${cardIdx}`;
                            const virado = flashcardVirado[cKey];
                            return (
                              <div
                                key={cardIdx}
                                onClick={() => toggleFlashcard(cKey)}
                                className={`p-3 rounded-xl border text-xs cursor-pointer transition-all ${
                                  virado
                                    ? 'bg-emerald-50 border-emerald-200 text-emerald-950 shadow-xs'
                                    : 'bg-slate-50 hover:bg-slate-100/80 border-slate-200 text-slate-800'
                                }`}
                              >
                                <div className="flex items-center justify-between mb-1 text-[10px] font-bold">
                                  <span className={virado ? 'text-emerald-700' : 'text-slate-400'}>
                                    {virado ? '✓ RESPOSTA' : '❓ PERGUNTA'}
                                  </span>
                                  <span className="text-slate-400 font-mono">
                                    {virado ? 'clica para voltar' : 'clica para virar'}
                                  </span>
                                </div>
                                <p className="leading-relaxed font-medium">
                                  {virado ? fc.verso : fc.frente}
                                </p>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ) : null}

      {/* Modal de Zoom de Imagem */}
      {imagemModal && (
        <div
          onClick={() => setImagemModal(null)}
          className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 cursor-pointer animate-fadeIn"
        >
          <div
            onClick={(e) => e.stopPropagation()}
            className="bg-white rounded-2xl max-w-4xl max-h-[90vh] overflow-hidden flex flex-col shadow-2xl relative"
          >
            <div className="p-4 border-b border-slate-100 flex items-center justify-between bg-slate-50">
              <span className="text-xs font-bold text-slate-800">
                {imagemModal.legenda || 'Diagrama Explicativo'}
              </span>
              <button
                onClick={() => setImagemModal(null)}
                className="p-1 rounded-lg hover:bg-slate-200 text-slate-600 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="p-4 flex items-center justify-center bg-slate-900/5 overflow-auto">
              <img
                src={imagemModal.src}
                alt={imagemModal.legenda}
                className="max-h-[75vh] object-contain rounded-lg shadow-sm"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
