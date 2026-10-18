import React, { useState } from 'react';
import {
  RotateCw,
  ChevronLeft,
  ChevronRight,
  CheckCircle,
  HelpCircle,
  Shuffle,
  Lightbulb,
  Sparkles
} from 'lucide-react';

export default function FlashcardsView({ resumoAtual, disciplina }) {
  const [cartaoIndex, setCartaoIndex] = useState(0);
  const [virado, setVirado] = useState(false);
  const [mostrarDica, setMostrarDica] = useState(false);
  const [aprendidos, setAprendidos] = useState(new Set());

  const flashcards = resumoAtual?.flashcards || [
    {
      id: 1,
      frente: 'O que são Minerais?',
      verso: 'Substâncias sólidas, naturais e inorgânicas, com uma estrutura cristalina bem definida e composição química fixa ou variável dentro de limites definidos.',
      dica: 'Características: sólido, natural, inorgânico, cristalino.',
      categoria: 'Conceitos'
    },
    {
      id: 2,
      frente: 'Qual a diferença entre Rocha e Mineral?',
      verso: 'Um mineral é um composto homogéneo individual; uma rocha é um agregado natural formado por um ou mais minerais (ou matéria orgânica).',
      dica: 'Pensa em tijolo (mineral) vs parede (rocha).',
      categoria: 'Comparações'
    },
    {
      id: 3,
      frente: 'Como se calcula a Velocidade Média?',
      verso: 'v = d / Δt, onde v é a velocidade média (m/s ou km/h), d é a distância percorrida e Δt é o intervalo de tempo decorrido.',
      dica: 'Lembra-te de converter horas para segundos ou km para metros se o teste pedir em SI.',
      categoria: 'Fórmulas'
    }
  ];

  const atual = flashcards[cartaoIndex] || flashcards[0];
  const total = flashcards.length;

  const anterior = () => {
    setVirado(false);
    setMostrarDica(false);
    setCartaoIndex((prev) => (prev > 0 ? prev - 1 : total - 1));
  };

  const seguinte = () => {
    setVirado(false);
    setMostrarDica(false);
    setCartaoIndex((prev) => (prev < total - 1 ? prev + 1 : 0));
  };

  const marcarAprendido = () => {
    const novo = new Set(aprendidos);
    if (novo.has(atual.id)) {
      novo.delete(atual.id);
    } else {
      novo.add(atual.id);
    }
    setAprendidos(novo);
    seguinte();
  };

  const jaSabe = aprendidos.has(atual.id);

  return (
    <div className="flex-1 p-6 max-w-3xl mx-auto flex flex-col items-center justify-center gap-6">
      {/* Topo do Modo de Treino */}
      <div className="w-full flex items-center justify-between">
        <div>
          <span className="text-xs uppercase font-bold text-slate-400">Flashcards de Memorização</span>
          <h2 className="text-lg font-bold text-slate-800">
            {disciplina?.nome || '7.º Ano'} • Cartão {cartaoIndex + 1} de {total}
          </h2>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
            {aprendidos.size} de {total} dominados
          </span>
        </div>
      </div>

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

            <div className="flex flex-col items-center text-center my-auto">
              <p className="text-xl font-bold text-slate-800 leading-snug">
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
                className="text-amber-600 hover:text-amber-700 font-semibold flex items-center gap-1"
              >
                <Lightbulb className="w-3.5 h-3.5" /> {mostrarDica ? 'Ocultar dica' : 'Ver dica'}
              </button>

              <span>Espaço para virar</span>
            </div>
          </div>

          {/* VERSO DO CARTÃO */}
          <div className="absolute inset-0 w-full h-full bg-gradient-to-br from-blue-900 to-indigo-950 text-white rounded-3xl p-8 border-2 border-blue-700 shadow-xl flex flex-col justify-between backface-hidden rotate-y-180">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-emerald-400 bg-emerald-950/60 border border-emerald-500/30 px-2.5 py-1 rounded-lg">
                Resposta / Definição
              </span>
              <span className="text-xs text-blue-200 flex items-center gap-1">
                <RotateCw className="w-3.5 h-3.5" /> Clica para voltar à pergunta
              </span>
            </div>

            <div className="flex flex-col items-center text-center my-auto">
              <p className="text-base md:text-lg font-medium text-slate-100 leading-relaxed max-w-xl">
                {atual.verso}
              </p>
            </div>

            <div className="text-center text-xs text-blue-300">
              Escola Virtual 7.º Ano • Critério Oficial
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
            <CheckCircle className="w-4 h-4" /> {jaSabe ? 'Dominado ✓' : 'Marcar como Dominado'}
          </button>
        </div>

        <button
          onClick={seguinte}
          className="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs flex items-center justify-center gap-1 shadow-md shadow-blue-500/20 transition-all cursor-pointer"
        >
          Próximo <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
