# =========================================================
# NYXARA OS — APPLE EDITION V3
# EDITORIAL OPERATING SYSTEM ENGINE
# CRASH-PROOF + CINEMATIC PDF ARCHITECTURE
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
    Table,
    TableStyle,
    KeepTogether,
    Preformatted
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
CARD_BG = "#FBFBFD"

TEXT_BLACK = "#1D1D1F"
TEXT_GRAY = "#6E6E73"

DIVIDER = "#D2D2D7"

ACCENT = "#0071E3"

# =========================================================
# GLOBAL META
# =========================================================

META = {
    "bundle_title": "",
    "bundle_subtitle": "",
    "niche": "",
    "prompt_count": 0,
    "cover_image": None,
    "creator_note": "",
    "intro_quote": "",
    "ending_quote": ""
}

# =========================================================
# SAFE HELPERS
# =========================================================

def safe_text(text):

    if text is None:
        return ""

    text = str(text)

    text = text.replace("\t", " ")

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def safe_get(data, key, default=""):

    try:
        return safe_text(data.get(key, default))
    except:
        return default


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


def split_prompt(text, max_chars=3500):

    if len(text) <= max_chars:
        return [text]

    return textwrap.wrap(
        text,
        width=max_chars,
        break_long_words=False,
        replace_whitespace=False
    )

# =========================================================
# STYLES
# =========================================================

styles = getSampleStyleSheet()

LABEL_STYLE = ParagraphStyle(
    "LABEL_STYLE",
    parent=styles["BodyText"],
    fontName="Helvetica-Bold",
    fontSize=8,
    leading=10,
    textColor=colors.HexColor(TEXT_GRAY),
    alignment=TA_LEFT,
    spaceAfter=8
)

TITLE_STYLE = ParagraphStyle(
    "TITLE_STYLE",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=28,
    leading=34,
    textColor=colors.HexColor(TEXT_BLACK),
    alignment=TA_LEFT,
    spaceAfter=20
)

CENTER_TITLE_STYLE = ParagraphStyle(
    "CENTER_TITLE_STYLE",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=30,
    leading=38,
    textColor=colors.HexColor(TEXT_BLACK),
    alignment=TA_CENTER,
    spaceAfter=20
)

BODY_STYLE = ParagraphStyle(
    "BODY_STYLE",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=10.5,
    leading=19,
    textColor=colors.HexColor(TEXT_GRAY),
    alignment=TA_LEFT,
    spaceAfter=16
)

QUOTE_STYLE = ParagraphStyle(
    "QUOTE_STYLE",
    parent=styles["BodyText"],
    fontName="Helvetica-Bold",
    fontSize=24,
    leading=34,
    textColor=colors.HexColor(TEXT_BLACK),
    alignment=TA_CENTER,
    spaceAfter=20
)

SMALL_STYLE = ParagraphStyle(
    "SMALL_STYLE",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=8,
    leading=12,
    textColor=colors.HexColor(TEXT_GRAY),
)

PROMPT_STYLE = ParagraphStyle(
    "PROMPT_STYLE",
    parent=styles["Code"],
    fontName="Courier",
    fontSize=9,
    leading=17,
    textColor=colors.HexColor(TEXT_BLACK),
)

SECTION_STYLE = ParagraphStyle(
    "SECTION_STYLE",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=18,
    textColor=colors.HexColor(TEXT_BLACK),
    spaceAfter=12
)

# =========================================================
# PAGE CANVAS
# =========================================================

class EditorialCanvas(canvas.Canvas):

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

        # HEADER LINE

        self.setStrokeColor(colors.HexColor(DIVIDER))
        self.setLineWidth(0.4)

        self.line(55, height - 45, width - 55, height - 45)

        # HEADER TEXT

        self.setFont("Helvetica-Bold", 8)

        self.setFillColor(colors.HexColor(TEXT_BLACK))

        self.drawString(
            55,
            height - 33,
            "NYXARA LABS"
        )

        self.setFont("Helvetica", 8)

        self.setFillColor(colors.HexColor(TEXT_GRAY))

        self.drawRightString(
            width - 55,
            height - 33,
            "PRIVATE CREATIVE OPERATIONS"
        )

        # FOOTER

        self.line(55, 42, width - 55, 42)

        self.setFont("Helvetica", 7)

        self.setFillColor(colors.HexColor(TEXT_GRAY))

        self.drawString(
            55,
            28,
            "NYXARA LABS"
        )

        self.drawCentredString(
            width / 2,
            28,
            "EDITORIAL OPERATING SYSTEM"
        )

        self.drawRightString(
            width - 55,
            28,
            f"PAGE {self._pageNumber:02d}"
        )

        self.restoreState()

# =========================================================
# COMPONENTS
# =========================================================

