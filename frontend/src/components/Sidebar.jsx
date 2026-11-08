import React from 'react';
import {
  Atom,
  Globe2,
  Leaf,
  Hourglass,
  Languages,
  Calculator,
  BookOpenText,
  Compass,
  CheckCircle2
} from 'lucide-react';

const ICON_MAP = {
  Atom,
  Globe2,
  Leaf,
  Hourglass,
  Languages,
  Calculator,
  BookOpenText,
  Compass
};

export default function Sidebar({
  disciplinas = [],
  disciplinaSelecionada,
  setDisciplinaSelecionada,
  anoAtivo = '3',
  onAbrirLivro
}) {
  const is3Ano = anoAtivo === '3';
  const is8Ano = anoAtivo === '8';

  return (
    <aside className="w-full md:w-64 bg-white border-r border-slate-200 p-4 shrink-0 flex flex-col gap-3">
      <div className="flex items-center justify-between px-2 py-1">
        <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
          {is3Ano ? 'Disciplinas do 3.º Ano' : is8Ano ? 'Disciplinas do 8.º Ano' : 'Disciplinas do 7.º Ano'}
        </span>
        <span
          className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
            is3Ano
              ? 'bg-purple-100 text-purple-700'
              : is8Ano
              ? 'bg-emerald-100 text-emerald-800'
              : 'bg-blue-100 text-blue-700'
          }`}
        >
          {is3Ano ? '🎒 Renata' : is8Ano ? '🚀 8.º Ano' : '🎓 7.º Ano'}
        </span>
      </div>

      <div className="flex flex-col gap-1.5">
        {disciplinas.map((disc) => {
          const IconeComp = ICON_MAP[disc.icone] || BookOpenText;
          const isAtivo = disciplinaSelecionada?.id === disc.id;

          return (
            <div
              key={disc.id}
              className={`w-full rounded-xl transition-all border ${
                isAtivo
                  ? is3Ano
                    ? 'bg-purple-50/80 text-purple-900 border-purple-200 shadow-sm'
                    : is8Ano
                    ? 'bg-emerald-50 text-emerald-900 border-emerald-300 font-semibold shadow-sm'
                    : 'bg-blue-50 text-blue-900 border-blue-200 font-semibold shadow-sm'
                  : 'hover:bg-slate-50 text-slate-700 hover:text-slate-900 border-transparent'
              }`}
            >
              <button
                onClick={() => setDisciplinaSelecionada(disc)}
                className="w-full flex items-center justify-between p-2.5 text-left cursor-pointer group"
              >
                <div className="flex items-center gap-3 min-w-0">
                  <div
                    className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 transition-transform group-hover:scale-105 ${
                      isAtivo
                        ? is3Ano
                          ? 'bg-purple-600 text-white'
                          : is8Ano
                          ? 'bg-emerald-600 text-white'
                          : 'bg-blue-600 text-white'
                        : 'bg-slate-100 text-slate-600'
                    }`}
                  >
                    <IconeComp className="w-4 h-4" />
                  </div>
                  <div className="min-w-0">
                    <p className={`text-sm truncate ${isAtivo ? 'font-bold' : 'font-medium'}`}>{disc.nome}</p>
                    <p className="text-[11px] text-slate-400 font-normal truncate">
                      {is3Ano
                        ? `${disc.total_recursos || 5} unidades • Manual ZUP`
                        : is8Ano
                        ? `${disc.total_manuais || 1} manual • ${disc.total_recursos || 4} unid.`
                        : `${disc.total_manuais || 0} manuais • ${disc.total_recursos || 0} rec.`}
                    </p>
                  </div>
                </div>

                {isAtivo && (
                  <CheckCircle2
                    className={`w-4 h-4 shrink-0 ${
                      is3Ano ? 'text-purple-600' : is8Ano ? 'text-emerald-600' : 'text-blue-600'
                    }`}
                  />
                )}
              </button>
            </div>
          );
        })}
      </div>

      {is3Ano && (
        <div className="mt-auto pt-3 border-t border-slate-100 text-xs text-slate-500 bg-purple-50/40 p-2.5 rounded-xl border border-purple-100">
          <p className="font-semibold text-purple-900 flex items-center gap-1.5">
            <span>📚 Manuais da Renata</span>
          </p>
          <p className="text-[11px] text-purple-700 mt-0.5">
            Porto Editora digitalizada em alta resolução com leitor PDF integrado e resumos.
          </p>
        </div>
      )}
    </aside>
  );
}
