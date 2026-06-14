# =========================================================================
# NYXARA OS V8 — THE ULTRA-PREMIUM LUXURY STUDIO EDITION
# OLD-SCHOOL SYSTEM INTEGRITY MEETS FUTURISTIC DESIGN
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
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# =========================================================
# INITIALIZATION & LOGIC LOCKS
# =========================================================
st.set_page_config(
    page_title="NYXARA OS V8 Pro Studio",
    page_icon="👑",
    layout="wide",
)

PERMANENT_LOGO_NAME = "logo.png"
logo_exists = os.path.exists(PERMANENT_LOGO_NAME)

# =========================================================
# THE ULTIMATE ANTI-DEPRESSION VISUAL GLOW-UP (CUSTOM CSS)
# =========================================================
st.markdown("""
    <style>
    /* Main App Workspace Canvas */
    .stApp {
        background: radial-gradient(circle at top right, #F5F7FF, #FAFAFA) !important;
    }
    
    /* Global Typography Reset */
    h1, h2, h3, h4, p, span, label {
        font-family: '-apple-system', BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, sans-serif !important;
    }
    
    /* Next-Gen Glassmorphic Premium Header */
    .premium-header {
        background: linear-gradient(135deg, #4F46E5 0%, #06B6D4 100%);
        padding: 3rem 2.5rem;
        border-radius: 24px;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 40px -15px rgba(79, 70, 229, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Clean Control Dashboard Cards */
    div[data-testid="stForm"], .stTextArea, .stTextInput, .stNumberInput {
        background-color: #FFFFFF !important;
        border-radius: 16px !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -1px rgba(0, 0, 0, 0.02) !important;
        padding: 5px !important;
    }
    
    /* High-contrast labels */
    label[data-testid="stWidgetLabel"] p {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.03em;
    }

    /* Sidebar Dashboard Control Panel */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #F3F4F6 !important;
    }
    
    /* Soft Pill Badges for System Tracking */
    .status-badge-secure {
        background: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
        padding: 0.75rem 1.2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 1.5rem;
    }
    .status-badge-warn {
        background: #FFFBEB;
        color: #B45309;
        border: 1px solid #FDE68A;
        padding: 0.75rem 1.2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 1.5rem;
    }
    
    /* Luxury High-Energy Button Matrix */
    .stButton>button {
        background: linear-gradient(135deg, #111827 0%, #1F2937 100%) !important;
        color: #FFFFFF !important;
        border-radius: 14px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em;
        border: none !important;
        box-shadow: 0 10px 20px -5px rgba(17, 24, 39, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 30px -5px rgba(79, 70, 229, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# GLOBAL ENGINE CONSTANTS & DESIGN STYLES (PDF)
# =========================================================
PAGE_WIDTH, PAGE_HEIGHT = letter
BRAND_NAME = "NYXARA LABS"

COLORS = {
    "bg": "#FAFAFA",
    "text": "#111111",
    "muted": "#4B5563",
    "line": "#E5E7EB",
    "soft": "#F9FAFB",
    "accent": "#4F46E5", 
}

styles = getSampleStyleSheet()

hero_style = ParagraphStyle(
    "Hero", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=32, leading=40, textColor=colors.HexColor(COLORS["text"]), spaceAfter=26
)
title_style = ParagraphStyle(
    "Title", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=20, leading=28, textColor=colors.HexColor(COLORS["text"]), spaceAfter=12
)
subtitle_style = ParagraphStyle(
    "Subtitle", parent=styles["Normal"], fontName="Helvetica",
    fontSize=11, leading=20, textColor=colors.HexColor(COLORS["muted"]), spaceAfter=18
)
body_style = ParagraphStyle(
    "Body", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10.5, leading=19, textColor=colors.HexColor("#1F2937"), spaceAfter=14
)
small_style = ParagraphStyle(
    "Small", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=8.5, leading=12, textColor=colors.HexColor(COLORS["accent"]), spaceAfter=4
)
quote_style = ParagraphStyle(
    "Quote", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=24, leading=36, alignment=1, textColor=colors.HexColor(COLORS["text"])
)
prompt_style = ParagraphStyle(
    "Prompt", parent=styles["Code"], fontName="Courier",
    fontSize=9, leading=16, textColor=colors.HexColor("#111827"),
    backColor=colors.HexColor(COLORS["soft"]), borderColor=colors.HexColor(COLORS["line"]),
    borderWidth=0.5, borderPadding=16, spaceBefore=6, spaceAfter=14
)

# =========================================================
# LOGIC CORE FUNCTIONS
# =========================================================
def safe_parse(raw):
    raw = raw.strip()
    if raw.startswith("data ="):
        raw = raw.replace("data =", "", 1)
    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, list):
            return parsed
    except:
        return []
    return []

class EditorialCanvas(canvas.Canvas):
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
            self.draw_layout(total_pages)
            super().showPage()
        super().save()

    def draw_layout(self, total_pages):
        self.saveState()
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                self.drawImage(self.logo_path, 50, PAGE_HEIGHT - 42, width=18, height=18, mask='auto')
                self.setFont("Helvetica-Bold", 8)
                self.setFillColor(colors.HexColor("#111827"))
                self.drawString(76, PAGE_HEIGHT - 35, BRAND_NAME)
            except:
                self.setFont("Helvetica-Bold", 8)
                self.drawString(50, PAGE_HEIGHT - 35, BRAND_NAME)
        else:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#111827"))
            self.drawString(50, PAGE_HEIGHT - 35, BRAND_NAME)

        self.drawRightString(PAGE_WIDTH - 50, PAGE_HEIGHT - 35, "CREATIVE OPERATIONS SYSTEM")
        self.setStrokeColor(colors.HexColor(COLORS["line"]))
        self.line(50, PAGE_HEIGHT - 48, PAGE_WIDTH - 50, PAGE_HEIGHT - 48)

        # Footer Setup
        self.line(50, 42, PAGE_WIDTH - 50, 42)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#6B7280"))
        self.drawString(50, 28, "Operational Editorial Publishing System")
        self.drawRightString(PAGE_WIDTH - 50, 28, f"PAGE {self._pageNumber}")
        self.restoreState()

def divider(story):
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor(COLORS["line"])))
    story.append(Spacer(1, 18))

# =========================================================
# LAYOUT GRAPHICS ENGINE
# =========================================================
def render_cover(story, cover_path, bundle_title, niche):
    if cover_path and os.path.exists(cover_path):
        story.append(Image(cover_path, width=PAGE_WIDTH - 100, height=PAGE_HEIGHT - 140))
    else:
        story.append(Spacer(1, 240))
        story.append(Paragraph(bundle_title.upper(), hero_style))
        story.append(Paragraph(niche, subtitle_style))
    story.append(PageBreak())

def render_intro(story, bundle_title, niche, total_prompts, bonus_count):
    story.append(Spacer(1, 80))
    story.append(Paragraph(bundle_title.upper(), hero_style))
    story.append(Paragraph(f"{total_prompts} operational AI systems designed for structured execution inside the <b>{niche}</b> niche.", subtitle_style))
    divider(story)

    intro = f"""
    This operating system was built for creators, freelancers, agencies, and operators who want more consistency inside their creative workflows.
    <br/><br/>
    Instead of relying on random prompting, disconnected experimentation, or repetitive manual work, this bundle focuses on operational clarity.
    """
    story.append(Paragraph(intro, body_style))
    story.append(PageBreak())

def render_contents(story, main_prompts, bonus_prompts):
    story.append(Paragraph("SYSTEM INDEX", hero_style))
    divider(story)
    story.append(Paragraph("MAIN SYSTEMS", small_style))
    story.append(Spacer(1, 10))

    for i, item in enumerate(main_prompts, start=1):
        story.append(Paragraph(f"{i:02d} — {item.get('title', 'Untitled')}", body_style))

    if bonus_prompts:
        story.append(Spacer(1, 28))
        story.append(Paragraph("BONUS SYSTEMS", small_style))
        story.append(Spacer(1, 10))
        for i, item in enumerate(bonus_prompts, start=1):
            story.append(Paragraph(f"BONUS {i:02d} — {item.get('title', 'Untitled')}", body_style))
    story.append(PageBreak())

def render_prompt_card(story, item, number, bonus=False):
    label = f"BONUS SYSTEM {number:02d}" if bonus else f"SYSTEM {number:02d}"
    story.append(Paragraph(label, small_style))
    story.append(Paragraph(item.get("title", "Untitled").upper(), title_style))
    story.append(Paragraph(item.get("description", ""), subtitle_style))
    divider(story)

    sections = [
        ("WHY THIS WORKS", item.get("why_this_works", "")),
        ("MICRO EXAMPLE", item.get("micro_example", "")),
        ("HOW TO USE", item.get("how_to_use", "")),
    ]
    for title, content in sections:
        if content:
            story.append(Paragraph(title, small_style))
            story.append(Paragraph(content.replace("\n", "<br/>"), body_style))
            story.append(Spacer(1, 8))

    story.append(Paragraph("OPERATIONAL PROMPT SYSTEM", small_style))
    prompt_text = item.get("prompt", "")
    if prompt_text:
        story.append(Paragraph(prompt_text.replace("\n", "<br/>"), prompt_style))
    story.append(PageBreak())

def generate_pdf(data, bundle_title, niche, main_count, bonus_count, cover_path=None, logo_path=None):
    pdf_name = "NYXARA_OS_V8.pdf"
    main_prompts = data[:main_count]
    bonus_prompts = data[main_count:]

    doc = SimpleDocTemplate(
        pdf_name, pagesize=letter,
        rightMargin=55, leftMargin=55, topMargin=70, bottomMargin=60
    )
    story = []

    render_cover(story, cover_path, bundle_title, niche)
    render_intro(story, bundle_title, niche, len(data), bonus_count)
    render_contents(story, main_prompts, bonus_prompts)
    
    story.append(Spacer(1, 220))
    story.append(Paragraph("Strong systems create calmer execution.", quote_style))
    story.append(PageBreak())

    for i, item in enumerate(main_prompts, start=1):
        render_prompt_card(story, item, i, bonus=False)

    if bonus_prompts:
        story.append(Spacer(1, 180))
        story.append(Paragraph("BONUS SYSTEMS", hero_style))
        story.append(PageBreak())
        for i, item in enumerate(bonus_prompts, start=1):
            render_prompt_card(story, item, i, bonus=True)

    doc.build(story, canvasmaker=lambda *args, **kwargs: EditorialCanvas(*args, logo_path=logo_path, **kwargs))
    return pdf_name

# =========================================================
# THE STUDIO INTERFACE WORKSPACE
# =========================================================

# Premium Branding Header Container
st.markdown("""
    <div class="premium-header">
        <h1 style='margin:0; font-size: 2.5rem; font-weight: 800; letter-spacing: -0.02em;'>👑 NYXARA STUDIO PRO OS</h1>
        <p style='margin:8px 0 0 0; opacity: 0.85; font-size: 1.1rem; font-weight: 400;'>The High-Energy Commercial Engine Workspace</p>
    </div>
""", unsafe_allow_html=True)

# Clean Sidebar Infrastructure
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    
    # Permanent Logo Validation UI
    if logo_exists:
        st.markdown(f'<div class="status-badge-secure">🔒 LOGO SYSTEM LOCK<br/><span style="font-weight:400; font-size:11px;">"{PERMANENT_LOGO_NAME}" is active inside structural cache.</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge-warn">⚠️ NO LOCAL LOGO FOUND<br/><span style="font-weight:400; font-size:11px;">Place "logo.png" inside the core system directory.</span></div>', unsafe_allow_html=True)
        
    st.markdown("---")
    main_count = st.number_input("Main System Assets", min_value=1, value=4)
    bonus_count = st.number_input("Bonus System Assets", min_value=0, value=1)
    
    st.markdown("---")
    cover_upload = st.file_uploader("Layer Cover Graphic Asset", type=["png", "jpg", "jpeg"])
    logo_upload = st.file_uploader("Override Cached Logo", type=["png", "jpg", "jpeg"])

# Primary Dynamic Workspace Columns
col_meta_1, col_meta_2 = st.columns(2)
with col_meta_1:
    bundle_title = st.text_input("Operational Bundle Title", value="Retro Packaging Design Operations System")
with col_meta_2:
    niche = st.text_input("Target Micro-Niche Segment", value="Vintage Packaging Design")

st.markdown("<br/>", unsafe_allow_html=True)

# High Volume Payload Input Block
raw_data = st.text_area("Drop Production Prompt Data Arrays Here", height=320, placeholder="data = [\n    {\n        'title': '01. System Engine',\n        ...\n    }\n]")

st.markdown("<br/>", unsafe_allow_html=True)

# Execution Control Terminal
if st.button("🚀 EXECUTE EDITORIAL SYSTEM COMPILATION", use_container_width=True):
    parsed = safe_parse(raw_data)
    if not parsed:
        st.error("Structural Payloads Error: Provided dataset mismatch with Python literal arrays.")
    else:
        total = len(parsed)
        if (main_count + bonus_count) != total:
            st.error(f"Configuration Discrepancy: Runtime expected {main_count + bonus_count} prompts, but payload provided {total} elements.")
        else:
            final_logo = PERMANENT_LOGO_NAME if logo_exists else None
            if logo_upload:
                final_logo = "logo_runtime_override.png"
                with open(final_logo, "wb") as f:
                    f.write(logo_upload.getbuffer())

            final_cover = None
            if cover_upload:
                final_cover = "cover_temp.png"
                with open(final_cover, "wb") as f:
                    f.write(cover_upload.getbuffer())

            pdf = generate_pdf(parsed, bundle_title, niche, main_count, bonus_count, final_cover, final_logo)

            with open(pdf, "rb") as f:
                st.markdown("<br/>", unsafe_allow_html=True)
                st.download_button("📥 DOWNLOAD PRODUCTION READY OPERATIONAL SYSTEM", f, file_name=pdf, use_container_width=True)
            st.success("Compilation Success. Layout assets loaded smoothly.")
