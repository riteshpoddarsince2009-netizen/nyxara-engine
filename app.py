# =========================================================
# NYXARA ENGINE V1.0 — CRASH-PROOF EDITION
# FILE: app.py
# =========================================================

import streamlit as st
import os
import re
import ast
import textwrap
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    KeepTogether,
    Image,
    Preformatted
)

from reportlab.platypus.tables import Table, TableStyle

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# =========================================================
# ENGINE CONFIG
# =========================================================

ENGINE_CONFIG = {

    "safe_mode": True,

    "debug_mode": False,

    "strict_validation": True,

    "auto_page_breaks": True,

    "auto_chunk_large_prompts": True,

    "max_prompt_chunk_size": 3500,

    "max_title_length": 80,

    "max_description_length": 300,

    "max_case_study_length": 500,

    "max_paragraph_length": 1200,

    "safe_image_mode": True,

    "enable_fallbacks": True,

    "enable_blank_cover": True,

    "enable_auto_cleanup": True,

    "prevent_full_page_tables": True
}

# =========================================================
# DOCUMENT META
# =========================================================

DOCUMENT_META = {

    "brand_name": "NYXARA LABS",

    "bundle_title": "",

    "bundle_subtitle": "",

    "target_niche": "",

    "target_audience": "",

    "primary_outcome": "",

    "prompt_count": 0,

    "bonus_count": 4,

    "cover_path": None,

    "logo_path": None
}

# =========================================================
# SAFE HELPERS
# =========================================================

def safe_get(data, key, default="N/A"):
    try:
        value = data.get(key, default)

        if value is None:
            return default

        return str(value).strip()

    except:
        return default


def normalize_text(text):

    if not text:
        return ""

    text = str(text)

    text = text.replace("\t", " ")

    text = re.sub(r"\n{3,}", "\n\n", text)

    text = re.sub(r" +", " ", text)

    text = text.strip()

    return text


def clean_text(text):

    text = normalize_text(text)

    replacements = {
        "•": "-",
        "’": "'",
        "“": '"',
        "”": '"'
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def safe_paragraph(text, style):

    try:

        text = clean_text(text)

        return Paragraph(text, style)

    except Exception as e:

        fallback = f"[Rendering Error Prevented]"

        return Paragraph(fallback, style)


def split_large_text(text, chunk_size=3500):

    if len(text) <= chunk_size:
        return [text]

    chunks = textwrap.wrap(
        text,
        width=chunk_size,
        break_long_words=False,
        replace_whitespace=False
    )

    return chunks


# =========================================================
# VALIDATION ENGINE
# =========================================================

REQUIRED_KEYS = [
    "title",
    "category",
    "description",
    "prompt",
    "why_this_works",
    "micro_example",
    "how_to_use",
    "business_application",
    "validation_case_study",
    "ecosystem_assets"
]


def validate_prompt_schema(item):

    safe_item = {}

    for key in REQUIRED_KEYS:

        safe_item[key] = safe_get(item, key)

    if not isinstance(item.get("ecosystem_assets", {}), dict):

        safe_item["ecosystem_assets"] = {}

    else:

        safe_item["ecosystem_assets"] = item.get("ecosystem_assets", {})

    return safe_item


def validate_root_structure(data):

    if not isinstance(data, list):
        return []

    validated = []

    for item in data:

        if isinstance(item, dict):

            validated.append(
                validate_prompt_schema(item)
            )

    return validated


# =========================================================
# DATA PARSER
# =========================================================

def parse_ai_data(raw_text):

    raw_text = raw_text.strip()

    if raw_text.startswith("data ="):
        raw_text = raw_text.replace("data =", "", 1).strip()

    try:

        parsed = ast.literal_eval(raw_text)

        return validate_root_structure(parsed)

    except Exception as e:

        return []


# =========================================================
# PDF STYLES
# =========================================================

styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "TITLE_STYLE",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=22,
    leading=28,
    textColor=colors.HexColor("#111111"),
    alignment=TA_CENTER,
    spaceAfter=20
)

SUBTITLE_STYLE = ParagraphStyle(
    "SUBTITLE_STYLE",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=11,
    leading=18,
    textColor=colors.HexColor("#444444"),
    alignment=TA_CENTER,
    spaceAfter=30
)

SECTION_TITLE_STYLE = ParagraphStyle(
    "SECTION_TITLE_STYLE",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=13,
    leading=18,
    textColor=colors.HexColor("#111111"),
    spaceAfter=10
)

BODY_STYLE = ParagraphStyle(
    "BODY_STYLE",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=10.5,
    leading=17,
    textColor=colors.HexColor("#333333"),
    spaceAfter=14
)

PROMPT_STYLE = ParagraphStyle(
    "PROMPT_STYLE",
    parent=styles["BodyText"],
    fontName="Courier",
    fontSize=9,
    leading=15,
    textColor=colors.HexColor("#111111"),
    spaceAfter=10
)

