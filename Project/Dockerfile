# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install necessary system dependencies for Playwright and Chromium
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libx11-xcb1 \
    libdrm2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libxshmfence1 \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Playwright
RUN pip install flask playwright
RUN playwright install --with-deps

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /app
COPY . .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the Flask app when the container launches
CMD ["python", "app.py"]
