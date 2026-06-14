# =========================================================
# NYXARA OS V7 — APPLE-INSPIRED EDITORIAL PDF ENGINE
# CRASH-PROOF COMMERCIAL OPERATIONS EDITION
# =========================================================

import streamlit as st
import ast
import os
import textwrap
from datetime import datetime

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
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NYXARA OS V7",
    layout="wide",
)

# =========================================================
# GLOBAL VARIABLES
# =========================================================

PAGE_WIDTH, PAGE_HEIGHT = letter

MAX_PROMPT_CHARS = 2200

COLOR_BG = "#FFFFFF"
COLOR_TEXT = "#111111"
COLOR_MUTED = "#6B7280"
COLOR_SOFT = "#F5F5F7"
COLOR_LINE = "#E5E7EB"
COLOR_ACCENT = "#C8A96B"

FONT_HERO = 28
FONT_TITLE = 19
FONT_SUBTITLE = 11
FONT_BODY = 10.5
FONT_SMALL = 8.5

BRAND_NAME = "NYXARA LABS"

# =========================================================
# STYLES
# =========================================================

styles = getSampleStyleSheet()

hero_style = ParagraphStyle(
    "Hero",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=FONT_HERO,
    leading=34,
    textColor=colors.HexColor(COLOR_TEXT),
    spaceAfter=24,
)

title_style = ParagraphStyle(
    "Title",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=FONT_TITLE,
    leading=26,
    textColor=colors.HexColor(COLOR_TEXT),
    spaceAfter=10,
)

subtitle_style = ParagraphStyle(
    "SubTitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=FONT_SUBTITLE,
    leading=18,
    textColor=colors.HexColor(COLOR_MUTED),
    spaceAfter=20,
)

body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=FONT_BODY,
    leading=18,
    textColor=colors.HexColor("#2C2C2C"),
    spaceAfter=14,
)

small_style = ParagraphStyle(
    "Small",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=FONT_SMALL,
    leading=14,
    textColor=colors.HexColor(COLOR_MUTED),
)

prompt_style = ParagraphStyle(
    "Prompt",
    parent=styles["Code"],
    fontName="Courier",
    fontSize=9.2,
    leading=16,
    textColor=colors.HexColor("#111827"),
    backColor=colors.HexColor("#F8F8F8"),
    borderPadding=16,
)

quote_style = ParagraphStyle(
    "Quote",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=22,
    leading=34,
    alignment=1,
    textColor=colors.HexColor("#111111"),
)

# =========================================================
# SAFE PARSER
# =========================================================

def safe_parse(raw_data):

    raw_data = raw_data.strip()

    if raw_data.startswith("data ="):
        raw_data = raw_data.replace("data =", "", 1)

    try:
        parsed = ast.literal_eval(raw_data)

        if isinstance(parsed, list):
            return parsed

    except:
        return []

    return []

# =========================================================
# PROMPT CHUNKER
# =========================================================

def chunk_prompt(text, max_chars=MAX_PROMPT_CHARS):

    chunks = textwrap.wrap(
        text,
        width=max_chars,
        break_long_words=False,
        replace_whitespace=False,
    )

    return chunks

# =========================================================
# PDF DECORATOR
# =========================================================

class EditorialCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):

        total_pages = len(self.pages)

        for page in self.pages:
            self.__dict__.update(page)
            self.draw_ui(total_pages)
            super().showPage()

        super().save()

    def draw_ui(self, total_pages):

        self.saveState()

        # Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#8B8B8B"))

        self.drawString(
            50,
            PAGE_HEIGHT - 38,
            BRAND_NAME
        )

        self.drawRightString(
            PAGE_WIDTH - 50,
            PAGE_HEIGHT - 38,
            "CREATIVE OPERATIONS SYSTEM"
        )

        self.setStrokeColor(colors.HexColor(COLOR_LINE))
        self.line(50, PAGE_HEIGHT - 50, PAGE_WIDTH - 50, PAGE_HEIGHT - 50)

        # Footer
        self.line(50, 42, PAGE_WIDTH - 50, 42)

        self.setFont("Helvetica", 8)

        self.drawString(
            50,
            28,
            "Operational Creative Publishing System"
        )

        self.drawRightString(
            PAGE_WIDTH - 50,
            28,
            f"PAGE {self._pageNumber}"
        )

        self.restoreState()

