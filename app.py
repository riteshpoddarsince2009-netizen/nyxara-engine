import streamlit as st
import re
import ast
import os

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable,
    Image
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.pdfgen import canvas
from reportlab.platypus.doctemplate import LayoutError

# =========================================================
# NYXARA SUPREME PDF ENGINE V5
# CRASH-PROOF EDITION
# =========================================================

PAGE_WIDTH = 612
PAGE_HEIGHT = 792

PRIMARY_BLACK = "#0B0B0C"
SOFT_BLACK = "#1F2937"
GOLD = "#C8A44D"
LIGHT_BG = "#F8F8F7"
MID_GREY = "#6B7280"
BORDER = "#E5E7EB"

# =========================================================
# SAFE TEXT CLEANER
# =========================================================

def safe_text(value):

    if value is None:
        return ""

    value = str(value)

    value = value.replace("&", "&amp;")
    value = value.replace("<", "&lt;")
    value = value.replace(">", "&gt;")

    return value.strip()

# =========================================================
# SAFE PARAGRAPH BUILDER
# =========================================================

def safe_paragraph(text, style):

    try:
        return Paragraph(text, style)

    except:

        cleaned = safe_text(text)
        return Paragraph(cleaned, style)

# =========================================================
# SUPREME CANVAS
# =========================================================

class NyxaraSupremeCanvas(canvas.Canvas):

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
            self.draw_ui(total_pages)

            super().showPage()

        super().save()

    def draw_ui(self, total_pages):

        self.saveState()

        # =================================================
        # HEADER
        # =================================================

        self.setFillColor(colors.HexColor(PRIMARY_BLACK))
        self.rect(0, 752, PAGE_WIDTH, 40, fill=1, stroke=0)

        logo_path = "nyxara_logo.png"

        if os.path.exists(logo_path):

            try:
                self.drawImage(
                    logo_path,
                    48,
                    760,
                    width=18,
                    height=18,
                    mask='auto'
                )
            except:
                pass

        self.setFillColor(colors.white)

        self.setFont("Helvetica-Bold", 10)
        self.drawString(78, 767, "NYXARA LABS")

        self.setFont("Helvetica", 8)

        self.setFillColor(colors.HexColor("#D1D5DB"))

        self.drawRightString(
            PAGE_WIDTH - 48,
            767,
            "PRIVATE CREATIVE SYSTEM"
        )

        # =================================================
        # FOOTER
        # =================================================

        self.setStrokeColor(colors.HexColor(BORDER))
        self.setLineWidth(0.7)

        self.line(
            48,
            52,
            PAGE_WIDTH - 48,
            52
        )

        self.setFont("Helvetica", 7.5)

        self.setFillColor(colors.HexColor(MID_GREY))

        self.drawString(
            48,
            38,
            "NYXARA LABS — INTERNAL CREATIVE ASSET"
        )

        self.drawRightString(
            PAGE_WIDTH - 48,
            38,
            f"PAGE {self._pageNumber:02d}"
        )

        self.restoreState()

# =========================================================
# BULLETPROOF PARSER
# =========================================================

def parse_bulletproof_data(raw_str):

    raw_str = raw_str.strip()

    if raw_str.startswith("data ="):
        raw_str = raw_str.replace("data =", "", 1).strip()

    items = []

    start = -1
    brace_count = 0

    for i, char in enumerate(raw_str):

        if char == "{":

            if brace_count == 0:
                start = i

            brace_count += 1

        elif char == "}":

            brace_count -= 1

            if brace_count == 0 and start != -1:

                dict_str = raw_str[start:i+1]

                try:

                    obj = ast.literal_eval(dict_str)

                    if isinstance(obj, dict):
                        items.append(obj)

                except Exception:
                    pass

                start = -1

    return items

# =========================================================
# SAFE IMAGE LOADER
# =========================================================

