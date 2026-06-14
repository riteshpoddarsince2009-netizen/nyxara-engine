# =========================================================
# NYXARA OS V10
# ELECTRIC APPLE-STYLE EDITORIAL PDF ENGINE
# CRASH-PROOF + MAIN/BONUS MODULES + PERMANENT LOGO LOCK
# =========================================================

import os
import ast
import re
import html
import textwrap

import streamlit as st

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
from reportlab.pdfgen import canvas

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NYXARA OS V10",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# FILE SYSTEM
# =========================================================

ASSETS_DIR = "assets"
OUTPUTS_DIR = "outputs"
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# =========================================================
# CORE VARIABLES
# =========================================================

PAGE_WIDTH, PAGE_HEIGHT = letter
MAX_PROMPT_CHARS = 1400
BRAND_NAME = "NYXARA LABS"

# =========================================================
# ELECTRIC COLOR SYSTEM
# =========================================================

COLORS = {
    "bg": "#F4F7FF",
    "paper": "#FBFCFF",
    "text": "#0F172A",
    "muted": "#667085",
    "line": "#E6EAF2",
    "soft_line": "#F1F5F9",

    "electric_blue": "#DCE8FF",
    "electric_blue_2": "#CFE3FF",
    "soft_violet": "#E9DFFF",
    "soft_violet_2": "#DDD6FE",
    "cyan_glow": "#DDF7FF",
    "cyan_glow_2": "#C9F2FF",
    "peach_glow": "#FFE7D6",
    "warm_peach": "#FFF3EA",

    "glass": "#F8FAFF",
    "glass_2": "#F3F7FF",
    "glass_3": "#EEF4FF",

    "midnight": "#0B1120",
    "midnight_2": "#111827",

    "accent_blue": "#60A5FA",
    "accent_violet": "#A78BFA",
    "accent_cyan": "#22D3EE",
}

# =========================================================
# STREAMLIT UI THEME
# =========================================================

