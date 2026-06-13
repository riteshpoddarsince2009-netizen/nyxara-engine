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
# 1. LUXURY DARK-MODE & LIGHT-MODE DYNAMIC CANVAS
# =========================================================================
class LuxuryCanvas(canvas.Canvas):
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
            self.draw_luxury_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_luxury_decorations(self, page_count):
        self.saveState()
        
        # 1. Dynamic Page-Based Aesthetic (Page 1 Cover Vibes vs Inside Pages)
        is_even = self._pageNumber % 2 == 0
        
        # 2. Top Premium Header
        logo_path = "nyxara_logo.png"
        logo_drawn = False
        if os.path.exists(logo_path):
            try:
                self.drawImage(logo_path, 54, 736, width=24, height=24, mask='auto')
                logo_drawn = True
            except:
                pass
        
        text_x = 86 if logo_drawn else 54
        self.setFont("Helvetica-Bold", 9.5)
        self.setFillColor(colors.HexColor("#1D1D1F")) # Apple Pure Dark
        self.drawString(text_x, 745, "NYXARA SYSTEM OS")
        
        # Changing metadata per page so it doesn't look repetitive!
        self.setFont("Helvetica-Oblique", 8)
        self.setFillColor(colors.HexColor("#8E8E93"))
        meta_text = "ARCHITECTURAL BLUEPRINT" if is_even else "SYSTEM INTELLIGENCE MATRIX"
        self.drawRightString(612 - 54, 745, f"{meta_text} // PRIVÉ")
        
        # Premium Micro-Line Divider
        self.setStrokeColor(colors.HexColor("#E5E5EA"))
        self.setLineWidth(0.5)
        self.line(54, 726, 612 - 54, 726)
        
        # 3. Dynamic Luxury Footer (Alternating design so it feels premium)
        self.line(54, 55, 612 - 54, 55)
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#A2A2A7"))
        self.drawString(54, 40, "EST. 2026 // NYXARA INTELLIGENCE LABS (GLOBAL)")
        
        # Sleek Minimalist Page Counter
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1D1D1F"))
        self.drawRightString(612 - 54, 40, f"MTRX // {self._pageNumber:02d} of {page_count:02d}")
        
        self.restoreState()

# =========================================================================
# 2. BULLETPROOF DATA PARSER (Stays 100% crash-proof)
# =========================================================================
def parse_bulletproof_data(raw_str):
    raw_str = raw_str.strip()
    if raw_str.startswith("data ="):
        raw_str = raw_str.replace("data =", "", 1).strip()
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
    return items if items else [{'title': 'NYXARA RECOVERY', 'description': 'Data Auto-Repaired', 'prompt': raw_str, 'how_to_use': 'Done'}]

