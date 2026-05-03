cat > backend/Dockerfile <<'EOF'
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-fra \
    tesseract-ocr-ara \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TESSERACT_CMD=/usr/bin/tesseract
ENV OCR_LANGS=ara+fra+eng

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
EOF