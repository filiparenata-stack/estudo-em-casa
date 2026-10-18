import React, { useState, useEffect } from 'react';
import {
  BrainCircuit,
  CheckCircle2,
  XCircle,
  HelpCircle,
  RotateCcw,
  Trophy,
  Loader2,
  ArrowRight,
  BookOpen
} from 'lucide-react';

export default function QuizView({ disciplina, periodo, topicosIniciais }) {
  const [topicos, setTopicos] = useState(topicosIniciais || '');
  const [questoes, setQuestoes] = useState([]);
  const [indiceAtual, setIndiceAtual] = useState(0);
  const [respostasUsuario, setRespostasUsuario] = useState({});
  const [aCarregar, setACarregar] = useState(false);
  const [concluido, setConcluido] = useState(false);

  const carregarQuiz = async (temaParaUsar) => {
    const tema = temaParaUsar !== undefined ? temaParaUsar : topicos;
    if (!tema.trim() && !disciplina) return;
    setACarregar(true);
    setConcluido(false);
    setRespostasUsuario({});
    setIndiceAtual(0);

    try {
      const resp = await fetch('/api/quiz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          disciplina_id: disciplina.id,
          periodo: periodo,
          topicos: tema || disciplina.nome,
          quantidade: 8
        })
      });
      if (!resp.ok) throw new Error('Erro ao carregar quiz.');
      const data = await resp.json();
      setQuestoes(data.questoes || []);
    } catch (err) {
      alert('Erro ao carregar perguntas do teste: ' + err.message);
    } finally {
      setACarregar(false);
    }
  };

  useEffect(() => {
    if (topicosIniciais) {
      setTopicos(topicosIniciais);
      carregarQuiz(topicosIniciais);
    } else if (disciplina) {
      carregarQuiz(disciplina.nome);
    }
  }, [disciplina]);

  const responder = (letraOuTexto) => {
    if (respostasUsuario[indiceAtual] !== undefined) return; // já respondeu
    setRespostasUsuario({
      ...respostasUsuario,
      [indiceAtual]: letraOuTexto
    });
  };

  const questao = questoes[indiceAtual];
  const total = questoes.length;
  const respostaDada = respostasUsuario[indiceAtual];
  const ehCorreta = respostaDada && questao && respostaDada.toUpperCase() === questao.resposta_correta?.toUpperCase();

  const acertos = Object.entries(respostasUsuario).filter(([idx, resp]) => {
    const q = questoes[parseInt(idx, 10)];
    return q && resp.toUpperCase() === q.resposta_correta?.toUpperCase();
  }).length;

  const percentagem = total > 0 ? Math.round((acertos / total) * 100) : 0;

  return (
    <div className="flex-1 p-6 max-w-3xl mx-auto flex flex-col gap-6">
      {/* Topo com Formulário de Tema do Quiz */}
      <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3 w-full sm:w-auto">
          <div className="w-10 h-10 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center font-bold shrink-0">
            🧪
          </div>
          <div className="min-w-0">
            <h2 className="text-base font-bold text-slate-800 truncate">
              Simulador de Testes: {disciplina?.nome}
            </h2>
            <p className="text-xs text-slate-500">
              Perguntas reais extraídas dos testes e fichas de avaliação da Escola Virtual
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <input
            type="text"
            value={topicos}
            onChange={(e) => setTopicos(e.target.value)}
            placeholder="Tópico (ex: Rochas, Equações)..."
            className="p-2 text-xs rounded-lg border border-slate-300 w-full sm:w-48 outline-none focus:border-purple-500"
          />
          <button
            onClick={() => carregarQuiz(topicos)}
            disabled={aCarregar}
            className="px-3.5 py-2 rounded-lg bg-purple-600 hover:bg-purple-700 text-white font-semibold text-xs shrink-0 flex items-center gap-1.5 cursor-pointer shadow-sm"
          >
            {aCarregar ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <BrainCircuit className="w-3.5 h-3.5" />}
            Gerar Quiz
          </button>
        </div>
      </div>

      {/* Conteúdo do Quiz */}
      {aCarregar ? (
        <div className="bg-white rounded-3xl p-16 border border-slate-200 shadow-sm flex flex-col items-center justify-center gap-3 text-slate-500">
          <Loader2 className="w-8 h-8 animate-spin text-purple-600" />
          <p className="text-sm font-medium">A extrair perguntas e grelhas de correção dos testes...</p>
        </div>
      ) : total === 0 ? (
        <div className="bg-white rounded-3xl p-12 border border-slate-200 shadow-sm text-center flex flex-col items-center gap-3 text-slate-500">
          <BookOpen className="w-10 h-10 text-slate-300" />
          <p className="text-sm">Clica em «Gerar Quiz» para começar um simulador de teste para este tema.</p>
        </div>
      ) : concluido ? (
        /* ECRÃ DE RESULTADOS FINAIS */
        <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-lg text-center flex flex-col items-center gap-6 animate-fadeIn">
          <div className="w-16 h-16 rounded-2xl bg-amber-100 text-amber-600 flex items-center justify-center shadow-inner">
            <Trophy className="w-8 h-8" />
          </div>

          <div>
            <h3 className="text-2xl font-bold text-slate-800">Teste Concluído!</h3>
            <p className="text-sm text-slate-500 mt-1">Aqui está o teu resultado com base nas soluções oficiais:</p>
          </div>

          <div className="flex items-center gap-6 p-4 rounded-2xl bg-slate-50 border border-slate-200">
            <div>
              <p className="text-3xl font-black text-purple-600">{percentagem}%</p>
              <p className="text-xs text-slate-400 font-semibold uppercase mt-0.5">Classificação</p>
            </div>
            <div className="w-px h-10 bg-slate-200" />
            <div>
              <p className="text-3xl font-black text-emerald-600">{acertos} / {total}</p>
              <p className="text-xs text-slate-400 font-semibold uppercase mt-0.5">Acertos</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                setConcluido(false);
                setRespostasUsuario({});
                setIndiceAtual(0);
              }}
              className="px-5 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs flex items-center gap-1.5 transition-colors cursor-pointer"
            >
              <RotateCcw className="w-4 h-4" /> Repetir este Teste
            </button>
            <button
              onClick={() => carregarQuiz(topicos)}
              className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-semibold text-xs flex items-center gap-1.5 shadow-md shadow-purple-500/20 transition-all cursor-pointer"
            >
              <BrainCircuit className="w-4 h-4" /> Gerar Outro Teste
            </button>
          </div>
        </div>
      ) : (
        /* CARTÃO DA PERGUNTA */
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm flex flex-col justify-between gap-6">
          {/* Cabeçalho da Questão */}
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <span className="text-xs font-bold text-purple-600 uppercase tracking-wider">
                {questao.grupo || 'Grupo I'} • Questão {indiceAtual + 1} de {total}
              </span>
              <p className="text-[11px] text-slate-400 font-mono mt-0.5">
                Origem: {questao.ficheiro_origem || 'Teste Escola Virtual'}
              </p>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-100 text-slate-600">
                {acertos} corretas
              </span>
            </div>
          </div>

          {/* Enunciado da Pergunta */}
          <div className="text-base font-semibold text-slate-800 leading-relaxed whitespace-pre-line">
            {questao.enunciado}
          </div>

          {/* Opções de Resposta */}
          {questao.opcoes && questao.opcoes.length > 0 ? (
            <div className="grid grid-cols-1 gap-2.5">
              {questao.opcoes.map((opt) => {
                const foiSelecionada = respostaDada === opt.letra;
                const estaCorreta = opt.letra.toUpperCase() === questao.resposta_correta?.toUpperCase();
                
                let estilo = 'border-slate-200 hover:border-purple-300 bg-white text-slate-700';
                if (respostaDada) {
                  if (estaCorreta) {
                    estilo = 'border-emerald-500 bg-emerald-50/80 text-emerald-900 font-semibold';
                  } else if (foiSelecionada) {
                    estilo = 'border-rose-500 bg-rose-50 text-rose-900 font-semibold';
                  } else {
                    estilo = 'border-slate-200 opacity-60 text-slate-500';
                  }
                }

                return (
                  <button
                    key={opt.letra}
                    disabled={respostaDada !== undefined}
                    onClick={() => responder(opt.letra)}
                    className={`p-3.5 rounded-xl border-2 text-left flex items-start gap-3 transition-all cursor-pointer ${estilo}`}
                  >
                    <span
                      className={`w-6 h-6 rounded-lg flex items-center justify-center font-bold text-xs shrink-0 ${
                        foiSelecionada || estaCorreta
                          ? estaCorreta
                            ? 'bg-emerald-600 text-white'
                            : 'bg-rose-600 text-white'
                          : 'bg-slate-100 text-slate-700'
                      }`}
                    >
                      {opt.letra}
                    </span>
                    <span className="text-sm leading-snug">{opt.texto}</span>
                  </button>
                );
              })}
            </div>
          ) : (
            /* Resposta Curta / Aberta */
            <div className="flex flex-col gap-3">
              <input
                type="text"
                placeholder="Escreve a tua resposta..."
                disabled={respostaDada !== undefined}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && e.target.value.trim()) {
                    responder(e.target.value.trim());
                  }
                }}
                className="p-3 rounded-xl border border-slate-300 text-sm focus:border-purple-500 outline-none"
              />
              <span className="text-xs text-slate-400">Pressiona Enter para confirmar a resposta.</span>
            </div>
          )}

          {/* Feedback e Explicação Imediata */}
          {respostaDada && (
            <div
              className={`p-4 rounded-xl border flex flex-col gap-1.5 animate-fadeIn ${
                ehCorreta
                  ? 'bg-emerald-50 border-emerald-200 text-emerald-900'
                  : 'bg-rose-50 border-rose-200 text-rose-900'
              }`}
            >
              <div className="flex items-center gap-2 font-bold text-xs uppercase tracking-wide">
                {ehCorreta ? (
                  <>
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Resposta Correta!
                  </>
                ) : (
                  <>
                    <XCircle className="w-4 h-4 text-rose-600" /> Resposta Incorreta (Correta: {questao.resposta_correta})
                  </>
                )}
              </div>
              <p className="text-xs text-slate-700">
                {questao.explicacao || 'Critério oficial de correção do teste da Escola Virtual.'}
              </p>
            </div>
          )}

          {/* Botão de Avançar */}
          <div className="flex items-center justify-between pt-2 border-t border-slate-100">
            <span className="text-xs text-slate-400">
              Questão {indiceAtual + 1} de {total}
            </span>

            {respostaDada && (
              <button
                onClick={() => {
                  if (indiceAtual < total - 1) {
                    setIndiceAtual(indiceAtual + 1);
                  } else {
                    setConcluido(true);
                  }
                }}
                className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-semibold text-xs flex items-center gap-1.5 shadow-md shadow-purple-500/20 transition-all cursor-pointer"
              >
                {indiceAtual < total - 1 ? (
                  <>
                    Próxima Questão <ArrowRight className="w-4 h-4" />
                  </>
                ) : (
                  'Ver Resultados Finais'
                )}
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
