import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  FolderOpen,
  Search,
  ExternalLink,
  FileText,
  CheckCircle,
  Sparkles,
  Laptop,
  DownloadCloud
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
      } else {
        alert('Este ficheiro PDF encontra-se guardado localmente no teu PC. Para o abrir com 1 clique, executa a aplicação no computador com o ficheiro iniciar_app.bat.');
      }
    } catch (e) {
      alert('Para abrir PDFs diretamente do disco rígido, executa a app no computador através do ficheiro iniciar_app.bat.');
    }
  };

  const manuaisFiltrados = manuais.filter((m) =>
    (m.nome || '').toLowerCase().includes(busca.toLowerCase()) ||
    (m.projeto || '').toLowerCase().includes(busca.toLowerCase())
  );

  return (
    <div className="flex-1 p-6 max-w-5xl mx-auto flex flex-col gap-6">
      {/* Banner Informativo */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200/80 rounded-2xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs text-blue-900 shadow-sm">
        <div className="flex items-center gap-2.5">
          <Sparkles className="w-4 h-4 text-blue-600 shrink-0" />
          <span>
            <strong>Acervo Oficial de 79 Manuais do 7.º Ano:</strong> Todos os manuais, cadernos e dossiês estão indexados para resumos e testes. Podes ler os PDFs em alta resolução alojados no GitHub ou aceder à Escola Virtual.
          </span>
        </div>
        <div className="flex items-center gap-1.5 text-slate-500 font-medium shrink-0">
          <DownloadCloud className="w-3.5 h-3.5 text-emerald-600" />
          <span>GitHub Cloud & PC</span>
        </div>
      </div>

      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <span className="text-xs uppercase font-bold text-blue-600">Biblioteca Digital</span>
          <h2 className="text-xl font-bold text-slate-800">
            Manuais e Dossiês de {disciplina?.nome}
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Manuais completos e cadernos de atividades em alta resolução (3840×2400) prontos a ler online ou offline.
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
    </div>
  );
}
