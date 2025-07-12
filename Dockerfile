# Use official Python image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy source files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 8080

# Start both bot and server
CMD ["sh", "-c", "python bot.py & python server.py"]
