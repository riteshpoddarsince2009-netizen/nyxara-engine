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
# 1. 3D LAYERED DYNAMIC CANVAS GENERATOR
# =========================================================================
class Nyxara3DCanvas(canvas.Canvas):
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
            self.draw_3d_environments(num_pages)
            super().showPage()
        super().save()

    def draw_3d_environments(self, page_count):
        self.saveState()
        is_even = self._pageNumber % 2 == 0
        
        # --- 3D BACKGROUND GEOMETRY (Subtle border depth for the whole page) ---
        self.setStrokeColor(colors.HexColor("#F2F2F7"))
        self.setLineWidth(1)
        self.rect(44, 44, 612 - 88, 792 - 88)
        
        # --- TOP HEADER ---
        logo_path = "nyxara_logo.png"
        logo_drawn = False
        if os.path.exists(logo_path):
            try:
                self.drawImage(logo_path, 60, 736, width=24, height=24, mask='auto')
                logo_drawn = True
            except:
                pass
        
        text_x = 92 if logo_drawn else 60
        self.setFont("Helvetica-Bold", 10)
        self.setFillColor(colors.HexColor("#1C1C1E"))
        self.drawString(text_x, 746, "NYXARA MATRIX OS")
        
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#A37636")) # Gold core
        meta_label = "CORE PROTOCOL // LAYER_02" if is_even else "OPERATIONAL METRIC // LAYER_01"
        self.drawRightString(612 - 60, 746, meta_label)
        
        # Sleek 3D Double Line Header Separator
        self.setStrokeColor(colors.HexColor("#E5E5EA"))
        self.setLineWidth(0.5)
        self.line(60, 726, 612 - 60, 726)
        self.setStrokeColor(colors.HexColor("#FFFFFF"))
        self.line(60, 725, 612 - 60, 725)
        
        # --- BOTTOM FOOTER ---
        self.setStrokeColor(colors.HexColor("#E5E5EA"))
        self.setLineWidth(0.5)
        self.line(60, 58, 612 - 60, 58)
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#8E8E93"))
        self.drawString(60, 42, "SECURE DIGITAL ARCHITECTURE // PROPERTY OF NYXARA LABS")
        
        # Dimensional Page Numbering
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1C1C1E"))
        self.drawRightString(612 - 60, 42, f"SYS_REF // P{self._pageNumber:02d}_{page_count:02d}")
        
        self.restoreState()

