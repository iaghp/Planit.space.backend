"""PDF formatter for cover letters using ReportLab."""

from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas

from src.config_manager import ConfigManager


class PDFFormatter:
    """Formats and generates professional PDF documents."""
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """Initialize the PDF formatter.
        
        Args:
            config_manager: Config manager instance
        """
        self.config = config_manager or ConfigManager()
        self.style_config = self.config.load_style()
    
    def create_cover_letter_pdf(
        self,
        content: str,
        output_path: Path,
        company: str,
        profile: Optional[Dict[str, Any]] = None
    ) -> Path:
        """Create a cover letter PDF.
        
        Args:
            content: Complete cover letter text
            output_path: Where to save the PDF
            company: Company name (for filename)
            profile: User profile (optional, will load if not provided)
            
        Returns:
            Path to the created PDF
        """
        if profile is None:
            profile = self.config.load_profile()
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get page size
        page_config = self.style_config.get("page", {})
        page_size = letter if page_config.get("size") == "letter" else A4
        
        # Get margins
        margins = self.style_config.get("margins", {})
        margin_top = margins.get("top", 72)
        margin_bottom = margins.get("bottom", 72)
        margin_left = margins.get("left", 72)
        margin_right = margins.get("right", 72)
        
        # Create document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=page_size,
            topMargin=margin_top,
            bottomMargin=margin_bottom,
            leftMargin=margin_left,
            rightMargin=margin_right
        )
        
        # Build story (content elements)
        story = []
        styles = self._create_styles()
        
        # Parse and add content
        paragraphs = content.split('\n\n')
        
        for i, para in enumerate(paragraphs):
            if para.strip():
                # Determine style based on position
                if i == 0:
                    # First paragraph might be header
                    style = styles['Header'] if self._looks_like_header(para) else styles['Body']
                else:
                    style = styles['Body']
                
                p = Paragraph(para.replace('\n', '<br/>'), style)
                story.append(p)
                story.append(Spacer(1, self.style_config["spacing"]["paragraph_spacing"]))
        
        # Add signature if configured
        sig_config = self.style_config.get("signature", {})
        if sig_config.get("use_image", False):
            sig_path = Path(sig_config.get("image_path", "templates/signature.png"))
            if sig_path.exists():
                story.append(Spacer(1, sig_config.get("spacing_above", 24)))
                img = Image(str(sig_path), height=sig_config.get("image_height", 30))
                story.append(img)
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    def _create_styles(self) -> Dict[str, ParagraphStyle]:
        """Create paragraph styles from configuration."""
        base_styles = getSampleStyleSheet()
        fonts = self.style_config.get("fonts", {})
        spacing = self.style_config.get("spacing", {})
        
        # Header style
        header_font = fonts.get("header", {})
        header_style = ParagraphStyle(
            'Header',
            parent=base_styles['Normal'],
            fontName=header_font.get("family", "Helvetica-Bold"),
            fontSize=header_font.get("size", 12),
            leading=header_font.get("size", 12) * spacing.get("line_height", 1.2),
            spaceBefore=0,
            spaceAfter=spacing.get("section_spacing", 18)
        )
        
        # Body style
        body_font = fonts.get("body", {})
        body_style = ParagraphStyle(
            'Body',
            parent=base_styles['Normal'],
            fontName=body_font.get("family", "Helvetica"),
            fontSize=body_font.get("size", 11),
            leading=body_font.get("size", 11) * spacing.get("line_height", 1.2),
            alignment=TA_LEFT
        )
        
        # Contact style
        contact_font = fonts.get("contact", {})
        contact_style = ParagraphStyle(
            'Contact',
            parent=base_styles['Normal'],
            fontName=contact_font.get("family", "Helvetica"),
            fontSize=contact_font.get("size", 10),
            leading=contact_font.get("size", 10) * 1.2
        )
        
        # Signature style
        sig_font = fonts.get("signature", {})
        signature_style = ParagraphStyle(
            'Signature',
            parent=base_styles['Normal'],
            fontName=sig_font.get("family", "Helvetica-Oblique"),
            fontSize=sig_font.get("size", 12)
        )
        
        return {
            'Header': header_style,
            'Body': body_style,
            'Contact': contact_style,
            'Signature': signature_style
        }
    
    def _looks_like_header(self, text: str) -> bool:
        """Check if text looks like a header line."""
        # Simple heuristic: headers are usually short and might contain name/address
        return len(text) < 100 and any(
            keyword in text.lower() 
            for keyword in ['street', 'avenue', 'road', '@']
        )


def generate_filename(company: str, doc_type: str = "CoverLetter") -> str:
    """Generate a standardized filename.
    
    Args:
        company: Company name
        doc_type: Type of document (CoverLetter, Resume, etc.)
        
    Returns:
        Formatted filename
    """
    # Clean company name
    clean_company = "".join(c for c in company if c.isalnum() or c in (' ', '-'))
    clean_company = clean_company.replace(' ', '_')
    
    # Add date
    date_str = datetime.now().strftime("%Y%m%d")
    
    return f"{doc_type}_{clean_company}_{date_str}.pdf"
