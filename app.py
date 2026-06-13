import streamlit as st
import ast
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# =========================================================================
# 1. DESIGN CANVAS (UI Constant, Labels Simplified)
# =========================================================================
class NyxaraDesignCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def _draw_header_footer(self, page_count):
        self.saveState()
        # Header - Simplified
        self.setFont("Helvetica-Bold", 10)
        self.drawString(50, 760, "NYXARA DESIGN")
        self.line(50, 755, 562, 755)
        
        # Footer - Simplified
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.gray)
        self.drawString(50, 35, "Design & Framework")
        self.drawRightString(562, 35, f"Page {self._pageNumber} / {page_count}")
        self.restoreState()

# =========================================================================
# 2. PDF ENGINE (Clean Labels, Professional Tone)
# =========================================================================
def generate_design_pdf(data_list, pdf_name="NYXARA_Asset.pdf"):
    doc = SimpleDocTemplate(pdf_name, pagesize=letter, leftMargin=50, rightMargin=50, topMargin=100, bottomMargin=80)
    styles = getSampleStyleSheet()
    
    # Styles
    title_style = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=18, leading=22, spaceAfter=20)
    h2_style = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=colors.black, spaceAfter=10)
    body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=10, leading=14, spaceAfter=12)
    prompt_style = ParagraphStyle('Prompt', fontName='Courier', fontSize=9, leading=14, backColor=colors.whitesmoke, borderPadding=10, spaceAfter=20)

    story = []
    for item in data_list:
        story.append(Paragraph(item['title'].upper(), title_style))
        
        # S.H.E.L.F Framework
        story.append(Paragraph("S.H.E.L.F FRAMEWORK", h2_style))
        shelf_data = [["Shelf Visibility", "Hierarchy", "Emotion"], ["Legibility", "Familiarity", "Goal"]]
        t = Table(shelf_data, colWidths=[154, 154, 154])
        t.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey), ('PADDING', (0,0), (-1,-1), 6), ('FONTNAME', (0,0), (-1,-1), 'Helvetica'), ('FONTSIZE', (0,0), (-1,-1), 8)]))
        story.append(t)
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("PROMPT", h2_style))
        story.append(Paragraph(item['prompt'], prompt_style))
        
        story.append(Paragraph("DESIGN LOGIC", h2_style))
        story.append(Paragraph(item['reasoning'], body_style))
        
        story.append(PageBreak())
            
    doc.build(story, canvasmaker=NyxaraDesignCanvas)
    return pdf_name

# =========================================================================
# 3. INTERFACE (Clean)
# =========================================================================
st.set_page_config(page_title="NYXARA Design", layout="centered")
st.title("NYXARA Design Tool")

input_data = st.text_area("Asset Data", height=300, 
                          placeholder="[{'title': '...', 'prompt': '...', 'reasoning': '...'}]")

if st.button("Generate PDF"):
    try:
        data = ast.literal_eval(input_data)
        pdf = generate_design_pdf(data)
        with open(pdf, "rb") as f:
            st.download_button("Download", f, file_name=pdf)
    except Exception as e:
        st.error(f"Error: {e}")
