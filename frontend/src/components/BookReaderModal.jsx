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
  Layers,
  Sparkles,
  Bookmark,
  Sun,
  Moon,
  Loader2,
  AlertCircle,
  RotateCw
} from 'lucide-react';
import * as pdfjsLib from 'pdfjs-dist';
import pdfWorkerUrl from 'pdfjs-dist/build/pdf.worker.min.mjs?url';

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfWorkerUrl;

const RANGE_CHUNK_SIZE = 262144; // 256 KB por bloco HTTP Range

class HttpRangePdfTransport extends pdfjsLib.PDFDataRangeTransport {
  constructor(length, initialData, url) {
    super(length, initialData);
    this.url = url;
    this.controllers = new Set();
  }

  requestDataRange(begin, end) {
    const controller = new AbortController();
    this.controllers.add(controller);
    const inclusiveEnd = Math.max(begin, end - 1);

    fetch(this.url, {
      headers: { Range: `bytes=${begin}-${inclusiveEnd}` },
      signal: controller.signal
    })
      .then((res) => {
        if (!res.ok && res.status !== 206) {
          throw new Error(`Falha HTTP ${res.status} ao carregar bloco do PDF`);
        }
        return res.arrayBuffer();
      })
      .then((buffer) => {
        this.controllers.delete(controller);
        this.onDataRange(begin, new Uint8Array(buffer));
      })
      .catch((err) => {
        this.controllers.delete(controller);
        if (err.name !== 'AbortError') {
          console.error('Erro ao obter intervalo de bytes do PDF:', err);
        }
      });
  }

  abort() {
    for (const c of this.controllers) {
      c.abort();
    }
    this.controllers.clear();
    super.abort();
  }
}

async function abrirDocumentoPdfComRange(pdfUrl, canonicalFilename, signal) {
  let activeUrl = pdfUrl;

  const fazerPedidoInicial = async (urlAlvo) => {
    const resp = await fetch(urlAlvo, {
      headers: { Range: `bytes=0-${RANGE_CHUNK_SIZE - 1}` },
      signal
    });
    if (!resp.ok && resp.status !== 206) {
      throw new Error(`HTTP ${resp.status}`);
    }
    const buf = await resp.arrayBuffer();
    return { resp, bytes: new Uint8Array(buf) };
  };

  let { resp, bytes } = await fazerPedidoInicial(activeUrl);

  // Em ambiente local Windows onde /books pode ser um symlink de texto (18 bytes),
  // fazemos fallback automático para o endpoint /api/pdf-proxy do backend FastAPI
  const isPdfHeader =
    bytes.byteLength > 100 &&
    bytes[0] === 0x25 && // %
    bytes[1] === 0x50 && // P
    bytes[2] === 0x44 && // D
    bytes[3] === 0x46;   // F

  if (!isPdfHeader && !activeUrl.startsWith('/api/pdf-proxy')) {
    const fallbackName = canonicalFilename || activeUrl.split('/').pop().split('#')[0];
    activeUrl = `/api/pdf-proxy?file=${encodeURIComponent(fallbackName)}`;
    const retry = await fazerPedidoInicial(activeUrl);
    resp = retry.resp;
    bytes = retry.bytes;
  }

  const contentRange = resp.headers.get('Content-Range') || resp.headers.get('content-range') || '';
  let totalLength = 0;
  if (contentRange.includes('/')) {
    const parsedTotal = parseInt(contentRange.split('/').pop().trim(), 10);
    if (!isNaN(parsedTotal) && parsedTotal > 0) {
      totalLength = parsedTotal;
    }
  }

  if (resp.status === 206 && totalLength > bytes.byteLength) {
    const transport = new HttpRangePdfTransport(totalLength, bytes, activeUrl);
    const loadingTask = pdfjsLib.getDocument({
      range: transport,
      length: totalLength,
      rangeChunkSize: RANGE_CHUNK_SIZE,
      disableAutoFetch: true,
      disableStream: true
    });
    return { loadingTask, transport };
  }

  // Caso o servidor tenha devolvido o ficheiro completo (200 OK ou ficheiro pequeno)
  const loadingTask = pdfjsLib.getDocument({
    data: bytes
  });
  return { loadingTask, transport: null };
}

