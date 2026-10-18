import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  FolderOpen,
  Search,
  ExternalLink,
  FileText,
  CheckCircle,
  FileCheck
} from 'lucide-react';

export default function BibliotecaView({ disciplina }) {
  const [manuais, setManuais] = useState([]);
  const [busca, setBusca] = useState('');
  const [abertoInfo, setAbertoInfo] = useState(null);

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
      }
    } catch (e) {
      alert('Erro ao abrir ficheiro no computador: ' + e.message);
    }
  };

  const manuaisFiltrados = manuais.filter((m) =>
    m.nome.toLowerCase().includes(busca.toLowerCase())
  );

  return (
    <div className="flex-1 p-6 max-w-5xl mx-auto flex flex-col gap-6">
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <span className="text-xs uppercase font-bold text-blue-600">Biblioteca Digital</span>
          <h2 className="text-xl font-bold text-slate-800">
            Manuais e Dossiês de {disciplina?.nome}
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            PDFs em alta resolução vertical (3840×2400) prontos a ler no computador ou tablet.
          </p>
        </div>

        <div className="relative w-full md:w-64">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
            placeholder="Pesquisar manual..."
            className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-300 outline-none focus:border-blue-500"
          />
        </div>
      </div>

      {abertoInfo && (
        <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 px-4 py-2.5 rounded-xl text-xs flex items-center gap-2 animate-fadeIn">
          <CheckCircle className="w-4 h-4 text-emerald-600" />
          <span>Ficheiro aberto com sucesso no teu leitor de PDF predefinido!</span>
        </div>
      )}

      {/* Grid de Manuais */}
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
                  {m.nome.replace('.pdf', '').replace(/_/g, ' ')}
                </h3>
                <span className="text-[11px] text-slate-400 font-medium">
                  {m.tamanho_mb} MB • PDF Alta Resolução
                </span>
              </div>
            </div>

            <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
              <span className="text-[11px] font-semibold text-slate-400">
                Página a página vertical
              </span>
              <button
                onClick={() => abrirFicheiro(m.caminho)}
                className="px-3 py-1.5 rounded-lg bg-blue-50 hover:bg-blue-600 text-blue-700 hover:text-white text-xs font-semibold flex items-center gap-1 transition-all cursor-pointer"
              >
                Abrir PDF <ExternalLink className="w-3 h-3" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
