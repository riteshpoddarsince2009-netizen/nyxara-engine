# =========================================================================
# NYXARA OS V8 — THE BULLETPROOF REFRESH EDITION (ZERO LAYOUT ERRORS)
# FRONT-FACING MAIN PANEL CONTROLS + STABLE MULTI-PAGE FLOW ENGINE
# =========================================================================

import streamlit as st
import ast
import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
    HRFlowable,
    Table,
    TableStyle,
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# =========================================================
# INITIALIZATION & STREAMLIT CONFIG
# =========================================================
st.set_page_config(
    page_title="NYXARA OS V8 Ultimate Refresh",
    page_icon="⚡",
    layout="wide",
)

PERMANENT_LOGO_NAME = "logo.png"
logo_exists = os.path.exists(PERMANENT_LOGO_NAME)

# High-Energy Electric Neon Styling
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 10% 20%, #F4F7FB 0%, #FFFFFF 90%) !important;
    }
    h1, h2, h3, p, span, label {
        font-family: '-apple-system', BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
    }
    .premium-header {
        background: linear-gradient(135deg, #090D16 0%, #0052D4 50%, #4364F7 100%);
        padding: 2.5rem;
        border-radius: 24px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(67, 100, 247, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    div[data-testid="stForm"], .stTextArea, .stTextInput, .stNumberInput {
        background-color: #FFFFFF !important;
        border-radius: 16px !important;
        border: 1px solid #E2E8F0 !important;
    }
    .section-container {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #0052D4 0%, #4364F7 100%) !important;
        color: #FFFFFF !important;
        border-radius: 14px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 8px 25px rgba(67, 100, 247, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

def safe_xml_text(text):
    if not text:
        return ""
    text = str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = text.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
    text = text.replace("&lt;br/&gt;", "<br/>").replace("&lt;br&gt;", "<br/>")
    return text.replace("\n", "<br/>")

# =========================================================
# PDF STYLE SCHEMATICS (STRICT METRICS TO PREVENT CLASH)
# =========================================================
PAGE_WIDTH, PAGE_HEIGHT = letter
BRAND_NAME = "NYXARA LABS"

PDF_COLORS = {
    "text": "#1D1D1F",
    "muted": "#6E6E73",
    "bg_box": "#F5F5F7",
    "border_box": "#D2D2D7",
    "electric": "#0066CC",
    "line": "#E5E5EA"
}

styles = getSampleStyleSheet()

hero_style = ParagraphStyle(
    "ElHero", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=24, leading=32, textColor=colors.HexColor(PDF_COLORS["text"]), spaceAfter=20
)
title_style = ParagraphStyle(
    "ElTitle", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=16, leading=22, textColor=colors.HexColor(PDF_COLORS["text"]), spaceAfter=10
)
subtitle_style = ParagraphStyle(
    "ElSubtitle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=11, leading=16, textColor=colors.HexColor(PDF_COLORS["muted"]), spaceAfter=14
)
body_style = ParagraphStyle(
    "ElBody", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10, leading=16, textColor=colors.HexColor(PDF_COLORS["text"]), spaceAfter=12
)
accent_label = ParagraphStyle(
    "ElAccent", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=8.5, leading=12, textColor=colors.HexColor(PDF_COLORS["electric"]), spaceAfter=6, letterSpacing=0.5
)
box_prompt_style = ParagraphStyle(
    "ElBoxPrompt", parent=styles["Code"], fontName="Courier",
    fontSize=9, leading=14, textColor=colors.HexColor(PDF_COLORS["text"])
)

class ElectricStudioCanvas(canvas.Canvas):
    def __init__(self, *args, logo_path=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []
        self.logo_path = logo_path

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for page in self.pages:
            self.__dict__.update(page)
            if self._pageNumber > 1:
                self.draw_decorations()
            super().showPage()
        super().save()

    def draw_decorations(self):
        self.saveState()
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                self.drawImage(self.logo_path, 54, PAGE_HEIGHT - 42, width=16, height=16, mask='auto')
                self.setFont("Helvetica-Bold", 8)
                self.setFillColor(colors.HexColor(PDF_COLORS["text"]))
                self.drawString(76, PAGE_HEIGHT - 37, BRAND_NAME)
            except:
                self.draw_fallback_logo()
        else:
            self.draw_fallback_logo()

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor(PDF_COLORS["muted"]))
        self.drawRightString(PAGE_WIDTH - 54, PAGE_HEIGHT - 37, "PRODUCTION OS ACTIVE")
        
        self.setStrokeColor(colors.HexColor(PDF_COLORS["line"]))
        self.setLineWidth(0.5)
        self.line(54, PAGE_HEIGHT - 48, PAGE_WIDTH - 54, PAGE_HEIGHT - 48)
        self.line(54, 46, PAGE_WIDTH - 54, 46)
        self.drawString(54, 32, "Creative Operations Core Asset Blueprint")
        self.drawRightString(PAGE_WIDTH - 54, 32, f"PAGE {self._pageNumber}")
        self.restoreState()

    def draw_fallback_logo(self):
        self.setFont("Helvetica-Bold", 9)
        self.setFillColor(colors.HexColor(PDF_COLORS["electric"]))
        self.drawString(54, PAGE_HEIGHT - 37, f"⚡ {BRAND_NAME}")

def inject_divider(story):
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor(PDF_COLORS["line"]), spaceAfter=14))

# =========================================================
# SYSTEM PAGE RENDERERS (FLOWABLE SAFE)
# =========================================================
def render_cover(story, cover_path, title, niche):
    story.append(Spacer(1, 120))
    if cover_path and os.path.exists(cover_path):
        try:
            story.append(Image(cover_path, width=PAGE_WIDTH - 108, height=280))
            story.append(Spacer(1, 40))
        except:
            story.append(Spacer(1, 100))
    else:
        story.append(Spacer(1, 100))
        
    story.append(Paragraph(safe_xml_text(title.upper()), hero_style))
    story.append(Paragraph(f"DESIGNED FOR THE QUIET EXECUTORS // MICRO-NICHE: {safe_xml_text(niche.upper())}", subtitle_style))
    story.append(PageBreak())

def render_intro(story, title, niche, total_count, bonus_count):
    story.append(Spacer(1, 40))
    story.append(Paragraph("THE ARCHITECTURE OF ALIGNMENT", accent_label))
    story.append(Paragraph("SYSTEM INTRODUCTION", hero_style))
    inject_divider(story)
    
    heart_touching_copy = f"""
    Systems are not built to restrict creativity; they are built to set it free.
    <br/><br/>
    Har creative operator ka ek hi sabse bada dushman hota hai—<b>The Blank Screen Panic</b>. Jab har naya kaam ek naye experimentation jaisa lagne lage, toh exhaustion dimaag par haavi hone lagta hai. Ye blueprint koi random automated generator nahi hai. Ye ek systemized inheritance hai.
    <br/><br/>
    Is pure asset ko ek hi maqsad se deploy kiya gaya hai: Taaki aapki subah bina creative anxiety ke shuru ho, aapka workflow ek predictable art ban sake, aur aapka content quietly market me compound kare. Quality is not an accident; it's a product of consistent infrastructure inside the <b>{safe_xml_text(niche)}</b> domain.
    <br/><br/>
    <b>Structural Breakdown Inside This Deployment Asset:</b><br/>
    • {total_count - bonus_count} Core Operational Production Vectors<br/>
    • {bonus_count} Secondary Bonus Infrastructure Assets<br/>
    • Built-in Quality Control boxes and secure execution blueprints.
    """
    story.append(Paragraph(heart_touching_copy, body_style))
    story.append(PageBreak())

def render_table_of_contents(story, main_prompts, bonus_prompts):
    story.append(Spacer(1, 40))
    story.append(Paragraph("SYSTEM ARCHITECTURE INDEX", accent_label))
    story.append(Paragraph("TABLE OF CONTENTS", hero_style))
    inject_divider(story)
    
    story.append(Paragraph("PRIMARY EXECUTION MAP", accent_label))
    story.append(Spacer(1, 6))
    for i, item in enumerate(main_prompts, start=1):
        story.append(Paragraph(f"<b>SYSTEM {i:02d}</b> — {safe_xml_text(item.get('title', 'Untitled Production Node'))}", body_style))
        
    if bonus_prompts:
        story.append(Spacer(1, 22))
        story.append(Paragraph("BONUS OPERATIONS MAP", accent_label))
        story.append(Spacer(1, 6))
        start_bonus_idx = len(main_prompts) + 1
        for i, item in enumerate(bonus_prompts):
            story.append(Paragraph(f"<b>BONUS {start_bonus_idx + i:02d}</b> — {safe_xml_text(item.get('title', 'Untitled Bonus Vector'))}", body_style))
            
    story.append(PageBreak())

def render_prompt_card(story, item, current_display_num, is_bonus=False):
    story.append(Spacer(1, 15))
    heading_tag = f"BONUS MODULE DEPLOYMENT {current_display_num:02d}" if is_bonus else f"CORE PRODUCTION VECTOR {current_display_num:02d}"
    
    story.append(Paragraph(heading_tag, accent_label))
    story.append(Paragraph(safe_xml_text(item.get("title", "Untitled Base Parameter")), title_style))
    if item.get("description"):
        story.append(Paragraph(safe_xml_text(item.get("description")), subtitle_style))
        
    inject_divider(story)

    content_blocks = [
        ("STRATEGIC DEPLOYMENT MOTIVATION", item.get("why_this_works")),
        ("OPERATIONAL STEP-BY-STEP USE CASE", item.get("how_to_use")),
        ("MICRO VALIDATION EXAMPLE", item.get("micro_example")),
        ("BUSINESS & MONETIZATION ROADMAP", item.get("business_application")),
        ("VALIDATION CASE STUDY", item.get("validation_case_study")),
    ]

    for label, detailed_text in content_blocks:
        if detailed_text:
            story.append(Paragraph(label, accent_label))
            story.append(Paragraph(safe_xml_text(detailed_text), body_style))
            story.append(Spacer(1, 4))

    if 'ecosystem_assets' in item and isinstance(item['ecosystem_assets'], dict):
        story.append(Paragraph("ECOSYSTEM INVENTORY ASSETS", accent_label))
        for asset_key, asset_val in item['ecosystem_assets'].items():
            clean_key = asset_key.replace('_', ' ').upper()
            story.append(Paragraph(f"<b>• {clean_key}:</b> {safe_xml_text(asset_val)}", body_style))
        story.append(Spacer(1, 6))

    # NO KEEP-TOGETHER FOR PROMPT PACK: Let massive text naturally break pages!
    if item.get("prompt"):
        story.append(Spacer(1, 8))
        story.append(Paragraph("RAW SYSTEM AUTOMATION PROMPT MATRIX", accent_label))
        
        raw_prompt_paragraph = Paragraph(safe_xml_text(item.get("prompt")), box_prompt_style)
        box_container_width = PAGE_WIDTH - 108
        prompt_box_table = Table([[raw_prompt_paragraph]], colWidths=[box_container_width])
        prompt_box_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(PDF_COLORS["bg_box"])),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor(PDF_COLORS["border_box"])),
            ('PADDING', (0,0), (-1,-1), 12),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(prompt_box_table)
        
    story.append(PageBreak())

def render_outro(story):
    story.append(Spacer(1, 150))
    story.append(Paragraph("THE SILENT COMPOUNDING", accent_label))
    story.append(Paragraph("The goal was never to create more noise. The goal was to build calmer execution.", hero_style))
    inject_divider(story)
    
    outro_touching_text = """
    Yahan par aapka blueprint khatam nahi hota, balki aapki scale shuru hoti hai. Craftsmanship wahi sahi hai jo waqt ke saath bikhre nahi. Jab aap is engine ke prompts aur systems ko use karenge, yaad rakhna ki har ek systemized pipeline aapko aapka waqt waapis deti hai.
    <br/><br/>
    Go ahead, execute beautifully.
    """
    story.append(Paragraph(outro_touching_text, body_style))

def execute_pdf_compilation(payload, title, niche, main_count, bonus_count, cover_path=None, logo_path=None):
    target_output = "NYXARA_ELECTRIC_STUDIO_OS.pdf"
    sliced_main = payload[:main_count]
    sliced_bonus = payload[main_count:]

    doc = SimpleDocTemplate(
        target_output, pagesize=letter,
        rightMargin=54, leftMargin=54, topMargin=72, bottomMargin=64
    )
    storyboard = []

    render_cover(storyboard, cover_path, title, niche)
    render_intro(storyboard, title, niche, len(payload), bonus_count)
    render_table_of_contents(storyboard, sliced_main, sliced_bonus)
    
    for index, parameter in enumerate(sliced_main, start=1):
        render_prompt_card(storyboard, parameter, index, is_bonus=False)

    base_bonus_offset = main_count + 1
    for index, parameter in enumerate(sliced_bonus):
        render_prompt_card(storyboard, parameter, base_bonus_offset + index, is_bonus=True)

    render_outro(storyboard)
    doc.build(storyboard, canvasmaker=lambda *args, **kwargs: ElectricStudioCanvas(*args, logo_path=logo_path, **kwargs))
    return target_output

# =========================================================
# FRONTEND CONTROL INTERFACE
# =========================================================
st.markdown("""
    <div class="premium-header">
        <h1 style='margin:0; font-size: 2.4rem; font-weight: 800; letter-spacing: -0.03em;'>⚡ NYXARA REFRESH STUDIO V8</h1>
        <p style='margin:6px 0 0 0; opacity: 0.9; font-size: 1.1rem; font-weight: 400;'>Ultra-Premium Front-Control Automation Dashboard</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("### 🎛️ SYSTEM ARCHITECTURE SETTINGS")
col_inputs_1, col_inputs_2 = st.columns(2)

with col_inputs_1:
    st.markdown("<div class='section-container'>", unsafe_allow_html=True)
    ui_main_count = st.number_input("👉 Number of Main Prompts", min_value=1, value=4)
    st.markdown("</div>", unsafe_allow_html=True)

with col_inputs_2:
    st.markdown("<div class='section-container'>", unsafe_allow_html=True)
    ui_bonus_count = st.number_input("👉 Number of Bonus Prompts", min_value=0, value=1)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### 🖼️ BRAND DESIGN ASSETS (OPTIONAL)")
col_assets_1, col_assets_2 = st.columns(2)
with col_assets_1:
    uploaded_cover = st.file_uploader("Upload Cover Image", type=["png", "jpg", "jpeg"])
with col_assets_2:
    uploaded_logo = st.file_uploader("Upload Logo Branding Override", type=["png", "jpg", "jpeg"])

st.markdown("### 📝 METADATA INFRASTRUCTURE")
col_meta_left, col_meta_right = st.columns(2)
with col_meta_left:
    asset_title = st.text_input("Operational Blueprint Title", value="Retro Packaging Design Operations System")
with col_meta_right:
    asset_niche = st.text_input("Target Asset Micro-Niche", value="Vintage Packaging Design")

st.markdown("<br/>", unsafe_allow_html=True)
payload_text_area = st.text_area("📋 DROP YOUR PYTHON ARRAY DATA PAYLOAD HERE", height=250, placeholder="data = [...]")

if st.button("🚀 COMPILE ARCHITECTURE & GENERATE PDF", use_container_width=True):
    payload_text_area = payload_text_area.strip()
    if payload_text_area.startswith("data ="):
        payload_text_area = payload_text_area.replace("data =", "", 1).strip()
        
    try:
        sanitized_array = ast.literal_eval(payload_text_area)
    except Exception as failure_reason:
        sanitized_array = None
        st.error(f"Payload Error: Structural syntax parser failure. Details: {failure_reason}")
        
    if sanitized_array is not None:
        if not isinstance(sanitized_array, list):
            st.error("Format Error: Input data must wrap inside a standard Python list framework.")
        else:
            actual_count = len(sanitized_array)
            expected_count = ui_main_count + ui_bonus_count
            
            # Pure Bulletproof Fallback Logic
            if actual_count != expected_count:
                st.warning(f"💡 Auto-Adjust Active: Configuration standard matched smoothly to your 5-item list layout.")
                if actual_count >= ui_main_count:
                    ui_bonus_count = actual_count - ui_main_count
                else:
                    ui_main_count = actual_count
                    ui_bonus_count = 0

            final_active_logo = PERMANENT_LOGO_NAME if logo_exists else None
            if uploaded_logo:
                final_active_logo = "logo_runtime_override.png"
                with open(final_active_logo, "wb") as f:
                    f.write(uploaded_logo.getbuffer())

            final_active_cover = None
            if uploaded_cover:
                final_active_cover = "cover_runtime_temp.png"
                with open(final_active_cover, "wb") as f:
                    f.write(uploaded_cover.getbuffer())

            # SAFE COMPILATION TRIGGER
            output_pdf_filepath = execute_pdf_compilation(
                sanitized_array, asset_title, asset_niche, 
                ui_main_count, ui_bonus_count, 
                final_active_cover, final_active_logo
            )

            with open(output_pdf_filepath, "rb") as delivery_ready_file:
                st.markdown("<br/>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 DOWNLOAD REFRESHED ELECTRIC BLUE STUDIO PDF",
                    data=delivery_ready_file,
                    file_name=output_pdf_filepath,
                    use_container_width=True
                )
            st.success("Compilation complete! Your solid premium PDF is fully ready.")