def safe_image(image_path, width=420, height=240):

    try:

        if image_path and os.path.exists(image_path):

            return Image(
                image_path,
                width=width,
                height=height
            )

    except:
        return None

    return None

# =========================================================
# MAIN PDF ENGINE
# =========================================================

def generate_supreme_pdf(
    bundle_data,
    pdf_name="NYXARA_SUPREME_SYSTEM.pdf"
):

    doc = SimpleDocTemplate(
        pdf_name,
        pagesize=letter,
        leftMargin=48,
        rightMargin=48,
        topMargin=92,
        bottomMargin=72
    )

    story = []

    # =====================================================
    # STYLES
    # =====================================================

    category_style = ParagraphStyle(
        'CategoryStyle',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=12,
        textColor=colors.HexColor(GOLD),
        spaceAfter=8
    )

    title_style = ParagraphStyle(
        'TitleStyle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.HexColor(PRIMARY_BLACK),
        spaceAfter=10
    )

    desc_style = ParagraphStyle(
        'DescStyle',
        fontName='Helvetica',
        fontSize=10.5,
        leading=18,
        textColor=colors.HexColor(SOFT_BLACK),
        spaceAfter=18
    )

    section_style = ParagraphStyle(
        'SectionStyle',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor(GOLD),
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        fontName='Helvetica',
        fontSize=10,
        leading=17,
        textColor=colors.HexColor(SOFT_BLACK)
    )

    prompt_style = ParagraphStyle(
        'PromptStyle',
        fontName='Helvetica',
        fontSize=9.5,
        leading=16,
        textColor=colors.HexColor("#111827")
    )

    callout_style = ParagraphStyle(
        'CalloutStyle',
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=15,
        textColor=colors.HexColor("#374151")
    )

    # =====================================================
    # DOCUMENT LOOP
    # =====================================================

    for index, item in enumerate(bundle_data):

        try:

            # =============================================
            # CATEGORY
            # =============================================

            category = safe_text(
                item.get(
                    "category",
                    "CREATIVE OPERATIONS"
                )
            )

            story.append(
                safe_paragraph(
                    category.upper(),
                    category_style
                )
            )

            # =============================================
            # TITLE
            # =============================================

            title = safe_text(
                item.get(
                    "title",
                    "SYSTEM MODULE"
                )
            )

            story.append(
                safe_paragraph(
                    title.upper(),
                    title_style
                )
            )

            # =============================================
            # DESCRIPTION
            # =============================================

            desc = safe_text(
                item.get(
                    "description",
                    ""
                )
            )

            story.append(
                safe_paragraph(
                    desc,
                    desc_style
                )
            )

            story.append(
                HRFlowable(
                    width="100%",
                    thickness=0.7,
                    color=colors.HexColor(BORDER)
                )
            )

            story.append(Spacer(1, 18))

            # =============================================
            # WHY THIS WORKS
            # =============================================

            story.append(
                safe_paragraph(
                    "WHY THIS WORKS",
                    section_style
                )
            )

            why_this_works = safe_text(
                item.get(
                    "why_this_works",
                    "This framework improves operational consistency and reduces decision fatigue."
                )
            )

            why_box = Table(
                [[
                    safe_paragraph(
                        why_this_works,
                        callout_style
                    )
                ]],
                colWidths=[510]
            )

            why_box.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(LIGHT_BG)),
                ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor(BORDER)),
                ('LEFTPADDING', (0,0), (-1,-1), 14),
                ('RIGHTPADDING', (0,0), (-1,-1), 14),
                ('TOPPADDING', (0,0), (-1,-1), 12),
                ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ]))

            story.append(why_box)
            story.append(Spacer(1, 22))

            # =============================================
            # PROMPT SECTION
            # =============================================

            story.append(
                safe_paragraph(
                    "CORE PROMPT SYSTEM",
                    section_style
                )
            )

            # GOLD LINE
            story.append(
                HRFlowable(
                    width="100%",
                    thickness=2.5,
                    color=colors.HexColor(GOLD),
                    spaceAfter=14
                )
            )

            prompt_content = safe_text(
                item.get(
                    "prompt",
                    ""
                )
            )

            prompt_content = prompt_content.replace(
                "\n",
                "<br/>"
            )

            prompt_para = safe_paragraph(
                prompt_content,
                prompt_style
            )

            # IMPORTANT:
            # NO TABLES HERE
            # FULLY PAGE-SPLIT SAFE

            story.append(prompt_para)
            story.append(Spacer(1, 24))

            # =============================================
            # MICRO EXAMPLE
            # =============================================

            story.append(
                safe_paragraph(
                    "MICRO OUTPUT SAMPLE",
                    section_style
                )
            )

            micro_example = safe_text(
                item.get(
                    "micro_example",
                    "Example output preview."
                )
            )

            example_box = Table(
                [[
                    safe_paragraph(
                        micro_example,
                        body_style
                    )
                ]],
                colWidths=[510]
            )

            example_box.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor(BORDER)),
                ('LEFTPADDING', (0,0), (-1,-1), 14),
                ('RIGHTPADDING', (0,0), (-1,-1), 14),
                ('TOPPADDING', (0,0), (-1,-1), 12),
                ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ]))

            story.append(example_box)
            story.append(Spacer(1, 22))

            # =============================================
            # HOW TO USE
            # =============================================

            story.append(
                safe_paragraph(
                    "DEPLOYMENT WORKFLOW",
                    section_style
                )
            )

            how_to = safe_text(
                item.get(
                    "how_to_use",
                    ""
                )
            )

            how_to = how_to.replace(
                "\n",
                "<br/>"
            )

            story.append(
                safe_paragraph(
                    how_to,
                    body_style
                )
            )

            story.append(Spacer(1, 22))

            # =============================================
            # BUSINESS APPLICATION
            # =============================================

            business_application = safe_text(
                item.get(
                    "business_application",
                    ""
                )
            )

            if business_application:

                story.append(
                    safe_paragraph(
                        "BUSINESS APPLICATION",
                        section_style
                    )
                )

                story.append(
                    safe_paragraph(
                        business_application,
                        body_style
                    )
                )

                story.append(Spacer(1, 22))

            # =============================================
            # VALIDATION CASE STUDY
            # =============================================

            validation = safe_text(
                item.get(
                    "validation_case_study",
                    ""
                )
            )

            if validation:

                story.append(
                    safe_paragraph(
                        "VALIDATION CASE STUDY",
                        section_style
                    )
                )

                validation_box = Table(
                    [[
                        safe_paragraph(
                            validation,
                            body_style
                        )
                    ]],
                    colWidths=[510]
                )

                validation_box.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FAFAF9")),
                    ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor(BORDER)),
                    ('LEFTPADDING', (0,0), (-1,-1), 14),
                    ('RIGHTPADDING', (0,0), (-1,-1), 14),
                    ('TOPPADDING', (0,0), (-1,-1), 12),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                ]))

                story.append(validation_box)
                story.append(Spacer(1, 22))

            # =============================================
            # ECOSYSTEM ASSETS
            # =============================================

            assets = item.get(
                "ecosystem_assets",
                {}
            )

            if isinstance(assets, dict) and assets:

                story.append(
                    safe_paragraph(
                        "ECOSYSTEM ASSETS",
                        section_style
                    )
                )

                for asset_key, asset_value in assets.items():

                    if not asset_value:
                        continue

                    asset_title = asset_key.replace(
                        "_",
                        " "
                    ).title()

                    asset_value = safe_text(asset_value)

                    asset_table = Table(
                        [[
                            safe_paragraph(
                                f"<b>{asset_title}</b><br/><br/>{asset_value}",
                                body_style
                            )
                        ]],
                        colWidths=[510]
                    )

                    asset_table.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,-1), colors.white),
                        ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor(BORDER)),
                        ('LEFTPADDING', (0,0), (-1,-1), 14),
                        ('RIGHTPADDING', (0,0), (-1,-1), 14),
                        ('TOPPADDING', (0,0), (-1,-1), 12),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                    ]))

                    story.append(asset_table)
                    story.append(Spacer(1, 14))

            # =============================================
            # OPTIONAL IMAGE
            # =============================================

            image_path = item.get(
                "image_path",
                ""
            )

            img = safe_image(image_path)

            if img:

                story.append(
                    safe_paragraph(
                        "VISUAL REFERENCE",
                        section_style
                    )
                )

                story.append(img)
                story.append(Spacer(1, 22))

            # =============================================
            # PAGE BREAK
            # =============================================

            if index < len(bundle_data) - 1:
                story.append(PageBreak())

        except Exception as e:

            error_text = f"SECTION FAILED TO RENDER: {str(e)}"

            story.append(
                safe_paragraph(
                    error_text,
                    body_style
                )
            )

            story.append(PageBreak())

    # =====================================================
    # BUILD PDF
    # =====================================================

    try:

        doc.build(
            story,
            canvasmaker=NyxaraSupremeCanvas
        )

    except LayoutError:

        fallback_name = "NYXARA_FALLBACK_RENDER.pdf"

        fallback_doc = SimpleDocTemplate(
            fallback_name,
            pagesize=letter
        )

        fallback_story = []

        for item in bundle_data:

            fallback_story.append(
                safe_paragraph(
                    safe_text(item),
                    body_style
                )
            )

            fallback_story.append(Spacer(1, 20))

        fallback_doc.build(fallback_story)

        return fallback_name

    return pdf_name

