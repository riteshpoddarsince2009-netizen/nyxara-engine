import os
import ast
import re
import html
import textwrap
import tempfile
import time
from io import BytesIO
from PIL import Image as PILImage

import streamlit as st

# ReportLab Structural Grid Imports
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    NextPageTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
    KeepTogether,
    CondPageBreak,
)
from reportlab.lib.utils import ImageReader

# =========================================================
# SYSTEM CONFIG & PATHS MATRIX
# =========================================================

st.set_page_config(
    page_title="NYXARA ELECTRIC ENGINE v2.3",
    layout="wide",
    initial_sidebar_state="expanded",
)

ASSETS_DIR = "assets"
OUTPUTS_DIR = "outputs"
GENERATED_IMAGES_DIR = os.path.join(ASSETS_DIR, "generated_images")
LOGO_PATH = os.path.join(ASSETS_DIR, "locked_logo.png")

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(GENERATED_IMAGES_DIR, exist_ok=True)

PAGE_WIDTH, PAGE_HEIGHT = letter
BRAND_NAME = "NYXARA"
MAX_PROMPT_CHARS = 1400
MAX_INPUT_CHARS = 2_000_000
MAX_PROMPTS_GUARD = 200  
MAX_LINE_LENGTH_GUARD = 10000  

# =========================================================
# ⚡ THEME COLORS (HIGH-CONTRAST ELECTRIC PALETTE)
# =========================================================

COLORS = {
    "bg": "#0B0F19",                 
    "paper": "#121826",              
    "text": "#F8FAFC",               
    "muted": "#94A3B8",              
    "electric_blue": "#2563EB",       
    "electric_cyan": "#06B6D4",       
    "electric_violet": "#7C3AED",     
    "soft_glass": "#1E293B",          
    "soft_peach": "#2E1065",          
    "accent_blue": "#38BDF8",         
    "accent_violet": "#C084FC",       
    "line": "#334155",                
}

# =========================================================
# STREAMLIT PREMIUM CYBER-LUXURY UI STYLE SHEET
# =========================================================

