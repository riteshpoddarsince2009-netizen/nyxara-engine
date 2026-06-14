# =========================================================
# NYXARA OS V9
# APPLE-INSPIRED EDITORIAL PDF OPERATING SYSTEM
# FULL PREMIUM COMMERCIAL EDITION
# =========================================================

import streamlit as st
import ast
import os
import textwrap

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
    Flowable,
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
    page_title="NYXARA OS V9",
    layout="wide"
)

# =========================================================
# GLOBAL VARIABLES
# =========================================================

PAGE_WIDTH, PAGE_HEIGHT = letter

MAX_PROMPT_CHARS = 1800

# =========================================================
# COLOR SYSTEM (APPLE INSPIRED)
# =========================================================

COLORS = {
    "bg": "#FAFAFA",
    "text": "#111111",
    "muted": "#6B7280",
    "line": "#E7E7E7",
    "card": "#F5F5F7",
    "bonus": "#F8F2E8",
    "cream": "#F6F1EA",
    "accent": "#C5A46D",
    "white": "#FFFFFF",
}

# =========================================================
# TYPOGRAPHY
# =========================================================

styles = getSampleStyleSheet()

hero_style = ParagraphStyle(
    "Hero",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=31,
    leading=39,
    textColor=colors.HexColor(COLORS["text"]),
)

section_style = ParagraphStyle(
    "Section",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=21,
    leading=28,
    textColor=colors.HexColor(COLORS["text"]),
)

title_style = ParagraphStyle(
    "Title",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=18,
    leading=26,
    textColor=colors.HexColor(COLORS["text"]),
)

subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=11,
    leading=19,
    textColor=colors.HexColor(COLORS["muted"]),
)

body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=10.5,
    leading=19,
    textColor=colors.HexColor("#2D2D2D"),
)

small_style = ParagraphStyle(
    "Small",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8,
    leading=12,
    textColor=colors.HexColor(COLORS["muted"]),
)

prompt_style = ParagraphStyle(
    "Prompt",
    parent=styles["Code"],
    fontName="Courier",
    fontSize=8.8,
    leading=15,
    textColor=colors.HexColor("#1A1A1A"),
)

quote_style = ParagraphStyle(
    "Quote",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=26,
    leading=38,
    alignment=1,
    textColor=colors.HexColor(COLORS["text"]),
)

# =========================================================
# SAFE PARSER
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

# =========================================================
# SAFE SPLITTER
# =========================================================

def split_prompt(text):

    if len(text) <= MAX_PROMPT_CHARS:
        return [text]

    return textwrap.wrap(
        text,
        width=MAX_PROMPT_CHARS,
        break_long_words=False,
        replace_whitespace=False,
    )

# =========================================================
# FLOATING CARD
# =========================================================

class FloatingCard(Flowable):

    def __init__(
        self,
        content,
        width=470,
        height=0,
        background="#F5F5F7",
        padding=22
    ):

        Flowable.__init__(self)

        self.content = content
        self.width = width
        self.height = height
        self.background = background
        self.padding = padding

    def wrap(self, availWidth, availHeight):

        self.height = 20 + (len(self.content) / 3.5)

        return self.width, self.height

    def draw(self):

        self.canv.saveState()

        self.canv.setFillColor(
            colors.HexColor(self.background)
        )

        self.canv.roundRect(
            0,
            0,
            self.width,
            self.height,
            16,
            stroke=0,
            fill=1
        )

        self.canv.restoreState()

# =========================================================
# HEADER / FOOTER
# =========================================================

class EditorialCanvas(canvas.Canvas):

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

            self.draw_layout()

            super().showPage()

        super().save()

    def draw_layout(self):

        self.saveState()

        # HEADER LINE
        self.setStrokeColor(
            colors.HexColor(COLORS["line"])
        )

        self.line(
            55,
            PAGE_HEIGHT - 48,
            PAGE_WIDTH - 55,
            PAGE_HEIGHT - 48
        )

        # FOOTER LINE
        self.line(
            55,
            42,
            PAGE_WIDTH - 55,
            42
        )

        # LOGO
        if self.logo_path and os.path.exists(self.logo_path):

            try:

                self.drawImage(
                    self.logo_path,
                    55,
                    PAGE_HEIGHT - 41,
                    width=16,
                    height=16,
                    mask='auto'
                )

                self.setFont("Helvetica-Bold", 8)

                self.drawString(
                    78,
                    PAGE_HEIGHT - 35,
                    "NYXARA LABS"
                )

            except:

                self.drawString(
                    55,
                    PAGE_HEIGHT - 35,
                    "NYXARA LABS"
                )

        else:

            self.setFont("Helvetica-Bold", 8)

            self.drawString(
                55,
                PAGE_HEIGHT - 35,
                "NYXARA LABS"
            )

        # RIGHT HEADER
        self.setFont("Helvetica", 8)

        self.drawRightString(
            PAGE_WIDTH - 55,
            PAGE_HEIGHT - 35,
            "CREATIVE OPERATIONS SYSTEM"
        )

        # FOOTER
        self.setFont("Helvetica", 8)

        self.drawString(
            55,
            28,
            "Editorial Publishing Architecture"
        )

        self.drawRightString(
            PAGE_WIDTH - 55,
            28,
            f"PAGE {self._pageNumber}"
        )

        self.restoreState()

