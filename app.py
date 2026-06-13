import streamlit as st
import re
import ast
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.platypus.flowables import KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# =========================================================================
# 1. THE SUPREME "ONYX & GOLD" CANVAS ENGINE 👑
# =========================================================================
class NyxaraSupremeCanvas(canvas.Canvas):
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
            self.draw_supreme_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_supreme_decorations(self, page_count):
        self.saveState()
        
        # --- SUPREME TOP HEADER ---
        logo_path = "nyxara_logo.png"
        logo_offset = 50
        if os.path.exists(logo_path):
            try:
                self.drawImage(logo_path, 50, 738, width=20, height=20, mask='auto')
                logo_offset = 80
            except:
                pass
        
        # Brand Title Text
        self.setFont("Helvetica-Bold", 10.5)
        self.setFillColor(colors.HexColor("#0A0A0A")) # True Onyx Black
        self.drawString(logo_offset, 745, "NYXARA SYSTEM OS")
        
        # Luxury Right-Side Metadata
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(colors.HexColor("#D4AF37")) # Imperial Gold
        self.drawRightString(612 - 50, 745, "PROPRIETARY ASSET // RESTRICTED")
        
        # Sharp Top Separator Line
        self.setStrokeColor(colors.HexColor("#E5E7EB"))
        self.setLineWidth(1)
        self.line(50, 730, 612 - 50, 730)
        
        # --- SUPREME BOTTOM FOOTER ---
        self.setStrokeColor(colors.HexColor("#E5E7EB"))
        self.setLineWidth(1)
        self.line(50, 55, 612 - 50, 55)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#6B7280"))
        self.drawString(50, 40, "ENGINEERED BY NYXARA LABS | ALL RIGHTS RESERVED")
        
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(colors.HexColor("#0A0A0A"))
        self.drawRightString(612 - 50, 40, f"DATA NODE P.{self._pageNumber:02d}")
        
        self.restoreState()

# =========================================================================
# 2. BULLETPROOF DATA PARSER
# =========================================================================
def parse_bulletproof_data(raw_str):
    raw_str = raw_str.strip()
    if raw_str.startswith("data ="):
        raw_str = raw_str.replace("data =", "", 1).strip()
    if raw_str.startswith("Data ="):
        raw_str = raw_str.replace("Data =", "", 1).strip()
        
    items = []
    start = -1
    brace_count = 0
    for i, char in enumerate(raw_str):
        if char == '{':
            if brace_count == 0:
                start = i
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0 and start != -1:
                dict_str = raw_str[start:i+1]
                try:
                    obj = ast.literal_eval(dict_str)
                    if isinstance(obj, dict):
                        items.append(obj)
                except:
                    pass
                start = -1
    return items

