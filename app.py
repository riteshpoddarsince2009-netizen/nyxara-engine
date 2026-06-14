# =========================================================
# NYXARA OS V12 — FINAL STABLE ENGINE
# FIXED:
# ✅ Split crash
# ✅ Overflow crash
# ✅ Markdown table crash
# ✅ Prompt card recursion removed
# ✅ Electric Apple UI
# ✅ Main + Bonus system
# ✅ Permanent logo lock
# ✅ Contents page
# ✅ Intro / CTA / Editorial pages
# ✅ PRIVÉ header
# =========================================================

import os
import ast
import re
import html
import textwrap

import streamlit as st

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
    KeepTogether,
)
from reportlab.pdfgen import canvas

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NYXARA OS V12",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# PATHS
# =========================================================

ASSETS_DIR = "assets"
OUTPUTS_DIR = "outputs"
LOGO_PATH = os.path.join(ASSETS_DIR, "locked_logo.png")

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# =========================================================
# CORE CONSTANTS
# =========================================================

PAGE_WIDTH, PAGE_HEIGHT = letter
BRAND_NAME = "NYXARA"
MAX_PROMPT_CHARS = 1400

# =========================================================
# COLORS
# =========================================================

COLORS = {
    "bg": "#F6F8FF",
    "paper": "#FFFFFF",
    "text": "#0F172A",
    "muted": "#334155",   # darker for header/footer visibility

    "electric_blue": "#DCE8FF",
    "electric_cyan": "#DDF7FF",
    "electric_violet": "#E8DDFF",

    "soft_glass": "#F8FAFF",
    "soft_peach": "#FFF4EC",

    "accent_blue": "#60A5FA",
    "accent_violet": "#A78BFA",

    "line": "#E5EAF4",
}

# =========================================================
# STREAMLIT UI STYLE
# =========================================================