# =========================================================================
# 2. BULLETPROOF DATA PARSER (Extracts nested Ecosystem Assets)
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
# 3. 3D LAYERING PDF COMPILATION ENGINE
# =========================================================================
def generate_3d_luxury_pdf(bundle_data, pdf_name="NYXARA_3D_Premium_Asset.pdf"):
    doc = SimpleDocTemplate(
        pdf_name, pagesize=letter,
        leftMargin=60, rightMargin=60, topMargin=95, bottomMargin=90
    )
    styles = getSampleStyleSheet()
    story = []
    
    # Typography Styles Configuration
    title_style = ParagraphStyle('3DTitle', fontName='Helvetica-Bold', fontSize=22, leading=28, textColor=colors.HexColor("#1C1C1E"), spaceAfter=4)
    desc_style = ParagraphStyle('3DDesc', fontName='Helvetica', fontSize=10.5, leading=17, textColor=colors.HexColor("#3A3A3C"), spaceAfter=15)
    
    # Core prompt text block style
    prompt_style = ParagraphStyle(
        '3DPrompt', fontName='Courier', fontSize=9, leading=15, 
        textColor=colors.HexColor("#F2F2F7"), backColor=colors.HexColor("#1C1C1E"),
        spaceAfter=0
    )
    
    meta_style = ParagraphStyle('3DMeta', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=colors.HexColor("#8E8E93"), spaceAfter=6)
    gold_meta_style = ParagraphStyle('3DGoldMeta', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=colors.HexColor("#A37636"), spaceAfter=6)
    body_style = ParagraphStyle('3DBody', fontName='Helvetica', fontSize=9.5, leading=15, textColor=colors.HexColor("#2C2C2E"))
    asset_title_style = ParagraphStyle('AssetTitle', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=colors.HexColor("#1C1C1E"))

    for index, item in enumerate(bundle_data):
        # 1. Asset Title & Description
        story.append(Paragraph(item.get('title', 'UNTITLED SYSTEM MATRIX').upper(), title_style))
        
        desc = item.get('description', '')
        desc = re.sub(r'\[(.*?)\]', r'<font color="#007AFF"><b> \1 </b></font>', desc)
        story.append(Paragraph(desc, desc_style))
        
        # 2. Framework Matrix Block
        story.append(Paragraph("SYSTEM NODE MAP", meta_style))
        framework_data = [
            [Paragraph("<b>INTELLIGENCE LAYER</b>", meta_style), Paragraph("<b>DYNAMIC EXECUTION PIPELINE</b>", meta_style)],
            [Paragraph("System Deployment Blueprint", body_style), Paragraph("High-Leverage Asymmetric Retention Protocol", body_style)]
        ]
        ft = Table(framework_data, colWidths=[160, 332])
        ft.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F2F2F7")),
            ('PADDING', (0,0), (-1,-1), 10),
            ('LINELEFT', (0,0), (0,-1), 3.5, colors.HexColor("#A37636")), # Gold edge depth
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(ft)
        story.append(Spacer(1, 15))
        
        # 3. CORE PROMPT INTERFACE WITH PSEUDO-3D SHADOW LAYERING
        story.append(Paragraph("CORE AUTOMATION MATRIX PROMPT", meta_style))
        prompt_content = item.get('prompt', '').replace('\n', '<br/>')
        
        # Wrap prompt in a 3D Neumorphic shadow table structure
        prompt_table_data = [[Paragraph(prompt_content, prompt_style)]]
        pt = Table(prompt_table_data, colWidths=[492])
        pt.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.HexColor("#1C1C1E")),
            ('PADDING', (0,0), (0,0), 16),
            ('LINEBELOW', (0,0), (0,0), 4, colors.HexColor("#A37636")), # 3D Shadow Bottom (Gold)
            ('LINERIGHT', (0,0), (0,0), 4, colors.HexColor("#A37636")),  # 3D Shadow Right (Gold)
        ]))
        story.append(pt)
        story.append(Spacer(1, 18))
        
        # 4. HOW TO DEPLOY SYSTEM
        story.append(Paragraph("DEPLOYMENT MAP & VERIFICATION PROOF", gold_meta_style))
        how_to = item.get('how_to_use', '').replace('\n', '<br/>')
        story.append(Paragraph(how_to, body_style))
        story.append(Spacer(1, 15))
        
        # 5. ECOSYSTEM ASSETS LAYER (3D Stacked Cards Layout)
        assets = item.get('ecosystem_assets', {})
        if assets:
            story.append(Paragraph("PROPRIETARY SYSTEM ECOSYSTEM INFRASTRUCTURE", meta_style))
            
            # Card 1: Notion Dashboard Template
            notion_txt = assets.get('notion_dashboard_template', 'N/A')
            n_table = Table([[Paragraph("<b>[01] NYXARA NOTION DATASPACE</b>", gold_meta_style)], [Paragraph(notion_txt, body_style)]], colWidths=[492])
            n_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFFFF")),
                ('PADDING', (0,0), (-1,-1), 12),
                ('LINEBELOW', (0,0), (-1,-1), 3, colors.HexColor("#D1D1D6")), # Darker gray drop shadow
                ('LINERIGHT', (0,0), (-1,-1), 3, colors.HexColor("#D1D1D6")),
                ('LINEABOVE', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E5EA")),
                ('LINELEFT', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E5EA")),
            ]))
            story.append(n_table)
            story.append(Spacer(1, 12))
            
            # Card 2: SOP Execution Blueprint
            sop_txt = assets.get('sop_execution_blueprint', 'N/A')
            s_table = Table([[Paragraph("<b>[02] SYSTEM PRODUCTION SOP BLUEPRINT</b>", gold_meta_style)], [Paragraph(sop_txt, body_style)]], colWidths=[492])
            s_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFFFF")),
                ('PADDING', (0,0), (-1,-1), 12),
                ('LINEBELOW', (0,0), (-1,-1), 3, colors.HexColor("#D1D1D6")),
                ('LINERIGHT', (0,0), (-1,-1), 3, colors.HexColor("#D1D1D6")),
                ('LINEABOVE', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E5EA")),
                ('LINELEFT', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E5EA")),
            ]))
            story.append(s_table)
            story.append(Spacer(1, 12))
            
            # Card 3: Automation Flow Map (Rendered as a beautiful terminal-style connection box)
            auto_txt = assets.get('automation_map', 'N/A')
            # Turn arrows into a high-tech flow map representation
            auto_formatted = auto_txt.replace(" -> ", " <font color='#007AFF'><b>➔</b></font> ")
            a_table = Table([[Paragraph("<b>[03] AUTOMATION PIPELINE ROUTER MAP</b>", ParagraphStyle('BlueMeta', parent=meta_style, textColor=colors.HexColor("#007AFF")))], [Paragraph(auto_formatted, ParagraphStyle('ConsoleStyle', parent=body_style, fontName='Courier', fontSize=9, leading=14))]], colWidths=[492])
            a_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F2F2F7")),
                ('PADDING', (0,0), (-1,-1), 12),
                ('LINEBELOW', (0,0), (-1,-1), 3, colors.HexColor("#C7C7CC")),
                ('LINERIGHT', (0,0), (-1,-1), 3, colors.HexColor("#C7C7CC")),
            ]))
            story.append(a_table)
            
        if index < len(bundle_data) - 1:
            story.append(PageBreak())
            
    doc.build(story, canvasmaker=Nyxara3DCanvas)
    return pdf_name