st.markdown(
    f"""
    <style>
        .stApp {{
            background:
                radial-gradient(circle at top right, rgba(220,232,255,0.90), transparent 28%),
                radial-gradient(circle at bottom left, rgba(233,223,255,0.75), transparent 24%),
                linear-gradient(180deg, #FFFFFF 0%, {COLORS["bg"]} 100%);
        }}

        .block-container {{
            padding-top: 2.0rem;
            padding-bottom: 2.0rem;
        }}

        .nyx-title {{
            font-size: 34px;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: {COLORS["text"]};
            margin-bottom: 0.15rem;
        }}

        .nyx-subtitle {{
            font-size: 14px;
            color: {COLORS["muted"]};
            line-height: 1.5;
            margin-bottom: 1rem;
        }}

        .soft-card {{
            border: 1px solid rgba(230,234,242,0.95);
            border-radius: 22px;
            padding: 18px 18px 16px 18px;
            background: rgba(255,255,255,0.78);
            box-shadow: 0 18px 50px rgba(15,23,42,0.04);
            backdrop-filter: blur(14px);
            margin-bottom: 12px;
        }}

        .metric-label {{
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: {COLORS["muted"]};
        }}

        .metric-value {{
            font-size: 26px;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: {COLORS["text"]};
            margin-top: 4px;
        }}

        .metric-note {{
            font-size: 12px;
            color: {COLORS["muted"]};
            margin-top: 3px;
        }}

        .electric-btn button {{
            background: linear-gradient(135deg, #DCE8FF 0%, #E9DFFF 55%, #DDF7FF 100%) !important;
            color: #0F172A !important;
            border: 1px solid rgba(15,23,42,0.08) !important;
            border-radius: 16px !important;
            font-weight: 800 !important;
            padding: 0.85rem 1.1rem !important;
        }}

        .stTextInput input, .stTextArea textarea {{
            border-radius: 16px !important;
            border: 1px solid rgba(230,234,242,1) !important;
            background: rgba(255,255,255,0.86) !important;
        }}

        .stNumberInput input {{
            border-radius: 16px !important;
        }}

        .small-pill {{
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            background: rgba(243,244,246,0.9);
            border: 1px solid rgba(230,234,242,1);
            font-size: 12px;
            color: {COLORS["text"]};
            margin-right: 8px;
            margin-bottom: 8px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# DOCUMENT META
# =========================================================

META = {
    "bundle_title": "RETRO PACKAGING DESIGN OPERATIONS SYSTEM",
    "main_prompt_count": 20,
    "bonus_prompt_count": 4,
}

# =========================================================
# SAFE HELPERS
# =========================================================

def clean_text(value):
    if value is None:
        return ""
    text = str(value)
    text = text.replace("\t", " ")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \u00A0]+", " ", text)
    return text.strip()

def safe_html(value):
    return html.escape(clean_text(value)).replace("\n", "<br/>")

def safe_parse(raw):
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

def sanitize_filename(name):
    name = clean_text(name).lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_") or "nyxara_os_v10"

def split_text_into_chunks(text, max_chars=MAX_PROMPT_CHARS):
    text = clean_text(text)
    if len(text) <= max_chars:
        return [text]

    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []
    current = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        candidate = f"{current}\n\n{para}" if current else para
        if len(candidate) <= max_chars:
            current = candidate
            continue

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
# STYLE SYSTEM
# =========================================================

styles = getSampleStyleSheet()

HERO_STYLE = ParagraphStyle(
    "HERO_STYLE",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=31,
    leading=38,
    textColor=colors.HexColor(COLORS["text"]),
)

INTRO_TITLE_STYLE = ParagraphStyle(
    "INTRO_TITLE_STYLE",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=28,
    leading=34,
    textColor=colors.HexColor(COLORS["text"]),
)

SECTION_STYLE = ParagraphStyle(
    "SECTION_STYLE",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=20,
    leading=26,
    textColor=colors.HexColor(COLORS["text"]),
)

TITLE_STYLE = ParagraphStyle(
    "TITLE_STYLE",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=18,
    leading=24,
    textColor=colors.HexColor(COLORS["text"]),
)

SUBTITLE_STYLE = ParagraphStyle(
    "SUBTITLE_STYLE",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=11.2,
    leading=18,
    textColor=colors.HexColor(COLORS["muted"]),
)

BODY_STYLE = ParagraphStyle(
    "BODY_STYLE",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=10.5,
    leading=18,
    textColor=colors.HexColor("#273244"),
)

SMALL_STYLE = ParagraphStyle(
    "SMALL_STYLE",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8,
    leading=10,
    textColor=colors.HexColor(COLORS["muted"]),
)

QUOTE_STYLE = ParagraphStyle(
    "QUOTE_STYLE",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=24,
    leading=36,
    alignment=1,
    textColor=colors.HexColor(COLORS["text"]),
)

PROMPT_STYLE = ParagraphStyle(
    "PROMPT_STYLE",
    parent=styles["Normal"],
    fontName="Courier",
    fontSize=8.75,
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
# PERMANENT LOGO
# =========================================================

def get_persistent_logo_path():
    return LOGO_PATH if os.path.exists(LOGO_PATH) else None

def save_logo_permanently(uploaded_file):
    if not uploaded_file:
        return None
    with open(LOGO_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return LOGO_PATH

# =========================================================
# PDF COMPONENTS
# =========================================================

class GlassPromptCard(Flowable):
    """
    Premium prompt card with:
    - real measured height
    - soft electric glow
    - auto split support
    - safe paragraph wrapping
    """

    def __init__(
        self,
        text,
        width=470,
        padding=20,
        bg_color="#F8FAFF",
        glow_color="#DCE8FF",
        accent_color="#60A5FA",
        bonus=False,
    ):
        super().__init__()
        self.text = clean_text(text)
        self.width = width
        self.padding = padding
        self.bg_color = bg_color
        self.glow_color = glow_color
        self.accent_color = accent_color
        self.bonus = bonus

        self.label = "BONUS OPERATIONAL SYSTEM" if bonus else "OPERATIONAL PROMPT SYSTEM"
        self.label_text = None
        self.body_para = None
        self.label_para = None

    def _build_paragraphs(self):
        self.label_text = self.label
        self.label_para = Paragraph(
            safe_html(self.label_text),
            PROMPT_LABEL_STYLE
        )
        self.body_para = Paragraph(
            safe_html(self.text),
            PROMPT_STYLE
        )

    def _measure(self, width, height_limit=99999):
        content_w = self.width - (self.padding * 2)

        _, label_h = self.label_para.wrap(content_w, height_limit)
        _, body_h = self.body_para.wrap(content_w, height_limit)

        self.real_height = (
            self.padding
            + label_h
            + 10
            + body_h
            + self.padding
        )
        self.real_width = self.width
        self.label_h = label_h
        self.body_h = body_h
        self.content_w = content_w
        return self.real_width, self.real_height

    def wrap(self, availWidth, availHeight):
        self._build_paragraphs()
        return self._measure(availWidth, availHeight)

    def split(self, availWidth, availHeight):
        self._build_paragraphs()
        _, h = self._measure(availWidth, availHeight)

        if h <= availHeight:
            return [self]

        words = self.text.split()
        if len(words) < 8:
            return [self]

        def fitted_height(text_part):
            tmp = GlassPromptCard(
                text_part,
                width=self.width,
                padding=self.padding,
                bg_color=self.bg_color,
                glow_color=self.glow_color,
                accent_color=self.accent_color,
                bonus=self.bonus,
            )
            tmp._build_paragraphs()
            _, th = tmp._measure(availWidth, 99999)
            return th

        lo, hi = 1, len(words) - 1
        best = None

        # Binary search for a split point that fits in one page
        while lo <= hi:
            mid = (lo + hi) // 2
            first = " ".join(words[:mid])
            th = fitted_height(first)

            if th <= availHeight - 20:
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1

        if not best:
            best = max(1, len(words) // 2)

        first_part = " ".join(words[:best]).strip()
        second_part = " ".join(words[best:]).strip()

        if not second_part:
            return [self]

        first_card = GlassPromptCard(
            first_part,
            width=self.width,
            padding=self.padding,
            bg_color=self.bg_color,
            glow_color=self.glow_color,
            accent_color=self.accent_color,
            bonus=self.bonus,
        )

        second_card = GlassPromptCard(
            second_part,
            width=self.width,
            padding=self.padding,
            bg_color=self.bg_color,
            glow_color=self.glow_color,
            accent_color=self.accent_color,
            bonus=self.bonus,
        )

        # Make continued label visually clear
        second_card.label = f"{self.label} — CONTINUED"
        return [first_card, second_card]

    def draw(self):
        c = self.canv

        # glow
        c.saveState()
        c.setFillColor(colors.HexColor(self.glow_color))
        c.roundRect(
            -3, -3,
            self.real_width + 6,
            self.real_height + 6,
            24,
            stroke=0,
            fill=1
        )

        # card
        c.setFillColor(colors.HexColor(self.bg_color))
        c.roundRect(
            0, 0,
            self.real_width,
            self.real_height,
            22,
            stroke=0,
            fill=1
        )

        # accent strip
        c.setFillColor(colors.HexColor(self.accent_color))
        c.roundRect(
            12,
            12,
            4,
            self.real_height - 24,
            2,
            stroke=0,
            fill=1
        )

        # white outline
        c.setStrokeColor(colors.HexColor("#FFFFFF"))
        c.setLineWidth(0.7)
        c.roundRect(
            0, 0,
            self.real_width,
            self.real_height,
            22,
            stroke=1,
            fill=0
        )

        # draw paragraphs
        content_x = self.padding + 10
        label_y = self.real_height - self.padding - self.label_h
        body_y = self.real_height - self.padding - self.label_h - 10 - self.body_h

        self.label_para.drawOn(
            c,
            content_x,
            label_y
        )

        self.body_para.drawOn(
            c,
            content_x,
            body_y
        )

        c.restoreState()

# =========================================================
# CANVAS
# =========================================================

class EditorialCanvas(canvas.Canvas):
    def __init__(self, *args, logo_path=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        self.logo_path = logo_path

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_layout()
            super().showPage()
        super().save()

    def draw_layout(self):
        self.saveState()

        # cover page: keep clean
        if self._pageNumber != 1:
            # background
            self.setFillColor(colors.HexColor(COLORS["bg"]))
            self.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

            # soft electric glows
            self.setFillColor(colors.HexColor(COLORS["electric_blue"]))
            self.circle(PAGE_WIDTH - 70, PAGE_HEIGHT - 80, 110, fill=1, stroke=0)

            self.setFillColor(colors.HexColor(COLORS["soft_violet"]))
            self.circle(65, PAGE_HEIGHT - 135, 85, fill=1, stroke=0)

            self.setFillColor(colors.HexColor(COLORS["cyan_glow"]))
            self.circle(68, 86, 92, fill=1, stroke=0)

            # header line
            self.setStrokeColor(colors.HexColor(COLORS["line"]))
            self.setLineWidth(0.5)
            self.line(55, PAGE_HEIGHT - 48, PAGE_WIDTH - 55, PAGE_HEIGHT - 48)

            # header branding
            if self.logo_path and os.path.exists(self.logo_path):
                try:
                    self.drawImage(
                        self.logo_path,
                        55,
                        PAGE_HEIGHT - 42,
                        width=16,
                        height=16,
                        mask='auto'
                    )
                    self.setFont("Helvetica-Bold", 8)
                    self.setFillColor(colors.HexColor(COLORS["muted"]))
                    self.drawString(78, PAGE_HEIGHT - 35, BRAND_NAME)
                except:
                    self.setFont("Helvetica-Bold", 8)
                    self.setFillColor(colors.HexColor(COLORS["muted"]))
                    self.drawString(55, PAGE_HEIGHT - 35, BRAND_NAME)
            else:
                self.setFont("Helvetica-Bold", 8)
                self.setFillColor(colors.HexColor(COLORS["muted"]))
                self.drawString(55, PAGE_HEIGHT - 35, BRAND_NAME)

            self.setFont("Helvetica", 8)
            self.drawRightString(
                PAGE_WIDTH - 55,
                PAGE_HEIGHT - 35,
                "CREATIVE OPERATIONS SYSTEM"
            )

            # footer line
            self.line(55, 42, PAGE_WIDTH - 55, 42)

            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor(COLORS["muted"]))
            self.drawString(55, 28, "Editorial Publishing Architecture")
            self.drawRightString( PAGE_WIDTH - 55, 28, f"PAGE {self._pageNumber}" )

        self.restoreState()

# =========================================================
# UI CARDS
# =========================================================

def render_metric_card(title, value, note, bg="rgba(255,255,255,0.78)", accent="#DCE8FF"):
    st.markdown(
        f"""
        <div class="soft-card" style="background:{bg}; border-left: 4px solid {accent};">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# PAGE BUILDERS
# =========================================================

def render_cover(story, cover_path, bundle_title, total_prompts_text):
    if cover_path and os.path.exists(cover_path):
        img = Image(cover_path, width=PAGE_WIDTH, height=PAGE_HEIGHT)
        story.append(img)
    else:
        story.append(Spacer(1, 190))
        story.append(Paragraph(bundle_title.upper(), HERO_STYLE))
        story.append(Spacer(1, 12))
        story.append(
            Paragraph(
                total_prompts_text,
                SUBTITLE_STYLE
            )
        )
        story.append(Spacer(1, 24))
        story.append(
            Paragraph(
                "A premium editorial operating system for structured creative execution.",
                BODY_STYLE
            )
        )
    story.append(PageBreak())

def render_intro(story, bundle_title, main_count, bonus_count):
    total = main_count + bonus_count

    story.append(Spacer(1, 92))
    story.append(Paragraph(bundle_title.upper(), HERO_STYLE))
    story.append(Spacer(1, 18))
    story.append(
        Paragraph(
            f"""
            {total} operational AI systems built for
            commercially believable execution.
            <br/><br/>
            <b>{main_count}</b> core systems
            &nbsp;&nbsp;•&nbsp;&nbsp;
            <b>{bonus_count}</b> bonus systems
            """,
            SUBTITLE_STYLE
        )
    )

    story.append(Spacer(1, 36))
    story.append(
        Paragraph(
            """
            Most AI bundles fail because they look like random prompt dumps.

            This system was designed differently.

            The focus is not just output — the focus is calm execution,
            clear hierarchy, and repeatable creative workflows that save time,
            reduce confusion, and make the work feel more controlled.
            """,
            BODY_STYLE
        )
    )

    story.append(Spacer(1, 20))
    story.append(Paragraph("WHAT THIS SYSTEM INCLUDES", SMALL_STYLE))
    story.append(Spacer(1, 10))

    intro_points = [
        f"{main_count} core operational systems",
        f"{bonus_count} bonus workflow assets",
        "commercially usable prompt frameworks",
        "repeatable implementation flows",
        "clear business application logic",
    ]

    for p in intro_points:
        story.append(Paragraph(f"• {p}", BODY_STYLE))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

def render_contents(story, main_prompts, bonus_prompts):
    story.append(Spacer(1, 70))
    story.append(Paragraph("SYSTEM INDEX", SECTION_STYLE))
    story.append(Spacer(1, 8))

    story.append(Paragraph("MAIN SYSTEMS", SMALL_STYLE))
    story.append(Spacer(1, 14))

    for i, item in enumerate(main_prompts, start=1):
        title = clean_text(item.get("title", "Untitled"))
        story.append(Paragraph(f"{i:02d} — {title}", BODY_STYLE))
        story.append(Spacer(1, 8))

    if bonus_prompts:
        story.append(Spacer(1, 20))
        story.append(Paragraph("BONUS SYSTEMS", SMALL_STYLE))
        story.append(Spacer(1, 14))

        for i, item in enumerate(bonus_prompts, start=1):
            title = clean_text(item.get("title", "Untitled"))
            story.append(Paragraph(f"BONUS {i:02d} — {title}", BODY_STYLE))
            story.append(Spacer(1, 8))

    story.append(PageBreak())

def render_break_page(story, text):
    story.append(Spacer(1, 220))
    story.append(Paragraph(text, QUOTE_STYLE))
    story.append(PageBreak())

def render_system(story, item, number, is_bonus=False):
    title = clean_text(item.get("title", "Untitled"))
    description = clean_text(item.get("description", ""))
    why = clean_text(item.get("why_this_works", ""))
    how = clean_text(item.get("how_to_use", ""))
    business = clean_text(item.get("business_application", ""))
    validation = clean_text(item.get("validation_case_study", ""))
    prompt = clean_text(item.get("prompt", ""))

    label = f"BONUS SYSTEM {number:02d}" if is_bonus else f"SYSTEM {number:02d}"

    story.append(Spacer(1, 48))
    story.append(Paragraph(label, SMALL_STYLE))
    story.append(Spacer(1, 8))
    story.append(Paragraph(title, TITLE_STYLE))
    story.append(Spacer(1, 10))
    story.append(Paragraph(description, SUBTITLE_STYLE))
    story.append(Spacer(1, 22))

    story.append(Paragraph("WHY THIS WORKS", SMALL_STYLE))
    story.append(Spacer(1, 8))
    story.append(Paragraph(why, BODY_STYLE))
    story.append(Spacer(1, 16))

    story.append(Paragraph("HOW TO USE", SMALL_STYLE))
    story.append(Spacer(1, 8))
    story.append(Paragraph(how.replace("\n", "<br/>"), BODY_STYLE))
    story.append(Spacer(1, 16))

    story.append(Paragraph("BUSINESS APPLICATION", SMALL_STYLE))
    story.append(Spacer(1, 8))
    story.append(Paragraph(business, BODY_STYLE))
    story.append(Spacer(1, 16))

    story.append(Paragraph("VALIDATION CASE", SMALL_STYLE))
    story.append(Spacer(1, 8))
    story.append(Paragraph(validation, BODY_STYLE))
    story.append(PageBreak())

    # Prompt page
    card_bg = COLORS["warm_peach"] if is_bonus else COLORS["glass"]
    glow = COLORS["peach_glow"] if is_bonus else COLORS["electric_blue"]
    label_text = "BONUS OPERATIONAL PROMPT SYSTEM" if is_bonus else "OPERATIONAL PROMPT SYSTEM"

    story.append(Spacer(1, 52))
    story.append(Paragraph(label_text, SMALL_STYLE))
    story.append(Spacer(1, 16))

    chunks = split_text_into_chunks(prompt)

    for idx, chunk in enumerate(chunks):
        prompt_card = GlassPromptCard(
            text=chunk,
            width=470,
            padding=20,
            bg_color=card_bg,
            glow_color=glow,
            accent_color=COLORS["accent_blue"] if not is_bonus else COLORS["accent_violet"],
            bonus=is_bonus,
        )
        story.append(prompt_card)
        if idx != len(chunks) - 1:
            story.append(Spacer(1, 14))

    story.append(PageBreak())

def render_bonus_intro(story):
    story.append(Spacer(1, 220))
    story.append(Paragraph("BONUS SYSTEMS", HERO_STYLE))
    story.append(Spacer(1, 18))
    story.append(
        Paragraph(
            """
            Additional operational assets designed to improve workflow depth,
            execution flexibility, and creative consistency.
            """,
            SUBTITLE_STYLE
        )
    )
    story.append(PageBreak())

def render_cta(story):
    story.append(Spacer(1, 200))
    story.append(
        Paragraph(
            """
            Creative momentum does not come from motivation.

            It comes from reduced friction.
            """,
            QUOTE_STYLE
        )
    )
    story.append(Spacer(1, 34))
    story.append(
        Paragraph(
            """
            The goal of this operating system was to create calmer execution,
            cleaner structure, and more sustainable creative output.

            Use it to reduce confusion, speed up decisions, and build a workflow
            that still works when motivation drops.
            """,
            SUBTITLE_STYLE
        )
    )
    story.append(PageBreak())

def render_end(story):
    story.append(Spacer(1, 230))
    story.append(
        Paragraph(
            """
            Built for creators, operators, and teams who value clarity,
            consistency, and sustainable execution.
            """,
            QUOTE_STYLE
        )
    )

# =========================================================
# PDF GENERATOR
# =========================================================

def generate_pdf(
    data,
    bundle_title,
    main_count,
    bonus_count,
    cover_path=None,
    logo_path=None,
):
    total = len(data)
    if main_count + bonus_count != total:
        raise ValueError(
            f"Main count + bonus count must equal total prompts. "
            f"Got main={main_count}, bonus={bonus_count}, total={total}."
        )

    main_prompts = data[:main_count]
    bonus_prompts = data[main_count:]

    safe_name = sanitize_filename(bundle_title)
    output_path = os.path.join(OUTPUTS_DIR, f"{safe_name}_nyxara_v10.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=55,
        leftMargin=55,
        topMargin=65,
        bottomMargin=60,
        pageCompression=1,
    )

    story = []

    total_prompts_text = f"{total} operational AI systems built for structured execution."

    # Cover
    render_cover(story, cover_path, bundle_title, total_prompts_text)

    # Intro
    render_intro(story, bundle_title, main_count, bonus_count)

    # Contents
    render_contents(story, main_prompts, bonus_prompts)

    # Breathing page
    render_break_page(story, "Strong systems create calmer execution.")

    # Main systems
    for i, item in enumerate(main_prompts, start=1):
        render_system(story, item, i, is_bonus=False)
        if i % 4 == 0 and i != len(main_prompts):
            render_break_page(story, "Consistency compounds quietly over time.")

    # Bonus intro and bonus systems
    if bonus_prompts:
        render_bonus_intro(story)
        for i, item in enumerate(bonus_prompts, start=1):
            render_system(story, item, i, is_bonus=True)

    # CTA + ending
    render_cta(story)
    render_end(story)

    doc.build(
        story,
        canvasmaker=lambda *args, **kwargs: EditorialCanvas(
            *args,
            logo_path=logo_path,
            **kwargs
        )
    )

    return output_path

# =========================================================
# INTERFACE
# =========================================================

st.markdown(
    """
    <div class="nyx-title">NYXARA OS V10</div>
    <div class="nyx-subtitle">
        Apple-inspired editorial publishing engine for premium AI prompt systems.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="small-pill">Electric UI</div>
    <div class="small-pill">Main + Bonus Split</div>
    <div class="small-pill">Permanent Logo Lock</div>
    <div class="small-pill">Crash-Proof Prompt Cards</div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# Sidebar controls
with st.sidebar:
    st.markdown("## NYXARA OS V10")
    st.markdown("Soft electric editorial publishing system.")

    st.markdown("### Permanent Logo")
    existing_logo = get_persistent_logo_path()

    if existing_logo:
        st.success("Logo locked and saved permanently.")
        try:
            st.image(existing_logo, width=96)
        except:
            pass
    else:
        logo_upload = st.file_uploader(
            "Upload Logo Once",
            type=["png", "jpg", "jpeg"],
            help="This logo will be saved permanently and used in future PDFs."
        )
        if logo_upload is not None:
            save_logo_permanently(logo_upload)
            st.success("Logo saved permanently. It will auto-lock for future PDFs.")

    st.markdown("---")

    # Count module cards
    st.markdown(
        f"""
        <div class="soft-card">
            <div class="metric-label">Main Prompt Count</div>
            <div class="metric-value">{META["main_prompt_count"]}</div>
            <div class="metric-note">Core operational systems.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="soft-card" style="border-left: 4px solid {COLORS["peach_glow"]};">
            <div class="metric-label">Bonus Prompt Count</div>
            <div class="metric-value">{META["bonus_prompt_count"]}</div>
            <div class="metric-note">Extra value systems at the end.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Main inputs
col1, col2 = st.columns([1.2, 1])

with col1:
    bundle_title = st.text_input(
        "Bundle Title",
        value=META["bundle_title"],
        help="Use the exact product title you want on the PDF."
    )

    cover_upload = st.file_uploader(
        "Upload Cover Page",
        type=["png", "jpg", "jpeg"],
        help="This is the first page of the PDF."
    )

with col2:
    main_prompt_count = st.number_input(
        "Main Prompt Count",
        min_value=1,
        value=int(META["main_prompt_count"]),
        step=1
    )

    bonus_prompt_count = st.number_input(
        "Bonus Prompt Count",
        min_value=0,
        value=int(META["bonus_prompt_count"]),
        step=1
    )

# Update meta
META["bundle_title"] = bundle_title
META["main_prompt_count"] = int(main_prompt_count)
META["bonus_prompt_count"] = int(bonus_prompt_count)

st.markdown("---")

# Dashboard line
st.markdown(
    f"""
    <div class="soft-card">
        <div class="metric-label">Bundle</div>
        <div class="metric-value" style="font-size:22px;">{clean_text(bundle_title)}</div>
        <div class="metric-note">No niche input. Title carries the positioning.</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="soft-card" style="border-left: 4px solid {COLORS["accent_blue"]};">
        <div class="metric-label">Module Split</div>
        <div class="metric-value" style="font-size:24px;">{main_prompt_count} Main + {bonus_prompt_count} Bonus</div>
        <div class="metric-note">Bonus prompts follow the main prompt sequence.</div>
    </div>
    """,
    unsafe_allow_html=True
)

raw_data = st.text_area(
    "Paste Prompt Data",
    height=440,
    help="Paste a Python list of dictionaries from the master prompt output."
)

generate = st.button(
    "Generate Editorial PDF",
    use_container_width=True
)

# =========================================================
# GENERATE
# =========================================================

if generate:
    parsed = safe_parse(raw_data)

    if not parsed:
        st.error("Invalid prompt data. Paste a Python list of dictionaries.")
    else:
        total = len(parsed)
        if main_prompt_count + bonus_prompt_count != total:
            st.error(
                f"Count mismatch: main ({main_prompt_count}) + bonus ({bonus_prompt_count}) must equal total prompts ({total})."
            )
        else:
            cover_path = None
            if cover_upload is not None:
                cover_path = os.path.join(ASSETS_DIR, "cover_temp.png")
                with open(cover_path, "wb") as f:
                    f.write(cover_upload.getbuffer())

            logo_path = get_persistent_logo_path()

            try:
                pdf_file = generate_pdf(
                    data=parsed,
                    bundle_title=bundle_title,
                    main_count=int(main_prompt_count),
                    bonus_count=int(bonus_prompt_count),
                    cover_path=cover_path,
                    logo_path=logo_path
                )

                st.success("Editorial PDF generated successfully.")

                with open(pdf_file, "rb") as f:
                    st.download_button(
                        "Download PDF",
                        f,
                        file_name=os.path.basename(pdf_file),
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"System prevented crash: {e}")
