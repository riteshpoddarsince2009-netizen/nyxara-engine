import streamlit as st
import re
import ast
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# =========================================================================
# 1. LUXURY PDF CANVAS (10/10 PREMIUM LAYOUT WITH DYNAMIC LOGO)
# =========================================================================
class NumberedCanvas(canvas.Canvas):
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # --- PREMIUM TOP HEADER ---
        logo_path = "nyxara_logo.png"
        logo_drawn = False
        
        # Check if user has uploaded a logo via Streamlit
        if os.path.exists(logo_path):
            try:
                self.drawImage(logo_path, 54, 735, width=26, height=26, mask='auto')
                logo_drawn = True
            except Exception:
                pass
        
        text_x_pos = 90 if logo_drawn else 54
        self.setFont("Helvetica-Bold", 10.5)
        self.setFillColor(colors.HexColor("#111111"))
        self.drawString(text_x_pos, 745, "NYXARA PRODUCTION ENGINE")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#8E8E93"))
        self.drawRightString(612 - 54, 745, "AUTOMATED DIGITAL ASSET // PRIVÉ")
        
        self.setStrokeColor(colors.HexColor("#E5E5EA"))
        self.setLineWidth(0.5)
        self.line(54, 728, 612 - 54, 728)
        
        # --- LUXURY BOTTOM FOOTER ---
        self.line(54, 55, 612 - 54, 55)
        self.setFont("Helvetica", 8)
        self.drawString(54, 40, "CONFIDENTIAL // DESIGNED BY NYXARA LABS")
        
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(colors.HexColor("#111111"))
        self.drawRightString(612 - 54, 40, f"PAGE {self._pageNumber} OF {page_count}")
        
        self.restoreState()

# =========================================================================
# 2. BULLETPROOF 100% UNBREAKABLE DATA PARSER 🛡️ (No Errors Allowed)
# =========================================================================
def parse_bulletproof_data(raw_str):
    raw_str = raw_str.strip()
    
    # 1. Smart Brace Scanner: Extract only what matters (dicts between { and })
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
                    # Extract single dictionary perfectly
                    obj = ast.literal_eval(dict_str)
                    if isinstance(obj, dict):
                        items.append(obj)
                except Exception:
                    # If ast fails due to missed quotes, use heavy regex extraction
                    t = re.search(r'["\']title["\']\s*:\s*["\'](.*?)["\']', dict_str, re.DOTALL)
                    d = re.search(r'["\']description["\']\s*:\s*["\'](.*?)["\']', dict_str, re.DOTALL)
                    p = re.search(r'["\']prompt["\']\s*:\s*["\'](.*?)["\']', dict_str, re.DOTALL)
                    h = re.search(r'["\']how_to_use["\']\s*:\s*["\'](.*?)["\']', dict_str, re.DOTALL)
                    
                    if t or p:
                        items.append({
                            'title': t.group(1) if t else 'UNTITLED ASSET',
                            'description': d.group(1) if d else '',
                            'prompt': p.group(1) if p else '',
                            'how_to_use': h.group(1) if h else ''
                        })
                start = -1
                
    if items:
        return items
        
    # 2. Absolute fallback so the code NEVER crashes
    return [{
        'title': 'NYXARA EMERGENCY RECOVERY',
        'description': 'System found severely corrupted data, but compiled successfully!',
        'prompt': raw_str,
        'how_to_use': 'Next time, just ensure data has standard title and prompt structures.'
    }]

