# =========================================================
# NYXARA OS V8 — APPLE INSPIRED EDITORIAL PDF ENGINE
# FULL PREMIUM COMMERCIAL OPERATIONS EDITION
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
    HRFlowable,
    KeepInFrame,
)

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NYXARA OS V8",
    layout="wide",
)

# =========================================================
# GLOBAL CONSTANTS
# =========================================================

PAGE_WIDTH, PAGE_HEIGHT = letter

MAX_PROMPT_CHARS = 2200

BRAND_NAME = "NYXARA LABS"

# =========================================================
# APPLE-STYLE COLOR SYSTEM
# =========================================================

COLORS = {
    "bg": "#FAFAFA",
    "text": "#111111",
    "muted": "#6B7280",
    "line": "#E5E7EB",
    "soft": "#F3F4F6",
    "card": "#FFFFFF",
    "bonus": "#F8F4EC",
    "accent": "#C6A56D",
    "cream": "#F7F3EE",
}

# =========================================================
# TYPOGRAPHY SYSTEM
# =========================================================

styles = getSampleStyleSheet()

hero_style = ParagraphStyle(
    "Hero",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=30,
    leading=38,
    textColor=colors.HexColor(COLORS["text"]),
    spaceAfter=26,
)

title_style = ParagraphStyle(
    "Title",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=19,
    leading=28,
    textColor=colors.HexColor(COLORS["text"]),
    spaceAfter=12,
)

subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=11,
    leading=20,
    textColor=colors.HexColor(COLORS["muted"]),
    spaceAfter=18,
)

body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=10.5,
    leading=19,
    textColor=colors.HexColor("#2A2A2A"),
    spaceAfter=14,
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
    fontSize=9,
    leading=16,
    textColor=colors.HexColor("#111827"),
)

