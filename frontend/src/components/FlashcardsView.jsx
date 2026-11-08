import React, { useState, useEffect } from 'react';
import {
  RotateCw,
  ChevronLeft,
  ChevronRight,
  CheckCircle,
  Shuffle,
  Lightbulb,
  Sparkles,
  Loader2,
  Layers
} from 'lucide-react';

function extrairCartoesDeTopicos(topicos = []) {
  const deck = [];
  let nextId = 1;

  topicos.forEach((topico) => {
    // 1. Flashcards diretos do tópico
    if (Array.isArray(topico.flashcards)) {
      topico.flashcards.forEach((fc) => {
        const frente = fc.frente || fc.pergunta;
        const verso = fc.verso || fc.resposta;
        if (frente && verso) {
          deck.push({
            id: `fc_${topico.id || nextId}_${nextId++}`,
            frente,
            verso,
            dica: fc.dica || `Tópico: ${topico.titulo}`,
            categoria: topico.titulo || 'Conceito Curricular'
          });
        }
      });
    }

    // 2. Conceitos-chave transformados em cartões
    if (Array.isArray(topico.conceitos_chave)) {
      topico.conceitos_chave.forEach((c) => {
        if (c.termo && c.definicao) {
          deck.push({
            id: `cc_${topico.id || nextId}_${nextId++}`,
            frente: `O que é ${c.termo}?`,
            verso: c.definicao,
            dica: `Tópico: ${topico.titulo}`,
            categoria: 'Conceito-Chave'
          });
        }
      });
    }

    // 3. Questão de exame do Foco no Teste
    if (
      topico.foco_teste &&
      topico.foco_teste.questao_exemplo &&
      topico.foco_teste.proposta_resolucao
    ) {
      deck.push({
        id: `ft_${topico.id || nextId}_${nextId++}`,
        frente: `Questão de Exame: ${topico.foco_teste.questao_exemplo}`,
        verso: topico.foco_teste.proposta_resolucao,
        dica:
          topico.foco_teste.erro_frequente ||
          topico.foco_teste.criterio_cotacao ||
          `Unidade: ${topico.titulo}`,
        categoria: 'Exame / Teste'
      });
    }
  });

  return deck;
}

