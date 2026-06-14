# =========================================================
# NYXARA OS V11
# ELECTRIC EDITORIAL PDF ENGINE
# FIXED: PRIVÉ HEADER, PERMANENT LOGO LOCK, MAIN/BONUS SPLIT
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
    NextPageTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
    Flowable,
)
from reportlab.pdfgen import canvas

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NYXARA OS V11",
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
# CORE CONSTANTS
# =========================================================

PAGE_WIDTH, PAGE_HEIGHT = letter
BRAND_NAME = "NYXARA LABS"
MAX_PROMPT_CHARS = 1400

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
# STREAMLIT LOOK
# =========================================================

st.markdown(
    f"""
    <style>
        .stApp {{
            background:
                radial-gradient(circle at top right, rgba(220,232,255,0.90), transparent 28%),
                radial-gradient(circle at bottom left, rgba(233,223,255,0.70), transparent 24%),
                linear-gradient(180deg, #FFFFFF 0%, {COLORS["bg"]} 100%);
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}

        .nyx-title {{
            font-size: 34px;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: {COLORS["text"]};
            margin-bottom: 0.1rem;
        }}

        .nyx-subtitle {{
            font-size: 14px;
            color: {COLORS["muted"]};
            line-height: 1.5;
            margin-bottom: 1rem;
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

        .stTextInput input, .stTextArea textarea, .stNumberInput input {{
            border-radius: 16px !important;
            border: 1px solid rgba(230,234,242,1) !important;
            background: rgba(255,255,255,0.86) !important;
        }}

        .stButton button {{
            background: linear-gradient(135deg, #DCE8FF 0%, #E9DFFF 55%, #DDF7FF 100%) !important;
            color: #0F172A !important;
            border: 1px solid rgba(15,23,42,0.08) !important;
            border-radius: 16px !important;
            font-weight: 800 !important;
            padding: 0.85rem 1.1rem !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# META
# =========================================================

DEFAULT_TITLE = "RETRO PACKAGING DESIGN OPERATIONS SYSTEM"
META = {
    "bundle_title": DEFAULT_TITLE,
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
    return name.strip("_") or "nyxara_os_v11"

def save_logo_permanently(uploaded_file):
    if not uploaded_file:
        return None
    with open(LOGO_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return LOGO_PATH

def get_persistent_logo():
    return LOGO_PATH if os.path.exists(LOGO_PATH) else None

def normalize_prompt_for_display(text):
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

        # Skip markdown separator rows like |---|---|
        if re.fullmatch(r"\|[\s:\-\|]+\|", s):
            continue

        # Table-like rows
        if s.startswith("|") and "|" in s[1:]:
            cells = [c.strip() for c in s.strip("|").split("|")]
            row = " | ".join(cells)

            wrapped = textwrap.wrap(
                row,
                width=95,
                break_long_words=True,
                break_on_hyphens=False
            )
            out.extend(wrapped if wrapped else [row])
            continue

        wrapped = textwrap.wrap(
            s,
            width=95,
            break_long_words=True,
            break_on_hyphens=False
        )
        out.extend(wrapped if wrapped else [s])

    return "\n".join(out).strip()

def split_prompt_into_chunks(text, max_chars=MAX_PROMPT_CHARS):
    text = normalize_prompt_for_display(text)

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

HERO_STYLE = ParagraphStyle(
    "HERO_STYLE",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=31,
    leading=38,
    textColor=colors.HexColor(COLORS["text"]),
)

INTRO_STYLE = ParagraphStyle(
    "INTRO_STYLE",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=26,
    leading=32,
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

PROMPT_LABEL_STYLE = ParagraphStyle(
    "PROMPT_LABEL_STYLE",
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
    fontSize=8.75,
    leading=15,
    textColor=colors.HexColor("#111827"),
)

# =========================================================
# PROMPT CARD
# =========================================================

class GlassPromptCard(Flowable):
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
        self.label_para = None
        self.body_para = None

    def _build(self):
        self.label_para = Paragraph(safe_html(self.label), PROMPT_LABEL_STYLE)
        self.body_para = Paragraph(safe_html(self.text), PROMPT_STYLE)

    def wrap(self, availWidth, availHeight):
        self._build()
        content_w = self.width - (self.padding * 2) - 10
        _, label_h = self.label_para.wrap(content_w, 99999)
        _, body_h = self.body_para.wrap(content_w, 99999)
        self.label_h = label_h
        self.body_h = body_h
        self.content_w = content_w
        self.real_height = self.padding + label_h + 10 + body_h + self.padding
        self.real_width = self.width
        return self.real_width, self.real_height

    def split(self, availWidth, availHeight):
        self._build()
        _, h = self.wrap(availWidth, availHeight)

        if h <= availHeight:
            return [self]

        lines = self.text.split("\n")
        if len(lines) < 4:
            words = self.text.split()
            if len(words) < 12:
                return [self]
            # Break a long single paragraph into two pieces
            mid = len(words) // 2
            first = " ".join(words[:mid]).strip()
            second = " ".join(words[mid:]).strip()
            if not second:
                return [self]
            first_card = GlassPromptCard(
                first,
                width=self.width,
                padding=self.padding,
                bg_color=self.bg_color,
                glow_color=self.glow_color,
                accent_color=self.accent_color,
                bonus=self.bonus,
            )
            second_card = GlassPromptCard(
                second,
                width=self.width,
                padding=self.padding,
                bg_color=self.bg_color,
                glow_color=self.glow_color,
                accent_color=self.accent_color,
                bonus=self.bonus,
            )
            second_card.label = f"{self.label} — CONTINUED"
            return [first_card, second_card]

        def height_for(sub_lines):
            sub_text = "\n".join(sub_lines).strip()
            tmp = GlassPromptCard(
                sub_text,
                width=self.width,
                padding=self.padding,
                bg_color=self.bg_color,
                glow_color=self.glow_color,
                accent_color=self.accent_color,
                bonus=self.bonus,
            )
            tmp._build()
            _, th = tmp.wrap(availWidth, 99999)
            return th

        lo, hi = 1, len(lines) - 1
        best = None

        while lo <= hi:
            mid = (lo + hi) // 2
            first_lines = lines[:mid]
            th = height_for(first_lines)

            if th <= availHeight - 20:
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1

        if not best:
            best = max(1, len(lines) // 2)

        first_text = "\n".join(lines[:best]).strip()
        second_text = "\n".join(lines[best:]).strip()

        if not second_text:
            return [self]

        first_card = GlassPromptCard(
            first_text,
            width=self.width,
            padding=self.padding,
            bg_color=self.bg_color,
            glow_color=self.glow_color,
            accent_color=self.accent_color,
            bonus=self.bonus,
        )
        second_card = GlassPromptCard(
            second_text,
            width=self.width,
            padding=self.padding,
            bg_color=self.bg_color,
            glow_color=self.glow_color,
            accent_color=self.accent_color,
            bonus=self.bonus,
        )
        second_card.label = f"{self.label} — CONTINUED"
        return [first_card, second_card]

    def draw(self):
        c = self.canv
        c.saveState()

        # glow
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

        content_x = self.padding + 10
        label_y = self.real_height - self.padding - self.label_h
        body_y = self.real_height - self.padding - self.label_h - 10 - self.body_h

        self.label_para.drawOn(c, content_x, label_y)
        self.body_para.drawOn(c, content_x, body_y)

        c.restoreState()

# =========================================================
# PAGE DRAWING
# =========================================================

def draw_cover_page(canvas_obj, doc):
    if getattr(doc, "_has_cover_image", False):
        return

    canvas_obj.saveState()
    canvas_obj.setFillColor(colors.HexColor(COLORS["bg"]))
    canvas_obj.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    canvas_obj.setFillColor(colors.HexColor(COLORS["electric_blue"]))
    canvas_obj.circle(PAGE_WIDTH - 70, PAGE_HEIGHT - 80, 110, fill=1, stroke=0)

    canvas_obj.setFillColor(colors.HexColor(COLORS["soft_violet"]))
    canvas_obj.circle(65, PAGE_HEIGHT - 135, 85, fill=1, stroke=0)

    canvas_obj.setFillColor(colors.HexColor(COLORS["cyan_glow"]))
    canvas_obj.circle(68, 86, 92, fill=1, stroke=0)

    canvas_obj.setStrokeColor(colors.HexColor(COLORS["line"]))
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(55, PAGE_HEIGHT - 48, PAGE_WIDTH - 55, PAGE_HEIGHT - 48)

    canvas_obj.setFont("Helvetica-Bold", 8)
    canvas_obj.setFillColor(colors.HexColor(COLORS["muted"]))
    canvas_obj.drawString(55, PAGE_HEIGHT - 35, BRAND_NAME)

    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawRightString(PAGE_WIDTH - 55, PAGE_HEIGHT - 35, "PRIVÉ")

    canvas_obj.line(55, 42, PAGE_WIDTH - 55, 42)

    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawString(55, 28, "Editorial Publishing Architecture")
    canvas_obj.drawRightString(PAGE_WIDTH - 55, 28, "PAGE 1")
    canvas_obj.restoreState()

def draw_content_page(canvas_obj, doc):
    canvas_obj.saveState()

    canvas_obj.setFillColor(colors.HexColor(COLORS["bg"]))
    canvas_obj.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    canvas_obj.setFillColor(colors.HexColor(COLORS["electric_blue"]))
    canvas_obj.circle(PAGE_WIDTH - 70, PAGE_HEIGHT - 80, 110, fill=1, stroke=0)

    canvas_obj.setFillColor(colors.HexColor(COLORS["soft_violet"]))
    canvas_obj.circle(65, PAGE_HEIGHT - 135, 85, fill=1, stroke=0)

    canvas_obj.setFillColor(colors.HexColor(COLORS["cyan_glow"]))
    canvas_obj.circle(68, 86, 92, fill=1, stroke=0)

    canvas_obj.setStrokeColor(colors.HexColor(COLORS["line"]))
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(55, PAGE_HEIGHT - 48, PAGE_WIDTH - 55, PAGE_HEIGHT - 48)

    if getattr(doc, "_logo_path", None) and os.path.exists(doc._logo_path):
        try:
            canvas_obj.drawImage(
                doc._logo_path,
                55,
                PAGE_HEIGHT - 42,
                width=16,
                height=16,
                mask='auto'
            )
            canvas_obj.setFont("Helvetica-Bold", 8)
            canvas_obj.setFillColor(colors.HexColor(COLORS["muted"]))
            canvas_obj.drawString(78, PAGE_HEIGHT - 35, BRAND_NAME)
        except:
            canvas_obj.setFont("Helvetica-Bold", 8)
            canvas_obj.setFillColor(colors.HexColor(COLORS["muted"]))
            canvas_obj.drawString(55, PAGE_HEIGHT - 35, BRAND_NAME)
    else:
        canvas_obj.setFont("Helvetica-Bold", 8)
        canvas_obj.setFillColor(colors.HexColor(COLORS["muted"]))
        canvas_obj.drawString(55, PAGE_HEIGHT - 35, BRAND_NAME)

    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawRightString(PAGE_WIDTH - 55, PAGE_HEIGHT - 35, "PRIVÉ")

    canvas_obj.line(55, 42, PAGE_WIDTH - 55, 42)

    canvas_obj.setFont("Helvetica", 8)
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
    if bundle_title:
        story.append(Spacer(1, 180))
        story.append(Paragraph(bundle_title.upper(), HERO_STYLE))
        spacer(story, 14)
        story.append(Paragraph(total_prompts_text, SUBTITLE_STYLE))
        spacer(story, 24)
        story.append(Paragraph("A premium editorial operating system for structured creative execution.", BODY_STYLE))

def render_intro(story, bundle_title, main_count, bonus_count):
    total = main_count + bonus_count
    story.append(Spacer(1, 80))
    story.append(Paragraph(bundle_title.upper(), HERO_STYLE))
    spacer(story, 16)
    story.append(
        Paragraph(
            f"""
            {total} operational AI systems designed for commercially believable execution.
            <br/><br/>
            <b>{main_count}</b> core systems &nbsp;&nbsp;•&nbsp;&nbsp; <b>{bonus_count}</b> bonus systems
            """,
            SUBTITLE_STYLE
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
            BODY_STYLE
        )
    )
    spacer(story, 18)
    story.append(Paragraph("WHAT THIS SYSTEM INCLUDES", SMALL_STYLE))
    spacer(story, 10)

    items = [
        f"{main_count} core operational systems",
        f"{bonus_count} bonus workflow assets",
        "commercially usable prompt frameworks",
        "repeatable implementation flows",
        "clear business application logic",
    ]
    for item in items:
        story.append(Paragraph(f"• {item}", BODY_STYLE))
        spacer(story, 4)
    story.append(PageBreak())

def render_contents(story, main_prompts, bonus_prompts):
    spacer(story, 70)
    story.append(Paragraph("SYSTEM INDEX", SECTION_STYLE))
    spacer(story, 8)

    story.append(Paragraph("MAIN SYSTEMS", SMALL_STYLE))
    spacer(story, 12)
    for i, item in enumerate(main_prompts, start=1):
        title = clean_text(item.get("title", "Untitled"))
        story.append(Paragraph(f"{i:02d} — {title}", BODY_STYLE))
        spacer(story, 8)

    if bonus_prompts:
        spacer(story, 18)
        story.append(Paragraph("BONUS SYSTEMS", SMALL_STYLE))
        spacer(story, 12)
        for i, item in enumerate(bonus_prompts, start=1):
            title = clean_text(item.get("title", "Untitled"))
            story.append(Paragraph(f"BONUS {i:02d} — {title}", BODY_STYLE))
            spacer(story, 8)
    story.append(PageBreak())

def render_breathing(story, text):
    spacer(story, 210)
    story.append(Paragraph(text, QUOTE_STYLE))
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
    story.append(Paragraph(label, SMALL_STYLE))
    spacer(story, 8)
    story.append(Paragraph(title, TITLE_STYLE))
    spacer(story, 10)
    if description:
        story.append(Paragraph(description, SUBTITLE_STYLE))
    spacer(story, 18)

    blocks = [
        ("WHY THIS WORKS", why),
        ("MICRO EXAMPLE", micro),
        ("HOW TO USE", how),
        ("BUSINESS APPLICATION", business),
        ("VALIDATION CASE", validation),
    ]

    for heading, content in blocks:
        if not content:
            continue
        story.append(Paragraph(heading, SMALL_STYLE))
        spacer(story, 8)
        story.append(Paragraph(content.replace("\n", "<br/>"), BODY_STYLE))
        spacer(story, 14)

    story.append(Paragraph("OPERATIONAL PROMPT SYSTEM", SMALL_STYLE))
    spacer(story, 14)

    card_bg = COLORS["warm_peach"] if bonus else COLORS["glass"]
    glow = COLORS["peach_glow"] if bonus else COLORS["electric_blue"]
    accent = COLORS["accent_violet"] if bonus else COLORS["accent_blue"]

    chunks = split_prompt_into_chunks(prompt)
    for idx, chunk in enumerate(chunks):
        story.append(
            GlassPromptCard(
                text=chunk,
                width=470,
                padding=20,
                bg_color=card_bg,
                glow_color=glow,
                accent_color=accent,
                bonus=bonus,
            )
        )
        if idx != len(chunks) - 1:
            spacer(story, 14)

    story.append(PageBreak())

def render_bonus_intro(story):
    spacer(story, 210)
    story.append(Paragraph("BONUS SYSTEMS", HERO_STYLE))
    spacer(story, 18)
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
    spacer(story, 180)
    story.append(
        Paragraph(
            """
            Creative momentum does not come from motivation.

            It comes from reduced friction.
            """,
            QUOTE_STYLE
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
            SUBTITLE_STYLE
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
            QUOTE_STYLE
        )
    )

# =========================================================
# PDF GENERATOR
# =========================================================

def generate_pdf(data, bundle_title, main_count, bonus_count, cover_path=None, logo_path=None):
    total = len(data)
    if main_count + bonus_count != total:
        raise ValueError(
            f"Main count + bonus count must equal total prompts. "
            f"Got main={main_count}, bonus={bonus_count}, total={total}."
        )

    main_prompts = data[:main_count]
    bonus_prompts = data[main_count:]

    safe_name = sanitize_filename(bundle_title)
    out_path = os.path.join(OUTPUTS_DIR, f"{safe_name}_nyxara_v11.pdf")

    doc = BaseDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=55,
        rightMargin=55,
        topMargin=65,
        bottomMargin=55,
        pageCompression=1,
    )

    full_frame = Frame(
        0, 0,
        PAGE_WIDTH, PAGE_HEIGHT,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
        showBoundary=0
    )

    content_frame = Frame(
        55, 55,
        PAGE_WIDTH - 110,
        PAGE_HEIGHT - 110,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
        showBoundary=0
    )

    cover_template = PageTemplate(id="Cover", frames=[full_frame], onPage=draw_cover_page)
    content_template = PageTemplate(id="Content", frames=[content_frame], onPage=draw_content_page)

    doc.addPageTemplates([cover_template, content_template])

    doc._has_cover_image = bool(cover_path and os.path.exists(cover_path))
    doc._logo_path = logo_path if logo_path and os.path.exists(logo_path) else None

    story = []

    # Cover page content
    if cover_path and os.path.exists(cover_path):
        story.append(Image(cover_path, width=PAGE_WIDTH, height=PAGE_HEIGHT))
    else:
        render_cover_story(
            story,
            bundle_title,
            f"{total} operational AI systems built for structured execution."
        )

    # Switch to content template
    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # Intro
    render_intro(story, bundle_title, main_count, bonus_count)

    # Contents
    render_contents(story, main_prompts, bonus_prompts)

    # Breathing page
    render_breathing(story, "Strong systems create calmer execution.")

    # Main systems
    for i, item in enumerate(main_prompts, start=1):
        render_system(story, item, i, bonus=False)
        if i % 4 == 0 and i != len(main_prompts):
            render_breathing(story, "Consistency compounds quietly over time.")

    # Bonus intro + bonus systems
    if bonus_prompts:
        render_bonus_intro(story)
        for i, item in enumerate(bonus_prompts, start=1):
            render_system(story, item, i, bonus=True)

    # CTA + end
    render_cta(story)
    render_end(story)

    doc.build(story)
    return out_path

# =========================================================
# INTERFACE
# =========================================================

st.markdown(
    """
    <div class="nyx-title">NYXARA OS V11</div>
    <div class="nyx-subtitle">Apple-inspired editorial publishing engine for premium AI prompt systems.</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="small-pill">Electric UI</div>
    <div class="small-pill">Main + Bonus Split</div>
    <div class="small-pill">Permanent Logo Lock</div>
    <div class="small-pill">Crash-Proof Prompt Cards</div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

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

META["bundle_title"] = bundle_title
META["main_prompt_count"] = int(main_prompt_count)
META["bonus_prompt_count"] = int(bonus_prompt_count)

st.markdown("---")

st.markdown(
    f"""
    <div class="soft-card">
        <div class="metric-label">Bundle</div>
        <div class="metric-value" style="font-size:22px;">{clean_text(bundle_title)}</div>
        <div class="metric-note">No niche input. Title carries the positioning.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="soft-card" style="border-left: 4px solid {COLORS["accent_blue"]};">
        <div class="metric-label">Module Split</div>
        <div class="metric-value" style="font-size:24px;">{main_prompt_count} Main + {bonus_prompt_count} Bonus</div>
        <div class="metric-note">Bonus prompts follow the main prompt sequence.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Permanent logo system
logo_locked = get_persistent_logo()
if logo_locked:
    st.success("Logo locked permanently. Future PDFs will use it automatically.")
    try:
        st.image(logo_locked, width=96)
    except:
        pass
else:
    logo_upload = st.file_uploader(
        "Upload Logo Once",
        type=["png", "jpg", "jpeg"],
        help="This logo will be saved permanently and reused in future PDFs."
    )
    if logo_upload is not None:
        save_logo_permanently(logo_upload)
        st.success("Logo saved permanently. It will auto-lock for future PDFs.")

raw_data = st.text_area(
    "Paste Prompt Data",
    height=440,
    help="Paste a Python list of dictionaries from the master prompt output."
)

generate = st.button("Generate Editorial PDF", use_container_width=True)

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

            logo_path = get_persistent_logo()

            try:
                pdf_file = generate_pdf(
                    data=parsed,
                    bundle_title=bundle_title,
                    main_count=int(main_prompt_count),
                    bonus_count=int(bonus_prompt_count),
                    cover_path=cover_path,
                    logo_path=logo_path,
                )

                st.success("Editorial PDF generated successfully.")

                with open(pdf_file, "rb") as f:
                    st.download_button(
                        "Download PDF",
                        f,
                        file_name=os.path.basename(pdf_file),
                        use_container_width=True,
                    )

            except Exception as e:
                st.error(f"System prevented crash: {e}")
