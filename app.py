import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class ElectricStudioCanvas(canvas.Canvas):
    """
    A traditional two-pass canvas to handle dynamic headers, footers, 
    and total page counts flawlessly without messing up layout flows.
    """
    def __init__(self, *args, logo_path=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.logo_path = logo_path
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, num_pages):
        self.saveState()
        
        # Traditional neat footer
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#7F8C8D"))
        self.drawString(54, 36, f"Retro Packaging Design Operations System — Page {self._pageNumber} of {num_pages}")
        
        # Optional Logo Placement
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                self.drawImage(self.logo_path, 500, 740, width=50, height=50, mask='auto')
            except Exception:
                pass # Gracefully skip if image format is acting up
                
        self.restoreState()


def execute_pdf_compilation(sanitized_array, asset_title, asset_niche, ui_main_count, ui_bonus_count, final_active_cover, final_active_logo):
    """
    Compiles the data payload safely into a beautiful PDF. 
    Uses Paragraph text wrapping to prevent any multi-page LayoutErrors.
    """
    output_pdf_filepath = "nyxara_refresh_blueprint.pdf"
    
    # Initialize document template with standard 0.75 in (54 points) margins
    doc = SimpleDocTemplate(
        output_pdf_filepath,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Define robust typography choices (Always set leading proportional to font size!)
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        spaceAfter=6,
        textColor=colors.HexColor('#2C3E50')
    )

    niche_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        leading=16,
        spaceAfter=24,
        textColor=colors.HexColor('#7F8C8D')
    )

    h2_style = ParagraphStyle(
        'ItemTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.HexColor('#16A085'),
        keepWithNext=True # Keeps title structurally locked to its metadata
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        spaceAfter=6,
        textColor=colors.HexColor('#34495E')
    )

    # Monospaced prompt style with explicit line-wrapping rules
    code_style = ParagraphStyle(
        'PromptCodeText',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=9,
        leading=13,
        spaceBefore=4,
        spaceAfter=10,
        textColor=colors.HexColor('#2980B9')
    )

    storyboard = []

    # Blueprint Cover Meta Block
    storyboard.append(Paragraph(str(asset_title), title_style))
    storyboard.append(Paragraph(f"Target Asset Micro-Niche: {asset_niche}", niche_style))
    storyboard.append(Spacer(1, 15))

    total_prompts_to_render = int(ui_main_count) + int(ui_bonus_count)
    
    for idx, item in enumerate(sanitized_array[:total_prompts_to_render]):
        # Keep title and immediate description bound tightly together
        header_group = []
        header_group.append(Paragraph(f"{item.get('title', 'Untitled Direction')}", h2_style))
        header_group.append(Paragraph(f"<b>Category:</b> {item.get('category', 'N/A')}", body_style))
        header_group.append(Paragraph(f"<b>Description:</b> {item.get('description', 'N/A')}", body_style))
        storyboard.append(KeepTogether(header_group))
        
        # Format the core AI prompt payload safely
        # Transforming raw newlines into HTML breaks prevents ReportLab from breaking layout bounds
        raw_prompt = item.get('prompt', '')
        formatted_prompt = raw_prompt.replace('\n', '<br/>').replace('    ', '&nbsp;&nbsp;&nbsp;&nbsp;')
        storyboard.append(Paragraph(f"<b>System Prompt Blueprint:</b><br/>{formatted_prompt}", code_style))

        # Core operational metadata rendering
        meta_keys = [
            ('why_this_works', 'Why This Works'),
            ('micro_example', 'Micro-Example'),
            ('how_to_use', 'How to Use'),
            ('business_application', 'Business Application'),
            ('validation_case_study', 'Validation Case Study')
        ]
        
        for field_key, display_name in meta_keys:
            if field_key in item:
                storyboard.append(Paragraph(f"<b>{display_name}:</b> {item[field_key]}", body_style))

        # Ecosystem checklist mapping layout
        if 'ecosystem_assets' in item:
            storyboard.append(Spacer(1, 4))
            storyboard.append(Paragraph("<b>Ecosystem Assets & Tooling:</b>", body_style))
            assets = item['ecosystem_assets']
            for asset_key, asset_val in assets.items():
                clean_asset_name = asset_key.replace('_', ' ').title()
                formatted_asset_val = str(asset_val).replace('\n', '<br/>')
                storyboard.append(Paragraph(f"• <u>{clean_asset_name}</u>: {formatted_asset_val}", body_style))

        # Separate distinct prompts on clean pages like an authentic production blueprint
        if idx < total_prompts_to_render - 1:
            storyboard.append(PageBreak())

    # Compile everything into standard storage
    logo_path = final_active_logo if final_active_logo else None
    doc.build(
        storyboard, 
        canvasmaker=lambda *args, **kwargs: ElectricStudioCanvas(*args, logo_path=logo_path, **kwargs)
    )

    return output_pdf_filepath
