# =========================================================
# NYXARA OS — APPLE EDITION
# PREMIUM PDF SYSTEM ENGINE
# VERSION: V2.0
# =========================================================

import streamlit as st
import ast
import os
import re
import textwrap

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
    Preformatted,
    KeepTogether,
    Table,
    TableStyle
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.enums import (
    TA_CENTER,
    TA_LEFT,
    TA_RIGHT
)

from reportlab.pdfgen import canvas

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NYXARA OS",
    layout="wide"
)

# =========================================================
# COLOR SYSTEM
# =========================================================

PURE_WHITE = "#FFFFFF"
SOFT_WHITE = "#F5F5F7"
TEXT_BLACK = "#1D1D1F"
SECONDARY_TEXT = "#6E6E73"
DIVIDER = "#D2D2D7"
ACCENT = "#0071E3"
CARD_BG = "#FBFBFD"

# =========================================================
# DOCUMENT META
# =========================================================

DOCUMENT_META = {
    "brand_name": "NYXARA LABS",
    "bundle_title": "",
    "bundle_subtitle": "",
    "target_niche": "",
    "prompt_count": 0,
    "cover_path": None,
    "logo_path": None
}

# =========================================================
# SAFE HELPERS
# =========================================================

def clean_text(text):

    if not text:
        return ""

    text = str(text)

    text = text.replace("\t", " ")

    text = text.replace("•", "-")

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def safe_get(data, key, default=""):

    try:
        return clean_text(data.get(key, default))
    except:
        return default


def split_large_text(text, size=3200):

    if len(text) <= size:
        return [text]

    return textwrap.wrap(
        text,
        width=size,
        break_long_words=False,
        replace_whitespace=False
    )


# =========================================================
# DATA PARSER
# =========================================================

def parse_data(raw):

    raw = raw.strip()

    if raw.startswith("data ="):
        raw = raw.replace("data =", "", 1).strip()

    try:

        parsed = ast.literal_eval(raw)

        if isinstance(parsed, list):
            return parsed

        return []

    except:
        return []

# =========================================================
# PDF STYLES
# =========================================================

styles = getSampleStyleSheet()

STYLE_LABEL = ParagraphStyle(
    "STYLE_LABEL",
    parent=styles["BodyText"],
    fontName="Helvetica-Bold",
    fontSize=8,
    leading=10,
    textColor=colors.HexColor(SECONDARY_TEXT),
    alignment=TA_LEFT,
    spaceAfter=10
)

STYLE_TITLE = ParagraphStyle(
    "STYLE_TITLE",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=30,
    leading=36,
    textColor=colors.HexColor(TEXT_BLACK),
    alignment=TA_CENTER,
    spaceAfter=24
)

STYLE_SUBTITLE = ParagraphStyle(
    "STYLE_SUBTITLE",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=12,
    leading=20,
    textColor=colors.HexColor(SECONDARY_TEXT),
    alignment=TA_CENTER,
    spaceAfter=40
)

STYLE_SECTION = ParagraphStyle(
    "STYLE_SECTION",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=16,
    textColor=colors.HexColor(TEXT_BLACK),
    spaceAfter=12
)

STYLE_BODY = ParagraphStyle(
    "STYLE_BODY",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=10.5,
    leading=18,
    textColor=colors.HexColor(SECONDARY_TEXT),
    spaceAfter=16
)

STYLE_CARD = ParagraphStyle(
    "STYLE_CARD",
    parent=styles["Code"],
    fontName="Courier",
    fontSize=9,
    leading=16,
    textColor=colors.HexColor(TEXT_BLACK),
)

STYLE_FOOTER = ParagraphStyle(
    "STYLE_FOOTER",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=7,
    leading=10,
    textColor=colors.HexColor(SECONDARY_TEXT),
)

# =========================================================
# APPLE PAGE CANVAS
# =========================================================

class AppleCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._saved_page_states = []

    def showPage(self):

        self._saved_page_states.append(dict(self.__dict__))

        self._startPage()

    def save(self):

        total_pages = len(self._saved_page_states)

        for state in self._saved_page_states:

            self.__dict__.update(state)

            self.draw_layout(total_pages)

            super().showPage()

        super().save()

    def draw_layout(self, total_pages):

        self.saveState()

        width, height = letter

        # TOP DIVIDER

        self.setStrokeColor(colors.HexColor(DIVIDER))

        self.setLineWidth(0.5)

        self.line(50, height - 50, width - 50, height - 50)

        # HEADER

        self.setFont("Helvetica-Bold", 8)

        self.setFillColor(colors.HexColor(TEXT_BLACK))

        self.drawString(
            50,
            height - 38,
            "NYXARA LABS"
        )

        self.setFont("Helvetica", 8)

        self.setFillColor(colors.HexColor(SECONDARY_TEXT))

        self.drawRightString(
            width - 50,
            height - 38,
            "PRIVATE CREATIVE OPERATIONS"
        )

        # FOOTER

        self.line(50, 45, width - 50, 45)

        self.setFont("Helvetica", 7)

        self.setFillColor(colors.HexColor(SECONDARY_TEXT))

        self.drawString(
            50,
            30,
            "NYXARA LABS"
        )

        self.drawCentredString(
            width / 2,
            30,
            "CREATIVE OPERATIONS SYSTEM"
        )

        self.drawRightString(
            width - 50,
            30,
            f"PAGE {self._pageNumber:02d}"
        )

        self.restoreState()

