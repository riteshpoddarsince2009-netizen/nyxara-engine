import streamlit as st
import re
import ast
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# =========================================================================
# 1. APPLE iOS 26 MINIMALIST CANVAS ENGINE 🍏
# =========================================================================
class iOSCanvas(canvas.Canvas):
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
            self.draw_ios_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_ios_decorations(self, page_count):
        self.saveState()
        
        # --- iOS TOP HEADER ---
        logo_path = "nyxara_logo.png"
        logo_drawn = False
        if os.path.exists(logo_path):
            try:
                self.drawImage(logo_path, 54, 735, width=22, height=22, mask='auto')
                logo_drawn = True
            except:
                pass
        
        text_x = 84 if logo_drawn else 54
        self.setFont("Helvetica-Bold", 10)
        self.setFillColor(colors.HexColor("#1D1D1F")) # Apple Dark
        self.drawString(text_x, 743, "NYXARA SYSTEM OS")
        
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#86868B")) # Apple Grey
        self.drawRightString(612 - 54, 743, "AUTOMATED DIGITAL ASSET // PRIVÉ")
        
        # Sleek Micro-Line
        self.setStrokeColor(colors.HexColor("#E5E5EA"))
        self.setLineWidth(0.5)
        self.line(54, 726, 612 - 54, 726)
        
        # --- iOS BOTTOM FOOTER ---
        self.line(54, 55, 612 - 54, 55)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#86868B"))
        self.drawString(54, 40, "DESIGNED BY NYXARA INTELLIGENCE LABS")
        
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(colors.HexColor("#1D1D1F"))
        self.drawRightString(612 - 54, 40, f"Page {self._pageNumber} of {page_count}")
        
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
# 3. iOS 26 SLEEK PDF COMPILATION ENGINE
# =========================================================================
def generate_ios_pdf(bundle_data, pdf_name="NYXARA_iOS_Premium_Asset.pdf"):
    doc = SimpleDocTemplate(
        pdf_name, pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=90, bottomMargin=85
    )
    styles = getSampleStyleSheet()
    story = []
    
    # iOS Typography Styles
    title_style = ParagraphStyle('iOSTitle', fontName='Helvetica-Bold', fontSize=22, leading=28, textColor=colors.HexColor("#1D1D1F"), spaceAfter=8)
    desc_style = ParagraphStyle('iOSDesc', fontName='Helvetica', fontSize=10.5, leading=17, textColor=colors.HexColor("#424245"), spaceAfter=18)
    
    # Apple style grey box for prompt
    prompt_style = ParagraphStyle(
        'iOSPrompt', fontName='Courier', fontSize=9, leading=15, 
        textColor=colors.HexColor("#1D1D1F"), backColor=colors.HexColor("#F5F5F7"),
        borderColor=colors.HexColor("#E5E5EA"), borderWidth=0.5, borderPadding=16, spaceAfter=0
    )
    
    meta_style = ParagraphStyle('iOSMeta', fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=colors.HexColor("#86868B"), spaceAfter=8)
    blue_meta_style = ParagraphStyle('iOSBlueMeta', fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=colors.HexColor("#0071E3"), spaceAfter=8) # Apple Blue
    body_style = ParagraphStyle('iOSBody', fontName='Helvetica', fontSize=10, leading=16, textColor=colors.HexColor("#1D1D1F"))

    for index, item in enumerate(bundle_data):
        # 1. Asset Title
        story.append(Paragraph(item.get('title', 'UNTITLED ASSET').upper(), title_style))
        
        # 2. Description
        desc = item.get('description', '')
        desc = re.sub(r'\[(.*?)\]', r'<font color="#0071E3"><b>\1</b></font>', desc)
        story.append(Paragraph(desc, desc_style))
        
        # 3. Framework Node Map (Flat iOS style)
        story.append(Paragraph("SYSTEM NODE MAP", meta_style))
        framework_data = [
            [Paragraph("<b>INTELLIGENCE LAYER</b>", meta_style), Paragraph("<b>DYNAMIC EXECUTION PIPELINE</b>", meta_style)],
            [Paragraph("System Deployment Blueprint", body_style), Paragraph("High-Leverage Retention Protocol", body_style)]
        ]
        ft = Table(framework_data, colWidths=[150, 342])
        ft.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F5F5F7")),
            ('PADDING', (0,0), (-1,-1), 10),
            ('LINELEFT', (0,0), (0,-1), 2, colors.HexColor("#0071E3")), # Blue accent line instead of gold
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(ft)
        story.append(Spacer(1, 15))
        
        # 4. Core Prompt
        story.append(Paragraph("CORE AUTOMATION MATRIX PROMPT", blue_meta_style))
        prompt_content = item.get('prompt', '').replace('\n', '<br/>')
        story.append(Paragraph(prompt_content, prompt_style))
        story.append(Spacer(1, 18))
        
        # 5. Deployment Map
        story.append(Paragraph("DEPLOYMENT MAP & VERIFICATION PROOF", meta_style))
        how_to = item.get('how_to_use', '').replace('\n', '<br/>')
        story.append(Paragraph(how_to, body_style))
        story.append(Spacer(1, 15))
        
        # 6. Ecosystem Assets (Clean Flat Cards, REMOVING N/A 🔥)
        assets = item.get('ecosystem_assets', {})
        
        valid_assets = []
        if assets:
            for key, display_name in [('notion_dashboard_template', '[01] NYXARA NOTION DATASPACE'),
                                      ('sop_execution_blueprint', '[02] SYSTEM PRODUCTION SOP BLUEPRINT'),
                                      ('automation_map', '[03] AUTOMATION PIPELINE ROUTER MAP')]:
                val = assets.get(key, 'N/A').strip()
                # Sirf tabhi add hoga agar N/A nahi hai!
                if val.upper() != 'N/A' and val != '':
                    valid_assets.append((display_name, val))
                    
        if valid_assets:
            story.append(Paragraph("PROPRIETARY SYSTEM ECOSYSTEM INFRASTRUCTURE", blue_meta_style))
            
            for title, content in valid_assets:
                # Flow arrows ko techy banaya
                if 'AUTOMATION PIPELINE' in title:
                    content = content.replace(" -> ", " <font color='#0071E3'><b>➔</b></font> ")
                    content_para = Paragraph(content, ParagraphStyle('Console', parent=body_style, fontName='Courier', fontSize=9, leading=14))
                else:
                    content_para = Paragraph(content, body_style)

                c_table = Table([[Paragraph(f"<b>{title}</b>", meta_style)], [content_para]], colWidths=[492])
                c_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFFFF")),
                    ('PADDING', (0,0), (-1,-1), 12),
                    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E5EA")), # Clean single outline
                ]))
                story.append(c_table)
                story.append(Spacer(1, 10))
            
        if index < len(bundle_data) - 1:
            story.append(PageBreak())
            
    doc.build(story, canvasmaker=iOSCanvas)
    return pdf_name

