import os
from weasyprint import HTML
from bs4 import BeautifulSoup
from datetime import datetime

# Default folders
input_dir = "/app/input"
output_dir = "/app/output"
os.makedirs(output_dir, exist_ok=True)

log_file = os.path.join(output_dir, "conversion_log.txt")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    print(entry, end="")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

def clean_html(source_html):
    """Remove unsupported attributes to avoid parsing errors."""
    soup = BeautifulSoup(source_html, "html.parser")
    allowed_attrs = {"href", "src", "style", "alt", "title", "id", "class"}
    for tag in soup.find_all(True):
        for attr in list(tag.attrs):
            if attr not in allowed_attrs:
                del tag.attrs[attr]
    return str(soup)

def convert_html_to_pdf(source_file, dest_file):
    try:
        with open(source_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        cleaned_html = clean_html(html_content)
        HTML(string=cleaned_html).write_pdf(dest_file)
        log(f"✅ Converted: {source_file} → {dest_file}")
    except Exception as e:
        log(f"❌ Error converting {source_file}: {e}")

# Process all HTML files
for file in os.listdir(input_dir):
    if file.endswith(".html"):
        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, file.replace(".html", ".pdf"))
        convert_html_to_pdf(input_path, output_path)

log("🎉 All conversions completed successfully.")
