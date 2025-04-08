FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg libsodium-dev

# Copy source code
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Jalankan bot
CMD ["python", "main.py"]