def divider(story):

    line = Table(
        [[""]],
        colWidths=[490],
        rowHeights=[1]
    )

    line.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor(DIVIDER))
    ]))

    story.append(line)

    story.append(Spacer(1, 28))


def cinematic_quote(story, text):

    story.append(Spacer(1, 220))

    story.append(
        Paragraph(
            text,
            QUOTE_STYLE
        )
    )

    story.append(Spacer(1, 220))

    story.append(PageBreak())


def prompt_card(title, prompt):

    label = Paragraph(
        "CORE OPERATIONAL SYSTEM",
        LABEL_STYLE
    )

    heading = Paragraph(
        title,
        SECTION_STYLE
    )

    prompt_para = Preformatted(
        safe_text(prompt),
        PROMPT_STYLE
    )

    footer = Paragraph(
        "Recommended Use: Internal workflow development, operational creative execution, repeatable production systems.",
        SMALL_STYLE
    )

    table = Table([

        [label],
        [heading],
        [prompt_para],
        [footer]

    ], colWidths=[490])

    table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor(CARD_BG)),

        ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor(DIVIDER)),

        ("LEFTPADDING", (0,0), (-1,-1), 28),

        ("RIGHTPADDING", (0,0), (-1,-1), 28),

        ("TOPPADDING", (0,0), (-1,-1), 24),

        ("BOTTOMPADDING", (0,0), (-1,-1), 24),

    ]))

    return table

# =========================================================
# COVER PAGE
# =========================================================

def build_cover(story):

    if META["cover_image"] and os.path.exists(META["cover_image"]):

        img = Image(META["cover_image"])

        img.drawWidth = 612
        img.drawHeight = 792

        story.append(img)

    else:

        story.append(Spacer(1, 240))

        story.append(
            Paragraph(
                META["bundle_title"],
                CENTER_TITLE_STYLE
            )
        )

        story.append(
            Paragraph(
                META["bundle_subtitle"],
                BODY_STYLE
            )
        )

    story.append(PageBreak())

# =========================================================
# INTRO PAGE
# =========================================================

def build_intro(story):

    story.append(
        Paragraph(
            "CREATIVE OPERATIONS SYSTEM",
            LABEL_STYLE
        )
    )

    story.append(
        Paragraph(
            META["bundle_title"],
            TITLE_STYLE
        )
    )

    story.append(
        Paragraph(
            META["bundle_subtitle"],
            BODY_STYLE
        )
    )

    divider(story)

    intro = f"""
    Most AI-generated work fails for one reason:
    the systems behind the outputs are inconsistent.

    Ideas become scattered.
    Creative direction changes too often.
    Production workflows become difficult to repeat.

    This operational system was designed to solve that problem.

    Instead of relying on random experimentation,
    these workflows focus on structure, consistency,
    commercial realism, and implementation clarity.

    The systems inside this bundle were designed to help creators,
    freelance designers, agencies, and operators develop more
    repeatable creative workflows while reducing production friction.

    Over time, the value of these systems comes not only from the outputs —
    but from the operational consistency they help create.
    """

    story.append(
        Paragraph(
            intro,
            BODY_STYLE
        )
    )

    story.append(Spacer(1, 26))

    story.append(
        Paragraph(
            "WHAT THIS SYSTEM INCLUDES",
            SECTION_STYLE
        )
    )

    grid = Table([

        [

            Paragraph("""
            • Operational AI Systems<br/>
            • Prompt Workflows<br/>
            • Commercial Use Cases<br/>
            • Production Structures
            """, BODY_STYLE),

            Paragraph("""
            • Workflow Systems<br/>
            • Deployment Guidance<br/>
            • Creative Direction Logic<br/>
            • Repeatable Processes
            """, BODY_STYLE)

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

def build_contents(story, data):

    story.append(
        Paragraph(
            "SYSTEM CONTENTS",
            CENTER_TITLE_STYLE
        )
    )

    story.append(Spacer(1, 20))

    for i, item in enumerate(data, start=1):

        title = safe_get(item, "title")

        row = Table([[
            Paragraph(f"{i:02d}", SECTION_STYLE),
            Paragraph(title, BODY_STYLE)
        ]], colWidths=[50, 420])

        row.setStyle(TableStyle([
            ("BOTTOMPADDING", (0,0), (-1,-1), 8)
        ]))

        story.append(row)

    story.append(PageBreak())

# =========================================================
# SYSTEM PAGE FLOW
# =========================================================

def build_system(story, item, index):

    title = safe_get(item, "title")

    description = safe_get(item, "description")

    why = safe_get(item, "why_this_works")

    how = safe_get(item, "how_to_use")

    business = safe_get(item, "business_application")

    case = safe_get(item, "validation_case_study")

    prompt = safe_get(item, "prompt")

    # -----------------------------------------------------
    # OVERVIEW PAGE
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "OPERATIONAL SYSTEM",
            LABEL_STYLE
        )
    )

    story.append(
        Paragraph(
            title,
            TITLE_STYLE
        )
    )

    story.append(
        Paragraph(
            description,
            BODY_STYLE
        )
    )

    divider(story)

    story.append(
        Paragraph(
            "WHY THIS SYSTEM WORKS",
            SECTION_STYLE
        )
    )

    story.append(
        Paragraph(
            why,
            BODY_STYLE
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "RECOMMENDED WORKFLOW",
            SECTION_STYLE
        )
    )

    story.append(
        Paragraph(
            how.replace("\n", "<br/><br/>"),
            BODY_STYLE
        )
    )

    story.append(PageBreak())

    # -----------------------------------------------------
    # PROMPT PAGE
    # -----------------------------------------------------

    chunks = split_prompt(prompt)

    for chunk in chunks:

        story.append(Spacer(1, 80))

        story.append(
            prompt_card(title, chunk)
        )

        story.append(PageBreak())

    # -----------------------------------------------------
    # APPLICATION PAGE
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "COMMERCIAL IMPLEMENTATION",
            LABEL_STYLE
        )
    )

    story.append(
        Paragraph(
            "Where This System Creates Operational Leverage",
            SECTION_STYLE
        )
    )

    story.append(
        Paragraph(
            business,
            BODY_STYLE
        )
    )

    divider(story)

    story.append(
        Paragraph(
            "Validation Scenario",
            SECTION_STYLE
        )
    )

    story.append(
        Paragraph(
            case,
            BODY_STYLE
        )
    )

    story.append(PageBreak())

    # -----------------------------------------------------
    # PHILOSOPHY BREAK
    # -----------------------------------------------------

    if index % 3 == 0:

        cinematic_quote(
            story,
            "Strong systems reduce creative friction."
        )