# =========================================================================
# 4. STREAMLIT FRONT-END OS INTERFACE
# =========================================================================
st.set_page_config(page_title="NYXARA 3D STUDIO OS", layout="wide")

with st.sidebar:
    st.markdown("### 🌌 Brand Spatial Identity")
    uploaded_logo = st.file_uploader("Upload Vector Logo", type=["png", "jpg", "jpeg"])
    if uploaded_logo is not None:
        with open("nyxara_logo.png", "wb") as f:
            f.write(uploaded_logo.getbuffer())
        st.success("Identity Locked in Space!")
    if os.path.exists("nyxara_logo.png"):
        st.image("nyxara_logo.png", width=70)

st.markdown("# 🌌 NYXARA 3D DIGITAL PRODUCTION ENGINE")
st.write("### *The Ultimate Spatial Architecture of Digital Product Design*")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    input_data = st.text_area("Paste NYXARA Highly-Structured Token Data String", height=450)
    generate_btn = st.button("🚀 EXECUTE 3D LAYERED COMPILATION", use_container_width=True)

with col2:
    st.write("### 3D Rendering Pipeline Status")
    status = st.empty()
    status.info("Spatial Engine standing by...")

if generate_btn and input_data:
    try:
        status.warning("🛡️ Activating Spatial Matrix Layers & Fixing Node Alignments...")
        cleaned_data = parse_bulletproof_data(input_data)
        if not cleaned_data:
            st.error("❌ PARSING ERROR: Data format parse fail. Make sure it's valid Python array block.")
        else:
            pdf_file = generate_3d_luxury_pdf(cleaned_data)
            status.success("✅ 3D Structural Compilation Complete! Perfection Score: 100%")
            with open(pdf_file, "rb") as f:
                st.download_button("📥 DOWNLOAD 3D LUXURY DIGITAL ASSET", f, file_name=pdf_file, use_container_width=True)
    except Exception as e:
        status.error(f"❌ COMPILER CRITICAL ERROR: {str(e)}")
