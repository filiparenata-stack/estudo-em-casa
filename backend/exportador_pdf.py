import os
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
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