# =========================================================
# DIVIDER
# =========================================================

def divider(story):

    story.append(Spacer(1, 8))

# =========================================================
# COVER
# =========================================================

def render_cover(story, cover_path, title, niche):

    if cover_path and os.path.exists(cover_path):

        img = Image(
            cover_path,
            width=PAGE_WIDTH,
            height=PAGE_HEIGHT
        )

        story.append(img)

    else:

        story.append(Spacer(1, 260))

        story.append(
            Paragraph(
                title.upper(),
                hero_style
            )
        )

        story.append(Spacer(1, 18))

        story.append(
            Paragraph(
                niche,
                subtitle_style
            )
        )

    story.append(PageBreak())

# =========================================================
# INTRO PAGE
# =========================================================

def render_intro(
    story,
    title,
    niche,
    total_prompts,
    main_count,
    bonus_count
):

    story.append(Spacer(1, 85))

    story.append(
        Paragraph(
            title.upper(),
            hero_style
        )
    )

    story.append(Spacer(1, 22))

    story.append(
        Paragraph(
            f"""
            {total_prompts} operational AI systems designed
            for commercially believable execution
            inside the {niche} niche.
            """,
            subtitle_style
        )
    )

    story.append(Spacer(1, 44))

    intro = f"""
    Most AI bundles are filled with disconnected prompts,
    repetitive structures,
    and random experimentation.

    This system was designed differently.

    Instead of focusing on quantity alone,
    the goal was to create calmer execution,
    stronger creative consistency,
    and more repeatable operational workflows.

    <br/><br/>

    INCLUDED INSIDE THIS SYSTEM:

    <br/><br/>

    • {main_count} core operational systems<br/>
    • {bonus_count} bonus workflow assets<br/>
    • structured implementation flows<br/>
    • commercially usable prompt frameworks<br/>
    • repeatable creative systems
    """

    story.append(
        Paragraph(
            intro,
            body_style
        )
    )

    story.append(PageBreak())

# =========================================================
# CONTENTS PAGE
# =========================================================

def render_contents(
    story,
    main_prompts,
    bonus_prompts
):

    story.append(Spacer(1, 70))

    story.append(
        Paragraph(
            "SYSTEM INDEX",
            hero_style
        )
    )

    story.append(Spacer(1, 36))

    story.append(
        Paragraph(
            "MAIN SYSTEMS",
            small_style
        )
    )

    story.append(Spacer(1, 18))

    for i, item in enumerate(main_prompts, start=1):

        story.append(
            Paragraph(
                f"{i:02d} — {item.get('title', 'Untitled')}",
                body_style
            )
        )

        story.append(Spacer(1, 10))

    if bonus_prompts:

        story.append(Spacer(1, 30))

        story.append(
            Paragraph(
                "BONUS SYSTEMS",
                small_style
            )
        )

        story.append(Spacer(1, 18))

        for i, item in enumerate(bonus_prompts, start=1):

            story.append(
                Paragraph(
                    f"BONUS {i:02d} — {item.get('title', 'Untitled')}",
                    body_style
                )
            )

            story.append(Spacer(1, 10))

    story.append(PageBreak())

# =========================================================
# BREAK PAGE
# =========================================================

def render_break_page(story, text):

    story.append(Spacer(1, 240))

    story.append(
        Paragraph(
            text,
            quote_style
        )
    )

    story.append(PageBreak())

# =========================================================
# SYSTEM PAGE
# =========================================================

def render_system(
    story,
    item,
    number,
    bonus=False
):

    bg = COLORS["bonus"] if bonus else COLORS["card"]

    label = (
        f"BONUS SYSTEM {number:02d}"
        if bonus else
        f"SYSTEM {number:02d}"
    )

    story.append(Spacer(1, 50))

    story.append(
        Paragraph(
            label,
            small_style
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            item.get("title", "Untitled"),
            title_style
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            item.get("description", ""),
            subtitle_style
        )
    )

    story.append(Spacer(1, 34))

    sections = [

        ("WHY THIS WORKS", item.get("why_this_works", "")),
        ("HOW TO USE", item.get("how_to_use", "")),
        ("BUSINESS APPLICATION", item.get("business_application", "")),
        ("VALIDATION CASE", item.get("validation_case_study", "")),
    ]

    for title, content in sections:

        if content:

            story.append(
                Paragraph(
                    title,
                    small_style
                )
            )

            story.append(Spacer(1, 10))

            story.append(
                Paragraph(
                    content.replace("\n", "<br/>"),
                    body_style
                )
            )

            story.append(Spacer(1, 22))

    # PROMPT BLOCK
    story.append(
        Paragraph(
            "OPERATIONAL PROMPT SYSTEM",
            small_style
        )
    )

    story.append(Spacer(1, 16))

    chunks = split_prompt(
        item.get("prompt", "")
    )

    for chunk in chunks:

        story.append(
            FloatingCard(
                chunk,
                background=bg
            )
        )

        story.append(Spacer(1, 12))

        story.append(
            Paragraph(
                chunk.replace("\n", "<br/>"),
                prompt_style
            )
        )

        story.append(Spacer(1, 24))

    story.append(PageBreak())

