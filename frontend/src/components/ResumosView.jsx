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
  PlusCircle
} from 'lucide-react';

export default function ResumosView({
  disciplina,
  periodo,
  onIniciarQuiz,
  onIrParaFlashcards,
  resumoAtual,
  setResumoAtual
}) {
  const [indicacaoProfessor, setIndicacaoProfessor] = useState('');
  const [topicosSugeridos, setTopicosSugeridos] = useState([]);
  const [aCarregar, setACarregar] = useState(false);
  const [aExportarPdf, setAExportarPdf] = useState(false);
  const [erro, setErro] = useState(null);

  // Carregar tópicos sugeridos para a disciplina e período
  useEffect(() => {
    if (!disciplina) return;
    fetch(`/api/topicos/${disciplina.id}?periodo=${periodo}`)
      .then((res) => res.json())
      .then((data) => setTopicosSugeridos(data || []))
      .catch(() => setTopicosSugeridos([]));
  }, [disciplina, periodo]);

  const gerarResumo = async () => {
    if (!indicacaoProfessor.trim()) {
      setErro('Por favor, escreve os tópicos ou conteúdos que o professor indicou.');
      return;
    }
    setErro(null);
    setACarregar(true);

    try {
      const resp = await fetch('/api/resumo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          disciplina_id: disciplina.id,
          periodo: periodo,
          conteudos: indicacaoProfessor,
          nivel: 'completo'
        })
      });

      if (!resp.ok) throw new Error('Erro ao gerar resumo no servidor.');
      const data = await resp.json();
      setResumoAtual(data);
    } catch (err) {
      setErro('Não foi possível gerar o resumo. Certifica-te de que o backend está a correr.');
    } finally {
      setACarregar(false);
    }
  };

  const descarregarPdf = async () => {
    if (!resumoAtual) return;
    setAExportarPdf(true);
    try {
      const resp = await fetch('/api/exportar-pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(resumoAtual)
      });
      if (!resp.ok) throw new Error('Falha ao gerar PDF.');
      const blob = await resp.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Resumo_${disciplina.nome.replace(/\s+/g, '_')}_7Ano.pdf`;
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

  const adicionarTopicoAoInput = (topico) => {
    if (!indicacaoProfessor) {
      setIndicacaoProfessor(topico);
    } else if (!indicacaoProfessor.includes(topico)) {
      setIndicacaoProfessor(`${indicacaoProfessor}, ${topico}`);
    }
  };

  return (
    <div className="flex-1 p-6 max-w-5xl mx-auto flex flex-col gap-6">
      {/* Caixa de Entrada: O que disse o professor? */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center font-bold">
              🎯
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900">
                O que disse o professor que sai no teste?
              </h2>
              <p className="text-xs text-slate-500">
                Insere a matéria, capítulos, páginas do manual ou os objetivos indicados para {disciplina?.nome}.
              </p>
            </div>
          </div>
          <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
            {periodo === 'Todos' ? 'Ano Completo' : periodo.replace('_', '.º ')}
          </span>
        </div>

        <div className="flex flex-col gap-2">
          <textarea
            value={indicacaoProfessor}
            onChange={(e) => setIndicacaoProfessor(e.target.value)}
            placeholder="Exemplo: Espaço e Universo, Sistema Solar, movimentos da Terra e da Lua, eclipses e estações do ano (páginas 20 a 45 do manual)..."
            rows={3}
            className="w-full p-3.5 rounded-xl border border-slate-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 text-sm text-slate-800 placeholder-slate-400 outline-none transition-all resize-none"
          />

          {erro && <p className="text-xs text-rose-600 font-medium">{erro}</p>}

          {/* Pílulas de Tópicos Sugeridos */}
          {topicosSugeridos.length > 0 && (
            <div className="flex flex-col gap-1.5 mt-1">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                <Lightbulb className="w-3 h-3 text-amber-500" /> Tópicos frequentes nos testes de {disciplina?.nome}:
              </span>
              <div className="flex flex-wrap gap-1.5 max-h-24 overflow-y-auto pr-1">
                {topicosSugeridos.slice(0, 15).map((top, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => adicionarTopicoAoInput(top)}
                    className="text-xs bg-slate-100 hover:bg-blue-50 hover:text-blue-700 text-slate-600 px-2.5 py-1 rounded-lg border border-slate-200 hover:border-blue-200 transition-colors flex items-center gap-1"
                  >
                    <PlusCircle className="w-3 h-3 opacity-60" /> {top}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="flex items-center justify-end gap-3 pt-2 border-t border-slate-100">
          <button
            onClick={gerarResumo}
            disabled={aCarregar}
            className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-semibold text-sm flex items-center gap-2 shadow-md shadow-blue-500/20 transition-all cursor-pointer"
          >
            {aCarregar ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" /> A compilar conteúdos dos manuais...
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" /> Gerar Resumo Estruturado
              </>
            )}
          </button>
        </div>
      </div>

      {/* Exibição do Resumo Estruturado */}
      {resumoAtual && (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
          {/* Topo do Resumo */}
          <div className="bg-gradient-to-r from-slate-900 to-slate-800 text-white p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <span className="text-xs uppercase font-bold tracking-wider text-blue-400">
                {resumoAtual.disciplina_nome} • 7.º Ano
              </span>
              <h3 className="text-xl font-bold tracking-tight mt-0.5 text-white">
                {resumoAtual.titulo}
              </h3>
              <p className="text-xs text-slate-300 mt-1 max-w-2xl">
                {resumoAtual.introducao}
              </p>
            </div>

            <div className="flex items-center gap-2 shrink-0">
              <button
                onClick={descarregarPdf}
                disabled={aExportarPdf}
                className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-semibold flex items-center gap-2 border border-white/20 backdrop-blur-sm transition-all cursor-pointer"
              >
                {aExportarPdf ? (
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                ) : (
                  <Printer className="w-3.5 h-3.5" />
                )}
                Descarregar PDF
              </button>

              <button
                onClick={() => onIniciarQuiz && onIniciarQuiz(indicacaoProfessor)}
                className="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white text-xs font-semibold flex items-center gap-2 shadow-md shadow-emerald-500/20 transition-all cursor-pointer"
              >
                <BrainCircuit className="w-3.5 h-3.5" /> Fazer Quiz do Tema
              </button>
            </div>
          </div>

          <div className="p-6 flex flex-col gap-6">
            {/* 1. Conceitos-Chave */}
            {resumoAtual.conceitos_chave?.length > 0 && (
              <div className="flex flex-col gap-3">
                <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2 uppercase tracking-wider text-xs">
                  <span className="w-2 h-2 rounded-full bg-blue-600" />
                  Conceitos Fundamentais que Tens de Saber Explicar
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {resumoAtual.conceitos_chave.map((c, i) => (
                    <div
                      key={i}
                      className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80 hover:border-blue-200 transition-colors flex flex-col gap-1"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-sm text-blue-900">{c.termo}</span>
                        <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-blue-100 text-blue-700">
                          {c.destaque || 'Conceito'}
                        </span>
                      </div>
                      <p className="text-xs text-slate-600 leading-relaxed">{c.definicao}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 2. Esquemas e Fórmulas */}
            {resumoAtual.esquemas_formulas?.length > 0 && (
              <div className="flex flex-col gap-3">
                <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2 uppercase tracking-wider text-xs">
                  <span className="w-2 h-2 rounded-full bg-emerald-600" />
                  Esquemas, Relações e Regras de Cálculo
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {resumoAtual.esquemas_formulas.map((eq, i) => (
                    <div
                      key={i}
                      className="p-3.5 rounded-xl bg-emerald-50/60 border border-emerald-200 flex flex-col gap-1"
                    >
                      <span className="text-xs font-bold text-emerald-900">{eq.titulo}</span>
                      <p className="text-xs font-mono text-emerald-800 bg-white/70 p-2 rounded-lg border border-emerald-100">
                        {eq.conteudo}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 3. Pontos Fundamentais */}
            {resumoAtual.pontos_fundamentais?.length > 0 && (
              <div className="flex flex-col gap-4">
                <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2 uppercase tracking-wider text-xs">
                  <span className="w-2 h-2 rounded-full bg-indigo-600" />
                  Síntese de Conteúdos por Tópico
                </h4>
                <div className="flex flex-col gap-3">
                  {resumoAtual.pontos_fundamentais.map((sec, i) => (
                    <div key={i} className="p-4 rounded-xl bg-slate-50 border border-slate-200 flex flex-col gap-2">
                      <h5 className="text-xs font-bold text-slate-800 uppercase tracking-wide">
                        {sec.subtitulo}
                      </h5>
                      <ul className="flex flex-col gap-1.5">
                        {sec.itens.map((it, j) => (
                          <li key={j} className="text-xs text-slate-700 flex items-start gap-2">
                            <span className="text-blue-500 font-bold">•</span>
                            <span className="leading-relaxed">{it}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 4. Atenção no Teste */}
            {resumoAtual.atencao_no_teste?.length > 0 && (
              <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 flex flex-col gap-2">
                <h4 className="text-xs font-bold text-amber-900 flex items-center gap-1.5 uppercase tracking-wide">
                  <AlertTriangle className="w-4 h-4 text-amber-600" /> Cuidado no Teste: O que os professores mais descontam
                </h4>
                <ul className="flex flex-col gap-1 text-xs text-amber-900/90">
                  {resumoAtual.atencao_no_teste.map((d, i) => (
                    <li key={i} className="flex items-start gap-1.5">
                      <span>⚠️</span>
                      <span>{d}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Rodapé do Resumo com Documentos Oficiais Usados */}
            {resumoAtual.documentos_consultados?.length > 0 && (
              <div className="pt-3 border-t border-slate-100 flex flex-col gap-1.5">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                  <BookOpen className="w-3 h-3 text-slate-400" /> Baseado nos Manuais e Testes Oficiais:
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {resumoAtual.documentos_consultados.map((doc, idx) => (
                    <span
                      key={idx}
                      className="text-[11px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded-md border border-slate-200 font-mono truncate max-w-xs"
                      title={doc}
                    >
                      {doc}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
