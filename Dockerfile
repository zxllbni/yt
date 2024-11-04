# Base image with Python
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot script into the container
COPY . .

# Expose the port if necessary (Pyrogram doesn’t require specific ports, but Flask does if you expand)
EXPOSE 5000

# Run the bot script
CMD ["python", "main.py"]
