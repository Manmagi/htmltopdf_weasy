FROM python:3.11-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    fontconfig \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python script and fonts
COPY html_to_pdf_weasy.py /app/html_to_pdf_weasy.py
COPY fonts /usr/share/fonts/truetype/noto

# Rebuild font cache
RUN fc-cache -f -v

# Install Python libraries
RUN pip install --no-cache-dir weasyprint beautifulsoup4

# Non-root user
RUN useradd -m appuser
USER appuser

ENTRYPOINT ["python", "html_to_pdf_weasy.py"]
