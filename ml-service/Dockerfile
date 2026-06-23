FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for OpenCV and other ML packages
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the easyocr models so they are baked into the Docker image
# This prevents startup timeouts and massive log spam during deployment
RUN python -c "import easyocr; easyocr.Reader(['en'], gpu=False)" > /dev/null

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