st.markdown(
    f"""
    <style>
    .stApp {{
        background:
        radial-gradient(circle at top right, rgba(37,99,235,0.2), transparent 35%),
        radial-gradient(circle at bottom left, rgba(124,58,237,0.25), transparent 30%),
        linear-gradient(180deg, #090D16 0%, {COLORS["bg"]} 100%);
    }}
    .block-container {{ padding-top: 1.5rem; padding-bottom: 2rem; }}
    
    .hero-container {{
        background: rgba(18, 24, 38, 0.6);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(38, 189, 248, 0.2);
        border-radius: 24px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    }}
    .title {{ font-size: 38px; font-weight: 900; letter-spacing: -0.05em; color: #FFFFFF; text-shadow: 0 0 15px rgba(38,189,248,0.4); margin: 0; }}
    .subtitle {{ font-size: 14px; color: {COLORS["muted"]}; margin-top: 0.5rem; margin-bottom: 1rem; }}
    
    .status-chip {{
        display: inline-flex;
        align-items: center;
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid {COLORS["line"]};
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        color: {COLORS["accent_blue"]};
        margin-right: 8px;
    }}

    .stButton button {{
        border-radius: 16px !important;
        border: 1px solid rgba(124,58,237,0.4) !important;
        font-weight: 700 !important;
        padding: 0.8rem 1rem !important;
        background: linear-gradient(135deg, #1E40AF 0%, #6D28D9 60%, #0369A1 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.3) !important;
        transition: all 0.2s ease-on-out !important;
    }}
    
    .sidebar-stat-card {{
        background: rgba(18, 24, 38, 0.8);
        border: 1px solid {COLORS["line"]};
        padding: 12px;
        border-radius: 14px;
        margin-bottom: 10px;
    }}
    .sidebar-stat-val {{ font-size: 18px; font-weight: 700; color: {COLORS["accent_violet"]}; }}
    .sidebar-stat-lbl {{ font-size: 11px; color: {COLORS["muted"]}; }}
    
    p, h3, label, span {{ color: #F8FAFC !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# DATA HELPERS & PARSING GUARD LOGIC
# =========================================================

def clean_text(value):
    if value is None: return ""
    value = str(value).replace("\t", " ")
    value = re.sub(r"\n{3,}", "\n\n", value)
    return re.sub(r"[ ]+", " ", value).strip()

def strip_unsupported(text):
    return text.encode("latin-1", "ignore").decode("latin-1")

def safe_paragraph(text, style):
    clean = html.escape(clean_text(text))  # Bug 2 Fixed: Safe escaping first
    clean = strip_unsupported(clean).replace("\n", "<br/>")
    return Paragraph(clean, style)

def sanitize_filename(name):
    name = clean_text(name).lower()
    return re.sub(r"[^a-z0-9]+", "_", name).strip("_") or "nyxara_output"

def parse_data(raw):
    # Bug 5 Fixed: Better regex array extraction fallback
    errors = []
    raw = clean_text(raw).replace("```python", "").replace("```", "").strip()
    
    if len(raw) > MAX_INPUT_CHARS:
        return [], ["Input limit exceeded."]

    # Try literal eval first
    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, list): return parsed, []
    except Exception:
        pass

    # Fallback to regex finding list-like structures
    collected = []
    match = re.search(r'\[\s*\{.*?\}\s*\]', raw, re.DOTALL)
    if match:
        try:
            parsed = ast.literal_eval(match.group(0))
            if isinstance(parsed, list):
                collected.extend(parsed)
        except Exception as e:
            errors.append(f"Regex fallback failed: {str(e)}")

    return collected, errors

def fit_image(path, max_w, max_h):
    # Bug 4 Fixed: Prevents OS file locks using BytesIO
    try:
        with open(path, "rb") as f:
            img_data = f.read()
        img_bytes = BytesIO(img_data)
        
        with PILImage.open(img_bytes) as im:
            im.verify()
        img_bytes.seek(0)
    except Exception:
        raise ValueError("Corrupted image stream.")

    reader = ImageReader(img_bytes)
    orig_w, orig_h = reader.getSize()

    if orig_w <= 0 or orig_h <= 0:
        raise ValueError("Invalid dimensions")

    scale = min(float(max_w) / orig_w, float(max_h) / orig_h)
    img_w, img_h = orig_w * scale, orig_h * scale

    img = Image(path, width=img_w, height=img_h)
    img.hAlign = "CENTER"
    return img, img_w, img_h

# =========================================================
# ⚡ HIGH-END ELECTRIC TYPOGRAPHY
# =========================================================

styles = getSampleStyleSheet()

# Bug 1 Fixed: Adjusted cover texts to be hyper-visible on dark background
HERO_COVER = ParagraphStyle("HERO_COVER", parent=styles["Normal"], fontName="Times-Bold", fontSize=36, leading=40, textColor=colors.HexColor("#FFFFFF"), alignment=1)
SUB_COVER = ParagraphStyle("SUB_COVER", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=12, leading=18, textColor=colors.HexColor(COLORS["accent_blue"]), alignment=1)

HERO = ParagraphStyle("HERO", parent=styles["Normal"], fontName="Times-Bold", fontSize=32, leading=38, textColor=colors.HexColor(COLORS["accent_blue"]))
TITLE = ParagraphStyle("TITLE", parent=styles["Normal"], fontName="Times-Bold", fontSize=20, leading=26, textColor=colors.HexColor(COLORS["text"]))
SUB = ParagraphStyle("SUB", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=10.5, leading=17, textColor=colors.HexColor(COLORS["accent_violet"]))
BODY = ParagraphStyle("BODY", parent=styles["Normal"], fontName="Helvetica", fontSize=9.5, leading=17, textColor=colors.HexColor("#CBD5E1"))
SMALL = ParagraphStyle("SMALL", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=7.5, leading=10, textColor=colors.HexColor(COLORS["accent_blue"]))
PROMPT_STYLE = ParagraphStyle("PROMPT_STYLE", parent=styles["Normal"], fontName="Courier", fontSize=8, leading=14, textColor=colors.HexColor("#E2E8F0"))

def create_prompt_card(text, bonus=False):
    bg = COLORS["soft_peach"] if bonus else COLORS["soft_glass"]
    accent = COLORS["accent_violet"] if bonus else COLORS["accent_blue"]
    
    # Bug 2 Fixed: Proper safe HTML formatting sequence
    escaped_text = html.escape(clean_text(text))
    escaped_text = strip_unsupported(escaped_text).replace("\n", "<br/>")
    label = "⚡ BONUS NEON CONTEXT FLOW ⚡" if bonus else "⚡ ELECTRIC SYSTEM ARCHITECTURE ⚡"

    style = ParagraphStyle(
        "CARD", parent=PROMPT_STYLE, backColor=colors.HexColor(bg), borderPadding=16,
        borderRadius=12, borderWidth=1.5, borderColor=colors.HexColor(accent), leading=14,
    )

    html_block = f'<b><font color="{accent}">{label}</font></b><br/><br/>{escaped_text}'
    return Paragraph(html_block, style)

# =========================================================
# CANVAS PAGE LAYERS
# =========================================================

def draw_cover_page(canvas_obj, doc):
    if getattr(doc, "_has_cover_image", False): return

    canvas_obj.saveState()
    canvas_obj.setFillColor(colors.HexColor(COLORS["bg"]))
    canvas_obj.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    canvas_obj.setFillColor(colors.HexColor("#1D4ED8")) 
    canvas_obj.circle(PAGE_WIDTH - 40, PAGE_HEIGHT - 40, 160, fill=1, stroke=0)
    canvas_obj.setFillColor(colors.HexColor("#5B21B6")) 
    canvas_obj.circle(40, PAGE_HEIGHT - 100, 120, fill=1, stroke=0)
    canvas_obj.restoreState()

def draw_page(canvas_obj, doc):
    page_no = canvas_obj.getPageNumber()
    canvas_obj.saveState()

    canvas_obj.setFillColor(colors.HexColor(COLORS["bg"]))
    canvas_obj.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    canvas_obj.setStrokeColor(colors.HexColor(COLORS["electric_blue"]))
    canvas_obj.setLineWidth(1)
    canvas_obj.line(55, PAGE_HEIGHT - 48, PAGE_WIDTH - 55, PAGE_HEIGHT - 48)

    canvas_obj.setFont("Helvetica-Bold", 8)
    canvas_obj.setFillColor(colors.HexColor(COLORS["accent_blue"]))
    canvas_obj.drawString(55, PAGE_HEIGHT - 35, BRAND_NAME)
    
    canvas_obj.setFillColor(colors.HexColor(COLORS["accent_violet"]))
    canvas_obj.drawRightString(PAGE_WIDTH - 55, PAGE_HEIGHT - 35, "NEON SYSTEM")

    canvas_obj.setStrokeColor(colors.HexColor(COLORS["line"]))
    canvas_obj.line(55, 42, PAGE_WIDTH - 55, 42)
    
    canvas_obj.setFillColor(colors.HexColor(COLORS["muted"]))
    canvas_obj.drawString(55, 30, "Electric Engine")
    
    canvas_obj.setFillColor(colors.HexColor(COLORS["accent_blue"]))
    canvas_obj.drawRightString(PAGE_WIDTH - 55, 30, f"NODE // {page_no}")

    canvas_obj.restoreState()

# =========================================================
# STORY ASSEMBLERS
# =========================================================

def spacer(story, h=12):
    story.append(Spacer(1, h))

def render_cover_story(story, bundle_title, total_prompts_text):
    story.append(Spacer(1, 200))
    story.append(safe_paragraph(bundle_title.upper(), HERO_COVER))
    spacer(story, 20)
    story.append(safe_paragraph(total_prompts_text, SUB_COVER))

def render_system(story, item, number, bonus=False, is_last=False):
    title = clean_text(item.get("title", "Untitled"))
    prompt = clean_text(item.get("prompt", ""))

    label = f"✦ AUX NODE {number:02d} ✦" if bonus else f"✦ CORE INJECTION {number:02d} ✦"

    story.append(Spacer(1, 40))
    story.append(Paragraph(label, SMALL))
    spacer(story, 8)
    story.append(safe_paragraph(title, TITLE))
    spacer(story, 10)

    sections = [
        ("ANALYSIS MODEL", clean_text(item.get("why_this_works", ""))),
        ("EXECUTION PIPELINE", clean_text(item.get("how_to_use", ""))),
    ]

    for heading, content in sections:
        if content:
            story.append(CondPageBreak(50))
            story.append(Paragraph(heading, SMALL))
            spacer(story, 8)
            story.append(safe_paragraph(content, BODY))
            spacer(story, 14)

    # Bug 3 Fixed: KeepTogether prevents prompt card from splitting wildly
    card_elements = [
        Paragraph("COMPILED PARADIGM DATA", SMALL),
        Spacer(1, 12),
        create_prompt_card(prompt, bonus=bonus)
    ]
    story.append(KeepTogether(card_elements))

    if not is_last:
        story.append(PageBreak())

# =========================================================
# SYSTEM GENERATOR
# =========================================================

def generate_pdf(data, bundle_title, main_count, bonus_count, cover=None):
    filename = f"{sanitize_filename(bundle_title)}_{int(time.time())}.pdf"
    out_path = os.path.join(OUTPUTS_DIR, filename)

    doc = BaseDocTemplate(out_path, pagesize=letter, leftMargin=55, rightMargin=55, topMargin=65, bottomMargin=55)
    doc._has_cover_image = bool(cover and os.path.exists(cover))

    cover_frame = Frame(0, 0, PAGE_WIDTH, PAGE_HEIGHT, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    content_frame = Frame(55, 55, PAGE_WIDTH - 110, PAGE_HEIGHT - 110, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)

    doc.addPageTemplates([
        PageTemplate(id="Cover", frames=[cover_frame], onPage=draw_cover_page),
        PageTemplate(id="Content", frames=[content_frame], onPage=draw_page),
    ])

    # Bug 6 Fixed: Auto-adjust counts instead of crashing
    total = len(data)
    main_count = min(int(main_count), total)
    bonus_count = min(int(bonus_count), total - main_count)

    main_prompts = data[:main_count]
    bonus_prompts = data[main_count:main_count+bonus_count]

    story = []

    if doc._has_cover_image:
        cover_img, _, _ = fit_image(cover, PAGE_WIDTH, PAGE_HEIGHT)
        story.append(cover_img)
    else:
        render_cover_story(story, bundle_title, f"[{total}] active laser nodes fully mapped.")

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    all_items = [(x, False) for x in main_prompts] + [(x, True) for x in bonus_prompts]
    for idx, (item, is_bonus) in enumerate(all_items):
        render_system(story, item, idx + 1, bonus=is_bonus, is_last=(idx == len(all_items) - 1))

    doc.build(story)
    return out_path

# =========================================================
# STREAMLIT UI
# =========================================================

st.markdown(
    f"""<div class="hero-container">
        <div class="title">NYXARA ELECTRIC CONTROL</div>
        <div class="subtitle">Premium Core Dashboard</div>
    </div>""", unsafe_allow_html=True
)

title = st.text_input("Operational Title", value="HYPER ENGINE")
col1, col2 = st.columns(2)
with col1: main_count = st.number_input("Core Prompts", min_value=1, value=2)
with col2: bonus_count = st.number_input("Bonus Prompts", min_value=0, value=1)

raw = st.text_area("Input Data Array", height=360)

if st.button("Trigger Compilation", use_container_width=True):
    parsed, warnings = parse_data(raw)
    
    if not parsed:
        st.error("Execution Aborted: Invalid structure.")
    else:
        try:
            pdf = generate_pdf(parsed, title, main_count, bonus_count)
            st.success("⚡ Success! Cyber PDF generated.")
            with open(pdf, "rb") as f:
                st.download_button("📥 Download Asset", f, file_name=os.path.basename(pdf), use_container_width=True)
        except Exception as e:
            st.error(f"Crash: {e}")