# =========================================================
# FINAL CTA
# =========================================================

def build_cta(story):

    story.append(Spacer(1, 180))

    story.append(
        Paragraph(
            "BUILD SLOWLY.<br/>SYSTEMS LAST LONGER.",
            QUOTE_STYLE
        )
    )

    story.append(Spacer(1, 70))

    ending = """
    The strongest creative systems are not built on inspiration alone.

    They are built on repeatable workflows,
    operational clarity,
    and consistent execution over time.

    Use these systems as foundations.

    Adapt them.
    Improve them.
    Build your own internal processes around them.

    Over time, the value of this operational system
    will come not from individual outputs —
    but from the consistency and confidence
    it helps create inside your creative workflow.
    """

    story.append(
        Paragraph(
            ending,
            BODY_STYLE
        )
    )

# =========================================================
# PDF ENGINE
# =========================================================

def generate_pdf(data):

    output_file = "NYXARA_OS_EDITORIAL.pdf"

    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        leftMargin=60,
        rightMargin=60,
        topMargin=70,
        bottomMargin=55
    )

    story = []

    build_cover(story)

    build_intro(story)

    cinematic_quote(
        story,
        "Consistency scales creativity."
    )

    build_contents(story, data)

    for index, item in enumerate(data, start=1):

        build_system(
            story,
            item,
            index
        )

    build_cta(story)

    doc.build(
        story,
        canvasmaker=EditorialCanvas
    )

    return output_file

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## NYXARA OS")

    META["bundle_title"] = st.text_input(
        "Bundle Title",
        "RETRO PACKAGING DESIGN OPERATIONS SYSTEM"
    )

    META["bundle_subtitle"] = st.text_area(
        "Bundle Subtitle",
        "Operational systems built for nostalgic packaging, commercial retro branding, visual consistency, and repeatable creative workflows."
    )

    META["niche"] = st.text_input(
        "Target Niche",
        "Retro Packaging Design"
    )

    uploaded_cover = st.file_uploader(
        "Upload Cover Image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_cover:

        cover_path = "nyxara_cover.png"

        with open(cover_path, "wb") as f:
            f.write(uploaded_cover.getbuffer())

        META["cover_image"] = cover_path

        st.success("Cover uploaded successfully.")

# =========================================================
# MAIN UI
# =========================================================

st.markdown("# NYXARA OS — Editorial Engine")

st.markdown("""
Generate Apple-inspired operational PDF systems
with cinematic pacing and editorial structure.
""")

input_data = st.text_area(
    "Paste Operational System Data",
    height=500
)

# =========================================================
# GENERATE BUTTON
# =========================================================

if st.button("Generate Editorial PDF"):

    parsed = parse_data(input_data)

    if not parsed:

        st.error("Invalid Python list format.")

    else:

        META["prompt_count"] = len(parsed)

        try:

            output = generate_pdf(parsed)

            st.success("Editorial PDF generated successfully.")

            with open(output, "rb") as f:

                st.download_button(
                    "Download Editorial PDF",
                    f,
                    file_name=output
                )

        except Exception as e:

            st.error(f"System prevented crash: {str(e)}")
