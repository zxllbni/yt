# Use the latest official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the bot code into the container
COPY . .

# Install necessary packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the necessary port (if needed)
EXPOSE 5000

# Run the bot
CMD ["python", "main.py"]