SMALL_STYLE = ParagraphStyle(
    "SMALL_STYLE",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor("#666666"),
    alignment=TA_CENTER
)

# =========================================================
# PAGE DECORATOR
# =========================================================

class NyxaraCanvas(canvas.Canvas):

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

            self.draw_layout(num_pages)

            super().showPage()

        super().save()

    def draw_layout(self, page_count):

        self.saveState()

        width, height = letter

        self.setStrokeColor(colors.HexColor("#DDDDDD"))

        self.line(50, height - 50, width - 50, height - 50)

        self.line(50, 45, width - 50, 45)

        self.setFont("Helvetica-Bold", 8)

        self.setFillColor(colors.HexColor("#999999"))

        self.drawString(
            50,
            30,
            DOCUMENT_META["brand_name"]
        )

        self.drawRightString(
            width - 50,
            30,
            f"PAGE {self._pageNumber}"
        )

        self.restoreState()

# =========================================================
# COVER PAGE
# =========================================================

def render_cover_page(story):

    cover = DOCUMENT_META["cover_path"]

    if cover and os.path.exists(cover):

        img = Image(cover)

        img.drawHeight = 720

        img.drawWidth = 520

        story.append(img)

    else:

        story.append(Spacer(1, 250))

        story.append(
            safe_paragraph(
                "COVER PAGE PLACEHOLDER",
                TITLE_STYLE
            )
        )

    story.append(PageBreak())

# =========================================================
# INTRO PAGE
# =========================================================

def render_intro_page(story):

    story.append(
        safe_paragraph(
            DOCUMENT_META["bundle_title"],
            TITLE_STYLE
        )
    )

    subtitle = f"""
    {DOCUMENT_META["prompt_count"]} Operational AI Systems Built for
    {DOCUMENT_META["target_niche"]}
    """

    story.append(
        safe_paragraph(
            subtitle,
            SUBTITLE_STYLE
        )
    )

    intro = """
    This operational system was designed to help creators,
    freelancers, agencies, and commercial operators improve
    consistency, reduce manual workload, and streamline production workflows.
    """

    story.append(
        safe_paragraph(
            intro,
            BODY_STYLE
        )
    )

    story.append(
        safe_paragraph(
            "WHAT THIS SYSTEM INCLUDES",
            SECTION_TITLE_STYLE
        )
    )

    includes = """
    - Premium AI Systems<br/>
    - Workflow Frameworks<br/>
    - Commercial Use Cases<br/>
    - Operational Templates<br/>
    - Production Systems
    """

    story.append(
        safe_paragraph(
            includes,
            BODY_STYLE
        )
    )

    story.append(PageBreak())

# =========================================================
# CONTENTS PAGE
# =========================================================

def render_contents_page(story, data):

    story.append(
        safe_paragraph(
            "SYSTEM CONTENTS",
            TITLE_STYLE
        )
    )

    for idx, item in enumerate(data, start=1):

        title = safe_get(item, "title")

        line = f"{idx:02d}. {title}"

        story.append(
            safe_paragraph(
                line,
                BODY_STYLE
            )
        )

    story.append(PageBreak())

# =========================================================
# WORKFLOW PAGE
# =========================================================

def render_workflow_page(story):

    story.append(
        safe_paragraph(
            "RECOMMENDED WORKFLOW",
            TITLE_STYLE
        )
    )

    workflow = """
    01 — Select the appropriate operational system.<br/><br/>

    02 — Generate outputs using ChatGPT or Claude.<br/><br/>

    03 — Refine the outputs for your project or client.<br/><br/>

    04 — Apply the generated assets to production workflows.<br/><br/>

    05 — Save successful systems for future reuse.
    """

    story.append(
        safe_paragraph(
            workflow,
            BODY_STYLE
        )
    )

    story.append(PageBreak())

# =========================================================
# PROMPT PAGE RENDERER
# =========================================================

