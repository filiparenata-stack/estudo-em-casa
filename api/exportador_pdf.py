import os
import io
import re
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable, Image as RLImage
)
from reportlab.pdfgen import canvas

_SUPERSCRIPT_MAP = {
    '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4',
    '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9',
    '⁺': '+', '⁻': '-', '⁼': '=', '⁽': '(', '⁾': ')',
    'ⁿ': 'n', 'ᵐ': 'm', 'ˣ': 'x'
}

_SUBSCRIPT_MAP = {
    '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4',
    '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9',
    '₊': '+', '₋': '-', 'ᵢ': 'i', 'ⱼ': 'j', 'ₐ': 'a', 'ₑ': 'e', 'ₒ': 'o', 'ₓ': 'x'
}

_SUP_REGEX = re.compile("[" + "".join(re.escape(k) for k in _SUPERSCRIPT_MAP.keys()) + "]+")
_SUB_REGEX = re.compile("[" + "".join(re.escape(k) for k in _SUBSCRIPT_MAP.keys()) + "]+")

_SYMBOL_REPLACEMENTS = [
    # Combining marks
    ("x\u0304", "x (media)"),
    ("\u0304", ""),
    # Emojis and variation selectors
    ("\ufe0f", ""),
    ("🎯", "[METAS] "),
    ("📝", "[TESTE] "),
    ("✅", "[RESOLUCAO] "),
    ("📋", "[CRITERIO] "),
    ("⚠️", "[ATENCAO] "),
    ("⚠", "[ATENCAO] "),
    ("⚡", "[DESTAQUE] "),
    ("📌", "[CONCEITOS] "),
    ("💡", "[DICA] "),
    ("🔍", "[PESQUISA] "),
    ("📚", "[ESTUDO] "),
    ("🎴", "[FLASHCARDS] "),
    ("🧪", "[LAB] "),
    ("✓", "[OK]"),
    ("✔", "[OK]"),
    ("✗", "[X]"),
    ("✘", "[X]"),
    # Greek and math symbols
    ("ρ", "d (ro)"),
    ("π", "pi"),
    ("Δ", "Delta"),
    ("η", "eta"),
    ("∑", "Soma"),
    ("√", "raiz"),
    ("∞", "infinito"),
    ("∅", "{ }"),
    ("‰", " por mil"),
    ("×", "x"),
    ("·", "."),
    ("÷", "/"),
    ("≠", "!="),
    ("≈", "~="),
    ("≤", "&lt;="),
    ("≥", "&gt;="),
    ("➔", "-&gt;"),
    ("→", "-&gt;"),
    ("←", "&lt;-"),
    ("↔", "&lt;-&gt;"),
    ("⇒", "=&gt;"),
    ("⇔", "&lt;=&gt;"),
    # Typography
    ("—", "-"),
    ("–", "-"),
    ("−", "-"),
    ("•", "-"),
    ("“", '"'),
    ("”", '"'),
    ("‘", "'"),
    ("’", "'"),
    ("…", "..."),
]

_VALID_TAG_PATTERN = re.compile(
    r"(</?(?:b|i|u|super|sub|sup|br\s*/?|font(?:\s+[^>]*)?)>)",
    flags=re.IGNORECASE
)