# =========================================================
# STREAMLIT UI
# =========================================================

st.set_page_config(
    page_title="NYXARA SUPREME ENGINE",
    layout="wide"
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## NYXARA LABS")

    uploaded_logo = st.file_uploader(
        "Upload Brand Logo",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_logo is not None:

        with open(
            "nyxara_logo.png",
            "wb"
        ) as f:

            f.write(uploaded_logo.getbuffer())

        st.success("Logo uploaded.")

    if os.path.exists("nyxara_logo.png"):

        st.image(
            "nyxara_logo.png",
            width=90
        )

    st.markdown("---")

    st.markdown("""
### SYSTEM STATUS

- Crash-Proof Rendering
- Dynamic Page Splitting
- Safe Paragraph Engine
- Fallback PDF Recovery
- Long Prompt Support
- Layout Protection
""")

# =========================================================
# MAIN UI
# =========================================================

st.markdown("# NYXARA SUPREME PDF ENGINE")
st.write(
    "Operational-grade AI asset rendering system."
)

st.markdown("---")

col1, col2 = st.columns([2,1])

with col1:

    input_data = st.text_area(
        "Paste Bundle Data",
        height=520
    )

    generate_btn = st.button(
        "GENERATE PDF",
        use_container_width=True
    )

with col2:

    st.markdown("### RENDER STATUS")

    status = st.empty()

    status.info(
        "Awaiting payload..."
    )

# =========================================================
# PDF GENERATION
# =========================================================

if generate_btn and input_data:

    try:

        status.warning(
            "Initializing render engine..."
        )

        cleaned_data = parse_bulletproof_data(
            input_data
        )

        if not cleaned_data:

            status.error(
                "Parsing failed."
            )

        else:

            pdf_file = generate_supreme_pdf(
                cleaned_data
            )

            status.success(
                "PDF generated successfully."
            )

            with open(pdf_file, "rb") as f:

                st.download_button(
                    "DOWNLOAD PDF",
                    f,
                    file_name=pdf_file,
                    use_container_width=True
                )

    except Exception as e:

        status.error(
            f"SYSTEM FAILURE: {str(e)}"
  )
