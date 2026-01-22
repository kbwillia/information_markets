"""
Script to convert Polymarket API Documentation PDF to Markdown.
"""
import sys
import os
import re

# Add project root to path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    try:
        import PyPDF2
        PYPDF2_AVAILABLE = True
    except ImportError:
        PYPDF2_AVAILABLE = False

def clean_text(text):
    """Clean and format extracted text."""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    
    # Fix common PDF extraction issues
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    
    return text.strip()

def extract_with_pdfplumber(pdf_path):
    """Extract text using pdfplumber (better for structured content)."""
    text_parts = []
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        
        for i, page in enumerate(pdf.pages):
            print(f"Processing page {i+1}/{len(pdf.pages)}...")
            text = page.extract_text()
            if text:
                text_parts.append(clean_text(text))
    
    return '\n\n'.join(text_parts)

def extract_with_pypdf2(pdf_path):
    """Extract text using PyPDF2 (fallback)."""
    text_parts = []
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        print(f"Total pages: {len(pdf_reader.pages)}")
        
        for i, page in enumerate(pdf_reader.pages):
            print(f"Processing page {i+1}/{len(pdf_reader.pages)}...")
            text = page.extract_text()
            if text:
                text_parts.append(clean_text(text))
    
    return '\n\n'.join(text_parts)

def convert_to_markdown(text):
    """Convert plain text to markdown format."""
    lines = text.split('\n')
    markdown_lines = []
    in_code_block = False
    in_list = False
    
    for line in lines:
        line = line.strip()
        
        if not line:
            if in_list:
                in_list = False
            markdown_lines.append('')
            continue
        
        # Detect code blocks (lines starting with curl, import, etc.)
        if re.match(r'^(curl|import|from|npm install|pip install|```)', line, re.IGNORECASE):
            if not in_code_block:
                markdown_lines.append('```bash' if 'curl' in line.lower() or 'install' in line.lower() else '```python')
                in_code_block = True
            markdown_lines.append(line)
            continue
        
        # Detect end of code block
        if in_code_block and (line.endswith('```') or not re.match(r'^[#\w\s\[\]{}":,./\-=<>()]+$', line)):
            if line != '```':
                markdown_lines.append(line)
            markdown_lines.append('```')
            in_code_block = False
            continue
        
        if in_code_block:
            markdown_lines.append(line)
            continue
        
        # Detect headers (lines that are all caps or start with #)
        if line.isupper() and len(line) > 5 and not line.endswith('?'):
            markdown_lines.append(f'\n## {line.title()}\n')
            continue
        
        # Detect section headers (lines ending with colon or short lines)
        if line.endswith(':') and len(line) < 50:
            markdown_lines.append(f'\n### {line[:-1]}\n')
            continue
        
        # Detect numbered lists
        if re.match(r'^\d+[\.\)]\s+', line):
            markdown_lines.append(line)
            in_list = True
            continue
        
        # Detect bullet points
        if re.match(r'^[-*•]\s+', line):
            markdown_lines.append(line)
            in_list = True
            continue
        
        # Regular text
        markdown_lines.append(line)
    
    # Close any open code blocks
    if in_code_block:
        markdown_lines.append('```')
    
    return '\n'.join(markdown_lines)

def main():
    pdf_path = os.path.join(project_root, 'docs', 'Polymarket API Documentation black and white.pdf')
    output_path = os.path.join(project_root, 'docs', 'POLYMARKET_API_DOCUMENTATION.md')
    
    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    print(f"Converting PDF to Markdown...")
    print(f"Input: {pdf_path}")
    print(f"Output: {output_path}")
    
    # Extract text from PDF
    if PDFPLUMBER_AVAILABLE:
        print("\nUsing pdfplumber for extraction...")
        text = extract_with_pdfplumber(pdf_path)
    elif PYPDF2_AVAILABLE:
        print("\nUsing PyPDF2 for extraction...")
        text = extract_with_pypdf2(pdf_path)
    else:
        print("ERROR: No PDF library available!")
        print("Install one of:")
        print("  pip install pdfplumber  (recommended)")
        print("  pip install PyPDF2")
        sys.exit(1)
    
    # Convert to markdown
    print("\nConverting to Markdown format...")
    markdown_content = convert_to_markdown(text)
    
    # Add header
    header = """# Polymarket API Documentation

> This document was automatically converted from the PDF documentation.
> Source: `docs/Polymarket API Documentation black and white.pdf`

---

"""
    
    final_content = header + markdown_content
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"\n[SUCCESS] Successfully converted PDF to Markdown!")
    print(f"  Output saved to: {output_path}")
    print(f"  Total characters: {len(final_content)}")

if __name__ == "__main__":
    main()