quote_style = ParagraphStyle(
    "Quote",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=24,
    leading=36,
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
# SAFE PROMPT SPLITTER
# =========================================================

def split_prompt(prompt, max_chars=MAX_PROMPT_CHARS):

    if len(prompt) <= max_chars:
        return [prompt]

    return textwrap.wrap(
        prompt,
        width=max_chars,
        break_long_words=False,
        replace_whitespace=False,
    )

# =========================================================
# HEADER / FOOTER ENGINE
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

        total_pages = len(self.pages)

        for page in self.pages:
            self.__dict__.update(page)
            self.draw_layout(total_pages)
            super().showPage()

        super().save()

    def draw_layout(self, total_pages):

        self.saveState()

        # HEADER
        if self.logo_path and os.path.exists(self.logo_path):

            try:
                self.drawImage(
                    self.logo_path,
                    50,
                    PAGE_HEIGHT - 42,
                    width=18,
                    height=18,
                    mask='auto'
                )

                self.setFont("Helvetica-Bold", 8)
                self.setFillColor(colors.HexColor("#7A7A7A"))

                self.drawString(
                    76,
                    PAGE_HEIGHT - 35,
                    BRAND_NAME
                )

            except:

                self.setFont("Helvetica-Bold", 8)
                self.drawString(
                    50,
                    PAGE_HEIGHT - 35,
                    BRAND_NAME
                )

        else:

            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#7A7A7A"))

            self.drawString(
                50,
                PAGE_HEIGHT - 35,
                BRAND_NAME
            )

        self.drawRightString(
            PAGE_WIDTH - 50,
            PAGE_HEIGHT - 35,
            "CREATIVE OPERATIONS SYSTEM"
        )

        self.setStrokeColor(colors.HexColor(COLORS["line"]))
        self.line(50, PAGE_HEIGHT - 48, PAGE_WIDTH - 50, PAGE_HEIGHT - 48)

        # FOOTER
        self.line(50, 42, PAGE_WIDTH - 50, 42)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#8B8B8B"))

        self.drawString(
            50,
            28,
            "Operational Editorial Publishing System"
        )

        self.drawRightString(
            PAGE_WIDTH - 50,
            28,
            f"PAGE {self._pageNumber}"
        )

        self.restoreState()

# =========================================================
# HELPERS
# =========================================================

def divider(story):

    story.append(
        HRFlowable(
            width="100%",
            thickness=0.5,
            color=colors.HexColor(COLORS["line"]),
        )
    )

    story.append(Spacer(1, 18))

# =========================================================
# COVER PAGE
# =========================================================

def render_cover(story, cover_path, bundle_title, niche):

    if cover_path and os.path.exists(cover_path):

        img = Image(
            cover_path,
            width=PAGE_WIDTH,
            height=PAGE_HEIGHT
        )

        story.append(img)

    else:

        story.append(Spacer(1, 240))

        story.append(
            Paragraph(
                bundle_title.upper(),
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

# =========================================================
# INTRO PAGE
# =========================================================

def render_intro(
    story,
    bundle_title,
    niche,
    total_prompts,
    bonus_count
):

    story.append(Spacer(1, 80))

    story.append(
        Paragraph(
            bundle_title.upper(),
            hero_style
        )
    )

    story.append(
        Paragraph(
            f"""
            {total_prompts} operational AI systems designed for
            structured execution inside the
            <b>{niche}</b> niche.
            """,
            subtitle_style
        )
    )

    divider(story)

    intro = f"""
    This operating system was built for creators,
    freelancers, agencies, and operators who want
    more consistency inside their creative workflows.

    Instead of relying on random prompting,
    disconnected experimentation,
    or repetitive manual work,
    this bundle focuses on operational clarity.

    Inside this system:
    <br/><br/>

    • {total_prompts - bonus_count} core operational systems<br/>
    • {bonus_count} bonus implementation assets<br/>
    • structured workflows<br/>
    • repeatable execution models<br/>
    • commercially usable outputs
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

    story.append(
        Paragraph(
            "SYSTEM INDEX",
            hero_style
        )
    )

    divider(story)

    story.append(
        Paragraph(
            "MAIN SYSTEMS",
            small_style
        )
    )

    story.append(Spacer(1, 10))

    for i, item in enumerate(main_prompts, start=1):

        story.append(
            Paragraph(
                f"{i:02d} — {item.get('title', 'Untitled')}",
                body_style
            )
        )

    if bonus_prompts:

        story.append(Spacer(1, 28))

        story.append(
            Paragraph(
                "BONUS SYSTEMS",
                small_style
            )
        )

        story.append(Spacer(1, 10))

        for i, item in enumerate(bonus_prompts, start=1):

            story.append(
                Paragraph(
                    f"BONUS {i:02d} — {item.get('title', 'Untitled')}",
                    body_style
                )
            )

    story.append(PageBreak())

# =========================================================
# BREATHING PAGE
# =========================================================

def render_breathing(story, text):

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

def render_prompt_card(
    story,
    item,
    number,
    bonus=False
):

    bg = COLORS["bonus"] if bonus else COLORS["soft"]

    label = (
        f"BONUS SYSTEM {number:02d}"
        if bonus else
        f"SYSTEM {number:02d}"
    )

    story.append(
        Paragraph(
            label,
            small_style
        )
    )

    story.append(
        Paragraph(
            item.get("title", "Untitled"),
            title_style
        )
    )

    story.append(
        Paragraph(
            item.get("description", ""),
            subtitle_style
        )
    )

    divider(story)

    sections = [

        ("WHY THIS WORKS", item.get("why_this_works", "")),
        ("MICRO EXAMPLE", item.get("micro_example", "")),
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

            story.append(
                Paragraph(
                    content.replace("\n", "<br/>"),
                    body_style
                )
            )

            story.append(Spacer(1, 8))

    # PROMPT BOX
    story.append(
        Paragraph(
            "OPERATIONAL PROMPT SYSTEM",
            small_style
        )
    )

    chunks = split_prompt(
        item.get("prompt", "")
    )

    for idx, chunk in enumerate(chunks):

        box = KeepInFrame(
            460,
            620,
            [
                Paragraph(
                    chunk.replace("\n", "<br/>"),
                    prompt_style
                )
            ],
            mode='shrink'
        )

        story.append(box)

        story.append(Spacer(1, 14))

    story.append(PageBreak())

# =========================================================
# BONUS INTRO PAGE
# =========================================================

def render_bonus_intro(story):

    story.append(Spacer(1, 180))

    story.append(
        Paragraph(
            "BONUS SYSTEMS",
            hero_style
        )
    )

    story.append(
        Paragraph(
            """
            Additional operational assets included
            to improve implementation flexibility,
            execution depth,
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

    story.append(Spacer(1, 150))

    text = """
    Strong systems reduce friction.

    Reduced friction improves consistency.

    Consistency compounds quietly over time.

    The goal was never
    to create more noise.

    The goal was to build
    calmer execution.
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

    story.append(Spacer(1, 220))

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
    bundle_title,
    niche,
    main_count,
    bonus_count,
    cover_path=None,
    logo_path=None
):

    pdf_name = "NYXARA_OS_V8.pdf"

    main_prompts = data[:main_count]

    bonus_prompts = data[main_count:]

    doc = SimpleDocTemplate(
        pdf_name,
        pagesize=letter,
        rightMargin=55,
        leftMargin=55,
        topMargin=70,
        bottomMargin=60,
    )

    story = []

    # COVER
    render_cover(
        story,
        cover_path,
        bundle_title,
        niche
    )

    # INTRO
    render_intro(
        story,
        bundle_title,
        niche,
        len(data),
        bonus_count
    )

    # CONTENTS
    render_contents(
        story,
        main_prompts,
        bonus_prompts
    )

    # BREATHING
    render_breathing(
        story,
        "Strong systems create calmer execution."
    )

    # MAIN SYSTEMS
    for i, item in enumerate(main_prompts, start=1):

        render_prompt_card(
            story,
            item,
            i,
            bonus=False
        )

    # BONUS INTRO
    if bonus_prompts:

        render_bonus_intro(story)

        for i, item in enumerate(bonus_prompts, start=1):

            render_prompt_card(
                story,
                item,
                i,
                bonus=True
            )

    # CTA
    render_cta(story)

    # END
    render_end(story)

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
# STREAMLIT INTERFACE
# =========================================================

st.title("👑 NYXARA OS V8")
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

        st.error("Invalid data format.")

    else:

        total = len(parsed)

        if (main_count + bonus_count) != total:

            st.error(
                f"""
                Prompt mismatch detected.

                Total prompts found: {total}

                Main + Bonus must equal total prompts.
                """
            )

        else:

            cover_path = None
            logo_path = None

            if cover_upload:

                cover_path = "cover_temp.png"

                with open(cover_path, "wb") as f:
                    f.write(cover_upload.getbuffer())

            if logo_upload:

                logo_path = "logo_temp.png"

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
