from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import asyncio
import os

app = FastAPI()

async def fetch_html(url: str) -> str:
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Initialize the Chrome WebDriver
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        await asyncio.sleep(2)  # Wait for the page to load
        html = driver.page_source
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching the page: {str(e)}")
    finally:
        driver.quit()

    return html

@app.get("/fetch")
async def read_item(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="URL must be provided.")
    html = await fetch_html(url)
    return {"html": html}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))