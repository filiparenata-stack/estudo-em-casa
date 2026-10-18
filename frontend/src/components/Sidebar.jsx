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

export default function Sidebar({ disciplinas, disciplinaSelecionada, setDisciplinaSelecionada }) {
  return (
    <aside className="w-full md:w-64 bg-white border-r border-slate-200 p-4 shrink-0 flex flex-col gap-2">
      <div className="px-2 py-1.5 text-xs font-bold text-slate-400 uppercase tracking-wider">
        Disciplinas do 7.º Ano
      </div>

      <div className="flex flex-col gap-1.5">
        {disciplinas.map((disc) => {
          const IconeComp = ICON_MAP[disc.icone] || BookOpenText;
          const isAtivo = disciplinaSelecionada?.id === disc.id;

          return (
            <button
              key={disc.id}
              onClick={() => setDisciplinaSelecionada(disc)}
              className={`w-full flex items-center justify-between p-2.5 rounded-xl text-left transition-all group ${
                isAtivo
                  ? 'bg-blue-50 text-blue-900 border border-blue-200 font-semibold shadow-sm'
                  : 'hover:bg-slate-50 text-slate-700 hover:text-slate-900 border border-transparent'
              }`}
            >
              <div className="flex items-center gap-3 min-w-0">
                <div
                  className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 transition-transform group-hover:scale-105 ${
                    isAtivo ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-600'
                  }`}
                >
                  <IconeComp className="w-4 h-4" />
                </div>
                <div className="min-w-0">
                  <p className="text-sm truncate">{disc.nome}</p>
                  <p className="text-[11px] text-slate-400 font-normal truncate">{disc.total_manuais} manuais • {disc.total_recursos} rec.</p>
                </div>
              </div>

              {isAtivo && <CheckCircle2 className="w-4 h-4 text-blue-600 shrink-0" />}
            </button>
          );
        })}
      </div>
    </aside>
  );
}
