# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Install system dependencies (for pyrogram + flask)
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to install deps
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose Flask port
EXPOSE 5000

# Start both: Telegram bot & Flask server
CMD ["sh", "-c", "python stream_server.py & python bot.py"]
