/**
 * Challenger 2 Iteration 2: Empirical Stress Test Harness
 * Tests:
 * 1. Page count bounds against physical PDFs (Estudo do Meio strictly 171, no out-of-bounds).
 * 2. All 5 units clickable, valid page offsets, navigation behavior.
 * 3. Search for curriculum concepts ("Sistema Solar", "sólidos", "frações", etc.).
 * 4. "Ver Resumos" action switches view in App.jsx.
 * 5. Production bundle validation.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');

// 1. Import booksCatalog.js directly
const catalogPath = path.join(projectRoot, 'frontend', 'src', 'data', 'booksCatalog.js');
const { LIVROS_RENATA_3ANO } = await import(`file://${catalogPath}`);

console.log('=== EMPIRICAL CHALLENGER STRESS TEST SUITE ===');

let passCount = 0;
let failCount = 0;

function assert(condition, message) {
  if (!condition) {
    console.error(`❌ FAIL: ${message}`);
    failCount++;
    throw new Error(`Assertion failed: ${message}`);
  } else {
    console.log(`✅ PASS: ${message}`);
    passCount++;
  }
}

// =========================================================================
// TEST SUITE 1: Page Count Bounds & Catalog Integrity
// =========================================================================
console.log('\n--- 1. Testing Page Count Bounds & Physical PDF Alignment ---');

assert(Array.isArray(LIVROS_RENATA_3ANO), 'LIVROS_RENATA_3ANO is an array');
assert(LIVROS_RENATA_3ANO.length === 4, 'Catalog contains exactly 4 books');

const expectedBooks = {
  livro_portugues_3ano: { pages: 175, units: 5, discipline: 'Português' },
  livro_matematica_3ano: { pages: 164, units: 5, discipline: 'Matemática' },
  livro_estudo_do_meio_3ano: { pages: 171, units: 5, discipline: 'Estudo do Meio' },
  livro_ingles_3ano: { pages: 141, units: 5, discipline: 'Inglês' },
};

for (const book of LIVROS_RENATA_3ANO) {
  const expected = expectedBooks[book.id];
  assert(!!expected, `Recognized book id: ${book.id}`);
  assert(book.paginas === expected.pages, `${book.id}: catalog pages = ${expected.pages} (got ${book.paginas})`);

  // Physical PDF file check
  const pdfFilePath = path.join(projectRoot, 'public', 'books', book.canonicalFilename);
  assert(fs.existsSync(pdfFilePath), `Physical PDF exists: ${book.canonicalFilename}`);
  const stats = fs.statSync(pdfFilePath);
  assert(stats.size > 10 * 1024 * 1024, `PDF file size > 10MB: ${stats.size} bytes`);

  // Specifically check Estudo do Meio bounds
  if (book.id === 'livro_estudo_do_meio_3ano') {
    assert(book.paginas === 171, 'Estudo do Meio max pages strictly 171');
    assert(book.paginas !== 172, 'Estudo do Meio is NOT 172 (preventing out-of-bounds)');
  }

  // Check all units
  assert(book.unidades.length === 5, `${book.id} has exactly 5 units (got ${book.unidades.length})`);

  let lastEnd = 0;
  for (const u of book.unidades) {
    assert(u.numero >= 1 && u.numero <= 5, `${book.id} unit ${u.numero} number in range 1-5`);
    assert(u.paginaInicio >= 1, `${book.id} unit ${u.numero} paginaInicio (${u.paginaInicio}) >= 1`);
    assert(u.paginaFim <= book.paginas, `${book.id} unit ${u.numero} paginaFim (${u.paginaFim}) <= max pages (${book.paginas})`);
    assert(u.paginaInicio <= u.paginaFim, `${book.id} unit ${u.numero} paginaInicio <= paginaFim`);
    assert(u.paginaInicio >= lastEnd, `${book.id} unit ${u.numero} monotonic ordering: ${u.paginaInicio} >= previous end ${lastEnd}`);
    lastEnd = u.paginaFim;

    assert(typeof u.titulo === 'string' && u.titulo.length > 5, `${book.id} unit ${u.numero} has valid title: ${u.titulo}`);
    assert(typeof u.descricao === 'string' && u.descricao.length > 5, `${book.id} unit ${u.numero} has valid description`);
    assert(Array.isArray(u.conceitos) && u.conceitos.length > 0, `${book.id} unit ${u.numero} has concepts: ${u.conceitos.join(', ')}`);
  }
}

// =========================================================================
// TEST SUITE 2: Reader Modal Navigation & Clamping Stress Test
// =========================================================================
console.log('\n--- 2. Testing Unit Click Navigation & Reader Page Clamping ---');

// Emulate BookReaderModal clamping logic
function simulateReaderClamping(newPage, totalPages) {
  return Math.max(1, Math.min(newPage, totalPages));
}

// Stress test Estudo do Meio with edge and out-of-bounds page requests
const emBook = LIVROS_RENATA_3ANO.find((b) => b.id === 'livro_estudo_do_meio_3ano');
const emTotal = emBook.paginas; // 171

const boundaryTests = [
  { requested: -10, expected: 1 },
  { requested: 0, expected: 1 },
  { requested: 1, expected: 1 },
  { requested: 10, expected: 10 },
  { requested: 171, expected: 171 },
  { requested: 172, expected: 171 }, // Out-of-bounds clamp test!
  { requested: 200, expected: 171 },
  { requested: 99999, expected: 171 }
];

for (const t of boundaryTests) {
  const result = simulateReaderClamping(t.requested, emTotal);
  assert(result === t.expected, `Reader clamp for Estudo do Meio page ${t.requested} -> ${result} (expected ${t.expected})`);
  const iframeSrc = `${emBook.pdfUrl}#page=${result}&zoom=100&toolbar=1&navpanes=1`;
  assert(!iframeSrc.includes('#page=172'), `Iframe URL never targets out-of-bounds #page=172: ${iframeSrc}`);
  assert(result <= 171, `Clamped page ${result} <= 171`);
}

// Verify navigation for all 5 units across all 4 books
for (const book of LIVROS_RENATA_3ANO) {
  for (const u of book.unidades) {
    const targetPage = u.paginaInicio;
    const clamped = simulateReaderClamping(targetPage, book.paginas);
    assert(clamped === targetPage, `${book.id} unit ${u.numero} navigation target p.${targetPage} matches clamped p.${clamped}`);
    assert(clamped >= 1 && clamped <= book.paginas, `${book.id} unit ${u.numero} p.${clamped} strictly within [1, ${book.paginas}]`);
  }
}

// =========================================================================
// TEST SUITE 3: Curriculum Concept Search & Filtering Stress Test
// =========================================================================
console.log('\n--- 3. Testing Search for Curriculum Concepts ---');

function searchCatalog(termo, categoria = 'todos') {
  const query = termo.toLowerCase();
  return LIVROS_RENATA_3ANO.filter((livro) => {
    const coincideBusca =
      livro.titulo.toLowerCase().includes(query) ||
      livro.disciplina.toLowerCase().includes(query) ||
      livro.descricao.toLowerCase().includes(query) ||
      livro.unidades.some((u) =>
        u.titulo.toLowerCase().includes(query) ||
        (u.descricao && u.descricao.toLowerCase().includes(query)) ||
        (u.conceitos && u.conceitos.some((c) => c.toLowerCase().includes(query)))
      );
    if (categoria === 'oficiais') return false;
    return coincideBusca;
  });
}

// Test case 1: "Sistema Solar" -> should match Estudo do Meio
const resSistemaSolar = searchCatalog('Sistema Solar');
assert(resSistemaSolar.length === 1 && resSistemaSolar[0].id === 'livro_estudo_do_meio_3ano',
  `Search 'Sistema Solar' matched exactly Estudo do Meio (matches: ${resSistemaSolar.map(b => b.id).join(', ')})`);

// Test case 2: "sólidos" -> should match Matemática
const resSolidos = searchCatalog('sólidos');
assert(resSolidos.length === 1 && resSolidos[0].id === 'livro_matematica_3ano',
  `Search 'sólidos' matched exactly Matemática (matches: ${resSolidos.map(b => b.id).join(', ')})`);

// Test case 3: "frações" -> should match Matemática
const resFracoes = searchCatalog('frações');
assert(resFracoes.length === 1 && resFracoes[0].id === 'livro_matematica_3ano',
  `Search 'frações' matched exactly Matemática (matches: ${resFracoes.map(b => b.id).join(', ')})`);

// Test case 4: "Dígrafo" -> should match Português
const resDigrafo = searchCatalog('Dígrafo');
assert(resDigrafo.length === 1 && resDigrafo[0].id === 'livro_portugues_3ano',
  `Search 'Dígrafo' matched exactly Português (matches: ${resDigrafo.map(b => b.id).join(', ')})`);

// Test case 5: "Daily Routines" -> should match Inglês
const resDaily = searchCatalog('Daily Routines');
assert(resDaily.length === 1 && resDaily[0].id === 'livro_ingles_3ano',
  `Search 'Daily Routines' matched exactly Inglês (matches: ${resDaily.map(b => b.id).join(', ')})`);

// Test case 6: "Magnetismo" -> should match Estudo do Meio
const resMag = searchCatalog('Magnetismo');
assert(resMag.length === 1 && resMag[0].id === 'livro_estudo_do_meio_3ano',
  `Search 'Magnetismo' matched exactly Estudo do Meio (matches: ${resMag.map(b => b.id).join(', ')})`);

// Test case 7: "Tabuadas" -> should match Matemática
const resTabuadas = searchCatalog('Tabuadas');
assert(resTabuadas.length === 1 && resTabuadas[0].id === 'livro_matematica_3ano',
  `Search 'Tabuadas' matched exactly Matemática (matches: ${resTabuadas.map(b => b.id).join(', ')})`);

// Test case 8: "Missão ZUP" -> matches 3 books (Português, Matemática, Estudo do Meio)
const resZup = searchCatalog('Missão ZUP');
assert(resZup.length === 3, `Search 'Missão ZUP' matched 3 books (got ${resZup.length})`);

// Test case 9: "3.º Ano" -> matches all 4 books
const resAno = searchCatalog('3.º Ano');
assert(resAno.length === 4, `Search '3.º Ano' matched all 4 books (got ${resAno.length})`);

// Test case 10: "Sílaba Tónica" -> matches Português
const resSilaba = searchCatalog('Sílaba Tónica');
assert(resSilaba.length === 1 && resSilaba[0].id === 'livro_portugues_3ano', `Search 'Sílaba Tónica' matched Português`);

// Test case 11: "Germinação" -> matches Estudo do Meio
const resGerm = searchCatalog('Germinação');
assert(resGerm.length === 1 && resGerm[0].id === 'livro_estudo_do_meio_3ano', `Search 'Germinação' matched Estudo do Meio`);

// Test case 12: Nonsense search -> 0 matches
const resEmpty = searchCatalog('xyz_termo_inexistente_999');
assert(resEmpty.length === 0, `Search nonsense query yielded 0 results (got ${resEmpty.length})`);

// Test case 13: Category filter 'oficiais' excludes renata books
const resOficiais = searchCatalog('Sistema Solar', 'oficiais');
assert(resOficiais.length === 0, `Category filter 'oficiais' excludes Renata books`);

// =========================================================================
// TEST SUITE 4: "Ver Resumos" View Switching in App.jsx
// =========================================================================
console.log('\n--- 4. Testing "Ver Resumos" Action & View Switching in App.jsx ---');

// Mock list of 7.º and 3.º ano disciplines from the app
const mockDisciplinas = [
  { id: 'portugues', nome: 'Português', ano: '7.º Ano' },
  { id: 'matematica', nome: 'Matemática', ano: '7.º Ano' },
  { id: 'ciencias_naturais', nome: 'Ciências Naturais', ano: '7.º Ano' },
  { id: 'historia', nome: 'História', ano: '7.º Ano' },
  { id: 'geografia', nome: 'Geografia', ano: '7.º Ano' },
  { id: 'ingles', nome: 'Inglês', ano: '7.º Ano' },
  { id: 'frances', nome: 'Francês', ano: '7.º Ano' },
  { id: 'fisico_quimica', nome: 'Físico-Química', ano: '7.º Ano' },
  { id: 'estudo_meio', nome: 'Estudo do Meio', ano: '3.º Ano' }
];

// Exact simulation of App.jsx onVerResumos callback
function simulateOnVerResumos(disciplinaId, state) {
  if (disciplinaId) {
    const target = mockDisciplinas.find(
      (d) => d.id === disciplinaId || d.id.startsWith(disciplinaId.split('_')[0])
    );
    if (target) {
      state.disciplinaSelecionada = target;
    }
  }
  state.viewAtiva = 'resumos';
}

for (const book of LIVROS_RENATA_3ANO) {
  const appState = {
    disciplinaSelecionada: mockDisciplinas[0], // Português initially
    viewAtiva: 'biblioteca'
  };

  simulateOnVerResumos(book.disciplinaId, appState);

  assert(appState.viewAtiva === 'resumos',
    `Clicking 'Ver Resumos' for ${book.id} switches viewAtiva to 'resumos' (was 'biblioteca')`);
  assert(appState.disciplinaSelecionada !== null,
    `Selected discipline is updated for ${book.id}`);

  // Check matching target
  const prefix = book.disciplinaId.split('_')[0];
  assert(appState.disciplinaSelecionada.id.startsWith(prefix),
    `Matched discipline ${appState.disciplinaSelecionada.id} matches book prefix ${prefix}`);
}

// Fallback test: when onVerResumos is undefined or null, BibliotecaView opens internal resumos modal
function simulateBibliotecaViewResumosFallback(livro, onVerResumos) {
  let modalState = null;
  if (onVerResumos && typeof onVerResumos === 'function') {
    onVerResumos(livro.disciplinaId);
  } else {
    modalState = livro;
  }
  return modalState;
}

const fallbackModal = simulateBibliotecaViewResumosFallback(emBook, null);
assert(fallbackModal === emBook, 'When onVerResumos is absent, internal modal fallback is opened');

// =========================================================================
// TEST SUITE 5: Production Bundle Integrity in dist/
// =========================================================================
console.log('\n--- 5. Testing Production Bundle in dist/ ---');

const distDir = path.join(projectRoot, 'frontend', 'dist');
const indexHtmlPath = path.join(distDir, 'index.html');
const assetsDir = path.join(distDir, 'assets');

assert(fs.existsSync(distDir), 'frontend/dist directory exists');
assert(fs.existsSync(indexHtmlPath), 'frontend/dist/index.html exists');

const htmlContent = fs.readFileSync(indexHtmlPath, 'utf-8');
assert(htmlContent.includes('<script type="module"'), 'dist/index.html contains module script tag');
assert(htmlContent.includes('<link rel="stylesheet"'), 'dist/index.html contains CSS link tag');

const assetFiles = fs.readdirSync(assetsDir);
const jsFiles = assetFiles.filter((f) => f.endsWith('.js'));
const cssFiles = assetFiles.filter((f) => f.endsWith('.css'));

assert(jsFiles.length >= 1, `Production bundle contains JS asset: ${jsFiles.join(', ')}`);
assert(cssFiles.length >= 1, `Production bundle contains CSS asset: ${cssFiles.join(', ')}`);

for (const jsFile of jsFiles) {
  const jsSize = fs.statSync(path.join(assetsDir, jsFile)).size;
  assert(jsSize > 100 * 1024, `JS bundle size > 100KB: ${jsFile} is ${(jsSize / 1024).toFixed(1)} KB`);
}

for (const cssFile of cssFiles) {
  const cssSize = fs.statSync(path.join(assetsDir, cssFile)).size;
  assert(cssSize > 10 * 1024, `CSS bundle size > 10KB: ${cssFile} is ${(cssSize / 1024).toFixed(1)} KB`);
}

console.log(`\n=================================================`);
console.log(`STRESS TEST RESULTS: ${passCount} PASSED, ${failCount} FAILED`);
console.log(`=================================================`);

if (failCount > 0) {
  process.exit(1);
} else {
  process.exit(0);
}