# =========================================================
# SECTION HELPERS
# =========================================================

def add_spacing(story, size=16):
    story.append(Spacer(1, size))


def add_divider(story):
    story.append(
        HRFlowable(
            width="100%",
            thickness=0.5,
            color=colors.HexColor(COLOR_LINE),
        )
    )
    add_spacing(story, 14)

# =========================================================
# INTRO PAGE
# =========================================================

def build_intro_page(story, bundle_title, niche, prompt_count):

    story.append(Spacer(1, 100))

    story.append(
        Paragraph(
            bundle_title.upper(),
            hero_style
        )
    )

    story.append(
        Paragraph(
            f"""
            {prompt_count} operational AI systems designed for
            commercially believable execution inside the
            <b>{niche}</b> niche.
            """,
            subtitle_style
        )
    )

    add_spacing(story, 30)

    intro_text = """
    Most AI systems fail after the excitement disappears.

    Too many disconnected prompts.
    Too much experimentation.
    Too little operational structure.

    This system was designed differently.

    Instead of generating random ideas,
    the goal is to create repeatable creative clarity.

    Every workflow inside this document was structured
    to reduce friction, improve consistency,
    and make execution easier to sustain over time.
    """

    story.append(
        Paragraph(
            intro_text,
            body_style
        )
    )

    story.append(PageBreak())

# =========================================================
# CONTENT PAGE
# =========================================================

def build_contents_page(story, data):

    story.append(
        Paragraph(
            "SYSTEM INDEX",
            title_style
        )
    )

    add_divider(story)

    for idx, item in enumerate(data, start=1):

        title = item.get("title", f"System {idx}")

        story.append(
            Paragraph(
                f"{idx:02d}. {title}",
                body_style
            )
        )

    story.append(PageBreak())

# =========================================================
# BREATHING PAGE
# =========================================================

def build_breathing_page(story, text):

    story.append(Spacer(1, 220))

    story.append(
        Paragraph(
            text,
            quote_style
        )
    )

    story.append(PageBreak())

# =========================================================
# PROMPT CARD
# =========================================================

def build_prompt_card(story, item, index):

    title = item.get("title", "Untitled")
    description = item.get("description", "")
    prompt = item.get("prompt", "")
    why = item.get("why_this_works", "")
    how = item.get("how_to_use", "")
    app = item.get("business_application", "")
    validation = item.get("validation_case_study", "")

    # Meta
    story.append(
        Paragraph(
            f"SYSTEM {index:02d}",
            small_style
        )
    )

    # Title
    story.append(
        Paragraph(
            title,
            title_style
        )
    )

    # Description
    story.append(
        Paragraph(
            description,
            subtitle_style
        )
    )

    add_divider(story)

    # WHY IT WORKS
    story.append(
        Paragraph(
            "Why This System Works",
            small_style
        )
    )

    story.append(
        Paragraph(
            why,
            body_style
        )
    )

    add_spacing(story, 8)

    # PROMPT
    story.append(
        Paragraph(
            "Operational System",
            small_style
        )
    )

    chunks = chunk_prompt(prompt)

    for chunk_index, chunk in enumerate(chunks):

        if len(chunks) > 1:
            story.append(
                Paragraph(
                    f"Part {chunk_index + 1}",
                    small_style
                )
            )

        story.append(
            Paragraph(
                chunk.replace("\n", "<br/>"),
                prompt_style
            )
        )

        add_spacing(story, 14)

    # HOW TO USE
    story.append(
        Paragraph(
            "Recommended Workflow",
            small_style
        )
    )

    story.append(
        Paragraph(
            how.replace("\n", "<br/>"),
            body_style
        )
    )

    # BUSINESS
    story.append(
        Paragraph(
            "Where This Creates Operational Leverage",
            small_style
        )
    )

    story.append(
        Paragraph(
            app,
            body_style
        )
    )

    # VALIDATION
    story.append(
        Paragraph(
            "Validation Scenario",
            small_style
        )
    )

    story.append(
        Paragraph(
            validation,
            body_style
        )
    )

    story.append(PageBreak())