def _sanitizar_texto_pdf(texto: str) -> str:
    """
    Sanitiza qualquer string destinada ao ReportLab Paragraph (fonte Helvetica WinAnsi / Latin-1),
    convertendo expoentes/índices Unicode em tags XML (<super>, <sub>), substituindo símbolos
    matemáticos/gregos/emojis e garantindo zero ocorrências do glifo nulo '\\u25a0' ('■').
    """
    if texto is None:
        return ""
    s = str(texto)

    # 1. Converter expoentes e índices Unicode para tags ReportLab <super> e <sub>
    s = _SUP_REGEX.sub(
        lambda m: "<super>" + "".join(_SUPERSCRIPT_MAP[c] for c in m.group(0)) + "</super>",
        s
    )
    s = _SUB_REGEX.sub(
        lambda m: "<sub>" + "".join(_SUBSCRIPT_MAP[c] for c in m.group(0)) + "</sub>",
        s
    )

    # 2. Substituir símbolos matemáticos, gregos e emojis
    for orig, repl in _SYMBOL_REPLACEMENTS:
        if orig in s:
            s = s.replace(orig, repl)

    # 3. Proteger tags XML válidas do ReportLab e escapar '<' / '>' soltos (ex: '<=>')
    partes = _VALID_TAG_PATTERN.split(s)
    partes_limpas = []
    for idx, parte in enumerate(partes):
        if idx % 2 == 1:
            # É uma tag XML válida do ReportLab
            partes_limpas.append(parte)
        else:
            # Escapar '<' e '>' literais que não pertençam a entidades já escapadas
            p = re.sub(r"&(?!(?:lt|gt|amp|quot|apos|#\d+);)", "&amp;", parte)
            p = p.replace("<", "&lt;").replace(">", "&gt;")
            # Rede de segurança final: remover/substituir qualquer caracter fora de Latin-1
            p = p.encode("latin-1", errors="ignore").decode("latin-1")
            partes_limpas.append(p)

    return "".join(partes_limpas)


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        texto = f"Escola Virtual 7.º Ano | Guia de Resumo para Estudo - Pagina {self._pageNumber} de {page_count}"
        self.drawRightString(A4[0] - 40, 25, texto)
        self.restoreState()