# =========================================================
# BONUS INTRO
# =========================================================

def render_bonus_intro(story):

    story.append(Spacer(1, 230))

    story.append(
        Paragraph(
            "BONUS SYSTEMS",
            hero_style
        )
    )

    story.append(Spacer(1, 18))

    story.append(
        Paragraph(
            """
            Additional operational assets
            designed to improve workflow depth,
            execution flexibility,
            and creative consistency.
            """,
            subtitle_style
        )
    )

    story.append(PageBreak())

# =========================================================
# CTA PAGE
# =========================================================

def render_cta(story):

    story.append(Spacer(1, 210))

    text = """
    Creative momentum
    does not come
    from motivation.

    It comes from
    reduced friction.
    """

    story.append(
        Paragraph(
            text,
            quote_style
        )
    )

    story.append(PageBreak())

# =========================================================
# END PAGE
# =========================================================

def render_end(story):

    story.append(Spacer(1, 230))

    story.append(
        Paragraph(
            """
            Built for creators,
            operators,
            and teams who value
            clarity,
            consistency,
            and sustainable execution.
            """,
            quote_style
        )
    )

# =========================================================
# MAIN PDF ENGINE
# =========================================================

def generate_pdf(
    data,
    title,
    niche,
    main_count,
    bonus_count,
    cover_path=None,
    logo_path=None
):

    pdf_name = "NYXARA_OS_V9.pdf"

    main_prompts = data[:main_count]

    bonus_prompts = data[main_count:]

    doc = SimpleDocTemplate(
        pdf_name,
        pagesize=letter,
        rightMargin=55,
        leftMargin=55,
        topMargin=65,
        bottomMargin=60,
    )

    story = []

    # COVER
    render_cover(
        story,
        cover_path,
        title,
        niche
    )

    # INTRO
    render_intro(
        story,
        title,
        niche,
        len(data),
        main_count,
        bonus_count
    )

    # CONTENTS
    render_contents(
        story,
        main_prompts,
        bonus_prompts
    )

    # BREAK PAGE
    render_break_page(
        story,
        "Strong systems create calmer execution."
    )

    # MAIN SYSTEMS
    for i, item in enumerate(main_prompts, start=1):

        render_system(
            story,
            item,
            i,
            bonus=False
        )

        if i % 4 == 0:

            render_break_page(
                story,
                "Consistency compounds quietly over time."
            )

    # BONUS SECTION
    if bonus_prompts:

        render_bonus_intro(story)

        for i, item in enumerate(bonus_prompts, start=1):

            render_system(
                story,
                item,
                i,
                bonus=True
            )

    # CTA
    render_cta(story)

    # END PAGE
    render_end(story)

    # BUILD
    doc.build(
        story,
        canvasmaker=lambda *args, **kwargs:
        EditorialCanvas(
            *args,
            logo_path=logo_path,
            **kwargs
        )
    )

    return pdf_name

# =========================================================
# INTERFACE
# =========================================================

st.title("👑 NYXARA OS V9")
st.caption("Apple-Inspired Editorial Publishing Engine")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    bundle_title = st.text_input(
        "Bundle Title",
        value="Retro Packaging Design Operations System"
    )

    niche = st.text_input(
        "Micro-Niche",
        value="Vintage Packaging Design"
    )

with col2:

    main_count = st.number_input(
        "Main Prompt Count",
        min_value=1,
        value=20
    )

    bonus_count = st.number_input(
        "Bonus Prompt Count",
        min_value=0,
        value=4
    )

st.markdown("---")

cover_upload = st.file_uploader(
    "Upload Cover Page",
    type=["png", "jpg", "jpeg"]
)

logo_upload = st.file_uploader(
    "Upload Logo",
    type=["png", "jpg", "jpeg"]
)

raw_data = st.text_area(
    "Paste Prompt Data",
    height=420
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

        st.error("Invalid prompt data.")

    else:

        total = len(parsed)

        if main_count + bonus_count != total:

            st.error(
                f"""
                Prompt count mismatch.

                Total prompts detected: {total}

                Main + Bonus must equal total prompts.
                """
            )

        else:

            cover_path = None
            logo_path = None

            if cover_upload:

                cover_path = "temp_cover.png"

                with open(cover_path, "wb") as f:
                    f.write(cover_upload.getbuffer())

            if logo_upload:

                logo_path = "temp_logo.png"

                with open(logo_path, "wb") as f:
                    f.write(logo_upload.getbuffer())

            pdf = generate_pdf(
                parsed,
                bundle_title,
                niche,
                main_count,
                bonus_count,
                cover_path,
                logo_path
            )

            with open(pdf, "rb") as f:

                st.download_button(
                    "📥 Download NYXARA PDF",
                    f,
                    file_name=pdf,
                    use_container_width=True
                )

            st.success(
                "Editorial operating system generated successfully."
            )
