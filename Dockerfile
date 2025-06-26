# Base image with Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir torch pandas numpy scikit-learn flask

# Expose Flask default port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
