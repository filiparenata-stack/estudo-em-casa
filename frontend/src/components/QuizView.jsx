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
  BookOpen,
  Sparkles,
  Award,
  Clock,
  ListFilter
} from 'lucide-react';

const SUGESTOES_TOPICOS = {
  "01_Fisico_Quimica_7": ["Sistema Solar", "Planetas Telúricos", "Unidade Astronómica", "Misturas Homogéneas", "Separação de Misturas", "Massa Volúmica", "Energias Renováveis"],
  "02_Geografia_7": ["Coordenadas Geográficas", "Latitude e Longitude", "Escalas de Mapas", "Climas do Mundo", "Relevo e Montanhas", "Densidade Populacional"],
  "03_Ciencias_Naturais_7": ["Deriva Continental", "Tectónica de Placas", "Hipocentro e Epicentro", "Vulcões e Lava", "Rochas Magmáticas", "Fósseis"],
  "04_Historia_7": ["Revolução Neolítica", "Democracia Ateniense", "Romanização", "Sociedade Feudal", "Invenção da Escrita"],
  "05_Ingles_7": ["Present Continuous", "Past Simple Verbs", "Comparatives & Superlatives", "Daily Routines", "Vocabulary"],
  "06_Matematica_7": ["Equações do 1.º Grau", "Potências de Base 10", "Proporcionalidade Direta", "Ângulos do Triângulo", "Áreas e Perímetros"],
  "07_Portugues_7": ["Classes de Palavras", "Funções Sintáticas", "Complemento Indireto", "Personificação", "Metáfora"],
  "08_Frances_7": ["Verbes du 1er groupe", "Articles définis", "Présentation", "Vocabulaire de base"],
  "portugues_3ano": ["Ortografia e Dígrafos", "Classes de Palavras", "Nomes e Adjetivos", "Tipos de Frase", "Verbos e Tempos"],
  "matematica_3ano": ["Números até 10 000", "Adição e Subtração", "Multiplicação e Tabuadas", "Geometria e Polígonos", "Frações e Medidas"],
  "estudo_meio_3ano": ["Corpo Humano e Esqueleto", "Saúde e Higiene", "Rochas e Solos", "Portugal e Distritos", "Animais e Plantas"],
  "ingles_3ano": ["Greetings & Numbers", "School Supplies", "Family Members", "House & Rooms", "Farm Animals"]
};

