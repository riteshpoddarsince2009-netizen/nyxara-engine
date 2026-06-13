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

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# =========================================================
# NYXARA SUPREME VISUAL ENGINE V4
# =========================================================

PAGE_WIDTH = 612
PAGE_HEIGHT = 792

PRIMARY_BLACK = "#0B0B0C"
SOFT_BLACK = "#1F2937"
GOLD = "#C8A44D"
LIGHT_BG = "#F7F7F5"
MID_GREY = "#6B7280"
BORDER = "#E5E7EB"

# =========================================================
# SUPREME CANVAS SYSTEM
# =========================================================

class NyxaraSupremeCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self._saved_page_states)

        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_ui(page_count)
            super().showPage()

        super().save()

    def draw_ui(self, total_pages):
        self.saveState()

        # =========================================
        # HEADER
        # =========================================

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

        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#D1D5DB"))
        self.drawRightString(
            PAGE_WIDTH - 48,
            767,
            "PRIVATE CREATIVE SYSTEM"
        )

        # =========================================
        # FOOTER
        # =========================================

        self.setStrokeColor(colors.HexColor(BORDER))
        self.setLineWidth(0.7)
        self.line(48, 52, PAGE_WIDTH - 48, 52)

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
# BULLETPROOF DATA PARSER
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

                except:
                    pass

                start = -1

    return items

# =========================================================
# PDF ENGINE
# =========================================================

def generate_supreme_pdf(bundle_data, pdf_name="NYXARA_SUPREME_FINAL.pdf"):

    doc = SimpleDocTemplate(
        pdf_name,
        pagesize=letter,
        leftMargin=48,
        rightMargin=48,
        topMargin=92,
        bottomMargin=72
    )

    story = []
    styles = getSampleStyleSheet()

    # =====================================================
    # TYPOGRAPHY SYSTEM
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
        leading=14,
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
        fontSize=9.6,
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

    framework_style = ParagraphStyle(
        'FrameworkStyle',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=16,
        textColor=colors.HexColor(PRIMARY_BLACK)
    )

    # =====================================================
    # PAGE LOOP
    # =====================================================

    for index, item in enumerate(bundle_data):

        # =================================================
        # CATEGORY LABEL
        # =================================================

        category = item.get(
            "category",
            "RETRO CREATIVE SYSTEM"
        )

        story.append(
            Paragraph(category.upper(), category_style)
        )

        # =================================================
        # TITLE
        # =================================================

        title = item.get(
            "title",
            "SYSTEM OVERRIDE"
        )

        story.append(
            Paragraph(title.upper(), title_style)
        )

        # =================================================
        # DESCRIPTION
        # =================================================

        desc = item.get("description", "")

        desc = re.sub(
            r'\[(.*?)\]',
            r'<font color="#C8A44D"><b>\1</b></font>',
            desc
        )

        story.append(
            Paragraph(desc, desc_style)
        )

        # =================================================
        # DIVIDER
        # =================================================

        story.append(
            HRFlowable(
                width="100%",
                thickness=0.6,
                color=colors.HexColor(BORDER)
            )
        )

        story.append(Spacer(1, 18))

        # =================================================
        # FRAMEWORK SECTION
        # =================================================

        framework = item.get(
            "framework",
            "THE SHELF METHOD — Visibility, Emotion, Recognition"
        )

        story.append(
            Paragraph(
                "PROPRIETARY CREATIVE FRAMEWORK",
                section_style
            )
        )

        fw_box = Table(
            [[Paragraph(framework, framework_style)]],
            colWidths=[510]
        )

        fw_box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(LIGHT_BG)),
            ('LEFTPADDING', (0,0), (-1,-1), 16),
            ('RIGHTPADDING', (0,0), (-1,-1), 16),
            ('TOPPADDING', (0,0), (-1,-1), 14),
            ('BOTTOMPADDING', (0,0), (-1,-1), 14),
            ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(GOLD)),
        ]))

        story.append(fw_box)
        story.append(Spacer(1, 22))

        # =================================================
        # WHY THIS WORKS
        # =================================================

        why_this_works = item.get(
            "why_this_works",
            "Retro visual systems increase emotional familiarity and shelf memorability."
        )

        story.append(
            Paragraph("WHY THIS WORKS", section_style)
        )

        callout_box = Table(
            [[Paragraph(why_this_works, callout_style)]],
            colWidths=[510]
        )

        callout_box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FAFAF9")),
            ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor(BORDER)),
            ('LEFTPADDING', (0,0), (-1,-1), 14),
            ('RIGHTPADDING', (0,0), (-1,-1), 14),
            ('TOPPADDING', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ]))

        story.append(callout_box)
        story.append(Spacer(1, 22))

        # =================================================
        # PROMPT SECTION
        # =================================================

        story.append(
            Paragraph(
                "CORE PROMPT SYSTEM",
                section_style
            )
        )

        prompt_content = item.get(
            "prompt",
            ""
        ).replace('\n', '<br/>')

        prompt_para = Paragraph(
            prompt_content,
            prompt_style
        )

        prompt_table = Table(
            [['', prompt_para]],
            colWidths=[5, 505]
        )

        prompt_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor(GOLD)),
            ('BACKGROUND', (1,0), (1,-1), colors.HexColor("#F3F4F6")),
            ('LEFTPADDING', (1,0), (1,-1), 16),
            ('RIGHTPADDING', (1,0), (1,-1), 16),
            ('TOPPADDING', (1,0), (1,-1), 16),
            ('BOTTOMPADDING', (1,0), (1,-1), 16),
        ]))

        story.append(prompt_table)
        story.append(Spacer(1, 22))

        # =================================================
        # MICRO EXAMPLE
        # =================================================

        micro_example = item.get(
            "micro_example",
            "Burnt orange cereal packaging with oversized cream typography and grain textures."
        )

        story.append(
            Paragraph(
                "MICRO OUTPUT SAMPLE",
                section_style
            )
        )

        example_box = Table(
            [[Paragraph(micro_example, body_style)]],
            colWidths=[510]
        )

        example_box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor(BORDER)),
            ('LEFTPADDING', (0,0), (-1,-1), 14),
            ('RIGHTPADDING', (0,0), (-1,-1), 14),
            ('TOPPADDING', (0,0), (-1,-1), 14),
            ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ]))

        story.append(example_box)
        story.append(Spacer(1, 22))

        # =================================================
        # DEPLOYMENT
        # =================================================

        deploy_elements = []

        deploy_elements.append(
            Paragraph(
                "DEPLOYMENT WORKFLOW",
                section_style
            )
        )

        how_to = item.get(
            "how_to_use",
            ""
        ).replace('\n', '<br/>')

        deploy_elements.append(
            Paragraph(how_to, body_style)
        )

        story.append(
            KeepTogether(deploy_elements)
        )

        story.append(Spacer(1, 24))

        # =================================================
        # OPTIONAL IMAGE SUPPORT
        # =================================================

        image_path = item.get("image_path", "")

        if image_path and os.path.exists(image_path):

            try:
                img = Image(
                    image_path,
                    width=420,
                    height=240
                )

                story.append(
                    Paragraph(
                        "VISUAL REFERENCE OUTPUT",
                        section_style
                    )
                )

                story.append(img)
                story.append(Spacer(1, 20))

            except:
                pass

        # =================================================
        # PAGE BREAK
        # =================================================

        if index < len(bundle_data) - 1:
            story.append(PageBreak())

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(
        story,
        canvasmaker=NyxaraSupremeCanvas
    )

    return pdf_name