# =========================================================================
# 3. NO-CUTOFF PDF COMPILATION ENGINE
# =========================================================================
def generate_supreme_pdf(bundle_data, pdf_name="NYXARA_Supreme_Asset.pdf"):
    # Expanded Margins so content breathes and flows easily
    doc = SimpleDocTemplate(
        pdf_name, pagesize=letter,
        leftMargin=50, rightMargin=50, topMargin=85, bottomMargin=75
    )
    styles = getSampleStyleSheet()
    story = []
    
    # Typography Styles Configuration
    title_style = ParagraphStyle('SupTitle', fontName='Helvetica-Bold', fontSize=20, leading=26, textColor=colors.HexColor("#0A0A0A"), spaceAfter=6)
    desc_style = ParagraphStyle('SupDesc', fontName='Helvetica', fontSize=10.5, leading=16, textColor=colors.HexColor("#374151"), spaceAfter=18)
    
    # Prompt Style (Clean text, background is handled by Table logic)
    prompt_text_style = ParagraphStyle(
        'SupPrompt', fontName='Courier', fontSize=9.5, leading=16, textColor=colors.HexColor("#111827")
    )
    
    meta_title_style = ParagraphStyle('SupMeta', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=colors.HexColor("#D4AF37"), spaceAfter=8) # Gold Headers
    body_style = ParagraphStyle('SupBody', fontName='Helvetica', fontSize=10, leading=16, textColor=colors.HexColor("#1F2937"))

    for index, item in enumerate(bundle_data):
        
        # 1. ASSET TITLE & DESCRIPTION
        story.append(Paragraph(item.get('title', 'SYSTEM NODE OVERRIDE').upper(), title_style))
        desc = item.get('description', '')
        desc = re.sub(r'\[(.*?)\]', r'<font color="#D4AF37"><b>\1</b></font>', desc)
        story.append(Paragraph(desc, desc_style))
        
        # 2. FRAMEWORK MATRIX
        story.append(Paragraph("INTELLIGENCE PIPELINE MAP", meta_title_style))
        framework_data = [
            [Paragraph("<b>CORE ARCHITECTURE</b>", ParagraphStyle('T', parent=meta_title_style, textColor=colors.HexColor("#6B7280"))), 
             Paragraph("<b>EXECUTION PROTOCOL</b>", ParagraphStyle('T', parent=meta_title_style, textColor=colors.HexColor("#6B7280")))],
            [Paragraph("Asymmetric Deployment Blueprint", body_style), Paragraph("High-Leverage Retention Matrix", body_style)]
        ]
        ft = Table(framework_data, colWidths=[200, 312])
        ft.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F9FAFB")),
            ('PADDING', (0,0), (-1,-1), 10),
            ('LINELEFT', (0,0), (0,-1), 2.5, colors.HexColor("#D4AF37")), # Gold Indicator
        ]))
        story.append(ft)
        story.append(Spacer(1, 20))
        
        # 3. THE PROMPT (ANTI-CUTOFF GOLD BORDER HACK)
        story.append(Paragraph("CORE AUTOMATION MATRIX PROMPT", meta_title_style))
        prompt_content = item.get('prompt', '').replace('\n', '<br/>')
        prompt_para = Paragraph(prompt_content, prompt_text_style)
        
        # Split Table: Col 1 = Gold Line, Col 2 = Text. (Prevents page break cutoffs!)
        pt = Table([['', prompt_para]], colWidths=[4, 508])
        pt.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#D4AF37")), # Solid Gold Left Line
            ('BACKGROUND', (1,0), (1,-1), colors.HexColor("#F3F4F6")), # Light Grey BG
            ('TOPPADDING', (1,0), (1,-1), 12),
            ('BOTTOMPADDING', (1,0), (1,-1), 12),
            ('LEFTPADDING', (1,0), (1,-1), 15),
            ('RIGHTPADDING', (1,0), (1,-1), 15),
        ]))
        story.append(pt)
        story.append(Spacer(1, 20))
        
        # 4. DEPLOYMENT MAP (Kept together to avoid awkward splits)
        deploy_elements = []
        deploy_elements.append(Paragraph("DEPLOYMENT MAP & VERIFICATION PROOF", meta_title_style))
        how_to = item.get('how_to_use', '').replace('\n', '<br/>')
        deploy_elements.append(Paragraph(how_to, body_style))
        story.append(KeepTogether(deploy_elements)) # Prevents Header on Page 1, Text on Page 2
        story.append(Spacer(1, 20))
        
        # 5. ECOSYSTEM ASSETS (Only renders if data exists and is not N/A)
        assets = item.get('ecosystem_assets', {})
        valid_assets = []
        if assets:
            for key, display_name in [('notion_dashboard_template', '[01] NYXARA NOTION DATASPACE'),
                                      ('sop_execution_blueprint', '[02] SYSTEM PRODUCTION SOP BLUEPRINT'),
                                      ('automation_map', '[03] AUTOMATION PIPELINE ROUTER MAP')]:
                val = str(assets.get(key, 'N/A')).strip()
                if val.upper() != 'N/A' and val != '':
                    valid_assets.append((display_name, val))
                    
        if valid_assets:
            story.append(Paragraph("PROPRIETARY SYSTEM ECOSYSTEM INFRASTRUCTURE", meta_title_style))
            for title, content in valid_assets:
                if 'AUTOMATION PIPELINE' in title:
                    content = content.replace(" -> ", " <b>➔</b> ")
                    content_para = Paragraph(content, ParagraphStyle('Console', parent=body_style, fontName='Courier', fontSize=9, leading=14, textColor=colors.HexColor("#0A0A0A")))
                else:
                    content_para = Paragraph(content, body_style)

                c_table = Table([[Paragraph(f"<b>{title}</b>", meta_title_style)], [content_para]], colWidths=[512])
                c_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFFFF")),
                    ('PADDING', (0,0), (-1,-1), 12),
                    ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E5E7EB")), 
                ]))
                story.append(c_table)
                story.append(Spacer(1, 10))
            
        if index < len(bundle_data) - 1:
            story.append(PageBreak())
            
    doc.build(story, canvasmaker=NyxaraSupremeCanvas)
    return pdf_name

# =========================================================================
# 4. STREAMLIT FRONT-END OS INTERFACE
# =========================================================================
st.set_page_config(page_title="NYXARA SUPREME OS", layout="wide")

with st.sidebar:
    st.markdown("### 👑 Brand Identity")
    uploaded_logo = st.file_uploader("Upload Vector Logo", type=["png", "jpg", "jpeg"])
    if uploaded_logo is not None:
        with open("nyxara_logo.png", "wb") as f:
            f.write(uploaded_logo.getbuffer())
        st.success("Logo securely anchored!")
    if os.path.exists("nyxara_logo.png"):
        st.image("nyxara_logo.png", width=80)

st.markdown("# 👑 NYXARA SUPREME PRODUCTION ENGINE")
st.write("### *The Absolute Pinnacle of Flawless Digital Asset Architecture*")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    input_data = st.text_area("Paste NYXARA Data Array (JSON/Python Format)", height=450)
    generate_btn = st.button("🚀 INITIATE SUPREME COMPILATION", use_container_width=True)

with col2:
    st.write("### Diagnostics & Routing")
    status = st.empty()
    status.info("Systems green. Awaiting data payload...")

if generate_btn and input_data:
    try:
        status.warning("🛡️ Engaging Anti-Cutoff Matrices & Gold Accents...")
        cleaned_data = parse_bulletproof_data(input_data)
        if not cleaned_data:
            st.error("❌ CRITICAL: Data format parse fail. Ensure Python array format.")
        else:
            pdf_file = generate_supreme_pdf(cleaned_data)
            status.success("✅ SUPREME Compilation Complete! Flawless Execution.")
            with open(pdf_file, "rb") as f:
                st.download_button("📥 DOWNLOAD SUPREME DIGITAL ASSET", f, file_name=pdf_file, use_container_width=True)
    except Exception as e:
        status.error(f"❌ KERNEL PANIC: {str(e)}")
