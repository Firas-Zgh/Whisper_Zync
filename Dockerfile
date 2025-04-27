FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Working dir
WORKDIR /app

# Copy files
COPY . .

# Install Python deps
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Start app
CMD ["python", "app.py"]
