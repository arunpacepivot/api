# Use the official Ubuntu image as the base
FROM ubuntu:20.04

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and ensure apt-get works correctly
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgbm1 \
    libgcc1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    fonts-liberation \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python and pip (if not already included)
RUN apt-get update && apt-get install -y python3 python3-pip

# Install Playwright dependencies and browser binaries
RUN pip3 install --no-cache-dir playwright && \
    playwright install-deps && \
    playwright install chromium

# Create a new user for Playwright
RUN groupadd -r playwright && useradd -r -g playwright -G audio,video playwright \
    && mkdir -p /home/playwright \
    && chown -R playwright:playwright /home/playwright

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Expose port 8080 for the FastAPI application
EXPOSE 8080

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
