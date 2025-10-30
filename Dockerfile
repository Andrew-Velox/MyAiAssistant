# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port (change if your app uses a different port)
EXPOSE 8000

# Start the app (adjust if you use Flask, FastAPI, etc.)
CMD ["python", "app.py"]