# =========================================================
# CTA PAGE
# =========================================================

def build_cta_page(story):

    story.append(Spacer(1, 120))

    cta_text = """
    Most creative people do not fail because of lack of talent.

    They fail because fragmented systems slowly destroy momentum.

    Strong workflows reduce decision fatigue.

    Reduced decision fatigue increases execution consistency.

    Consistent execution compounds quietly over time.

    Build systems that still work on difficult days.
    """

    story.append(
        Paragraph(
            cta_text,
            quote_style
        )
    )

    add_spacing(story, 40)

    story.append(
        Paragraph(
            """
            The goal of this operating system was never
            to create more digital noise.

            The goal was to create calmer execution.

            Cleaner systems.
            Better structure.
            More sustainable creative momentum.
            """,
            subtitle_style
        )
    )

# =========================================================
# PDF ENGINE
# =========================================================

def generate_pdf(
    data,
    bundle_title,
    niche,
    cover_path=None
):

    pdf_name = "NYXARA_OS_V7.pdf"

    doc = SimpleDocTemplate(
        pdf_name,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=70,
        bottomMargin=60,
    )

    story = []

    # COVER PAGE
    if cover_path and os.path.exists(cover_path):

        img = Image(
            cover_path,
            width=PAGE_WIDTH,
            height=PAGE_HEIGHT
        )

        story.append(img)
        story.append(PageBreak())

    else:

        story.append(Spacer(1, 260))

        story.append(
            Paragraph(
                bundle_title,
                hero_style
            )
        )

        story.append(
            Paragraph(
                niche,
                subtitle_style
            )
        )

        story.append(PageBreak())

    # INTRO
    build_intro_page(
        story,
        bundle_title,
        niche,
        len(data)
    )

    # CONTENTS
    build_contents_page(
        story,
        data
    )

    # BREATHING PAGE
    build_breathing_page(
        story,
        "Strong systems reduce creative friction."
    )

    # PROMPTS
    for index, item in enumerate(data, start=1):

        build_prompt_card(
            story,
            item,
            index
        )

        if index % 3 == 0:

            build_breathing_page(
                story,
                "Consistency compounds quietly."
            )

    # CTA
    build_cta_page(story)

    # BUILD
    doc.build(
        story,
        canvasmaker=EditorialCanvas
    )

    return pdf_name

# =========================================================
# STREAMLIT UI
# =========================================================

st.title("👑 NYXARA OS V7")
st.caption("Apple-Inspired Editorial PDF Operating System")

st.markdown("---")

bundle_title = st.text_input(
    "Bundle Title",
    value="Retro Packaging Design Operations System"
)

niche = st.text_input(
    "Target Micro-Niche",
    value="Vintage Packaging Design"
)

cover = st.file_uploader(
    "Upload Cover Page",
    type=["png", "jpg", "jpeg"]
)

raw_data = st.text_area(
    "Paste Prompt Data",
    height=400
)

generate = st.button(
    "🚀 Generate Editorial PDF",
    use_container_width=True
)

# =========================================================
# GENERATE
# =========================================================

if generate:

    parsed = safe_parse(raw_data)

    if not parsed:

        st.error("Invalid data format.")

    else:

        cover_path = None

        if cover:

            cover_path = "temp_cover.png"

            with open(cover_path, "wb") as f:
                f.write(cover.getbuffer())

        pdf = generate_pdf(
            parsed,
            bundle_title,
            niche,
            cover_path
        )

        with open(pdf, "rb") as f:

            st.download_button(
                "📥 Download PDF",
                f,
                file_name=pdf,
                use_container_width=True
            )

        st.success("Editorial system generated successfully.")