# =========================================================
# PAGE HELPERS
# =========================================================

def section_divider(story):

    line = Table(
        [[""]],
        colWidths=[500],
        rowHeights=[1]
    )

    line.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor(DIVIDER))
    ]))

    story.append(line)

    story.append(Spacer(1, 24))


# =========================================================
# PROMPT CARD
# =========================================================

def build_prompt_card(text):

    text = clean_text(text)

    prompt_para = Preformatted(
        text,
        STYLE_CARD
    )

    card = Table(
        [[prompt_para]],
        colWidths=[500]
    )

    card.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor(CARD_BG)),

        ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor(DIVIDER)),

        ("LEFTPADDING", (0,0), (-1,-1), 28),

        ("RIGHTPADDING", (0,0), (-1,-1), 28),

        ("TOPPADDING", (0,0), (-1,-1), 24),

        ("BOTTOMPADDING", (0,0), (-1,-1), 24),

    ]))

    return card

# =========================================================
# COVER PAGE
# =========================================================

def render_cover(story):

    path = DOCUMENT_META["cover_path"]

    if path and os.path.exists(path):

        img = Image(path)

        img.drawWidth = 612
        img.drawHeight = 792

        story.append(img)

    else:

        story.append(Spacer(1, 250))

        story.append(
            Paragraph(
                DOCUMENT_META["bundle_title"],
                STYLE_TITLE
            )
        )

    story.append(PageBreak())

# =========================================================
# INTRO PAGE
# =========================================================

def render_intro(story):

    story.append(
        Paragraph(
            "CREATIVE OPERATIONS SYSTEM",
            STYLE_LABEL
        )
    )

    story.append(
        Paragraph(
            DOCUMENT_META["bundle_title"],
            STYLE_TITLE
        )
    )

    subtitle = f"""
    {DOCUMENT_META["prompt_count"]} Operational Systems Built for
    {DOCUMENT_META["target_niche"]}
    """

    story.append(
        Paragraph(
            subtitle,
            STYLE_SUBTITLE
        )
    )

    intro = """
    Most AI-generated creative work fails for one reason:
    the systems behind the outputs are inconsistent.

    Ideas become scattered.
    Visual direction changes too often.
    Creative workflows become difficult to repeat at scale.

    This operational system was designed to solve that problem.

    Instead of relying on random experimentation,
    these workflows focus on structure, consistency,
    commercial realism, and production clarity.

    Each system inside this bundle was designed to help creators,
    freelance designers, agencies, and operators develop stronger
    creative direction while reducing unnecessary production friction.

    Over time, the value of these systems comes not only from the outputs —
    but from the repeatable workflows they help create.
    """

    story.append(
        Paragraph(
            intro,
            STYLE_BODY
        )
    )

    section_divider(story)

    story.append(
        Paragraph(
            "WHAT THIS SYSTEM INCLUDES",
            STYLE_SECTION
        )
    )

    grid = Table([

        [
            Paragraph("""
            - Operational AI Systems<br/>
            - Workflow Structures<br/>
            - Visual Direction Systems<br/>
            - Commercial Creative Processes
            """, STYLE_BODY),

            Paragraph("""
            - Deployment Workflows<br/>
            - Production Logic<br/>
            - Internal Documentation Systems<br/>
            - Repeatable Creative Structures
            """, STYLE_BODY)
        ]

    ], colWidths=[240, 240])

    grid.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP")
    ]))

    story.append(grid)

    story.append(PageBreak())

# =========================================================
# CONTENTS PAGE
# =========================================================

def render_contents(story, data):

    story.append(
        Paragraph(
            "SYSTEM CONTENTS",
            STYLE_TITLE
        )
    )

    for i, item in enumerate(data, start=1):

        title = safe_get(item, "title")

        row = Table([[
            Paragraph(
                f"{i:02d}",
                STYLE_SECTION
            ),

            Paragraph(
                title,
                STYLE_BODY
            )
        ]], colWidths=[50, 430])

        row.setStyle(TableStyle([
            ("BOTTOMPADDING", (0,0), (-1,-1), 12)
        ]))

        story.append(row)

    story.append(PageBreak())

# =========================================================
# SYSTEM PAGE
# =========================================================