# =========================================================
# STREAMLIT FRONTEND
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

        with open("nyxara_logo.png", "wb") as f:
            f.write(uploaded_logo.getbuffer())

        st.success("Logo uploaded successfully.")

    if os.path.exists("nyxara_logo.png"):
        st.image("nyxara_logo.png", width=90)

    st.markdown("---")

    st.markdown("""
### SYSTEM NOTES

- Dynamic page rendering
- Anti-cutoff architecture
- Intelligent spacing engine
- Premium layout hierarchy
- Conditional ecosystem blocks
- Optional visual references
""")

# =========================================================
# MAIN INTERFACE
# =========================================================

st.markdown("# NYXARA SUPREME PDF ENGINE")
st.write("Premium creative intelligence asset generation system.")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:

    input_data = st.text_area(
        "Paste Bundle Data",
        height=500
    )

    generate_btn = st.button(
        "GENERATE SUPREME PDF",
        use_container_width=True
    )

with col2:

    st.markdown("### SYSTEM STATUS")

    status = st.empty()

    status.info(
        "Awaiting creative payload..."
    )

# =========================================================
# GENERATION LOGIC
# =========================================================

if generate_btn and input_data:

    try:

        status.warning(
            "Initializing rendering engine..."
        )

        cleaned_data = parse_bulletproof_data(
            input_data
        )

        if not cleaned_data:

            st.error(
                "Data parsing failed."
            )

        else:

            pdf_file = generate_supreme_pdf(
                cleaned_data
            )

            status.success(
                "PDF compilation complete."
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
            f"SYSTEM ERROR: {str(e)}"
      )