# =========================================================================
# 4. STREAMLIT FRONT-END OS INTERFACE
# =========================================================================
st.set_page_config(page_title="NYXARA OS", layout="wide")

with st.sidebar:
    st.markdown("### 🌌 Brand Identity")
    uploaded_logo = st.file_uploader("Upload Vector Logo", type=["png", "jpg", "jpeg"])
    if uploaded_logo is not None:
        with open("nyxara_logo.png", "wb") as f:
            f.write(uploaded_logo.getbuffer())
        st.success("Logo applied successfully!")
    if os.path.exists("nyxara_logo.png"):
        st.image("nyxara_logo.png", width=70)

st.markdown("# 🌌 NYXARA DIGITAL PRODUCTION ENGINE")
st.write("### *The Ultimate Minimalist Architecture of Digital Product Design*")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    input_data = st.text_area("Paste NYXARA Highly-Structured Token Data String", height=450)
    generate_btn = st.button("🚀 EXECUTE iOS CLEAN COMPILATION", use_container_width=True)

with col2:
    st.write("### Rendering Pipeline Status")
    status = st.empty()
    status.info("Engine standing by...")

if generate_btn and input_data:
    try:
        status.warning("🛡️ Activating Minimalist Layers & Removing Empty Nodes...")
        cleaned_data = parse_bulletproof_data(input_data)
        if not cleaned_data:
            st.error("❌ PARSING ERROR: Data format parse fail. Make sure it's a valid Python array block.")
        else:
            pdf_file = generate_ios_pdf(cleaned_data)
            status.success("✅ Clean Compilation Complete! UI Score: Apple 10/10")
            with open(pdf_file, "rb") as f:
                st.download_button("📥 DOWNLOAD SLEEK DIGITAL ASSET", f, file_name=pdf_file, use_container_width=True)
    except Exception as e:
        status.error(f"❌ COMPILER CRITICAL ERROR: {str(e)}")
