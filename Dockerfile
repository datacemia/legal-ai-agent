FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-fra \
    tesseract-ocr-ara \
    && rm -rf /var/lib/apt/lists/*

ENV TESSERACT_CMD=/usr/bin/tesseract
ENV OCR_LANGS=ara+fra+eng