export default function FlashcardsView({
  resumoAtual,
  disciplina,
  periodo,
  onMudarPeriodo
}) {
  const [periodoEfetivo, setPeriodoEfetivo] = useState(
    periodo || '1_Periodo'
  );
  const [modoFonte, setModoFonte] = useState('periodo'); // 'periodo' | 'livre'
  const [cartoesPeriodo, setCartoesPeriodo] = useState([]);
  const [aCarregar, setACarregar] = useState(false);

  const [cartaoIndex, setCartaoIndex] = useState(0);
  const [virado, setVirado] = useState(false);
  const [mostrarDica, setMostrarDica] = useState(false);
  const [aprendidos, setAprendidos] = useState(new Set());

  // Sincronizar com a prop periodo vinda do App / Navbar
  useEffect(() => {
    if (periodo && periodo !== periodoEfetivo) {
      setPeriodoEfetivo(periodo);
    }
  }, [periodo]);

  // Se resumoAtual mudar e pertencer à disciplina atual, podemos ativar ou disponibilizar a fonte livre
  const temResumoLivre =
    resumoAtual &&
    (!resumoAtual.disciplina_id || resumoAtual.disciplina_id === disciplina?.id) &&
    Array.isArray(resumoAtual.flashcards) &&
    resumoAtual.flashcards.length > 0;

  // Carregar flashcards dinâmicos do período/disciplina
  useEffect(() => {
    if (!disciplina) return;

    setCartaoIndex(0);
    setVirado(false);
    setMostrarDica(false);
    setAprendidos(new Set());
    setACarregar(true);

    const periodosParaCarregar =
      periodoEfetivo === 'Todos'
        ? ['1_Periodo', '2_Periodo', '3_Periodo']
        : [periodoEfetivo || '1_Periodo'];

    Promise.all(
      periodosParaCarregar.map((p) =>
        fetch(`/api/resumo/periodo?disciplina_id=${disciplina.id}&periodo=${p}`)
          .then((r) => (r.ok ? r.json() : null))
          .catch(() => null)
      )
    )
      .then((respostas) => {
        const todosTopicos = [];
        respostas.forEach((dados) => {
          if (dados && Array.isArray(dados.topicos)) {
            todosTopicos.push(...dados.topicos);
          }
        });
        const sintetizados = extrairCartoesDeTopicos(todosTopicos);
        setCartoesPeriodo(sintetizados);
      })
      .finally(() => {
        setACarregar(false);
      });
  }, [disciplina, periodoEfetivo]);

  const cartoesLivre = temResumoLivre
    ? resumoAtual.flashcards.map((fc, idx) => ({
        id: `livre_${idx + 1}`,
        frente: fc.frente,
        verso: fc.verso,
        dica: fc.dica || resumoAtual.titulo,
        categoria: resumoAtual.titulo || 'Resumo Livre'
      }))
    : [];

  const flashcards =
    modoFonte === 'livre' && temResumoLivre ? cartoesLivre : cartoesPeriodo;

  const total = flashcards.length;
  const atual = flashcards[cartaoIndex] || flashcards[0];

  const selecionarPeriodo = (novoPeriodo) => {
    setModoFonte('periodo');
    setPeriodoEfetivo(novoPeriodo);
    if (onMudarPeriodo) {
      onMudarPeriodo(novoPeriodo);
    }
  };

  const anterior = () => {
    if (total === 0) return;
    setVirado(false);
    setMostrarDica(false);
    setCartaoIndex((prev) => (prev > 0 ? prev - 1 : total - 1));
  };

  const seguinte = () => {
    if (total === 0) return;
    setVirado(false);
    setMostrarDica(false);
    setCartaoIndex((prev) => (prev < total - 1 ? prev + 1 : 0));
  };

  const baralharCartoes = () => {
    if (cartoesPeriodo.length <= 1) return;
    const copia = [...cartoesPeriodo];
    for (let i = copia.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [copia[i], copia[j]] = [copia[j], copia[i]];
    }
    setCartoesPeriodo(copia);
    setCartaoIndex(0);
    setVirado(false);
    setMostrarDica(false);
  };

  const marcarAprendido = () => {
    if (!atual) return;
    const novo = new Set(aprendidos);
    if (novo.has(atual.id)) {
      novo.delete(atual.id);
    } else {
      novo.add(atual.id);
    }
    setAprendidos(novo);
    seguinte();
  };

  const jaSabe = atual ? aprendidos.has(atual.id) : false;

  return (
    <div className="flex-1 p-6 max-w-4xl mx-auto flex flex-col items-center justify-start gap-6 w-full">
      {/* Barra de Seleção de Período e Fonte */}
      <div className="w-full bg-white rounded-2xl p-4 border border-slate-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-3">
        <div className="flex items-center gap-1.5 p-1 bg-slate-100 rounded-xl w-full md:w-auto overflow-x-auto">
          {[
            { id: '1_Periodo', label: '1.º Período' },
            { id: '2_Periodo', label: '2.º Período' },
            { id: '3_Periodo', label: '3.º Período' },
            { id: 'Todos', label: 'Ano Completo / Todos' }
          ].map((p) => {
            const ativo = modoFonte === 'periodo' && periodoEfetivo === p.id;
            return (
              <button
                key={p.id}
                onClick={() => selecionarPeriodo(p.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer whitespace-nowrap ${
                  ativo
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
                }`}
              >
                {p.label}
              </button>
            );
          })}

          {temResumoLivre && (
            <button
              onClick={() => {
                setModoFonte('livre');
                setCartaoIndex(0);
                setVirado(false);
                setMostrarDica(false);
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer flex items-center gap-1 whitespace-nowrap ${
                modoFonte === 'livre'
                  ? 'bg-purple-600 text-white shadow-sm'
                  : 'text-purple-700 hover:bg-purple-50'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Flashcards do Resumo Livre ({cartoesLivre.length})</span>
            </button>
          )}
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={baralharCartoes}
            disabled={aCarregar || total <= 1}
            className="px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 disabled:opacity-50 text-slate-700 text-xs font-semibold flex items-center gap-1.5 cursor-pointer transition-colors"
            title="Baralhar ordem dos cartões"
          >
            <Shuffle className="w-3.5 h-3.5" />
            <span>Baralhar</span>
          </button>
          <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
            {aprendidos.size} de {total} dominados
          </span>
        </div>
      </div>

      {/* Topo do Modo de Treino */}
      <div className="w-full flex items-center justify-between">
        <div>
          <span className="text-xs uppercase font-bold text-slate-400">
            Flashcards 3D de Memorização Ativa
          </span>
          <h2 className="text-lg font-bold text-slate-800">
            {disciplina?.nome || '7.º Ano'} •{' '}
            {total > 0 ? `Cartão ${cartaoIndex + 1} de ${total}` : 'Sem cartões'}
          </h2>
        </div>
      </div>

      {aCarregar ? (
        <div className="w-full h-80 bg-white rounded-3xl border border-slate-200 flex flex-col items-center justify-center gap-3 text-slate-500 shadow-sm">
          <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
          <p className="text-sm font-semibold">
            A preparar baralho de flashcards de {disciplina?.nome}...
          </p>
        </div>
      ) : total === 0 || !atual ? (
        <div className="w-full h-80 bg-white rounded-3xl border border-slate-200 flex flex-col items-center justify-center gap-3 text-slate-500 p-8 text-center shadow-sm">
          <Layers className="w-10 h-10 text-slate-300" />
          <p className="text-sm font-semibold text-slate-700">
            Não foram encontrados flashcards para esta seleção.
          </p>
        </div>
      ) : (
        <>
          {/* Barra de Progresso */}
          <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
            <div
              className="bg-blue-600 h-full transition-all duration-300"
              style={{ width: `${((cartaoIndex + 1) / total) * 100}%` }}
            />
          </div>

          {/* Cartão 3D Interativo */}
          <div
            onClick={() => setVirado(!virado)}
            className="w-full h-80 perspective-1000 cursor-pointer select-none"
          >
            <div
              className={`relative w-full h-full duration-500 transform-style-3d transition-transform ${
                virado ? 'rotate-y-180' : ''
              }`}
            >
              {/* FRENTE DO CARTÃO */}
              <div className="absolute inset-0 w-full h-full bg-white rounded-3xl p-8 border-2 border-slate-200 shadow-lg hover:border-blue-400 flex flex-col justify-between backface-hidden transition-colors">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded-lg">
                    {atual.categoria || 'Pergunta de Teste'}
                  </span>
                  <span className="text-xs text-slate-400 flex items-center gap-1">
                    <RotateCw className="w-3.5 h-3.5" /> Clica para ver a resposta
                  </span>
                </div>

                <div className="flex flex-col items-center text-center my-auto overflow-y-auto max-h-44 px-2">
                  <p className="text-lg md:text-xl font-bold text-slate-800 leading-snug">
                    {atual.frente}
                  </p>

                  {mostrarDica && atual.dica && (
                    <div className="mt-4 p-2.5 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 font-medium animate-fadeIn">
                      💡 {atual.dica}
                    </div>
                  )}
                </div>

                <div className="flex items-center justify-between text-xs text-slate-400">
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      setMostrarDica(!mostrarDica);
                    }}
                    className="text-amber-600 hover:text-amber-700 font-semibold flex items-center gap-1 cursor-pointer"
                  >
                    <Lightbulb className="w-3.5 h-3.5" />{' '}
                    {mostrarDica ? 'Ocultar dica' : 'Ver dica'}
                  </button>

                  <span>Clica no cartão para virar</span>
                </div>
              </div>

              {/* VERSO DO CARTÃO */}
              <div className="absolute inset-0 w-full h-full bg-gradient-to-br from-blue-900 to-indigo-950 text-white rounded-3xl p-8 border-2 border-blue-700 shadow-xl flex flex-col justify-between backface-hidden rotate-y-180">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-emerald-400 bg-emerald-950/60 border border-emerald-500/30 px-2.5 py-1 rounded-lg">
                    Resposta / Definição Oficial
                  </span>
                  <span className="text-xs text-blue-200 flex items-center gap-1">
                    <RotateCw className="w-3.5 h-3.5" /> Clica para voltar à pergunta
                  </span>
                </div>

                <div className="flex flex-col items-center text-center my-auto overflow-y-auto max-h-44 px-2">
                  <p className="text-sm md:text-base font-medium text-slate-100 leading-relaxed max-w-xl">
                    {atual.verso}
                  </p>
                </div>

                <div className="text-center text-xs text-blue-300">
                  {disciplina?.nome || '7.º Ano'} •{' '}
                  {periodoEfetivo === 'Todos'
                    ? 'Ano Completo'
                    : periodoEfetivo.replace('_', '.º ')}
                </div>
              </div>
            </div>
          </div>

          {/* Controlos de Navegação e Autoavaliação */}
          <div className="w-full flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
            <button
              onClick={anterior}
              className="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs flex items-center justify-center gap-1 transition-colors cursor-pointer"
            >
              <ChevronLeft className="w-4 h-4" /> Anterior
            </button>

            <div className="flex items-center gap-2 w-full sm:w-auto justify-center">
              <button
                onClick={marcarAprendido}
                className={`px-4 py-2.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer ${
                  jaSabe
                    ? 'bg-emerald-600 text-white shadow-sm'
                    : 'bg-emerald-50 text-emerald-700 border border-emerald-200 hover:bg-emerald-100'
                }`}
              >
                <CheckCircle className="w-4 h-4" />{' '}
                {jaSabe ? 'Dominado ✓' : 'Marcar como Dominado'}
              </button>
            </div>

            <button
              onClick={seguinte}
              className="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs flex items-center justify-center gap-1 shadow-md shadow-blue-500/20 transition-all cursor-pointer"
            >
              Próximo <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </>
      )}
    </div>
  );
}
