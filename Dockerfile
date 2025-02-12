# Use a minimal Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required for audio processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies without cache
RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files into the container
COPY . .

# Expose the port for Flask
EXPOSE 6000

# Run the Flask application
CMD ["python", "app.py"]