def render_system(story, item):

    title = safe_get(item, "title")

    description = safe_get(item, "description")

    prompt = safe_get(item, "prompt")

    why = safe_get(item, "why_this_works")

    business = safe_get(item, "business_application")

    case = safe_get(item, "validation_case_study")

    how = safe_get(item, "how_to_use")

    story.append(
        Paragraph(
            "OPERATIONAL SYSTEM",
            STYLE_LABEL
        )
    )

    story.append(
        Paragraph(
            title,
            STYLE_TITLE
        )
    )

    story.append(
        Paragraph(
            description,
            STYLE_SUBTITLE
        )
    )

    section_divider(story)

    story.append(
        Paragraph(
            "WHY THIS EXISTS",
            STYLE_SECTION
        )
    )

    story.append(
        Paragraph(
            why,
            STYLE_BODY
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "SYSTEM WORKFLOW",
            STYLE_SECTION
        )
    )

    story.append(
        Paragraph(
            how.replace("\n", "<br/><br/>"),
            STYLE_BODY
        )
    )

    story.append(PageBreak())

    # PROMPT PAGE

    story.append(
        Paragraph(
            "CORE OPERATIONAL SYSTEM",
            STYLE_LABEL
        )
    )

    story.append(
        Paragraph(
            title,
            STYLE_SECTION
        )
    )

    chunks = split_large_text(prompt)

    for chunk in chunks:

        story.append(
            build_prompt_card(chunk)
        )

        story.append(Spacer(1, 28))

    story.append(PageBreak())

    # APPLICATION PAGE

    story.append(
        Paragraph(
            "COMMERCIAL APPLICATION",
            STYLE_LABEL
        )
    )

    story.append(
        Paragraph(
            "Business Application",
            STYLE_SECTION
        )
    )

    story.append(
        Paragraph(
            business,
            STYLE_BODY
        )
    )

    section_divider(story)

    story.append(
        Paragraph(
            "Validation Case Study",
            STYLE_SECTION
        )
    )

    story.append(
        Paragraph(
            case,
            STYLE_BODY
        )
    )

    story.append(PageBreak())

# =========================================================
# CTA PAGE
# =========================================================

def render_cta(story):

    story.append(Spacer(1, 100))

    story.append(
        Paragraph(
            "BUILD SYSTEMS THAT LAST",
            STYLE_TITLE
        )
    )

    text = """
    Most creative projects fail because the workflow changes every time.

    Ideas become inconsistent.
    Production becomes fragmented.
    Teams waste hours rebuilding systems that should already exist.

    This operational toolkit was designed to solve that problem.

    Not by replacing creativity —
    but by creating structure around it.

    The strongest creative operators do not rely on inspiration alone.

    They rely on repeatable systems.
    Clear production workflows.
    Consistent execution standards.
    And operational clarity across every stage of the process.

    Use these systems as foundations.

    Adapt them.
    Improve them.
    Build your own internal workflows around them.

    Over time, the true value of this system will not come from the prompts themselves.

    It will come from the consistency,
    speed,
    and operational confidence you build using them.
    """

    story.append(
        Paragraph(
            text,
            STYLE_BODY
        )
    )

# =========================================================
# PDF ENGINE
# =========================================================

def generate_pdf(data):

    output = "NYXARA_OS.pdf"

    doc = SimpleDocTemplate(
        output,
        pagesize=letter,
        leftMargin=56,
        rightMargin=56,
        topMargin=70,
        bottomMargin=60
    )

    story = []

    render_cover(story)

    render_intro(story)

    render_contents(story, data)

    for item in data:

        render_system(story, item)

    render_cta(story)

    doc.build(
        story,
        canvasmaker=AppleCanvas
    )

    return output

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## NYXARA OS")

    DOCUMENT_META["bundle_title"] = st.text_input(
        "Bundle Title",
        "RETRO PACKAGING DESIGN OPERATIONS SYSTEM"
    )

    DOCUMENT_META["target_niche"] = st.text_input(
        "Target Niche",
        "Retro Packaging Design"
    )

    cover = st.file_uploader(
        "Upload Cover Page",
        type=["png", "jpg", "jpeg"]
    )

    if cover:

        path = "cover_temp.png"

        with open(path, "wb") as f:
            f.write(cover.getbuffer())

        DOCUMENT_META["cover_path"] = path

        st.success("Cover uploaded.")

# =========================================================
# MAIN UI
# =========================================================

st.markdown("# NYXARA OS")

st.markdown("""
A premium operational document system designed for
commercial AI workflow products.
""")

input_data = st.text_area(
    "Paste Operational System Data",
    height=450
)

# =========================================================
# GENERATE
# =========================================================

if st.button("Generate Operational PDF"):

    parsed = parse_data(input_data)

    if not parsed:

        st.error("Invalid data structure.")

    else:

        DOCUMENT_META["prompt_count"] = len(parsed)

        try:

            file = generate_pdf(parsed)

            st.success("PDF generated successfully.")

            with open(file, "rb") as f:

                st.download_button(
                    "Download PDF",
                    f,
                    file_name=file
                )

        except Exception as e:

            st.error(f"System prevented crash: {str(e)}")
