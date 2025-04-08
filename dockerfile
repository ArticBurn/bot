# Gunakan base image Python
FROM python:3.11-slim

# Install ffmpeg dan dependensi lain
RUN apt-get update && apt-get install -y ffmpeg

# Bikin working directory
WORKDIR /app

# Copy requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file project
COPY . .

# Jalankan aplikasi
CMD ["python", "main.py"]