class ExportadorPDF:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._configurar_estilos()

    def _P(self, texto, estilo):
        return Paragraph(_sanitizar_texto_pdf(texto), estilo)

    def _configurar_estilos(self):
        self.styles.add(ParagraphStyle(
            name='HeaderDisciplina',
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=12,
            textColor=colors.HexColor('#0284c7'),
            textTransform='uppercase'
        ))
        self.styles.add(ParagraphStyle(
            name='HeaderTitulo',
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=22,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=4
        ))
        self.styles.add(ParagraphStyle(
            name='HeaderSub',
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#475569')
        ))
        self.styles.add(ParagraphStyle(
            name='SecaoTitulo',
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=16,
            textColor=colors.HexColor('#1e293b'),
            spaceBefore=12,
            spaceAfter=6
        ))
        self.styles.add(ParagraphStyle(
            name='SubSecaoTitulo',
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#0369a1'),
            spaceBefore=6,
            spaceAfter=4
        ))
        self.styles.add(ParagraphStyle(
            name='CorpoTexto',
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor('#334155'),
            spaceAfter=4
        ))
        self.styles.add(ParagraphStyle(
            name='ItemBullet',
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor('#1e293b'),
            leftIndent=15,
            spaceAfter=3
        ))
        self.styles.add(ParagraphStyle(
            name='TermoDestaque',
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=13,
            textColor=colors.HexColor('#0284c7')
        ))
        self.styles.add(ParagraphStyle(
            name='LegendaImagem',
            fontName='Helvetica-Oblique',
            fontSize=8.5,
            leading=11.5,
            alignment=1,  # CENTER
            textColor=colors.HexColor('#475569'),
            spaceBefore=3,
            spaceAfter=6
        ))

    def _criar_imagem_pdf(self, base_dir: str, rel_path: str, max_width: float = 440.0, max_height: float = 190.0):
        """
        Resolve o caminho relativo da imagem (ex: /imagens_resumos/01_Fisico_Quimica_7/...)
        e devolve uma instância RLImage redimensionada proporcionalmente e centrada.
        """
        if not rel_path or not isinstance(rel_path, str):
            return None
        clean_rel = rel_path.lstrip("/").replace("/", os.sep)
        caminhos_tentar = [
            os.path.join(base_dir, "frontend", "public", clean_rel),
            os.path.join(base_dir, "public", clean_rel),
        ]
        abs_path = None
        for c in caminhos_tentar:
            if os.path.exists(c) and os.path.isfile(c):
                abs_path = c
                break
        if not abs_path:
            return None

        try:
            with PILImage.open(abs_path) as img:
                orig_w, orig_h = img.size
            if orig_w <= 0 or orig_h <= 0:
                return None
            scale = min(max_width / float(orig_w), max_height / float(orig_h))
            target_w = orig_w * scale
            target_h = orig_h * scale
            rl_img = RLImage(abs_path, width=target_w, height=target_h)
            rl_img.hAlign = 'CENTER'
            return rl_img
        except Exception:
            return None

    def gerar_pdf_resumo(self, resumo_data, output_path=None):
        buffer = io.BytesIO() if output_path is None else output_path
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=40,
            rightMargin=40,
            topMargin=40,
            bottomMargin=45
        )

        elements = []

        # 1. Cabeçalho Visual
        disc = resumo_data.get("disciplina_nome", "7.º Ano")
        periodo = resumo_data.get("periodo", "Geral")
        titulo = resumo_data.get("titulo", "Ficha de Resumo")
        indicacao = resumo_data.get("indicacao_professor", "")

        header_data = [
            [
                self._P(f"<b>{disc.upper()}</b> - {periodo}", self.styles['HeaderDisciplina']),
                self._P("<b>7.º ANO - ENSINO BASICO</b>", self.styles['HeaderDisciplina'])
            ],
            [
                self._P(titulo, self.styles['HeaderTitulo']),
                ""
            ],
            [
                self._P(f"<b>Conteúdos avaliados no teste:</b> {indicacao}", self.styles['HeaderSub']),
                ""
            ]
        ]
        t_header = Table(header_data, colWidths=[380, 135])
        t_header.setStyle(TableStyle([
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        elements.append(t_header)
        elements.append(Spacer(1, 6))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=10))

        # 2. Introdução
        intro = resumo_data.get("introducao", "")
        if intro:
            elements.append(self._P(intro, self.styles['CorpoTexto']))
            elements.append(Spacer(1, 8))

        # 3. Conceitos-Chave (Tabela com fundo suave)
        conceitos = resumo_data.get("conceitos_chave", [])
        if conceitos:
            elements.append(self._P("📌 Conceitos-Chave e Definições Fundamentais", self.styles['SecaoTitulo']))
            t_data = []
            for c in conceitos:
                termo_p = self._P(f"<b>{c.get('termo', '')}</b>", self.styles['TermoDestaque'])
                def_p = self._P(c.get('definicao', ''), self.styles['CorpoTexto'])
                t_data.append([termo_p, def_p])

            t_conc = Table(t_data, colWidths=[140, 375])
            t_conc.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(t_conc)
            elements.append(Spacer(1, 10))

        # 4. Esquemas e Fórmulas (se existirem)
        esquemas = resumo_data.get("esquemas_formulas", [])
        if esquemas:
            elements.append(self._P("⚡ Esquemas, Relações e Regras de Cálculo", self.styles['SecaoTitulo']))
            e_data = []
            for eq in esquemas:
                tit_eq = self._P(f"<b>{eq.get('titulo', '')}</b>", self.styles['TermoDestaque'])
                cont_eq = self._P(eq.get('conteudo', ''), self.styles['CorpoTexto'])
                e_data.append([tit_eq, cont_eq])

            t_eq = Table(e_data, colWidths=[160, 355])
            t_eq.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f0fdf4")),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#bbf7d0")),
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#dcfce7")),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(t_eq)
            elements.append(Spacer(1, 10))

        # 5. Pontos Fundamentais
        pontos = resumo_data.get("pontos_fundamentais", [])
        if pontos:
            elements.append(self._P("📝 Síntese Estruturada dos Conteúdos", self.styles['SecaoTitulo']))
            for sec in pontos:
                elements.append(self._P(sec.get("subtitulo", "Tópico"), self.styles['SubSecaoTitulo']))
                for it in sec.get("itens", []):
                    elements.append(self._P(f"- {it}", self.styles['ItemBullet']))
                elements.append(Spacer(1, 4))

        # 6. Dicas para o Teste
        dicas = resumo_data.get("atencao_no_teste", [])
        if dicas:
            elements.append(Spacer(1, 6))
            elements.append(self._P("⚠️ Atenção no Teste (Erros Frequentes e Recomendações)", self.styles['SecaoTitulo']))
            d_data = []
            for d in dicas:
                d_data.append([self._P(f"⚠️ {d}", self.styles['CorpoTexto'])])
            t_dicas = Table(d_data, colWidths=[515])
            t_dicas.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#fffbeb")),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#fde68a")),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(t_dicas)

        # Construir documento
        doc.build(elements, canvasmaker=NumberedCanvas)

        if output_path is None:
            buffer.seek(0)
            return buffer.getvalue()
        return output_path

    def gerar_pdf_resumo_periodo(self, dados_periodo, output_path=None):
        """
        Gera uma sebenta/dossiê completo em PDF ilustrado para o período selecionado,
        contendo as Metas Curriculares, Teoria Essencial, Esquemas Ilustrados e Questões de Teste resolvidas.
        """
        buffer = io.BytesIO() if output_path is None else output_path
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=35,
            rightMargin=35,
            topMargin=35,
            bottomMargin=40
        )

        elements = []

        disc = dados_periodo.get("disciplina_nome", "7.º Ano")
        periodo = dados_periodo.get("periodo", "1.º Período").replace("_", " ")
        titulo = dados_periodo.get("titulo", f"Dossiê de Estudo - {periodo}")
        metas = dados_periodo.get("metas", [])
        topicos = dados_periodo.get("topicos", [])

        # 1. Cabeçalho de Dossiê
        header_data = [
            [
                self._P(f"<b>ESCOLA VIRTUAL 7.º ANO - {disc.upper()}</b>", self.styles['HeaderDisciplina']),
                self._P(f"<b>{periodo.upper()}</b>", self.styles['HeaderDisciplina'])
            ],
            [
                self._P(titulo, self.styles['HeaderTitulo']),
                ""
            ]
        ]
        t_header = Table(header_data, colWidths=[385, 140])
        t_header.setStyle(TableStyle([
            ('SPAN', (0, 1), (1, 1)),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        elements.append(t_header)
        elements.append(Spacer(1, 4))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#0284c7"), spaceAfter=8))

        # 2. Metas Curriculares Avaliadas
        if metas:
            elements.append(self._P("🎯 Metas Curriculares Oficiais Avaliadas no Período", self.styles['SecaoTitulo']))
            m_data = []
            for m in metas:
                m_data.append([self._P(f"✓ <b>{m}</b>", self.styles['CorpoTexto'])])
            t_metas = Table(m_data, colWidths=[525])
            t_metas.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f0fdf4")),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#86efac")),
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#dcfce7")),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(t_metas)
            elements.append(Spacer(1, 10))

        # Diretório base da aplicação para resolução de imagens locais
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # 3. Tópicos Curriculares
        for idx, topico in enumerate(topicos):
            tit_t = topico.get("titulo", f"Tópico {idx+1}")
            subdom = topico.get("subdominio", "")

            bloco_topico = []
            bloco_topico.append(
                self._P(f"<b>{idx+1}. {tit_t}</b> <font size=8 color='#64748b'>({subdom})</font>", self.styles['SecaoTitulo'])
            )

            # Esquema visual do manual (imagem_manual + legenda)
            img_manual_path = topico.get("imagem_manual")
            rl_img_manual = self._criar_imagem_pdf(base_dir, img_manual_path, max_width=440.0, max_height=190.0)
            if rl_img_manual is not None:
                bloco_topico.append(Spacer(1, 4))
                bloco_topico.append(rl_img_manual)
                legenda = topico.get("imagem_legenda", "")
                if legenda:
                    bloco_topico.append(self._P(f"<i>{legenda}</i>", self.styles['LegendaImagem']))
                else:
                    bloco_topico.append(Spacer(1, 4))

            # Conceitos-chave
            conceitos = topico.get("conceitos_chave", [])
            if conceitos:
                t_conc = []
                for c in conceitos:
                    t_conc.append([
                        self._P(f"<b>{c.get('termo', '')}</b>", self.styles['TermoDestaque']),
                        self._P(c.get('definicao', ''), self.styles['CorpoTexto'])
                    ])
                t_table = Table(t_conc, colWidths=[150, 375])
                t_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                    ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#cbd5e1")),
                    ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ]))
                bloco_topico.append(t_table)
                bloco_topico.append(Spacer(1, 6))

            # Foco no Teste (Questão real de exame + imagem_questao + resolução)
            ft = topico.get("foco_teste", {})
            if ft and ft.get("questao_exemplo"):
                q_texto = ft.get("questao_exemplo", "")
                r_texto = ft.get("proposta_resolucao", "")
                c_texto = ft.get("criterio_cotacao", "")
                e_texto = ft.get("erro_frequente", "")

                card_data = [
                    [self._P("<b>📝 COMO SAI NO TESTE (Questão Real de Avaliação)</b>", self.styles['SubSecaoTitulo'])],
                    [self._P(f"<b>Enunciado:</b> {q_texto}", self.styles['CorpoTexto'])],
                ]

                img_questao_path = ft.get("imagem_questao") or topico.get("imagem_questao")
                if img_questao_path and img_questao_path != img_manual_path:
                    rl_img_questao = self._criar_imagem_pdf(base_dir, img_questao_path, max_width=440.0, max_height=190.0)
                    if rl_img_questao is not None:
                        card_data.append([rl_img_questao])

                card_data.extend([
                    [self._P(f"<b>✅ Resolução Oficial:</b> {r_texto}", self.styles['CorpoTexto'])],
                    [self._P(f"<b>📋 Critério do Professor:</b> {c_texto}", self.styles['CorpoTexto'])],
                    [self._P(f"<b>⚠️ Cuidado com o Erro Comum:</b> {e_texto}", self.styles['CorpoTexto'])]
                ])

                t_ft = Table(card_data, colWidths=[525])
                t_ft.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
                    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#93c5fd")),
                    ('LINEBELOW', (0, 0), (0, 0), 1, colors.HexColor("#bfdbfe")),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ]))
                bloco_topico.append(t_ft)
                bloco_topico.append(Spacer(1, 10))

            elements.append(KeepTogether(bloco_topico[:2]))
            elements.extend(bloco_topico[2:])

        # 4. Flashcards de Memorização no Final
        all_flashcards = []
        for t in topicos:
            all_flashcards.extend(t.get("flashcards", []))

        if all_flashcards:
            elements.append(Spacer(1, 8))
            elements.append(self._P("⚡ Flashcards de Autoavaliação Rápida (Antes do Teste)", self.styles['SecaoTitulo']))
            fc_data = []
            for fc in all_flashcards[:8]:
                p_frente = self._P(f"<b>Pergunta:</b> {fc.get('frente', '')}", self.styles['CorpoTexto'])
                p_verso = self._P(f"<b>Resposta:</b> {fc.get('verso', '')}", self.styles['CorpoTexto'])
                fc_data.append([p_frente, p_verso])
            t_fc = Table(fc_data, colWidths=[260, 265])
            t_fc.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#fafaf9")),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#d6d3d1")),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e7e5e4")),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(t_fc)

        doc.build(elements, canvasmaker=NumberedCanvas)

        if output_path is None:
            buffer.seek(0)
            return buffer.getvalue()
        return output_path