export default function BookReaderModal({
  isOpen,
  onClose,
  book,
  initialPage = 1
}) {
  const [numPages, setNumPages] = useState(book?.paginas || 175);
  const [currentPage, setCurrentPage] = useState(initialPage || 1);
  const [pageInput, setPageInput] = useState(String(initialPage || 1));
  const [zoom, setZoom] = useState(100);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const [loadingDoc, setLoadingDoc] = useState(false);
  const [renderingPage, setRenderingPage] = useState(false);
  const [docError, setDocError] = useState(null);
  const [reloadCounter, setReloadCounter] = useState(0);

  const modalRef = useRef(null);
  const canvasRef = useRef(null);
  const viewportContainerRef = useRef(null);
  const pdfDocRef = useRef(null);
  const renderTaskRef = useRef(null);

  const totalPages = numPages || book?.paginas || 175;

  const handlePageChange = useCallback(
    (newPage) => {
      const clamped = Math.max(1, Math.min(newPage, totalPages));
      setCurrentPage(clamped);
      setPageInput(String(clamped));
      if (viewportContainerRef.current) {
        viewportContainerRef.current.scrollTop = 0;
      }
    },
    [totalPages]
  );

  const handlePrevPage = useCallback(() => {
    setCurrentPage((prev) => {
      const next = Math.max(1, prev - 1);
      setPageInput(String(next));
      return next;
    });
    if (viewportContainerRef.current) {
      viewportContainerRef.current.scrollTop = 0;
    }
  }, []);

  const handleNextPage = useCallback(() => {
    setCurrentPage((prev) => {
      const next = Math.min(totalPages, prev + 1);
      setPageInput(String(next));
      return next;
    });
    if (viewportContainerRef.current) {
      viewportContainerRef.current.scrollTop = 0;
    }
  }, [totalPages]);

  const [prevBookKey, setPrevBookKey] = useState(
    book?.id ? `${book.id}-${initialPage}` : ''
  );
  const currentBookKey = book?.id ? `${book.id}-${initialPage}` : '';
  if (currentBookKey !== prevBookKey) {
    setPrevBookKey(currentBookKey);
    const startPage = Math.max(1, Math.min(initialPage || 1, book?.paginas || 999));
    setCurrentPage(startPage);
    setPageInput(String(startPage));
    setNumPages(book?.paginas || 175);
  }

  // Carregar o documento PDF em memória via PDF.js + HTTP Range (nunca dispara download no browser)
  useEffect(() => {
    if (!isOpen || !book?.pdfUrl) return;

    let cancelled = false;
    const abortController = new AbortController();
    let activeTransport = null;
    let activeLoadingTask = null;

    setLoadingDoc(true);
    setDocError(null);
    pdfDocRef.current = null;

    abrirDocumentoPdfComRange(book.pdfUrl, book.canonicalFilename, abortController.signal)
      .then(({ loadingTask, transport }) => {
        activeLoadingTask = loadingTask;
        activeTransport = transport;
        return loadingTask.promise;
      })
      .then((pdfDoc) => {
        if (cancelled) {
          pdfDoc.destroy();
          return;
        }
        pdfDocRef.current = pdfDoc;
        const realPages = pdfDoc.numPages || book.paginas || 1;
        setNumPages(realPages);
        setCurrentPage((prev) => {
          const clamped = Math.max(1, Math.min(prev, realPages));
          setPageInput(String(clamped));
          return clamped;
        });
        setLoadingDoc(false);
      })
      .catch((err) => {
        if (cancelled || err?.name === 'AbortError') return;
        console.error('Erro ao carregar PDF no leitor integrado:', err);
        setDocError('Não foi possível carregar a visualização rápida deste manual.');
        setLoadingDoc(false);
      });

    return () => {
      cancelled = true;
      abortController.abort();
      if (renderTaskRef.current) {
        try {
          renderTaskRef.current.cancel();
        } catch {
          // Ignorar cancelamento
        }
      }
      if (activeTransport) {
        try {
          activeTransport.abort();
        } catch {
          // Ignorar
        }
      }
      if (activeLoadingTask) {
        try {
          activeLoadingTask.destroy();
        } catch {
          // Ignorar
        }
      }
      if (pdfDocRef.current) {
        try {
          pdfDocRef.current.destroy();
        } catch {
          // Ignorar
        }
        pdfDocRef.current = null;
      }
    };
  }, [isOpen, book?.pdfUrl, book?.canonicalFilename, book?.paginas, reloadCounter]);

  // Desenhar a página atual no elemento <canvas> sempre que currentPage ou zoom mudarem
  useEffect(() => {
    if (!isOpen || loadingDoc || !pdfDocRef.current || !canvasRef.current) return;

    let cancelled = false;
    const pdfDoc = pdfDocRef.current;
    const pageNumber = Math.max(1, Math.min(currentPage, pdfDoc.numPages || totalPages));

    setRenderingPage(true);

    if (renderTaskRef.current) {
      try {
        renderTaskRef.current.cancel();
      } catch {
        // Ignorar
      }
    }

    pdfDoc
      .getPage(pageNumber)
      .then((page) => {
        if (cancelled || !canvasRef.current) return;

        const baseScale = 1.35 * (zoom / 100);
        const viewport = page.getViewport({ scale: baseScale });
        const outputScale = window.devicePixelRatio || 1;

        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');

        canvas.width = Math.floor(viewport.width * outputScale);
        canvas.height = Math.floor(viewport.height * outputScale);
        canvas.style.width = `${Math.floor(viewport.width)}px`;
        canvas.style.height = `${Math.floor(viewport.height)}px`;

        const transform =
          outputScale !== 1 ? [outputScale, 0, 0, outputScale, 0, 0] : null;

        const renderContext = {
          canvasContext: context,
          transform,
          viewport
        };

        const renderTask = page.render(renderContext);
        renderTaskRef.current = renderTask;
        return renderTask.promise;
      })
      .then(() => {
        if (!cancelled) {
          setRenderingPage(false);
        }
      })
      .catch((err) => {
        if (cancelled || err?.name === 'RenderingCancelledException') return;
        console.error('Erro ao desenhar página do PDF:', err);
        setRenderingPage(false);
      });

    return () => {
      cancelled = true;
      if (renderTaskRef.current) {
        try {
          renderTaskRef.current.cancel();
        } catch {
          // Ignorar
        }
      }
    };
  }, [isOpen, loadingDoc, currentPage, zoom, totalPages]);

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

  const temUnidades = Array.isArray(book.unidades) && book.unidades.length > 0;
  const downloadHref = book.downloadUrl || book.pdfUrl;

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
                  Leitor Web PDF.js ⚡
                </span>
              </div>
              <p
                className={`text-xs truncate ${
                  darkMode ? 'text-slate-400' : 'text-slate-500'
                }`}
              >
                {book.editora || 'Porto Editora'} • {book.tamanhoFormatado || 'PDF Digital'} • {totalPages} páginas
              </p>
            </div>
          </div>

          {/* Ferramentas do Leitor */}
          <div className="flex items-center gap-1 sm:gap-2 shrink-0">
            {/* Seletor de Capítulos / Sidebar Toggle */}
            {temUnidades && (
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
            )}

            {/* Controlo de Zoom */}
            <div
              className={`flex items-center rounded-xl p-0.5 border ${
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

            {/* Descarregar PDF (único botão que efetua download explícito) */}
            <a
              href={downloadHref}
              download={book.canonicalFilename || 'livro.pdf'}
              target="_blank"
              rel="noopener noreferrer"
              className="px-3 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold flex items-center gap-1.5 transition-all shadow-sm cursor-pointer"
              title="Descarregar ficheiro PDF completo para o teu computador"
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

        {/* Corpo Principal: Sidebar de Capítulos + Visor Canvas PDF.js */}
        <div className="flex-1 flex overflow-hidden min-h-0 relative">
          {/* Sidebar / Gaveta de Unidades Curriculares */}
          {temUnidades && sidebarOpen && (
            <aside
              className={`w-64 sm:w-80 shrink-0 border-r flex flex-col overflow-y-auto transition-all ${
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
                {book.unidades?.map((u) => {
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
                          className={`text-[10px] font-semibold px-1.5 py-0.5 rounded shrink-0 ${
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
                })}
              </div>
            </aside>
          )}

          {/* Área Central: Visor Canvas Embutido do PDF */}
          <main
            ref={viewportContainerRef}
            className={`flex-1 flex flex-col items-center overflow-auto min-w-0 h-full relative p-3 sm:p-6 ${
              darkMode ? 'bg-slate-950' : 'bg-slate-200/70'
            }`}
          >
            {loadingDoc && (
              <div className="m-auto flex flex-col items-center justify-center gap-3 p-8 text-center">
                <Loader2 className="w-10 h-10 text-blue-600 animate-spin" />
                <div>
                  <p className="text-sm font-bold">
                    A abrir {book.titulo} no leitor do browser...
                  </p>
                  <p className="text-xs opacity-70 mt-1">
                    Carregamento inteligente página a página (Fast Web View) sem descarregar o ficheiro
                  </p>
                </div>
              </div>
            )}

            {!loadingDoc && docError && (
              <div className="m-auto max-w-md bg-white dark:bg-slate-800 rounded-2xl p-6 border border-red-200 dark:border-red-900/50 shadow-lg text-center flex flex-col items-center gap-3">
                <AlertCircle className="w-10 h-10 text-red-500" />
                <h4 className="text-sm font-bold">{docError}</h4>
                <p className="text-xs opacity-75">
                  Podes tentar recarregar a página no leitor ou transferir o PDF diretamente.
                </p>
                <div className="flex items-center gap-2 mt-1">
                  <button
                    onClick={() => setReloadCounter((c) => c + 1)}
                    className="px-3.5 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold flex items-center gap-1.5 cursor-pointer"
                  >
                    <RotateCw className="w-3.5 h-3.5" />
                    <span>Tentar Novamente</span>
                  </button>
                  <a
                    href={downloadHref}
                    download={book.canonicalFilename || 'livro.pdf'}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold flex items-center gap-1.5"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>Descarregar PDF</span>
                  </a>
                </div>
              </div>
            )}

            {!loadingDoc && !docError && (
              <div className="relative my-auto flex items-center justify-center">
                {renderingPage && (
                  <div className="absolute top-3 right-3 z-10 px-2.5 py-1 rounded-full bg-slate-900/75 text-white text-[11px] font-semibold flex items-center gap-1.5 backdrop-blur-xs shadow-sm">
                    <Loader2 className="w-3 h-3 animate-spin text-blue-400" />
                    <span>A desenhar pág. {currentPage}...</span>
                  </div>
                )}
                <canvas
                  ref={canvasRef}
                  className="bg-white shadow-xl rounded-lg border border-slate-300 dark:border-slate-700 transition-opacity"
                />
              </div>
            )}
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
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1 transition-colors disabled:opacity-40 cursor-pointer ${
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
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1 transition-colors disabled:opacity-40 cursor-pointer ${
                darkMode
                  ? 'bg-slate-700 hover:bg-slate-600 text-slate-200'
                  : 'bg-white hover:bg-slate-100 text-slate-700 border border-slate-200 shadow-sm'
              }`}
            >
              <span className="hidden sm:inline">Seguinte</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          {/* Dica de Leitura */}
          <div className="hidden sm:flex items-center gap-2 text-xs">
            <span
              className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-lg ${
                darkMode ? 'bg-slate-700/60 text-slate-300' : 'bg-white text-slate-600 border border-slate-200'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-500" />
              <span>Dica: Usa as setas ← e → do teclado para folhear sem sair da página</span>
            </span>
          </div>

          {/* Indicador de Modo Leitura Online */}
          <div className="flex items-center gap-2">
            <span
              className={`px-2.5 py-1 rounded-lg text-[11px] font-semibold ${
                darkMode
                  ? 'bg-emerald-900/40 text-emerald-300 border border-emerald-700/50'
                  : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
              }`}
            >
              Leitura no Browser Ativa
            </span>
          </div>
        </footer>
      </div>
    </div>
  );
}
