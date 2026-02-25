"""Export utilities for converting and saving ProjectForge outputs."""

from datetime import datetime
from io import BytesIO
import markdown


def convert_markdown_to_html(text):
    """Convert markdown to HTML using the markdown library with extensions.
    
    Args:
        text: Markdown-formatted text string
        
    Returns:
        str: HTML-formatted string
    """
    return markdown.markdown(text, extensions=['tables', 'fenced_code'])


def generate_text_content(timestamp, user_input, ba_output, architect_output, 
                          qa_output, synthesis_output, pm_output):
    """Generate text content in memory (returns string instead of writing file).
    
    Args:
        timestamp: Timestamp string for the report
        user_input: Original project description
        ba_output: Business Analyst output
        architect_output: Technical Architect output
        qa_output: Quality Auditor output
        synthesis_output: Technical Synthesizer output
        pm_output: Project Manager output
        
    Returns:
        str: Complete text content
    """
    content = f"ProjectForge Analysis\n"
    content += f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n"
    content += f"Project: {user_input}\n"
    content += "=" * 80 + "\n\n"
    
    content += "## Business Requirements\n\n"
    content += ba_output + "\n\n"
    
    content += "## Technical Design\n\n"
    content += architect_output + "\n\n"
    
    content += "## Risk Assessment\n\n"
    content += qa_output + "\n\n"
    
    content += "## Technical Synthesis\n\n"
    content += synthesis_output + "\n\n"
    
    content += "## Executive Summary & Roadmap\n\n"
    content += pm_output + "\n"
    
    return content


def generate_pdf_bytes(html_content):
    """Generate PDF in memory (returns bytes for download).
    
    Args:
        html_content: HTML content string to convert
        
    Returns:
        bytes: PDF file content as bytes, or None if generation failed
    """
    try:
        from weasyprint import HTML
        pdf_buffer = BytesIO()
        HTML(string=html_content).write_pdf(pdf_buffer)
        return pdf_buffer.getvalue()
    except ImportError:
        return None
    except Exception:
        return None


def save_text_output(output_file, user_input, ba_output, architect_output, qa_output, synthesis_output, pm_output):
    """Save the analysis outputs to a text file.
    
    Args:
        output_file: Path to the output text file
        user_input: Original project description
        ba_output: Business Analyst output
        architect_output: Technical Architect output
        qa_output: Quality Auditor output
        synthesis_output: Technical Synthesizer output
        pm_output: Project Manager output
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"ProjectForge Analysis\n")
        f.write(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
        f.write(f"Project: {user_input}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("## Business Requirements\n\n")
        f.write(ba_output + "\n\n")
        
        f.write("## Technical Design\n\n")
        f.write(architect_output + "\n\n")
        
        f.write("## Risk Assessment\n\n")
        f.write(qa_output + "\n\n")
        
        f.write("## Technical Synthesis\n\n")
        f.write(synthesis_output + "\n\n")
        
        f.write("## Executive Summary & Roadmap\n\n")
        f.write(pm_output + "\n")


def save_html_output(html_output_file, html_content):
    """Save HTML content to a file.
    
    Args:
        html_output_file: Path to the output HTML file
        html_content: HTML content string
    """
    with open(html_output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)


def save_pdf_output(pdf_output_file, html_content):
    """Generate and save PDF from HTML content.
    
    Args:
        pdf_output_file: Path to the output PDF file
        html_content: HTML content string to convert
        
    Returns:
        bool: True if PDF was generated successfully, False otherwise
    """
    try:
        from weasyprint import HTML
        HTML(string=html_content).write_pdf(pdf_output_file)
        return True
    except ImportError:
        print("\nWARNING: PDF export not available. Install with:")
        print("   pip install weasyprint")
        return False
    except Exception as e:
        print(f"\nWARNING: PDF generation failed: {e}")
        return False
