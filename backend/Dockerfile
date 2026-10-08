FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV TESSERACT_PATH=/usr/bin/tesseract

EXPOSE 8000

CMD ["python", "run.py"]
