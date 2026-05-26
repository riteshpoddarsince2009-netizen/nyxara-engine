import streamlit as st
import os
import re
import ast
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Permanent Logo Storage Path
SAVED_LOGO_PATH = "master_logo.png"

# =========================================================================
# 1. LUXURY COUTURE CANVAS ENGINE (Header/Footer Design)
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
        logo_path = SAVED_LOGO_PATH if os.path.exists(SAVED_LOGO_PATH) else None
        logo_offset = 54
        
        # Draw Premium Logo (Top Left)
        if logo_path:
            try:
                self.drawImage(logo_path, 54, 732, width=34, height=34, mask='auto')
                logo_offset = 98
            except:
                pass
        
        # Header Typography (iOS Minimalist Style)
        self.setFont("Helvetica-Bold", 11)
        self.setFillColor(colors.HexColor("#1D1D1F")) # Pure Apple Dark
        self.drawString(logo_offset, 746, "NYXARA SYSTEM")
        
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#86868B")) # Muted Executive Grey
        self.drawRightString(612 - 54, 746, "AUTOMATED DIGITAL ASSET // PRIVÉ")
        
        # Architectural Micro-Line
        self.setStrokeColor(colors.HexColor("#E5E5EA"))
        self.setLineWidth(0.5)
        self.line(54, 718, 612 - 54, 718)
        
        # Minimalist Footer Grid
        self.line(54, 65, 612 - 54, 65)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#86868B"))
        self.drawString(54, 46, "DESIGNED BY NYXARA INTELLIGENCE LABS")
        
        # Clean Page Metrics
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(colors.HexColor("#1D1D1F"))
        self.drawRightString(612 - 54, 46, f"PAGE {self._pageNumber:02d} / {page_count:02d}")
        self.restoreState()

# =========================================================================
# 2. PREMIUM PDF ARCHITECT (Layout & Typography)
# =========================================================================
def generate_premium_pdf(raw_data_string, pdf_name="NYXARA_Premium_Asset.pdf"):
    clean_string = raw_data_string.strip()
    if clean_string.startswith("data ="):
        clean_string = clean_string.replace("data =", "", 1).strip()
    bundle_data = ast.literal_eval(clean_string)
    
    # Grid System Margins
    doc = SimpleDocTemplate(
        pdf_name, 
        pagesize=letter, 
        leftMargin=54, 
        rightMargin=54, 
        topMargin=100, 
        bottomMargin=95
    )
    styles = getSampleStyleSheet()
    story = []
    
    # Advanced Typography Hierarchy
    title_style = ParagraphStyle("T", fontName="Helvetica-Bold", fontSize=23, leading=28, textColor=colors.HexColor("#1D1D1F"), spaceAfter=14)
    desc_style = ParagraphStyle("D", fontName="Helvetica", fontSize=11, leading=17, textColor=colors.HexColor("#424245"), spaceAfter=28)
    
    # Premium Prompt Container Typography
    prompt_content_style = ParagraphStyle("PC", fontName="Courier", fontSize=9.5, leading=15, textColor=colors.HexColor("#1D1D1F"))
    
    meta_style = ParagraphStyle("M", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=colors.HexColor("#0071E3"), spaceAfter=10)
    how_style = ParagraphStyle("H", fontName="Helvetica", fontSize=10.5, leading=16, textColor=colors.HexColor("#1D1D1F"))
    
    for index, item in enumerate(bundle_data):
        story.append(Spacer(1, 10))
        
        # 1. Title Block
        story.append(Paragraph(item["title"].upper(), title_style))
        
        # 2. Description with Premium Electric Blue Tags
        desc_text = re.sub(r"\[(.*?)\]", r"<font color='#0071E3'><b>\1</b></font>", item["description"])
        story.append(Paragraph(desc_text, desc_style))
        
        # 3. Upgraded Premium Prompt Card Box (With Solid Accent Left Border)
        prompt_p = Paragraph(item["prompt"].replace("\n", "<br/>"), prompt_content_style)
        
        # Table matrix layout to create a high-end designer block
        container_table = Table([[prompt_p]], colWidths=[504])
        container_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F5F5F7")), # Clean Card Background
            ('TOPPADDING', (0,0), (-1,-1), 16),
            ('BOTTOMPADDING', (0,0), (-1,-1), 16),
            ('LEFTPADDING', (0,0), (-1,-1), 18),
            ('RIGHTPADDING', (0,0), (-1,-1), 18),
            ('LINELEFT', (0,0), (0,-1), 3.5, colors.HexColor("#0071E3")), # Elegant Thick Blue Left Line
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E5E5EA")), # Light outer border
        ]))
        story.append(container_table)
        story.append(Spacer(1, 28))
        
        # 4. Roadmap Block
        story.append(Paragraph("SYSTEM EXECUTION ROADMAP", meta_style))
        story.append(Paragraph(item["how_to_use"].replace("\n", "<br/>"), how_style))
        
        if index < len(bundle_data) - 1:
            story.append(PageBreak())
            
    doc.build(story, canvasmaker=NumberedCanvas)
    return pdf_name

