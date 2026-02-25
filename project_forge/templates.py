"""HTML/CSS templates for ProjectForge output generation."""

from datetime import datetime


def generate_html_template(timestamp, ba_html, architect_html, qa_html, synthesis_html, pm_html):
    """Generate the complete HTML document with embedded CSS and content.
    
    Args:
        timestamp: Timestamp string for the report
        ba_html: Business Analyst section HTML
        architect_html: Technical Architect section HTML
        qa_html: Quality Auditor section HTML
        synthesis_html: Technical Synthesizer section HTML
        pm_html: Project Manager section HTML
        
    Returns:
        str: Complete HTML document as string
    """
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ProjectForge Analysis - {timestamp}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #1a73e8;
            border-bottom: 3px solid #1a73e8;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        
        .timestamp {{
            color: #666;
            font-size: 14px;
            margin-bottom: 30px;
        }}
        
        .section {{
            margin-bottom: 30px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .section-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
        }}
        
        .section-header:hover {{
            background: linear-gradient(135deg, #5568d3 0%, #65408b 100%);
        }}
        
        .section-header h2 {{
            margin: 0;
            font-size: 20px;
        }}
        
        .toggle-icon {{
            font-size: 24px;
            transition: transform 0.3s;
        }}
        
        .section-header.collapsed .toggle-icon {{
            transform: rotate(-90deg);
        }}
        
        .section-content {{
            padding: 20px;
            background: #fafafa;
            max-height: 5000px;
            overflow: hidden;
            transition: max-height 0.3s ease-out, padding 0.3s;
        }}
        
        .section-content.collapsed {{
            max-height: 0;
            padding: 0 20px;
        }}
        
        .section-content h3 {{
            color: #667eea;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        
        .section-content h4 {{
            color: #764ba2;
            margin-top: 15px;
            margin-bottom: 8px;
        }}
        
        .section-content ul {{
            margin-left: 20px;
            margin-bottom: 15px;
        }}
        
        .section-content li {{
            margin-bottom: 8px;
        }}
        
        .section-content p {{
            margin-bottom: 15px;
        }}
        
        .section-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            background: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            overflow-x: auto;
            display: block;
        }}
        
        .section-content th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        
        .section-content td {{
            padding: 10px 12px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .section-content tr:last-child td {{
            border-bottom: none;
        }}
        
        .section-content tr:hover {{
            background: #f5f5f5;
        }}
        
        .section-content code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            color: #d63384;
        }}
        
        .section-content pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 15px 0;
        }}
        
        .section-content pre code {{
            background: transparent;
            padding: 0;
            color: inherit;
            font-size: 0.9em;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 8px;
        }}
        
        .badge-ba {{
            background: #e3f2fd;
            color: #1976d2;
        }}
        
        .badge-architect {{
            background: #f3e5f5;
            color: #7b1fa2;
        }}
        
        .badge-qa {{
            background: #fff3e0;
            color: #e65100;
        }}
        
        .badge-synthesis {{
            background: #f3e5f5;
            color: #6a1b9a;
        }}
        
        .badge-pm {{
            background: #e8f5e9;
            color: #2e7d32;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>ProjectForge Analysis</h1>
        <div class="timestamp">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        
        <div class="section">
            <div class="section-header" onclick="toggleSection(this)">
                <h2><span class="badge badge-ba">BA</span>Business Requirements</h2>
                <span class="toggle-icon">▼</span>
            </div>
            <div class="section-content">
                {ba_html}
            </div>
        </div>
        
        <div class="section">
            <div class="section-header" onclick="toggleSection(this)">
                <h2><span class="badge badge-architect">Architect</span>Technical Design</h2>
                <span class="toggle-icon">▼</span>
            </div>
            <div class="section-content">
                {architect_html}
            </div>
        </div>
        
        <div class="section">
            <div class="section-header" onclick="toggleSection(this)">
                <h2><span class="badge badge-qa">QA</span>Risk Assessment</h2>
                <span class="toggle-icon">▼</span>
            </div>
            <div class="section-content">
                {qa_html}
            </div>
        </div>
        
        <div class="section">
            <div class="section-header" onclick="toggleSection(this)">
                <h2><span class="badge badge-synthesis">Synthesis</span>Technical Summary</h2>
                <span class="toggle-icon">▼</span>
            </div>
            <div class="section-content">
                {synthesis_html}
            </div>
        </div>
        
        <div class="section">
            <div class="section-header" onclick="toggleSection(this)">
                <h2><span class="badge badge-pm">PM</span>Executive Summary & Roadmap</h2>
                <span class="toggle-icon">▼</span>
            </div>
            <div class="section-content">
                {pm_html}
            </div>
        </div>
    </div>
    
    <script>
        function toggleSection(header) {{
            const content = header.nextElementSibling;
            header.classList.toggle('collapsed');
            content.classList.toggle('collapsed');
        }}
    </script>
</body>
</html>
"""
