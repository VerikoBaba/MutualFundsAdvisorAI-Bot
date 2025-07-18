# Use an official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for PaddleOCR and PDF handling
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Install PaddleOCR dependencies first
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the full project
COPY . .

# Run the Telegram bot
CMD ["python", "bot/main.py"]