st.markdown(
    f"""
    <style>
    .stApp {{
        background:
        radial-gradient(circle at top right, rgba(220,232,255,0.9), transparent 28%),
        radial-gradient(circle at bottom left, rgba(232,221,255,0.8), transparent 24%),
        linear-gradient(180deg, white 0%, {COLORS["bg"]} 100%);
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}

    .title {{
        font-size: 36px;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: {COLORS["text"]};
    }}

    .subtitle {{
        font-size: 14px;
        color: {COLORS["muted"]};
        margin-bottom: 1rem;
    }}

    .soft-card {{
        border-radius: 22px;
        background: rgba(255,255,255,0.82);
        border: 1px solid rgba(229,234,244,1);
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 20px 50px rgba(15,23,42,0.04);
        backdrop-filter: blur(16px);
    }}

    .stButton button {{
        border-radius: 16px !important;
        border: none !important;
        font-weight: 700 !important;
        padding: 0.9rem 1rem !important;
        background:
        linear-gradient(
            135deg,
            #DCE8FF 0%,
            #E8DDFF 55%,
            #DDF7FF 100%
        ) !important;
        color: #0F172A !important;
    }}

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {{
        border-radius: 16px !important;
        border: 1px solid rgba(229,234,244,1) !important;
        background: rgba(255,255,255,0.88) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# HELPERS
# =========================================================

def clean_text(value):
    if value is None:
        return ""
    value = str(value)
    value = value.replace("\t", " ")
    value = re.sub(r"\n{3,}", "\n\n", value)
    value = re.sub(r"[ ]+", " ", value)
    return value.strip()

def safe_html(value):
    return html.escape(clean_text(value)).replace("\n", "<br/>")

def sanitize_filename(name):
    name = clean_text(name).lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_") or "nyxara_os_v12"

def parse_data(raw):
    raw = clean_text(raw)

    if raw.startswith("data ="):
        raw = raw.replace("data =", "", 1).strip()

    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, list):
            return parsed
    except:
        return []

    return []

def save_logo(uploaded):
    with open(LOGO_PATH, "wb") as f:
        f.write(uploaded.getbuffer())

def get_logo():
    if os.path.exists(LOGO_PATH):
        return LOGO_PATH
    return None

def normalize_prompt(text):
    """
    Converts prompt text into a display-safe version so
    markdown tables and long lines don't blow up the PDF.
    """
    text = clean_text(text)
    lines = text.splitlines()

    out = []

    for line in lines:
        s = line.strip()

        if not s:
            out.append("")
            continue

        # skip markdown separator rows like |---|---|
        if re.fullmatch(r"\|[\s:\-\|]+\|", s):
            continue

        # table-like rows -> convert to safe text
        if s.startswith("|") and "|" in s[1:]:
            cells = [c.strip() for c in s.strip("|").split("|")]
            row = " • ".join(cells)

            wrapped = textwrap.wrap(
                row,
                width=90,
                break_long_words=True,
                break_on_hyphens=False,
            )
            out.extend(wrapped if wrapped else [row])
            continue

        wrapped = textwrap.wrap(
            s,
            width=90,
            break_long_words=True,
            break_on_hyphens=False,
        )
        out.extend(wrapped if wrapped else [s])

    return "\n".join(out).strip()

def split_prompt_into_chunks(text, max_chars=MAX_PROMPT_CHARS):
    """
    Safe chunk splitter.
    Handles:
    - markdown tables
    - giant paragraphs
    - long lines
    - unbreakable text
    """
    text = normalize_prompt(text)

    if len(text) <= max_chars:
        return [text]

    chunks = []
    current = ""

    paragraphs = text.split("\n\n")

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        candidate = f"{current}\n\n{para}" if current else para

        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current)
                current = ""

            if len(para) <= max_chars:
                current = para
            else:
                words = para.split()
                part = ""
                for w in words:
                    cand = f"{part} {w}".strip()
                    if len(cand) <= max_chars:
                        part = cand
                    else:
                        if part:
                            chunks.append(part)
                        part = w
                if part:
                    current = part

    if current:
        chunks.append(current)

    return chunks if chunks else [text]

# =========================================================
# STYLES
# =========================================================

styles = getSampleStyleSheet()

HERO = ParagraphStyle(
    "HERO",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=30,
    leading=36,
    textColor=colors.HexColor(COLORS["text"]),
)

TITLE = ParagraphStyle(
    "TITLE",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=18,
    leading=24,
    textColor=colors.HexColor(COLORS["text"]),
)

SUB = ParagraphStyle(
    "SUB",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=11,
    leading=18,
    textColor=colors.HexColor(COLORS["muted"]),
)

BODY = ParagraphStyle(
    "BODY",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=10,
    leading=18,
    textColor=colors.HexColor("#1E293B"),
)

SMALL = ParagraphStyle(
    "SMALL",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8,
    leading=10,
    textColor=colors.HexColor(COLORS["muted"]),
)

PROMPT_STYLE = ParagraphStyle(
    "PROMPT_STYLE",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=15,
    textColor=colors.HexColor("#111827"),
)

PROMPT_LABEL_STYLE = ParagraphStyle(
    "PROMPT_LABEL_STYLE",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8,
    leading=10,
    textColor=colors.HexColor(COLORS["muted"]),
)

# =========================================================
# PROMPT CARD
# =========================================================

def create_prompt_card(text, bonus=False):
    """
    Safe prompt card.
    No custom split logic.
    Uses native Paragraph rendering inside a styled box.
    """
    bg = COLORS["soft_peach"] if bonus else COLORS["soft_glass"]
    accent = COLORS["accent_violet"] if bonus else COLORS["accent_blue"]

    text = normalize_prompt(text)
    label = "BONUS OPERATIONAL SYSTEM" if bonus else "OPERATIONAL PROMPT SYSTEM"

    style = ParagraphStyle(
        "CARD",
        parent=PROMPT_STYLE,
        backColor=bg,
        borderPadding=18,
        borderRadius=18,
        borderWidth=1.2,
        borderColor=colors.HexColor(accent),
        leading=15,
    )

    html_block = f"""
    <font color="{COLORS['muted']}"><b>{label}</b></font>
    <br/><br/>
    <font color="#111827">
    {safe_html(text)}
    </font>
    """

    para = Paragraph(html_block, style)
    return para

# =========================================================
# PAGE DRAWING
# =========================================================

def draw_page(canvas_obj, doc):
    # If a full cover image exists, keep page 1 clean
    if getattr(doc, "_has_cover_image", False) and doc.page == 1:
        return

    canvas_obj.saveState()

    canvas_obj.setFillColor(colors.HexColor(COLORS["bg"]))
    canvas_obj.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    canvas_obj.setFillColor(colors.HexColor(COLORS["electric_blue"]))
    canvas_obj.circle(PAGE_WIDTH - 70, PAGE_HEIGHT - 80, 100, fill=1, stroke=0)

    canvas_obj.setFillColor(colors.HexColor(COLORS["electric_violet"]))
    canvas_obj.circle(70, PAGE_HEIGHT - 120, 80, fill=1, stroke=0)

    canvas_obj.setFillColor(colors.HexColor(COLORS["electric_cyan"]))
    canvas_obj.circle(80, 80, 90, fill=1, stroke=0)

    canvas_obj.setStrokeColor(colors.HexColor(COLORS["line"]))
    canvas_obj.line(55, PAGE_HEIGHT - 48, PAGE_WIDTH - 55, PAGE_HEIGHT - 48)

    logo = getattr(doc, "_logo", None)

    if logo and os.path.exists(logo):
        try:
            canvas_obj.drawImage(
                logo,
                55,
                PAGE_HEIGHT - 42,
                width=16,
                height=16,
                mask="auto",
            )
            canvas_obj.setFont("Helvetica-Bold", 8.5)
            canvas_obj.setFillColor(colors.HexColor(COLORS["muted"]))
            canvas_obj.drawString(78, PAGE_HEIGHT - 35, BRAND_NAME)
        except:
            canvas_obj.setFont("Helvetica-Bold", 8.5)
            canvas_obj.setFillColor(colors.HexColor(COLORS["muted"]))
            canvas_obj.drawString(55, PAGE_HEIGHT - 35, BRAND_NAME)
    else:
        canvas_obj.setFont("Helvetica-Bold", 8.5)
        canvas_obj.setFillColor(colors.HexColor(COLORS["muted"]))
        canvas_obj.drawString(55, PAGE_HEIGHT - 35, BRAND_NAME)

    canvas_obj.setFont("Helvetica-Bold", 8.5)
    canvas_obj.drawRightString(PAGE_WIDTH - 55, PAGE_HEIGHT - 35, "PRIVÉ")

    canvas_obj.line(55, 42, PAGE_WIDTH - 55, 42)

    canvas_obj.setFont("Helvetica-Bold", 8.5)
    canvas_obj.setFillColor(colors.HexColor(COLORS["muted"]))
    canvas_obj.drawString(55, 28, "Editorial Publishing Architecture")
    canvas_obj.drawRightString(PAGE_WIDTH - 55, 28, f"PAGE {canvas_obj.getPageNumber()}")

    canvas_obj.restoreState()

# =========================================================
# STORY HELPERS
# =========================================================

def spacer(story, h=12):
    story.append(Spacer(1, h))

def render_cover_story(story, bundle_title, total_prompts_text):
    story.append(Spacer(1, 180))
    story.append(Paragraph(bundle_title.upper(), HERO))
    spacer(story, 14)
    story.append(Paragraph(total_prompts_text, SUB))
    spacer(story, 24)
    story.append(
        Paragraph(
            "A premium editorial operating system for structured creative execution.",
            BODY,
        )
    )

def render_intro(story, bundle_title, main_count, bonus_count):
    total = main_count + bonus_count
    story.append(Spacer(1, 80))
    story.append(Paragraph(bundle_title.upper(), HERO))
    spacer(story, 16)
    story.append(
        Paragraph(
            f"""
            {total} operational AI systems designed for commercially believable execution.
            <br/><br/>
            <b>{main_count}</b> core systems &nbsp;&nbsp;•&nbsp;&nbsp; <b>{bonus_count}</b> bonus systems
            """,
            SUB,
        )
    )
    spacer(story, 36)
    story.append(
        Paragraph(
            """
            Most AI bundles fail because they look like random prompt dumps.

            This system was designed differently.

            The goal is not just output. The goal is calmer execution, clearer hierarchy,
            and repeatable creative workflows that save time and reduce confusion.
            """,
            BODY,
        )
    )
    spacer(story, 18)
    story.append(Paragraph("WHAT THIS SYSTEM INCLUDES", SMALL))
    spacer(story, 10)

    items = [
        f"{main_count} core operational systems",
        f"{bonus_count} bonus workflow assets",
        "commercially usable prompt frameworks",
        "repeatable implementation flows",
        "clear business application logic",
    ]
    for item in items:
        story.append(Paragraph(f"• {item}", BODY))
        spacer(story, 4)

    story.append(PageBreak())

def render_contents(story, main_prompts, bonus_prompts):
    spacer(story, 70)
    story.append(Paragraph("SYSTEM INDEX", TITLE))
    spacer(story, 8)

    story.append(Paragraph("MAIN SYSTEMS", SMALL))
    spacer(story, 12)
    for i, item in enumerate(main_prompts, start=1):
        title = clean_text(item.get("title", "Untitled"))
        story.append(Paragraph(f"{i:02d} — {title}", BODY))
        spacer(story, 8)

    if bonus_prompts:
        spacer(story, 18)
        story.append(Paragraph("BONUS SYSTEMS", SMALL))
        spacer(story, 12)
        for i, item in enumerate(bonus_prompts, start=1):
            title = clean_text(item.get("title", "Untitled"))
            story.append(Paragraph(f"BONUS {i:02d} — {title}", BODY))
            spacer(story, 8)

    story.append(PageBreak())

def render_breathing(story, text):
    spacer(story, 210)
    story.append(Paragraph(text, HERO))
    story.append(PageBreak())

def render_system(story, item, number, bonus=False):
    title = clean_text(item.get("title", "Untitled"))
    description = clean_text(item.get("description", ""))
    why = clean_text(item.get("why_this_works", ""))
    micro = clean_text(item.get("micro_example", ""))
    how = clean_text(item.get("how_to_use", ""))
    business = clean_text(item.get("business_application", ""))
    validation = clean_text(item.get("validation_case_study", ""))
    prompt = clean_text(item.get("prompt", ""))

    label = f"BONUS SYSTEM {number:02d}" if bonus else f"SYSTEM {number:02d}"
    story.append(Spacer(1, 48))
    story.append(Paragraph(label, SMALL))
    spacer(story, 8)
    story.append(Paragraph(title, TITLE))
    spacer(story, 10)

    if description:
        story.append(Paragraph(description, SUB))
        spacer(story, 18)

    sections = [
        ("WHY THIS WORKS", why),
        ("MICRO EXAMPLE", micro),
        ("HOW TO USE", how),
        ("BUSINESS APPLICATION", business),
        ("VALIDATION CASE", validation),
    ]

    for heading, content in sections:
        if not content:
            continue
        story.append(Paragraph(heading, SMALL))
        spacer(story, 8)
        story.append(Paragraph(content.replace("\n", "<br/>"), BODY))
        spacer(story, 14)

    prompt_block = KeepTogether([
        Paragraph("OPERATIONAL PROMPT", SMALL),
        Spacer(1, 12),
        create_prompt_card(prompt, bonus=bonus),
    ])
    story.append(prompt_block)
    story.append(PageBreak())

def render_bonus_intro(story):
    spacer(story, 210)
    story.append(Paragraph("BONUS SYSTEMS", HERO))
    spacer(story, 18)
    story.append(
        Paragraph(
            """
            Additional operational assets designed to improve workflow depth,
            execution flexibility, and creative consistency.
            """,
            SUB,
        )
    )
    story.append(PageBreak())

def render_cta(story):
    spacer(story, 180)
    story.append(
        Paragraph(
            """
            Creative momentum does not come from motivation.

            It comes from reduced friction.
            """,
            HERO,
        )
    )
    spacer(story, 30)
    story.append(
        Paragraph(
            """
            The goal of this operating system was to create calmer execution,
            cleaner structure, and more sustainable creative output.

            Use it to reduce confusion, speed up decisions,
            and build a workflow that still works when motivation drops.
            """,
            SUB,
        )
    )
    story.append(PageBreak())

def render_end(story):
    spacer(story, 230)
    story.append(
        Paragraph(
            """
            Built for creators, operators, and teams who value clarity,
            consistency, and sustainable execution.
            """,
            HERO,
        )
    )

# =========================================================
# PDF GENERATOR
# =========================================================

def generate_pdf(data, bundle_title, main_count, bonus_count, cover=None, logo=None):
    filename = sanitize_filename(bundle_title) + ".pdf"
    out_path = os.path.join(OUTPUTS_DIR, filename)

    doc = BaseDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=55,
        rightMargin=55,
        topMargin=65,
        bottomMargin=55,
        pageCompression=1,
    )

    doc._logo = logo
    doc._has_cover_image = bool(cover and os.path.exists(cover))

    frame = Frame(
        55,
        55,
        PAGE_WIDTH - 110,
        PAGE_HEIGHT - 110,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
        showBoundary=0,
    )

    template = PageTemplate(
        id="main",
        frames=[frame],
        onPage=draw_page,
    )

    doc.addPageTemplates([template])

    story = []

    main_prompts = data[:main_count]
    bonus_prompts = data[main_count:]

    # =====================================================
    # COVER
    # =====================================================

    if cover and os.path.exists(cover):
        story.append(
            Image(
                cover,
                width=PAGE_WIDTH,
                height=PAGE_HEIGHT,
            )
        )
    else:
        render_cover_story(
            story,
            bundle_title,
            f"{len(data)} operational AI systems built for structured execution."
        )

    story.append(PageBreak())

    # =====================================================
    # INTRO
    # =====================================================

    render_intro(story, bundle_title, main_count, bonus_count)

    # =====================================================
    # CONTENTS
    # =====================================================

    render_contents(story, main_prompts, bonus_prompts)

    # =====================================================
    # BREATHING PAGE
    # =====================================================

    render_breathing(story, "Strong systems create calmer execution.")

    # =====================================================
    # MAIN SYSTEMS
    # =====================================================

    for i, item in enumerate(main_prompts, start=1):
        render_system(story, item, i, bonus=False)
        if i % 4 == 0 and i != len(main_prompts):
            render_breathing(story, "Consistency compounds quietly over time.")

    # =====================================================
    # BONUS SYSTEMS
    # =====================================================

    if bonus_prompts:
        render_bonus_intro(story)
        for i, item in enumerate(bonus_prompts, start=1):
            render_system(story, item, i, bonus=True)

    # =====================================================
    # CTA + END
    # =====================================================

    render_cta(story)
    render_end(story)

    doc.build(story)
    return out_path

# =========================================================
# INTERFACE
# =========================================================

st.markdown(
    """
    <div class="title">NYXARA OS V12</div>
    <div class="subtitle">Apple-inspired editorial publishing engine for premium AI prompt systems.</div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

title = st.text_input(
    "Bundle Title",
    value="RETRO PACKAGING DESIGN OPERATIONS SYSTEM"
)

col1, col2 = st.columns(2)

with col1:
    main_count = st.number_input(
        "No. Of Main Prompts",
        min_value=1,
        value=20
    )

with col2:
    bonus_count = st.number_input(
        "No. Of Bonus Prompts",
        min_value=0,
        value=4
    )

st.markdown("---")

cover_upload = st.file_uploader(
    "Upload Cover Page",
    type=["png", "jpg", "jpeg"]
)

# =========================================================
# LOGO LOCK
# =========================================================

locked_logo = get_logo()

if locked_logo:
    st.success("Logo permanently locked.")
    st.image(locked_logo, width=80)
else:
    logo_upload = st.file_uploader(
        "Upload Logo Once",
        type=["png", "jpg", "jpeg"]
    )
    if logo_upload:
        save_logo(logo_upload)
        st.success("Logo locked permanently.")

# =========================================================
# DATA
# =========================================================

raw = st.text_area(
    "Paste Prompt Data",
    height=400
)

# =========================================================
# GENERATE
# =========================================================

if st.button("Generate Premium PDF", use_container_width=True):

    parsed = parse_data(raw)

    if not parsed:
        st.error("Invalid data format.")
    else:
        total = len(parsed)

        if total != (main_count + bonus_count):
            st.error(f"Prompt count mismatch. Total prompts = {total}")
        else:
            cover_path = None

            if cover_upload:
                cover_path = os.path.join(ASSETS_DIR, "cover_temp.png")
                with open(cover_path, "wb") as f:
                    f.write(cover_upload.getbuffer())

            try:
                pdf = generate_pdf(
                    parsed,
                    title,
                    int(main_count),
                    int(bonus_count),
                    cover=cover_path,
                    logo=get_logo(),
                )

                st.success("Premium PDF generated successfully.")

                with open(pdf, "rb") as f:
                    st.download_button(
                        "Download PDF",
                        f,
                        file_name=os.path.basename(pdf),
                        use_container_width=True,
                    )

            except Exception as e:
                st.error(f"System prevented crash: {e}")
