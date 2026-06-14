# =========================================================
# NYXARA OS V12 — FINAL STABLE ENGINE
# FIXED:
# ✅ Split crash
# ✅ Overflow crash
# ✅ Markdown table crash
# ✅ Prompt card recursion
# ✅ Electric Apple UI
# ✅ Main + Bonus system
# ✅ Permanent logo lock
# ✅ Contents page
# ✅ Intro / CTA / Editorial pages
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
# CONFIG
# =========================================================

st.set_page_config(
    page_title="NYXARA OS V12",
    layout="wide",
)

# =========================================================
# PATHS
# =========================================================

ASSETS_DIR = "assets"
OUTPUTS_DIR = "outputs"

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

LOGO_PATH = os.path.join(ASSETS_DIR, "locked_logo.png")

# =========================================================
# PAGE
# =========================================================

PAGE_WIDTH, PAGE_HEIGHT = letter

# =========================================================
# COLORS
# =========================================================

COLORS = {
    "bg": "#F6F8FF",
    "paper": "#FFFFFF",
    "text": "#0F172A",
    "muted": "#64748B",

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
# STREAMLIT UI
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
    return name.strip("_")

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

# =========================================================
# LOGO LOCK
# =========================================================

def save_logo(uploaded):
    with open(LOGO_PATH, "wb") as f:
        f.write(uploaded.getbuffer())

def get_logo():
    if os.path.exists(LOGO_PATH):
        return LOGO_PATH
    return None

# =========================================================
# NORMALIZE PROMPT
# =========================================================

def normalize_prompt(text):

    text = clean_text(text)

    lines = text.splitlines()

    out = []

    for line in lines:

        s = line.strip()

        if not s:
            out.append("")
            continue

        if re.fullmatch(r"\|[\s:\-\|]+\|", s):
            continue

        if s.startswith("|") and "|" in s[1:]:

            cells = [c.strip() for c in s.strip("|").split("|")]

            line = " • ".join(cells)

            wrapped = textwrap.wrap(
                line,
                width=90,
                break_long_words=True,
            )

            out.extend(wrapped)
            continue

        wrapped = textwrap.wrap(
            s,
            width=90,
            break_long_words=True,
        )

        out.extend(wrapped)

    return "\n".join(out)

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

# =========================================================
# SAFE PROMPT CARD
# =========================================================

def create_prompt_card(text, bonus=False):

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

    return KeepTogether([para])

# =========================================================
# PAGE DRAWING
# =========================================================

def draw_page(canvas_obj, doc):

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
                mask='auto'
            )
            canvas_obj.setFont("Helvetica-Bold", 8)
            canvas_obj.drawString(78, PAGE_HEIGHT - 35, "NYXARA LABS")
        except:
            canvas_obj.drawString(55, PAGE_HEIGHT - 35, "NYXARA LABS")
    else:
        canvas_obj.drawString(55, PAGE_HEIGHT - 35, "NYXARA LABS")

    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawRightString(PAGE_WIDTH - 55, PAGE_HEIGHT - 35, "PRIVÉ")

    canvas_obj.line(55, 42, PAGE_WIDTH - 55, 42)

    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawString(55, 28, "Editorial Publishing Architecture")

    canvas_obj.drawRightString(
        PAGE_WIDTH - 55,
        28,
        f"PAGE {canvas_obj.getPageNumber()}"
    )

    canvas_obj.restoreState()

# =========================================================
# PDF
# =========================================================