# =========================================================================
# 3. MODERN WEB UI INTERFACE (Minimalist Luxury Styling)
# =========================================================================
st.set_page_config(page_title="NYXARA CLOUD SYSTEM", page_icon="🌌", layout="centered")

# Inject Custom CSS for Premium Look & Mobile Responsiveness
st.markdown("""
    <style>
    .main {background-color: #FBFBFD;}
    .stTextArea textarea {border-radius: 12px; border: 1px solid #E5E5EA; font-family: 'Courier New', monospace;}
    .stButton>button {width: 100%; border-radius: 10px; font-weight: bold; height: 3em; background-color: #111111 !important; color: white !important;}
    .stTabs [data-baseweb="tab"] {font-weight: bold; color: #86868B;}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {color: #0071E3 !important; border-bottom-color: #0071E3 !important;}
    </style>
""", unsafe_allow_html=True)

st.title("🌌 NYXARA PRODUCTION ENGINE")
st.caption("The Ultra-Premium Cloud Architecture for Digital Assets")
st.markdown("---")

tab1, tab2 = st.tabs(["🚀 ENGINE WORKSPACE", "⚙️ CORE SERVER SETTINGS"])

with tab2:
    st.subheader("Master Brand Identity Setup")
    st.markdown("Setup your luxury brand logo once. It will stay locked in the server engine.")
    
    # Show current logo preview if it exists
    if os.path.exists(SAVED_LOGO_PATH):
        st.image(SAVED_LOGO_PATH, width=80, caption="Currently Active Core Logo")
        
    uploaded_logo = st.file_uploader("Upload New Logo (.png / .jpg)", type=["png", "jpg", "jpeg"])
    if uploaded_logo:
        with open(SAVED_LOGO_PATH, "wb") as f:
            f.write(uploaded_logo.getbuffer())
        st.success("🔥 SUCCESS: Logo locked into Server Core! Now switch to the Workspace tab.")

with tab1:
    input_data = st.text_area("Paste Your ChatGPT Python Code Block Here", placeholder="data = [...]", height=320)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("ENGINEER & COMPILE PREMIUM PDF"):
        if input_data:
            with st.spinner("Engineering master asset layers..."):
                try:
                    pdf_file = generate_premium_pdf(input_data)
                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            label="📥 DOWNLOAD CRUNCHED LUXURY ASSET", 
                            data=f, 
                            file_name=pdf_file, 
                            mime="application/pdf"
                        )
                    st.balloons()
                    st.success("✨ COMPILATION COMPLETE: PDF generated with ultra-sharp vector rendering!")
                except Exception as e:
                    st.error(f"❌ FORMAT ERROR: Make sure data starts with data = [...] and contains proper keys. Log: {str(e)}")
        else:
            st.warning("Pehle ChatGPT wala data toh paste karo bhai!")
