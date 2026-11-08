import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  X,
  BookOpen,
  ZoomIn,
  ZoomOut,
  Maximize2,
  Minimize2,
  ChevronLeft,
  ChevronRight,
  Download,
  ExternalLink,
  Layers,
  Sparkles,
  Bookmark,
  FileText,
  Sun,
  Moon
} from 'lucide-react';

export default function BookReaderModal({
  isOpen,
  onClose,
  book,
  initialPage = 1
}) {
  const [currentPage, setCurrentPage] = useState(initialPage);
  const [pageInput, setPageInput] = useState(String(initialPage));
  const [zoom, setZoom] = useState(100);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(Boolean(book?.unidades && book.unidades.length > 0));
  const modalRef = useRef(null);
  const iframeRef = useRef(null);

  const totalPages = book?.paginas || 175;

  const handlePageChange = useCallback((newPage) => {
    const clamped = Math.max(1, Math.min(newPage, totalPages));
    setCurrentPage(clamped);
    setPageInput(String(clamped));
  }, [totalPages]);

  const handlePrevPage = useCallback(() => {
    setCurrentPage((prev) => {
      const next = Math.max(1, prev - 1);
      setPageInput(String(next));
      return next;
    });
  }, []);

  const handleNextPage = useCallback(() => {
    setCurrentPage((prev) => {
      const next = Math.min(totalPages, prev + 1);
      setPageInput(String(next));
      return next;
    });
  }, [totalPages]);

  const [prevBookKey, setPrevBookKey] = useState(
    book?.id ? `${book.id}-${initialPage}` : ''
  );
  const currentBookKey = book?.id ? `${book.id}-${initialPage}` : '';
  if (currentBookKey !== prevBookKey) {
    setPrevBookKey(currentBookKey);
    setCurrentPage(initialPage || 1);
    setPageInput(String(initialPage || 1));
  }

  // Gestão de atalhos de teclado (Esc para fechar, setas para navegar páginas)
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        if (isFullscreen) {
          if (document.fullscreenElement) {
            document.exitFullscreen().catch(() => {});
          }
          setIsFullscreen(false);
        } else {
          onClose();
        }
      } else if (e.target.tagName !== 'INPUT') {
        if (e.key === 'ArrowRight' || e.key === 'PageDown') {
          handleNextPage();
        } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
          handlePrevPage();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, isFullscreen, handleNextPage, handlePrevPage, onClose]);

  // Listener para sincronizar estado de fullscreen nativo
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };
    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => document.removeEventListener('fullscreenchange', handleFullscreenChange);
  }, []);

  if (!isOpen || !book) return null;

  const handlePageInputSubmit = (e) => {
    e.preventDefault();
    const parsed = parseInt(pageInput, 10);
    if (!isNaN(parsed)) {
      handlePageChange(parsed);
    } else {
      setPageInput(String(currentPage));
    }
  };

  const handleZoomIn = () => {
    setZoom((prev) => Math.min(prev + 25, 200));
  };

  const handleZoomOut = () => {
    setZoom((prev) => Math.max(prev - 25, 50));
  };

  const handleZoomReset = () => {
    setZoom(100);
  };

  const toggleFullscreen = () => {
    if (!modalRef.current) return;
    if (!isFullscreen) {
      if (modalRef.current.requestFullscreen) {
        modalRef.current.requestFullscreen().catch(() => {});
      }
      setIsFullscreen(true);
    } else {
      if (document.fullscreenElement && document.exitFullscreen) {
        document.exitFullscreen().catch(() => {});
      }
      setIsFullscreen(false);
    }
  };

  // URL do PDF com parâmetros nativos do Adobe / leitor do navegador
  const pdfUrlWithParams = `${book.pdfUrl}#page=${currentPage}&zoom=${zoom}&toolbar=1&navpanes=1`;

  return (
    <div
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-slate-900/80 backdrop-blur-md transition-all animate-fadeIn"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        ref={modalRef}
        className={`w-full h-full max-w-7xl max-h-[96vh] rounded-2xl flex flex-col overflow-hidden shadow-2xl border transition-colors ${
          darkMode
            ? 'bg-slate-900 border-slate-700 text-slate-100'
            : 'bg-white border-slate-200 text-slate-800'
        }`}
      >
        {/* Barra Superior de Controlo / Cabeçalho */}
        <header
          className={`px-4 py-3 flex items-center justify-between gap-3 border-b shrink-0 ${
            darkMode
              ? 'bg-slate-800/90 border-slate-700'
              : 'bg-slate-50/90 border-slate-200'
          }`}
        >
          {/* Informações do Livro */}
          <div className="flex items-center gap-3 min-w-0">
            <div
              className={`w-9 h-9 rounded-xl flex items-center justify-center font-bold text-white shadow-sm shrink-0 bg-gradient-to-br ${
                book.corTema?.primaria || 'from-blue-600 to-indigo-700'
              }`}
            >
              <BookOpen className="w-5 h-5" />
            </div>
            <div className="min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <h3 className="text-sm sm:text-base font-bold truncate">
                  {book.titulo}
                </h3>
                <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-200">
                  {book.ano || '3.º Ano'}
                </span>
                <span className="hidden sm:inline-block px-2 py-0.5 rounded-md text-[10px] font-medium bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-200">
                  Fast Web View ⚡
                </span>
              </div>
              <p
                className={`text-xs truncate ${
                  darkMode ? 'text-slate-400' : 'text-slate-500'
                }`}
              >
                {book.editora} • {book.tamanhoFormatado} • {totalPages} páginas digitalizadas
              </p>
            </div>
          </div>

          {/* Ferramentas do Leitor */}
          <div className="flex items-center gap-1 sm:gap-2 shrink-0">
            {/* Seletor de Capítulos / Sidebar Toggle */}
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className={`p-2 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer ${
                sidebarOpen
                  ? 'bg-blue-600 text-white shadow-sm'
                  : darkMode
                  ? 'bg-slate-700 hover:bg-slate-600 text-slate-200'
                  : 'bg-white hover:bg-slate-100 text-slate-700 border border-slate-200'
              }`}
              title={sidebarOpen ? 'Ocultar Índice de Unidades' : 'Ver Índice de Unidades'}
            >
              <Layers className="w-4 h-4" />
              <span className="hidden md:inline">Unidades</span>
            </button>

            {/* Controlo de Zoom */}
            <div
              className={`hidden sm:flex items-center rounded-xl p-0.5 border ${
                darkMode ? 'bg-slate-700/60 border-slate-600' : 'bg-slate-100 border-slate-200'
              }`}
            >
              <button
                onClick={handleZoomOut}
                disabled={zoom <= 50}
                className="p-1.5 rounded-lg hover:bg-white/50 dark:hover:bg-slate-600 transition-colors disabled:opacity-40 cursor-pointer"
                title="Reduzir Zoom (-)"
              >
                <ZoomOut className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={handleZoomReset}
                className="px-2 py-1 text-[11px] font-semibold hover:bg-white/50 dark:hover:bg-slate-600 transition-colors cursor-pointer"
                title="Repor Zoom (100%)"
              >
                {zoom}%
              </button>
              <button
                onClick={handleZoomIn}
                disabled={zoom >= 200}
                className="p-1.5 rounded-lg hover:bg-white/50 dark:hover:bg-slate-600 transition-colors disabled:opacity-40 cursor-pointer"
                title="Aumentar Zoom (+)"
              >
                <ZoomIn className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Alternar Modo Escuro / Claro */}
            <button
              onClick={() => setDarkMode(!darkMode)}
              className={`p-2 rounded-xl text-xs transition-colors cursor-pointer ${
                darkMode
                  ? 'bg-slate-700 hover:bg-slate-600 text-amber-300'
                  : 'bg-white hover:bg-slate-100 text-slate-600 border border-slate-200'
              }`}
              title={darkMode ? 'Modo Claro' : 'Modo Escuro'}
            >
              {darkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>

            {/* Alternar Ecrã Inteiro */}
            <button
              onClick={toggleFullscreen}
              className={`hidden sm:flex p-2 rounded-xl text-xs transition-colors cursor-pointer ${
                darkMode
                  ? 'bg-slate-700 hover:bg-slate-600 text-slate-200'
                  : 'bg-white hover:bg-slate-100 text-slate-600 border border-slate-200'
              }`}
              title={isFullscreen ? 'Sair do Ecrã Inteiro' : 'Ecrã Inteiro'}
            >
              {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
            </button>

            {/* Abrir em Separador Externo */}
            <a
              href={book.pdfUrl}
              target="_blank"
              rel="noopener noreferrer"
              className={`hidden md:flex p-2 rounded-xl text-xs transition-colors cursor-pointer ${
                darkMode
                  ? 'bg-slate-700 hover:bg-slate-600 text-slate-200'
                  : 'bg-white hover:bg-slate-100 text-slate-600 border border-slate-200'
              }`}
              title="Abrir PDF numa nova aba"
            >
              <ExternalLink className="w-4 h-4" />
            </a>

            {/* Descarregar PDF */}
            <a
              href={book.pdfUrl}
              download={book.canonicalFilename || 'livro.pdf'}
              className="px-3 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold flex items-center gap-1.5 transition-all shadow-sm cursor-pointer"
              title="Descarregar ficheiro PDF completo"
            >
              <Download className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Descarregar</span>
            </a>

            {/* Fechar Modal */}
            <button
              onClick={onClose}
              className={`p-2 rounded-xl transition-colors cursor-pointer ${
                darkMode
                  ? 'bg-slate-700 hover:bg-red-900/60 text-slate-200 hover:text-red-200'
                  : 'bg-white hover:bg-red-50 text-slate-600 hover:text-red-600 border border-slate-200 hover:border-red-200'
              }`}
              title="Fechar Leitor (Esc)"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </header>

        {/* Corpo Principal: Sidebar de Capítulos + Visor Iframe PDF */}
        <div className="flex-1 flex overflow-hidden min-h-0 relative">
          {/* Sidebar / Gaveta de Unidades Curriculares */}
          {sidebarOpen && (
            <aside
              className={`w-72 sm:w-80 shrink-0 border-r flex flex-col overflow-y-auto transition-all ${
                darkMode
                  ? 'bg-slate-800/60 border-slate-700 text-slate-200'
                  : 'bg-slate-50/70 border-slate-200 text-slate-700'
              }`}
            >
              <div className="p-3 border-b border-inherit flex items-center justify-between">
                <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400">
                  <Bookmark className="w-3.5 h-3.5" />
                  <span>Índice Curricular</span>
                </div>
                <span className="text-[11px] font-semibold opacity-70">
                  {book.unidades?.length || 0} Unidades
                </span>
              </div>

              <div className="p-2 space-y-1.5">
                {(!book.unidades || book.unidades.length === 0) ? (
                  <div className={`p-4 text-center rounded-xl border text-xs ${
                    darkMode ? 'bg-slate-800/40 border-slate-700 text-slate-400' : 'bg-white border-slate-200 text-slate-500'
                  }`}>
                    <p className="font-semibold text-slate-700 dark:text-slate-200">Manual Integral</p>
                    <p className="mt-1 text-[11px] leading-relaxed">
                      Este manual encontra-se digitalizado na íntegra. Folheia o conteúdo usando a barra inferior ou as teclas ← e →.
                    </p>
                  </div>
                ) : (
                  book.unidades.map((u) => {
                  const isActive =
                    currentPage >= u.paginaInicio && currentPage <= u.paginaFim;
                  return (
                    <button
                      key={u.numero}
                      onClick={() => handlePageChange(u.paginaInicio)}
                      className={`w-full text-left p-3 rounded-xl transition-all cursor-pointer flex flex-col gap-1 border ${
                        isActive
                          ? darkMode
                            ? 'bg-blue-900/40 border-blue-500/50 text-white shadow-sm'
                            : 'bg-white border-blue-400 text-blue-950 shadow-sm ring-1 ring-blue-400'
                          : darkMode
                          ? 'bg-slate-800/40 border-slate-700/60 hover:bg-slate-700/50 text-slate-300'
                          : 'bg-white/80 border-slate-200/80 hover:bg-white text-slate-700 hover:border-slate-300'
                      }`}
                    >
                      <div className="flex items-center justify-between gap-1">
                        <span className="text-xs font-bold leading-tight line-clamp-1">
                          {u.titulo}
                        </span>
                        <span
                          className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${
                            isActive
                              ? 'bg-blue-600 text-white'
                              : darkMode
                              ? 'bg-slate-700 text-slate-300'
                              : 'bg-slate-100 text-slate-600'
                          }`}
                        >
                          Pág. {u.paginaInicio}
                        </span>
                      </div>
                      <p
                        className={`text-[11px] line-clamp-2 leading-relaxed ${
                          darkMode ? 'text-slate-400' : 'text-slate-500'
                        }`}
                      >
                        {u.descricao}
                      </p>
                      {u.conceitos && u.conceitos.length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-1">
                          {u.conceitos.slice(0, 3).map((c, ci) => (
                            <span
                              key={ci}
                              className={`text-[9px] px-1.5 py-0.2 rounded font-medium ${
                                darkMode
                                  ? 'bg-slate-700/80 text-slate-300'
                                  : 'bg-slate-100 text-slate-600'
                              }`}
                            >
                              {c}
                            </span>
                          ))}
                        </div>
                      )}
                    </button>
                  );
                }))}
              </div>
            </aside>
          )}

          {/* Área Central: Iframe Embutido do PDF */}
          <main
            className={`flex-1 flex flex-col min-w-0 h-full relative ${
              darkMode ? 'bg-slate-950' : 'bg-slate-100'
            }`}
          >
            {/* Visualizador de PDF via Iframe Nativo com Toolbar e Navegação */}
            <iframe
              ref={iframeRef}
              key={`${book.pdfUrl}-${currentPage}-${zoom}`}
              src={pdfUrlWithParams}
              title={`Leitor do ${book.titulo}`}
              className="w-full h-full border-0 bg-transparent"
            />

            {/* Aviso de Apoio e Fallback caso o navegador não renderize iframe de PDF */}
            <noscript>
              <div className="p-6 text-center">
                <p className="text-sm">O teu navegador não suporta visualização embutida de PDFs.</p>
                <a
                  href={book.pdfUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="mt-2 inline-block px-4 py-2 bg-blue-600 text-white rounded-lg text-xs font-semibold"
                >
                  Abrir PDF numa nova aba
                </a>
              </div>
            </noscript>
          </main>
        </div>

        {/* Barra Inferior de Navegação de Páginas */}
        <footer
          className={`px-4 py-2.5 flex items-center justify-between gap-3 border-t shrink-0 ${
            darkMode
              ? 'bg-slate-800/90 border-slate-700'
              : 'bg-slate-50/90 border-slate-200'
          }`}
        >
          {/* Navegação Rápida Anterior / Próxima */}
          <div className="flex items-center gap-1 sm:gap-2">
            <button
              onClick={handlePrevPage}
              disabled={currentPage <= 1}
              className={`px-2.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1 transition-colors disabled:opacity-40 cursor-pointer ${
                darkMode
                  ? 'bg-slate-700 hover:bg-slate-600 text-slate-200'
                  : 'bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 shadow-sm'
              }`}
            >
              <ChevronLeft className="w-4 h-4" />
              <span className="hidden sm:inline">Anterior</span>
            </button>

            {/* Input de Página */}
            <form onSubmit={handlePageInputSubmit} className="flex items-center gap-1.5">
              <span className={`text-xs ${darkMode ? 'text-slate-400' : 'text-slate-500'}`}>
                Página
              </span>
              <input
                type="number"
                min="1"
                max={totalPages}
                value={pageInput}
                onChange={(e) => setPageInput(e.target.value)}
                onBlur={handlePageInputSubmit}
                className={`w-14 px-2 py-1 text-center text-xs font-bold rounded-lg border outline-none ${
                  darkMode
                    ? 'bg-slate-900 border-slate-600 text-white focus:border-blue-500'
                    : 'bg-white border-slate-300 text-slate-800 focus:border-blue-500'
                }`}
              />
              <span className={`text-xs ${darkMode ? 'text-slate-400' : 'text-slate-500'}`}>
                de {totalPages}
              </span>
            </form>

            <button
              onClick={handleNextPage}
              disabled={currentPage >= totalPages}
              className={`px-2.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1 transition-colors disabled:opacity-40 cursor-pointer ${
                darkMode
                  ? 'bg-slate-700 hover:bg-slate-600 text-slate-200'
                  : 'bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 shadow-sm'
              }`}
            >
              <span className="hidden sm:inline">Seguinte</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          {/* Dica de Leitura e Unidade Atual */}
          <div className="hidden sm:flex items-center gap-2 text-xs">
            <span
              className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-lg ${
                darkMode ? 'bg-slate-700/60 text-slate-300' : 'bg-white text-slate-600 border border-slate-200'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-500" />
              <span>Dica: Podes usar as setas do teclado ← e → para folhear</span>
            </span>
          </div>

          {/* Ações Rápidas à Direita */}
          <div className="flex items-center gap-2">
            <a
              href={book.pdfUrl}
              target="_blank"
              rel="noopener noreferrer"
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors ${
                darkMode
                  ? 'bg-slate-700 hover:bg-slate-600 text-slate-200'
                  : 'bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 shadow-sm'
              }`}
            >
              <FileText className="w-3.5 h-3.5 text-blue-600" />
              <span>Ver PDF</span>
            </a>
          </div>
        </footer>
      </div>
    </div>
  );
}
