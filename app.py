# =========================================================================
# NYXARA OS V8 — THE ELECTRIC NEON STUDIO EDITION (FIXED DEFAULTS)
# PRODUCTION-READY BACKEND LOGIC + ANTI-OVERLAP TEXT ENGINE
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
# INITIALIZATION & STREAMLIT THEME CONFIG
# =========================================================
st.set_page_config(
    page_title="NYXARA OS V8 Electric Studio",
    page_icon="⚡",
    layout="wide",
)

PERMANENT_LOGO_NAME = "logo.png"
logo_exists = os.path.exists(PERMANENT_LOGO_NAME)

# =========================================================
# HIGH-ENERGY ELECTRIC NEON SAAS INTERFACE (CSS)
# =========================================================
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 10% 20%, #F4F7FB 0%, #FFFFFF 90%) !important;
    }
    h1, h2, h3, p, span, label {
        font-family: '-apple-system', BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
    }
    .premium-header {
        background: linear-gradient(135deg, #0D1117 0%, #00D2FF 100%);
        padding: 2.5rem;
        border-radius: 24px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0, 210, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    div[data-testid="stForm"], .stTextArea, .stTextInput, .stNumberInput {
        background-color: #FFFFFF !important;
        border-radius: 16px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 4px 20px rgba(0, 210, 255, 0.02) !important;
    }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    .status-badge {
        background: #F0FDFA;
        color: #0F766E;
        border: 1px solid #99F6E4;
        padding: 0.9rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #0071E3 0%, #00D2FF 100%) !important;
        color: #FFFFFF !important;
        border-radius: 14px !important;
        padding: 0.9rem 2rem !important;
        font-weight: 700 !important;
        border: none !important;
        letter-spacing: 0.03em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 25px rgba(0, 210, 255, 0.25) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(0, 210, 255, 0.4) !important;
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
# PDF DESIGN SCHEMATIC (ELECTRIC APPLE GUIDELINES)
# =========================================================
PAGE_WIDTH, PAGE_HEIGHT = letter
BRAND_NAME = "NYXARA LABS"

PDF_COLORS = {
    "text": "#1D1D1F",
    "muted": "#86868B",
    "bg_box": "#F5F5F7",
    "border_box": "#E5E7EB",
    "electric": "#0071E3",
    "line": "#E5E7EB"
}

styles = getSampleStyleSheet()

hero_style = ParagraphStyle(
    "ElHero", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=26, leading=34, textColor=colors.HexColor(PDF_COLORS["text"]), spaceAfter=22
)
title_style = ParagraphStyle(
    "ElTitle", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=18, leading=24, textColor=colors.HexColor(PDF_COLORS["text"]), spaceAfter=12
)
subtitle_style = ParagraphStyle(
    "ElSubtitle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=11, leading=17, textColor=colors.HexColor(PDF_COLORS["muted"]), spaceAfter=16
)
body_style = ParagraphStyle(
    "ElBody", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10, leading=16, textColor=colors.HexColor(PDF_COLORS["text"]), spaceAfter=14
)
accent_label = ParagraphStyle(
    "ElAccent", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=8.5, leading=13, textColor=colors.HexColor(PDF_COLORS["electric"]), spaceAfter=6, letterSpacing=0.5
)
box_prompt_style = ParagraphStyle(
    "ElBoxPrompt", parent=styles["Code"], fontName="Courier",
    fontSize=9, leading=15, textColor=colors.HexColor(PDF_COLORS["text"])
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
        total_pages = len(self.pages)
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
        self.drawRightString(PAGE_WIDTH - 54, PAGE_HEIGHT - 37, "PRODUCTION OS LAYER // ACTIVE")
        
        self.setStrokeColor(colors.HexColor(PDF_COLORS["line"]))
        self.setLineWidth(0.5)
        self.line(54, PAGE_HEIGHT - 48, PAGE_WIDTH - 54, PAGE_HEIGHT - 48)

        self.line(54, 46, PAGE_WIDTH - 54, 46)
        self.drawString(54, 32, "Operational Editorial Studio Automation Asset")
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
# ARCHITECTURE PAGES
# =========================================================
def render_cover(story, cover_path, title, niche):
    story.append(Spacer(1, 120))
    if cover_path and os.path.exists(cover_path):
        try:
            story.append(Image(cover_path, width=PAGE_WIDTH - 108, height=300))
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
    story.append(Spacer(1, 20))
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
    ]

    for label, detailed_text in content_blocks:
        if detailed_text:
            story.append(Paragraph(label, accent_label))
            story.append(Paragraph(safe_xml_text(detailed_text), body_style))
            story.append(Spacer(1, 4))

    if item.get("prompt"):
        story.append(Spacer(1, 8))
        story.append(Paragraph("RAW SYSTEM AUTOMATION PROMPT MATRIX", accent_label))
        
        raw_prompt_paragraph = Paragraph(safe_xml_text(item.get("prompt")), box_prompt_style)
        box_container_width = PAGE_WIDTH - 108
        prompt_box_table = Table([[raw_prompt_paragraph]], colWidths=[box_container_width])
        prompt_box_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(PDF_COLORS["bg_box"])),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor(PDF_COLORS["border_box"])),
            ('PADDING', (0,0), (-1,-1), 14),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(prompt_box_table)
        
    story.append(PageBreak())

def render_outro(story):
    story.append(Spacer(1, 200))
    story.append(Paragraph("THE SILENT COMPOUNDING", accent_label))
    story.append(Paragraph("The goal was never to create more noise. The goal was to build calmer execution.", hero_style))
    inject_divider(story)
    
    outro_touching_text = """
    Yahan par aapka blueprint khatam nahi hota, balki aapki scale shuru hoti hai. Craftsmanship wahi sahi hai jo waqt ke saath bikhre nahi. Jab aap is engine ke prompts aur systems ko use karenge, yaad rakhna ki har ek systemized pipeline aapko aapka waqt waapis deti hai.
    <br/><br/>
    Agar is system ko kisi naye operational module ke liye upgrade karna ho, ya custom workflow API inject karna ho, toh dashboard console hamesha ready hai. Go ahead, execute beautifully.
    """
    story.append(Paragraph(outro_touching_text, body_style))
    story.append(PageBreak())

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
# FRONTEND INTERFACE WORKSPACE CONTROLLER
# =========================================================
st.markdown("""
    <div class="premium-header">
        <h1 style='margin:0; font-size: 2.4rem; font-weight: 800; letter-spacing: -0.03em;'>⚡ NYXARA PREMIA STUDIO V8</h1>
        <p style='margin:6px 0 0 0; opacity: 0.9; font-size: 1.1rem; font-weight: 400;'>Ultra-Premium Light Electric Aesthetic Dashboard</p>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🎛️ Engine Parameters")
    
    if logo_exists:
        st.markdown(f'<div class="status-badge">🔒 CACHE SECURE<br/>"{PERMANENT_LOGO_NAME}" permanently active.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge" style="border-color:#00D2FF; background:#F0FDFB; color:#0891B2;">⚡ DYNAMIC LOGO<br/>Text layout fallback active.</div>', unsafe_allow_html=True)
        
    st.markdown("---")
    # DEFAULT RESET: Back to standard production metrics to avoid array out-of-bounds error
    ui_main_count = st.number_input("Core Operational Prompts", min_value=1, value=4)
    ui_bonus_count = st.number_input("Secondary Bonus Prompts", min_value=0, value=1)
    
    st.markdown("---")
    uploaded_cover = st.file_uploader("Layer Cover Page Image", type=["png", "jpg", "jpeg"])
    uploaded_logo = st.file_uploader("Override System Logo Asset", type=["png", "jpg", "jpeg"])

col_meta_left, col_meta_right = st.columns(2)
with col_meta_left:
    asset_title = st.text_input("Operational Blueprint Title", value="Retro Packaging Design Operations System")
with col_meta_right:
    asset_niche = st.text_input("Target Asset Micro-Niche", value="Vintage Packaging Design")

st.markdown