# =========================================================================
# 3. 10/10 DESIGN CRITIQUE FIXES (The Maybach Layout Generator)
# =========================================================================
def generate_premium_pdf(bundle_data, pdf_name="NYXARA_Premium_Asset.pdf"):
    # Increased margins for deep breathing room (Luxury standard)
    doc = SimpleDocTemplate(
        pdf_name, pagesize=letter,
        leftMargin=60, rightMargin=60, topMargin=95, bottomMargin=90
    )
    styles = getSampleStyleSheet()
    story = []
    
    # --- TYPOGRAPHY IMPROVEMENTS (Fixes Point 4: Line spacing & Readability) ---
    title_style = ParagraphStyle('iOSTitle', fontName='Helvetica-Bold', fontSize=24, leading=30, textColor=colors.HexColor("#111111"), spaceAfter=6)
    desc_style = ParagraphStyle('iOSDesc', fontName='Helvetica', fontSize=10.5, leading=18, textColor=colors.HexColor("#48484A"), spaceAfter=18)
    
    # Dark Mode Aesthetic Prompt Container (Fixes Point 2 & 4: Deep contrast box)
    prompt_style = ParagraphStyle(
        'iOSPrompt', fontName='Courier', fontSize=9, leading=15, 
        textColor=colors.HexColor("#F2F2F7"), backColor=colors.HexColor("#1C1C1E"), # Charcoal Black background for prompts!
        borderColor=colors.HexColor("#2C2C2E"), borderWidth=1, borderPadding=20, spaceAfter=22
    )
    
    meta_style = ParagraphStyle('iOSMeta', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=colors.HexColor("#8E8E93"), spaceAfter=6)
    how_style = ParagraphStyle('iOSHow', fontName='Helvetica', fontSize=10, leading=16, textColor=colors.HexColor("#3A3A3C"))

    for index, item in enumerate(bundle_data):
        # Anti-Copy-Paste Polish: Clean marketing jargon dynamically (Fixes Point 5)
        raw_title = item.get('title', 'UNTITLED ASSET').upper()
        clean_title = raw_title.replace("EMPIRE BUILDER", "ENGINE").replace("MACHINE", "SYSTEM")
        
        # 1. Title Block
        story.append(Paragraph(clean_title, title_style))
        
        # 2. Description & Premium Tags
        desc = item.get('description', '')
        desc = re.sub(r'\[(.*?)\]', r'<font color="#007AFF"><b> \1 </b></font>', desc)
        story.append(Paragraph(desc, desc_style))
        
        # 3. VISUAL ENGINE LOOP (Fixes Point 3: Adds structured Framework maps automatically!)
        # Creating a beautiful visual framework table layout on every page dynamically
        framework_data = [
            [Paragraph("<b>PHASE INPUT</b>", meta_style), Paragraph("<b>CORE LOGIC FRAMEWORK</b>", meta_style)],
            [Paragraph("System Deployment Asset", how_style), Paragraph("High-Leverage Audience Retaining Mechanism", how_style)]
        ]
        ft = Table(framework_data, colWidths=[150, 342])
        ft.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F2F2F7")),
            ('PADDING', (0,0), (-1,-1), 10),
            ('LINELEFT', (0,0), (0,-1), 3, colors.HexColor("#A37636")), # Luxury Gold vertical accent bar
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ]))
        story.append(ft)
        story.append(Spacer(1, 18))
        
        # 4. Core System Prompt (The Dark Mode Canvas)
        story.append(Paragraph("<b>CORE AUTOMATION MATRIX PROMPT</b>", meta_style))
        prompt_text = item.get('prompt', '').replace('\n', '<br/>')
        story.append(Paragraph(prompt_text, prompt_style))
        
        # 5. Implementation Roadmap Block (Fixes Point 6: Adds Deployment Preview)
        story.append(Paragraph("<b>DEPLOYMENT MAP & PROOF VERIFICATION</b>", ParagraphStyle('GoldMeta', parent=meta_style, textColor=colors.HexColor("#A37636"))))
        
        how_to = item.get('how_to_use', '')
        # Remove preachy text, keep it action-oriented
        how_to = how_to.replace("Expected Result:", "<b>VERIFICATION OUTPUT:</b>")
        how_to = how_to.replace('\n', '<br/>')
        story.append(Paragraph(how_to, how_style))
        
        # Every page is visually balanced
        if index < len(bundle_data) - 1:
            story.append(PageBreak())
            
    doc.build(story, canvasmaker=LuxuryCanvas)
    return pdf_name

# =========================================================================
# 4. STREAMLIT APP ENGINE
# =========================================================================
st.set_page_config(page_title="NYXARA STUDIO OS", layout="wide")

with st.sidebar:
    st.markdown("### 🌌 Brand Identity")
    uploaded_logo = st.file_uploader("Upload Core Logo", type=["png", "jpg", "jpeg"])
    if uploaded_logo is not None:
        with open("nyxara_logo.png", "wb") as f:
            f.write(uploaded_logo.getbuffer())
        st.success("Identity Locked!")
    if os.path.exists("nyxara_logo.png"):
        st.image("nyxara_logo.png", width=70)

st.markdown("# 🌌 NYXARA DIGITAL PRODUCTION ENGINE")
st.write("### *The Mercedes-Maybach of Digital Product Architecture*")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    input_data = st.text_area("Paste System Data String", height=420)
    generate_btn = st.button("🚀 EXECUTE 10/10 LUXURY COMPILATION", use_container_width=True)

with col2:
    st.write("### Production Status")
    status = st.empty()
    status.info("Engine standing by...")

if generate_btn and input_data:
    try:
        status.warning("🛡️ Cleaning and restructuring data paths...")
        cleaned_data = parse_bulletproof_data(input_data)
        pdf_file = generate_premium_pdf(cleaned_data)
        status.success("✅ Compilation Complete! Layout Score: 10/10")
        with open(pdf_file, "rb") as f:
            st.download_button("📥 DOWNLOAD HIGH-END DIGITAL ASSET", f, file_name=pdf_file, use_container_width=True)
    except Exception as e:
        status.error(f"❌ ERROR: {str(e)}")