def generate_pdf(
    data,
    title,
    main_count,
    bonus_count,
    cover=None,
    logo=None,
):

    filename = sanitize_filename(title) + ".pdf"

    out_path = os.path.join(OUTPUTS_DIR, filename)

    doc = BaseDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=55,
        rightMargin=55,
        topMargin=65,
        bottomMargin=55,
    )

    doc._logo = logo

    frame = Frame(
        55,
        55,
        PAGE_WIDTH - 110,
        PAGE_HEIGHT - 110,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )

    template = PageTemplate(
        id="main",
        frames=[frame],
        onPage=draw_page
    )

    doc.addPageTemplates([template])

    story = []

    # =====================================================
    # COVER
    # =====================================================

    if cover and os.path.exists(cover):

        story.append(
            Image(
                cover,
                width=PAGE_WIDTH - 110,
                height=PAGE_HEIGHT - 110
            )
        )

        story.append(PageBreak())

    # =====================================================
    # INTRO
    # =====================================================

    total = main_count + bonus_count

    story.append(Spacer(1, 120))

    story.append(Paragraph(title.upper(), HERO))

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"""
            {total} operational systems built for commercially believable execution.
            """,
            SUB
        )
    )

    story.append(Spacer(1, 35))

    story.append(
        Paragraph(
            """
            Most AI bundles feel disposable because they are built without operational thinking.

            This system was designed differently.

            The goal is not to overwhelm users with random prompts.
            The goal is to reduce friction, improve execution clarity,
            and create repeatable workflows that still work months later.
            """,
            BODY
        )
    )

    story.append(PageBreak())

    # =====================================================
    # CONTENTS
    # =====================================================

    story.append(Spacer(1, 80))

    story.append(Paragraph("SYSTEM INDEX", TITLE))

    story.append(Spacer(1, 20))

    main_prompts = data[:main_count]
    bonus_prompts = data[main_count:]

    story.append(Paragraph("MAIN SYSTEMS", SMALL))
    story.append(Spacer(1, 10))

    for i, item in enumerate(main_prompts, start=1):

        t = clean_text(item.get("title", "Untitled"))

        story.append(
            Paragraph(
                f"{i:02d} — {t}",
                BODY
            )
        )

        story.append(Spacer(1, 6))

    if bonus_prompts:

        story.append(Spacer(1, 24))

        story.append(Paragraph("BONUS SYSTEMS", SMALL))

        story.append(Spacer(1, 10))

        for i, item in enumerate(bonus_prompts, start=1):

            t = clean_text(item.get("title", "Untitled"))

            story.append(
                Paragraph(
                    f"BONUS {i:02d} — {t}",
                    BODY
                )
            )

            story.append(Spacer(1, 6))

    story.append(PageBreak())

    # =====================================================
    # SYSTEMS
    # =====================================================

    def render_system(item, number, bonus=False):

        title = clean_text(item.get("title", "Untitled"))

        desc = clean_text(item.get("description", ""))

        prompt = clean_text(item.get("prompt", ""))

        why = clean_text(item.get("why_this_works", ""))

        use = clean_text(item.get("how_to_use", ""))

        story.append(Spacer(1, 50))

        label = f"BONUS SYSTEM {number:02d}" if bonus else f"SYSTEM {number:02d}"

        story.append(Paragraph(label, SMALL))

        story.append(Spacer(1, 8))

        story.append(Paragraph(title, TITLE))

        story.append(Spacer(1, 10))

        if desc:
            story.append(Paragraph(desc, SUB))
            story.append(Spacer(1, 18))

        if why:
            story.append(Paragraph("WHY THIS WORKS", SMALL))
            story.append(Spacer(1, 6))
            story.append(Paragraph(why, BODY))
            story.append(Spacer(1, 14))

        if use:
            story.append(Paragraph("HOW TO USE", SMALL))
            story.append(Spacer(1, 6))
            story.append(Paragraph(use.replace("\n", "<br/>"), BODY))
            story.append(Spacer(1, 18))

        story.append(Paragraph("OPERATIONAL PROMPT", SMALL))
        story.append(Spacer(1, 12))

        story.append(
            create_prompt_card(
                prompt,
                bonus=bonus
            )
        )

        story.append(PageBreak())

    for i, item in enumerate(main_prompts, start=1):
        render_system(item, i, bonus=False)

    if bonus_prompts:

        story.append(Spacer(1, 180))

        story.append(
            Paragraph(
                "BONUS SYSTEMS",
                HERO
            )
        )

        story.append(PageBreak())

        for i, item in enumerate(bonus_prompts, start=1):
            render_system(item, i, bonus=True)

    # =====================================================
    # CTA
    # =====================================================

    story.append(Spacer(1, 220))

    story.append(
        Paragraph(
            """
            Strong systems create calmer execution.
            """,
            HERO
        )
    )

    story.append(Spacer(1, 30))

    story.append(
        Paragraph(
            """
            The goal of this operating system was never just output.

            It was clarity.

            Clearer execution.
            Better structure.
            Less creative friction.
            More consistent work.

            Build systems that still help you create even when motivation disappears.
            """,
            SUB
        )
    )

    doc.build(story)

    return out_path

# =========================================================
# INTERFACE
# =========================================================

st.markdown(
    """
    <div class="title">NYXARA OS V12</div>
    <div class="subtitle">
    Apple-inspired editorial AI publishing system.
    </div>
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
# LOGO
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
# BUTTON
# =========================================================

if st.button("Generate Premium PDF", use_container_width=True):

    parsed = parse_data(raw)

    if not parsed:
        st.error("Invalid data format.")

    else:

        total = len(parsed)

        if total != (main_count + bonus_count):

            st.error(
                f"Prompt count mismatch. Total prompts = {total}"
            )

        else:

            cover_path = None

            if cover_upload:

                cover_path = os.path.join(
                    ASSETS_DIR,
                    "cover_temp.png"
                )

                with open(cover_path, "wb") as f:
                    f.write(cover_upload.getbuffer())

            try:

                pdf = generate_pdf(
                    parsed,
                    title,
                    main_count,
                    bonus_count,
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