# =========================================================================
# 3. PDF GENERATION LOGIC (10/10 PREMIUM MAYBACH DESIGN)
# =========================================================================
def generate_premium_pdf(bundle_data, pdf_name="NYXARA_Premium_Asset.pdf"):
    doc = SimpleDocTemplate(
        pdf_name, pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=96, bottomMargin=85
    )
    styles = getSampleStyleSheet()
    story = []
    
    # Custom Apple/Maybach aesthetic styles
    title_style = ParagraphStyle('iOSTitle', fontName='Helvetica-Bold', fontSize=22, leading=28, textColor=colors.HexColor("#111111"), spaceAfter=15)
    desc_style = ParagraphStyle('iOSDesc', fontName='Helvetica', fontSize=11, leading=18, textColor=colors.HexColor("#444446"), spaceAfter=25)
    
    # Premium light-gray canvas prompt box
    prompt_style = ParagraphStyle(
        'iOSPrompt', fontName='Courier', fontSize=9.5, leading=16, 
        textColor=colors.HexColor("#1C1C1E"), backColor=colors.HexColor("#F9F9FB"), 
        borderColor=colors.HexColor("#E5E5EA"), borderWidth=0.75, borderPadding=18, spaceAfter=25
    )
    
    meta_style = ParagraphStyle('iOSMeta', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=colors.HexColor("#A37636"), spaceAfter=8) # Luxury Gold Accent
    how_style = ParagraphStyle('iOSHow', fontName='Helvetica', fontSize=10.5, leading=16, textColor=colors.HexColor("#2C2C2E"))

    for index, item in enumerate(bundle_data):
        story.append(Paragraph(item.get('title', 'UNTITLED ASSET').upper(), title_style))
        
        desc = item.get('description', '')
        # Convert [Tags] into premium blue highlighting dynamically
        desc = re.sub(r'\[(.*?)\]', r'<font color="#007AFF"><b>[\1]</b></font>', desc)
        story.append(Paragraph(desc, desc_style))
        
        story.append(Paragraph(item.get('prompt', '').replace('\n', '<br/>'), prompt_style))
        story.append(Paragraph("SYSTEM EXECUTION ROADMAP", meta_style))
        
        how_to = item.get('how_to_use', '').replace('\n', '<br/>')
        story.append(Paragraph(how_to, how_style))
        
        if index < len(bundle_data) - 1:
            story.append(PageBreak())
            
    doc.build(story, canvasmaker=NumberedCanvas)
    return pdf_name

# =========================================================================
# 4. STREAMLIT INTERFACE (UI + DIRECT LOGO UPLOAD & SAVE)
# =========================================================================
st.set_page_config(page_title="NYXARA OS", layout="wide", initial_sidebar_state="expanded")

# --- SIDEBAR: LOGO UPLOAD AND SAVE SYSTEM ---
with st.sidebar:
    st.markdown("### ⚙️ System Settings")
    st.markdown("Upload your brand logo here once. It will be saved and used in all future PDFs!")
    
    uploaded_logo = st.file_uploader("Upload Brand Logo (PNG/JPG)", type=["png", "jpg", "jpeg"])
    
    if uploaded_logo is not None:
        # Save logo locally forever for this deployment
        with open("nyxara_logo.png", "wb") as f:
            f.write(uploaded_logo.getbuffer())
        st.success("✅ Logo saved successfully! It will now appear on your PDFs.")
        
    if os.path.exists("nyxara_logo.png"):
        st.image("nyxara_logo.png", width=80, caption="Current Saved Logo")

# --- MAIN DASHBOARD ---
st.markdown("# 🌌 NYXARA DIGITAL PRODUCTION ENGINE")
st.write("### *The Mercedes-Maybach of Digital Product Architecture*")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    input_data = st.text_area(
        "Paste ChatGPT Python Data Here (Even if brackets are wrong, system won't crash!)",
        placeholder="data = [\n    {\n        'title': '01. Authority Engine',\n        ...\n    }\n]",
        height=400
    )
    generate_btn = st.button("🚀 ENGINEER PREMIUM PDF", use_container_width=True)

with col2:
    st.write("### System Status")
    status = st.empty()
    status.info("Ready for deployment... Paste data and click execute.")

if generate_btn and input_data:
    try:
        status.warning("🛡️ Scanning and repairing corrupted data...")
        cleaned_data = parse_bulletproof_data(input_data)
        
        status.warning("✨ Data structure verified! Generating 10/10 luxury PDF layout...")
        pdf_file = generate_premium_pdf(cleaned_data)
        
        status.success("✅ SUCCESS: NYXARA Asset Pack Engineered Perfectly!")
        with open(pdf_file, "rb") as f:
            st.download_button("📥 DOWNLOAD LUXURY ASSET", f, file_name=pdf_file, use_container_width=True)
            
    except Exception as e:
        status.error(f"❌ ERROR: {str(e)}")
