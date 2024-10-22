FROM mcr.microsoft.com/playwright/python:v1.40.0-focal

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
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

# Create a new user
RUN groupadd -r playwright && useradd -r -g playwright -G audio,video playwright \
    && mkdir -p /home/playwright \
    && chown -R playwright:playwright /home/playwright

# Copy requirements file
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install --with-deps
RUN DEBIAN_FRONTEND=noninteractive playwright install-deps

# Copy the application code
COPY main.py .

# Update permissions
RUN chown -R playwright:playwright /app

# Switch to non-root user
USER playwright

# Create the browser launch script
RUN echo 'from fastapi import FastAPI, HTTPException\n\
from playwright.async_api import async_playwright\n\
import asyncio\n\
import logging\n\
\n\
logging.basicConfig(level=logging.DEBUG)\n\
logger = logging.getLogger(__name__)\n\
\n\
app = FastAPI()\n\
\n\
async def fetch_html(url: str):\n\
    logger.info(f"Starting to fetch URL: {url}")\n\
    try:\n\
        async with async_playwright() as p:\n\
            browser = await p.chromium.launch(\n\
                headless=True,\n\
                args=[\n\
                    "--no-sandbox",\n\
                    "--disable-setuid-sandbox",\n\
                    "--disable-dev-shm-usage",\n\
                    "--single-process",\n\
                ]\n\
            )\n\
            try:\n\
                context = await browser.new_context(\n\
                    viewport={"width": 1920, "height": 1080},\n\
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"\n\
                )\n\
                page = await context.new_page()\n\
                logger.info("Navigating to page")\n\
                \n\
                response = await page.goto(\n\
                    url,\n\
                    wait_until="domcontentloaded",\n\
                    timeout=30000\n\
                )\n\
                \n\
                if not response:\n\
                    raise HTTPException(status_code=404, detail="Page not found")\n\
                \n\
                if response.status >= 400:\n\
                    raise HTTPException(\n\
                        status_code=response.status,\n\
                        detail=f"Page returned status code: {response.status}"\n\
                    )\n\
                \n\
                # Wait for the page to stabilize\n\
                await asyncio.sleep(2)\n\
                \n\
                logger.info("Page loaded successfully")\n\
                html = await page.content()\n\
                return html\n\
            finally:\n\
                await browser.close()\n\
    except Exception as e:\n\
        logger.error(f"Error in fetch_html: {str(e)}")\n\
        raise HTTPException(status_code=500, detail=str(e))\n\
\n\
@app.get("/fetch")\n\
async def read_item(url: str):\n\
    if not url:\n\
        raise HTTPException(status_code=400, detail="URL must be provided")\n\
    logger.info(f"Received request for URL: {url}")\n\
    return {"html": await fetch_html(url)}' > main.py

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]