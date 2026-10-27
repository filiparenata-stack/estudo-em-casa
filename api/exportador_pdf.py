import os
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable, Image as RLImage
)
from reportlab.pdfgen import canvas

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
        texto = f"Escola Virtual 7.º Ano | Guia de Resumo para Estudo — Página {self._pageNumber} de {page_count}"
        self.drawRightString(A4[0] - 40, 25, texto)
        self.restoreState()


class ExportadorPDF:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._configurar_estilos()

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
                Paragraph(f"<b>{disc.upper()}</b> • {periodo}", self.styles['HeaderDisciplina']),
                Paragraph("<b>7.º ANO • ENSINO BÁSICO</b>", self.styles['HeaderDisciplina'])
            ],
            [
                Paragraph(titulo, self.styles['HeaderTitulo']),
                ""
            ],
            [
                Paragraph(f"<b>Conteúdos avaliados no teste:</b> {indicacao}", self.styles['HeaderSub']),
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
            elements.append(Paragraph(intro, self.styles['CorpoTexto']))
            elements.append(Spacer(1, 8))

        # 3. Conceitos-Chave (Tabela com fundo suave)
        conceitos = resumo_data.get("conceitos_chave", [])
        if conceitos:
            elements.append(Paragraph("📌 Conceitos-Chave e Definições Fundamentais", self.styles['SecaoTitulo']))
            t_data = []
            for c in conceitos:
                termo_p = Paragraph(f"<b>{c['termo']}</b>", self.styles['TermoDestaque'])
                def_p = Paragraph(c['definicao'], self.styles['CorpoTexto'])
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
            elements.append(Paragraph("⚡ Esquemas, Relações e Regras de Cálculo", self.styles['SecaoTitulo']))
            e_data = []
            for eq in esquemas:
                tit_eq = Paragraph(f"<b>{eq['titulo']}</b>", self.styles['TermoDestaque'])
                cont_eq = Paragraph(eq['conteudo'], self.styles['CorpoTexto'])
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
            elements.append(Paragraph("📝 Síntese Estruturada dos Conteúdos", self.styles['SecaoTitulo']))
            for sec in pontos:
                elements.append(Paragraph(sec.get("subtitulo", "Tópico"), self.styles['SubSecaoTitulo']))
                for it in sec.get("itens", []):
                    elements.append(Paragraph(f"• {it}", self.styles['ItemBullet']))
                elements.append(Spacer(1, 4))

        # 6. Dicas para o Teste
        dicas = resumo_data.get("atencao_no_teste", [])
        if dicas:
            elements.append(Spacer(1, 6))
            elements.append(Paragraph("⚠️ Atenção no Teste (Erros Frequentes e Recomendações)", self.styles['SecaoTitulo']))
            d_data = []
            for d in dicas:
                d_data.append([Paragraph(f"⚠️ {d}", self.styles['CorpoTexto'])])
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
        contendo as Metas Curriculares, Teoria Essencial, Esquemas e Questões de Teste resolvidas.
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
                Paragraph(f"<b>ESCOLA VIRTUAL 7.º ANO • {disc.upper()}</b>", self.styles['HeaderDisciplina']),
                Paragraph(f"<b>{periodo.upper()}</b>", self.styles['HeaderDisciplina'])
            ],
            [
                Paragraph(titulo, self.styles['HeaderTitulo']),
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
            elements.append(Paragraph("🎯 Metas Curriculares Oficiais Avaliadas no Período", self.styles['SecaoTitulo']))
            m_data = []
            for m in metas:
                m_data.append([Paragraph(f"✓ <b>{m}</b>", self.styles['CorpoTexto'])])
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
        base_dir = os.path.dirname(os.path.dirname(__file__))

        # 3. Tópicos Curriculares
        for idx, topico in enumerate(topicos):
            tit_t = topico.get("titulo", f"Tópico {idx+1}")
            subdom = topico.get("subdominio", "")
            
            bloco_topico = []
            bloco_topico.append(Paragraph(f"<b>{idx+1}. {tit_t}</b> <font size=8 color='#64748b'>({subdom})</font>", self.styles['SecaoTitulo']))
            
            # Conceitos-chave
            conceitos = topico.get("conceitos_chave", [])
            if conceitos:
                t_conc = []
                for c in conceitos:
                    t_conc.append([
                        Paragraph(f"<b>{c.get('termo')}</b>", self.styles['TermoDestaque']),
                        Paragraph(c.get('definicao', ''), self.styles['CorpoTexto'])
                    ])
                t_table = Table(t_conc, colWidths=[150, 375])
                t_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                    ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#cbd5e1")),
                    ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ]))
                bloco_topico.append(t_table)
                bloco_topico.append(Spacer(1, 6))

            # Foco no Teste (Questão real de exame + resolução)
            ft = topico.get("foco_teste", {})
            if ft and ft.get("questao_exemplo"):
                q_texto = ft.get("questao_exemplo", "")
                r_texto = ft.get("proposta_resolucao", "")
                c_texto = ft.get("criterio_cotacao", "")
                e_texto = ft.get("erro_frequente", "")

                card_data = [
                    [Paragraph("<b>📝 COMO SAI NO TESTE (Questão Real de Avaliação)</b>", self.styles['SubSecaoTitulo'])],
                    [Paragraph(f"<b>Enunciado:</b> {q_texto}", self.styles['CorpoTexto'])],
                    [Paragraph(f"<b>✅ Resolução Oficial:</b> {r_texto}", self.styles['CorpoTexto'])],
                    [Paragraph(f"<b>📋 Critério do Professor:</b> {c_texto}", self.styles['CorpoTexto'])],
                    [Paragraph(f"<b>⚠️ Cuidado com o Erro Comum:</b> {e_texto}", self.styles['CorpoTexto'])]
                ]
                t_ft = Table(card_data, colWidths=[525])
                t_ft.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
                    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#93c5fd")),
                    ('LINEBELOW', (0, 0), (0, 0), 1, colors.HexColor("#bfdbfe")),
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
            elements.append(Paragraph("⚡ Flashcards de Autoavaliação Rápida (Antes do Teste)", self.styles['SecaoTitulo']))
            fc_data = []
            for fc in all_flashcards[:8]:
                p_frente = Paragraph(f"<b>Pergunta:</b> {fc.get('frente')}", self.styles['CorpoTexto'])
                p_verso = Paragraph(f"<b>Resposta:</b> {fc.get('verso')}", self.styles['CorpoTexto'])
                fc_data.append([p_frente, p_verso])
            t_fc = Table(fc_data, colWidths=[260, 265])
            t_fc.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#fafaf9")),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#d6d3d1")),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e7e5e4")),
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