def render_prompt_page(story, item):

    title = safe_get(item, "title")

    category = safe_get(item, "category")

    description = safe_get(item, "description")

    prompt = safe_get(item, "prompt")

    why = safe_get(item, "why_this_works")

    example = safe_get(item, "micro_example")

    how = safe_get(item, "how_to_use")

    business = safe_get(item, "business_application")

    case = safe_get(item, "validation_case_study")

    ecosystem = item.get("ecosystem_assets", {})

    # TITLE

    story.append(
        safe_paragraph(
            title,
            TITLE_STYLE
        )
    )

    # CATEGORY

    story.append(
        safe_paragraph(
            f"<b>Category:</b> {category}",
            BODY_STYLE
        )
    )

    # DESCRIPTION

    story.append(
        safe_paragraph(
            description,
            BODY_STYLE
        )
    )

    # PROMPT TITLE

    story.append(
        safe_paragraph(
            "CORE PROMPT",
            SECTION_TITLE_STYLE
        )
    )

    # SAFE PROMPT CHUNKING

    chunks = split_large_text(
        prompt,
        ENGINE_CONFIG["max_prompt_chunk_size"]
    )

    for chunk in chunks:

        story.append(
            Preformatted(
                chunk,
                PROMPT_STYLE
            )
        )

        story.append(Spacer(1, 10))

    # WHY

    story.append(
        safe_paragraph(
            "WHY THIS WORKS",
            SECTION_TITLE_STYLE
        )
    )

    story.append(
        safe_paragraph(
            why,
            BODY_STYLE
        )
    )

    # EXAMPLE

    story.append(
        safe_paragraph(
            "MICRO EXAMPLE",
            SECTION_TITLE_STYLE
        )
    )

    story.append(
        safe_paragraph(
            example,
            BODY_STYLE
        )
    )

    # HOW TO USE

    story.append(
        safe_paragraph(
            "HOW TO USE",
            SECTION_TITLE_STYLE
        )
    )

    story.append(
        safe_paragraph(
            how.replace("\n", "<br/>"),
            BODY_STYLE
        )
    )

    # BUSINESS

    story.append(
        safe_paragraph(
            "BUSINESS APPLICATION",
            SECTION_TITLE_STYLE
        )
    )

    story.append(
        safe_paragraph(
            business,
            BODY_STYLE
        )
    )

    # CASE STUDY

    story.append(
        safe_paragraph(
            "VALIDATION CASE STUDY",
            SECTION_TITLE_STYLE
        )
    )

    story.append(
        safe_paragraph(
            case,
            BODY_STYLE
        )
    )

    # ECOSYSTEM

    story.append(
        safe_paragraph(
            "ECOSYSTEM ASSETS",
            SECTION_TITLE_STYLE
        )
    )

    eco_text = ""

    for k, v in ecosystem.items():

        eco_text += f"<b>{k}</b><br/>{v}<br/><br/>"

    story.append(
        safe_paragraph(
            eco_text,
            BODY_STYLE
        )
    )

    story.append(PageBreak())

# =========================================================
# CTA PAGE
# =========================================================

def render_cta_page(story):

    story.append(
        safe_paragraph(
            "END OF SYSTEM",
            TITLE_STYLE
        )
    )

    closing = """
    This bundle was designed to support
    commercially useful operational workflows,
    repeatable execution systems,
    and long-term implementation consistency.
    """

    story.append(
        safe_paragraph(
            closing,
            BODY_STYLE
        )
    )

    story.append(
        safe_paragraph(
            DOCUMENT_META["brand_name"],
            SECTION_TITLE_STYLE
        )
    )

# =========================================================
# PDF ENGINE
# =========================================================

def generate_pdf(data):

    output_path = "NYXARA_OUTPUT.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=70,
        bottomMargin=60
    )

    story = []

    render_cover_page(story)

    render_intro_page(story)

    render_contents_page(story, data)

    render_workflow_page(story)

    for item in data:

        render_prompt_page(story, item)

    render_cta_page(story)

    doc.build(
        story,
        canvasmaker=NyxaraCanvas
    )

    return output_path

# =========================================================
# STREAMLIT UI
# =========================================================

st.set_page_config(
    page_title="NYXARA ENGINE",
    layout="wide"
)

st.title("👑 NYXARA ENGINE V1.0")

st.markdown("Crash-Proof Premium PDF Generator")

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("Bundle Settings")

    DOCUMENT_META["bundle_title"] = st.text_input(
        "Bundle Title",
        "NYXARA OPERATIONS SYSTEM"
    )

    DOCUMENT_META["target_niche"] = st.text_input(
        "Target Niche",
        "Retro Packaging Design"
    )

    cover_upload = st.file_uploader(
        "Upload Cover Page",
        type=["png", "jpg", "jpeg"]
    )

    if cover_upload:

        cover_path = "temp_cover.png"

        with open(cover_path, "wb") as f:

            f.write(cover_upload.getbuffer())

        DOCUMENT_META["cover_path"] = cover_path

        st.success("Cover Uploaded")

# =========================================================
# MAIN INPUT
# =========================================================

input_data = st.text_area(
    "Paste AI Bundle Data",
    height=500
)

# =========================================================
# GENERATE
# =========================================================

if st.button("🚀 GENERATE PDF"):

    parsed_data = parse_ai_data(input_data)

    if not parsed_data:

        st.error("Invalid AI data structure.")

    else:

        DOCUMENT_META["prompt_count"] = len(parsed_data)

        try:

            pdf_file = generate_pdf(parsed_data)

            st.success("PDF Generated Successfully")

            with open(pdf_file, "rb") as f:

                st.download_button(
                    "📥 DOWNLOAD PDF",
                    f,
                    file_name=pdf_file
                )

        except Exception as e:

            st.error(f"Crash Prevented: {str(e)}")