export default function QuizView({ disciplina, periodo, onMudarPeriodo, topicosIniciais, anoAtivo = '3' }) {
  const [topicos, setTopicos] = useState(topicosIniciais || '');
  const [questoes, setQuestoes] = useState([]);
  const [indiceAtual, setIndiceAtual] = useState(0);
  const [respostasUsuario, setRespostasUsuario] = useState({});
  const [aCarregar, setACarregar] = useState(false);
  const [concluido, setConcluido] = useState(false);
  const [modoExame, setModoExame] = useState(false); // false = modo prática (feedback na hora), true = modo exame (só no fim)

  const carregarQuiz = async (temaParaUsar, periodoParaUsar) => {
    const tema = temaParaUsar !== undefined ? temaParaUsar : topicos;
    const per = periodoParaUsar !== undefined ? periodoParaUsar : periodo;
    if (!disciplina) return;
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
          periodo: per,
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
      carregarQuiz(topicosIniciais, periodo);
    } else if (disciplina) {
      carregarQuiz(topicos || '', periodo);
    }
  }, [disciplina, periodo]);

  const responder = (letra) => {
    if (respostasUsuario[indiceAtual] !== undefined) return;
    setRespostasUsuario({
      ...respostasUsuario,
      [indiceAtual]: letra
    });
  };

  // Suporte a atalhos de teclado (A, B, C, D)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (aCarregar || concluido || questoes.length === 0) return;
      const key = e.key.toUpperCase();
      if (['A', 'B', 'C', 'D'].includes(key)) {
        responder(key);
      } else if (['1', '2', '3', '4'].includes(key)) {
        const mapa = { '1': 'A', '2': 'B', '3': 'C', '4': 'D' };
        responder(mapa[key]);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [indiceAtual, respostasUsuario, aCarregar, concluido, questoes]);

  const proximaQuestao = () => {
    if (indiceAtual < questoes.length - 1) {
      setIndiceAtual(indiceAtual + 1);
    } else {
      setConcluido(true);
    }
  };

  const anteriorQuestao = () => {
    if (indiceAtual > 0) {
      setIndiceAtual(indiceAtual - 1);
    }
  };

  const questao = questoes[indiceAtual];
  const total = questoes.length;
  const respostaDada = respostasUsuario[indiceAtual];
  const estaCorreta = respostaDada && questao && respostaDada.toUpperCase() === questao.resposta_correta?.toUpperCase();

  const acertos = Object.entries(respostasUsuario).filter(([idx, resp]) => {
    const q = questoes[parseInt(idx, 10)];
    return q && resp.toUpperCase() === q.resposta_correta?.toUpperCase();
  }).length;

  const percentagem = total > 0 ? Math.round((acertos / total) * 100) : 0;

  // Escala oficial de avaliação do 7.º Ano (Nível 1 a 5)
  const getNivelAvaliacao = (pct) => {
    if (pct >= 90) return { nivel: 5, label: 'Excelente (Nível 5)', cor: 'text-emerald-600', bg: 'bg-emerald-50 border-emerald-200' };
    if (pct >= 70) return { nivel: 4, label: 'Bom (Nível 4)', cor: 'text-blue-600', bg: 'bg-blue-50 border-blue-200' };
    if (pct >= 50) return { nivel: 3, label: 'Suficiente (Nível 3)', cor: 'text-amber-600', bg: 'bg-amber-50 border-amber-200' };
    if (pct >= 20) return { nivel: 2, label: 'Insuficiente (Nível 2)', cor: 'text-orange-600', bg: 'bg-orange-50 border-orange-200' };
    return { nivel: 1, label: 'Muito Fraco (Nível 1)', cor: 'text-rose-600', bg: 'bg-rose-50 border-rose-200' };
  };

  const sugestoes = (disciplina && SUGESTOES_TOPICOS[disciplina.id]) || [];

  return (
    <div className="flex-1 p-6 max-w-3xl mx-auto flex flex-col gap-6">
      {/* Topo com Formulário de Tema do Quiz */}
      <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col gap-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center font-bold shrink-0">
              🧪
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-800">
                Simulador de Testes: {disciplina?.nome}
              </h2>
              <p className="text-xs text-slate-500">
                Questões rigorosas e pedagógicas com base no programa curricular oficial
              </p>
            </div>
          </div>

          {/* Alternador de Modo */}
          <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs">
            <button
              onClick={() => setModoExame(false)}
              className={`px-3 py-1 rounded-lg font-semibold transition-all cursor-pointer ${
                !modoExame ? 'bg-white text-purple-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Modo Prática
            </button>
            <button
              onClick={() => setModoExame(true)}
              className={`px-3 py-1 rounded-lg font-semibold transition-all cursor-pointer ${
                modoExame ? 'bg-white text-purple-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Simulação de Teste
            </button>
          </div>
        </div>

        {/* Seletor Reativo de Período */}
        <div className="flex items-center gap-1.5 p-1.5 bg-slate-100 rounded-xl overflow-x-auto">
          {[
            { id: 'Todos', label: 'Todos os Períodos' },
            { id: '1_Periodo', label: '1.º Período' },
            { id: '2_Periodo', label: '2.º Período' },
            { id: '3_Periodo', label: '3.º Período' }
          ].map((p) => {
            const ativo = (periodo || 'Todos') === p.id;
            return (
              <button
                key={p.id}
                onClick={() => {
                  if (onMudarPeriodo) {
                    onMudarPeriodo(p.id);
                  }
                }}
                className={`flex-1 px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer whitespace-nowrap ${
                  ativo
                    ? 'bg-purple-600 text-white shadow-sm'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
                }`}
              >
                {p.label}
              </button>
            );
          })}
        </div>

        {/* Input de Pesquisa e Botão */}
        <div className="flex flex-col sm:flex-row items-center gap-2">
          <input
            type="text"
            value={topicos}
            onChange={(e) => setTopicos(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && carregarQuiz(topicos)}
            placeholder="Especifica um tema (ex: Rochas, Equações, Planetas)..."
            className="p-2.5 text-xs rounded-xl border border-slate-300 w-full outline-none focus:border-purple-500"
          />
          <button
            onClick={() => carregarQuiz(topicos)}
            disabled={aCarregar}
            className="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-semibold text-xs shrink-0 flex items-center justify-center gap-1.5 cursor-pointer shadow-sm transition-all"
          >
            {aCarregar ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <BrainCircuit className="w-3.5 h-3.5" />}
            Gerar Teste
          </button>
        </div>

        {/* Sugestões Rápidas de Tópicos */}
        {sugestoes.length > 0 && (
          <div className="flex items-center gap-1.5 flex-wrap pt-2 border-t border-slate-100">
            <span className="text-[11px] font-semibold text-slate-400 mr-1">Temas rápidos:</span>
            {sugestoes.map((sug, i) => (
              <button
                key={i}
                onClick={() => {
                  setTopicos(sug);
                  carregarQuiz(sug);
                }}
                className="text-[11px] px-2.5 py-1 rounded-lg bg-slate-50 hover:bg-purple-50 text-slate-600 hover:text-purple-700 border border-slate-200 transition-all cursor-pointer"
              >
                {sug}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Conteúdo do Quiz */}
      {aCarregar ? (
        <div className="bg-white rounded-3xl p-16 border border-slate-200 shadow-sm flex flex-col items-center justify-center gap-3 text-slate-500">
          <Loader2 className="w-8 h-8 animate-spin text-purple-600" />
          <p className="text-sm font-medium">A compor teste pedagógico com questões oficiais do 7.º Ano...</p>
        </div>
      ) : total === 0 ? (
        <div className="bg-white rounded-3xl p-12 border border-slate-200 shadow-sm text-center flex flex-col items-center gap-3 text-slate-500">
          <BookOpen className="w-10 h-10 text-slate-300" />
          <p className="text-sm">Clica em «Gerar Teste» para começar um simulador com questões desta disciplina.</p>
        </div>
      ) : concluido ? (
        /* ECRÃ DE RESULTADOS FINAIS */
        <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-lg flex flex-col gap-6 animate-fadeIn">
          <div className="text-center flex flex-col items-center gap-3">
            <div className="w-16 h-16 rounded-2xl bg-amber-100 text-amber-600 flex items-center justify-center shadow-inner">
              <Trophy className="w-8 h-8" />
            </div>
            <h3 className="text-2xl font-bold text-slate-800">Resultado do Teste</h3>
            <p className="text-xs text-slate-500">Avaliação calculada de acordo com as metas curriculares do 7.º Ano</p>
          </div>

          {/* Caixa de Classificação */}
          {(() => {
            const aval = getNivelAvaliacao(percentagem);
            return (
              <div className={`p-5 rounded-2xl border ${aval.bg} flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left`}>
                <div>
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Classificação Final</span>
                  <h4 className={`text-2xl font-black ${aval.cor}`}>{aval.label}</h4>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-center">
                    <p className="text-3xl font-black text-slate-800">{percentagem}%</p>
                    <p className="text-[10px] uppercase font-bold text-slate-400">Pontuação</p>
                  </div>
                  <div className="w-px h-8 bg-slate-200" />
                  <div className="text-center">
                    <p className="text-3xl font-black text-emerald-600">{acertos}/{total}</p>
                    <p className="text-[10px] uppercase font-bold text-slate-400">Acertos</p>
                  </div>
                </div>
              </div>
            );
          })()}

          {/* Revisão Questão a Questão */}
          <div className="flex flex-col gap-3">
            <h4 className="text-sm font-bold text-slate-800 flex items-center gap-2">
              <ListFilter className="w-4 h-4 text-purple-600" /> Revisão e Correção do Teste
            </h4>
            <div className="flex flex-col gap-2.5 max-h-96 overflow-y-auto pr-1">
              {questoes.map((q, idx) => {
                const resp = respostasUsuario[idx];
                const correta = resp?.toUpperCase() === q.resposta_correta?.toUpperCase();
                return (
                  <div
                    key={idx}
                    className={`p-4 rounded-xl border text-xs flex flex-col gap-2 ${
                      correta ? 'bg-emerald-50/50 border-emerald-200' : 'bg-rose-50/50 border-rose-200'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <span className="font-bold text-slate-800">
                        {idx + 1}. {q.enunciado}
                      </span>
                      {correta ? (
                        <span className="shrink-0 px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-bold text-[10px]">
                          ✓ Correto
                        </span>
                      ) : (
                        <span className="shrink-0 px-2 py-0.5 rounded-full bg-rose-100 text-rose-800 font-bold text-[10px]">
                          ✗ Errado
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-4 text-slate-600">
                      <span>A tua resposta: <strong className={correta ? 'text-emerald-700' : 'text-rose-700'}>{resp || 'Não respondida'}</strong></span>
                      <span>Resposta certa: <strong className="text-emerald-700">{q.resposta_correta}</strong></span>
                    </div>
                    {q.explicacao && (
                      <p className="text-slate-500 italic bg-white/70 p-2 rounded-lg border border-slate-100">
                        💡 {q.explicacao}
                      </p>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          <div className="flex items-center justify-center gap-3 pt-4 border-t border-slate-100">
            <button
              onClick={() => {
                setConcluido(false);
                setRespostasUsuario({});
                setIndiceAtual(0);
              }}
              className="px-5 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs flex items-center gap-1.5 transition-colors cursor-pointer"
            >
              <RotateCcw className="w-4 h-4" /> Repetir Teste
            </button>
            <button
              onClick={() => carregarQuiz(topicos)}
              className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-semibold text-xs flex items-center gap-1.5 shadow-md shadow-purple-500/20 transition-all cursor-pointer"
            >
              <BrainCircuit className="w-4 h-4" /> Gerar Novo Teste
            </button>
          </div>
        </div>
      ) : (
        /* CARTÃO DA PERGUNTA ATIVA */
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm flex flex-col justify-between gap-6">
          {/* Barra de Progresso Superior */}
          <div>
            <div className="flex items-center justify-between text-xs text-slate-400 font-semibold mb-2">
              <span className="text-purple-600 font-bold uppercase tracking-wider">
                {questao?.grupo || 'Consolidação'} • Questão {indiceAtual + 1} de {total}
              </span>
              <span>{Math.round(((indiceAtual + 1) / total) * 100)}%</span>
            </div>
            <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-purple-500 to-indigo-600 transition-all duration-300"
                style={{ width: `${((indiceAtual + 1) / total) * 100}%` }}
              />
            </div>
          </div>

          {/* Enunciado da Pergunta */}
          <div className="text-base font-semibold text-slate-800 leading-relaxed whitespace-pre-line">
            {questao?.enunciado}
          </div>

          {/* Opções de Resposta */}
          <div className="grid grid-cols-1 gap-3">
            {questao?.opcoes?.map((opt) => {
              const foiSelecionada = respostaDada === opt.letra;
              const ehOpcaoCorreta = opt.letra.toUpperCase() === questao.resposta_correta?.toUpperCase();

              let estilo = 'border-slate-200 hover:border-purple-300 bg-white text-slate-700 hover:bg-purple-50/20';

              if (respostaDada) {
                if (modoExame) {
                  // No modo exame, apenas destaca a selecionada sem dizer se está certa ou errada
                  estilo = foiSelecionada
                    ? 'border-purple-600 bg-purple-50 text-purple-900 font-semibold shadow-sm'
                    : 'border-slate-200 opacity-60 text-slate-500';
                } else {
                  // No modo prática, dá feedback imediato com cores
                  if (ehOpcaoCorreta) {
                    estilo = 'border-emerald-500 bg-emerald-50/80 text-emerald-900 font-semibold shadow-sm';
                  } else if (foiSelecionada) {
                    estilo = 'border-rose-500 bg-rose-50 text-rose-900 font-semibold shadow-sm';
                  } else {
                    estilo = 'border-slate-200 opacity-60 text-slate-500';
                  }
                }
              }

              return (
                <button
                  key={opt.letra}
                  disabled={respostaDada !== undefined}
                  onClick={() => responder(opt.letra)}
                  className={`p-3.5 rounded-2xl border-2 text-left flex items-start gap-3.5 transition-all cursor-pointer ${estilo}`}
                >
                  <span
                    className={`w-7 h-7 rounded-xl flex items-center justify-center font-bold text-xs shrink-0 transition-transform ${
                      respostaDada && !modoExame
                        ? ehOpcaoCorreta
                          ? 'bg-emerald-600 text-white'
                          : foiSelecionada
                          ? 'bg-rose-600 text-white'
                          : 'bg-slate-100 text-slate-600'
                        : foiSelecionada
                        ? 'bg-purple-600 text-white'
                        : 'bg-slate-100 text-slate-700'
                    }`}
                  >
                    {opt.letra}
                  </span>
                  <span className="text-sm leading-snug pt-0.5">{opt.texto}</span>
                </button>
              );
            })}
          </div>

          {/* Feedback Didático Imediato (no Modo Prática) */}
          {respostaDada && !modoExame && (
            <div
              className={`p-4 rounded-2xl border flex flex-col gap-1.5 animate-fadeIn ${
                estaCorreta
                  ? 'bg-emerald-50 border-emerald-200 text-emerald-900'
                  : 'bg-rose-50 border-rose-200 text-rose-900'
              }`}
            >
              <div className="flex items-center gap-2 font-bold text-xs uppercase tracking-wide">
                {estaCorreta ? (
                  <>
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Resposta Correta!
                  </>
                ) : (
                  <>
                    <XCircle className="w-4 h-4 text-rose-600" /> Resposta Incorreta (Opção Correta: {questao.resposta_correta})
                  </>
                )}
              </div>
              <p className="text-xs text-slate-700 leading-relaxed">
                {questao.explicacao || 'Critério oficial do programa do 7.º Ano.'}
              </p>
            </div>
          )}

          {/* Rodapé de Navegação */}
          <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
            <button
              onClick={anteriorQuestao}
              disabled={indiceAtual === 0}
              className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100 disabled:opacity-40 disabled:hover:bg-transparent cursor-pointer transition-all"
            >
              ← Anterior
            </button>

            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400">
                Dica: Podes carregar em A, B, C ou D no teclado
              </span>
            </div>

            <button
              onClick={proximaQuestao}
              disabled={respostaDada === undefined}
              className="px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-semibold text-xs flex items-center gap-1.5 shadow-md shadow-purple-500/20 disabled:opacity-50 cursor-pointer transition-all"
            >
              {indiceAtual === total - 1 ? 'Ver Resultado' : 'Seguinte'} <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
