from fastapi import FastAPI, HTTPException
from playwright.async_api import async_playwright

app = FastAPI()

async def ensure_playwright_installed():
    # Check and install playwright if needed
    pass  # Implement your logic here if required

async def fetch_html(url: str):
    print(f"Fetching URL: {url}")  # Debugging
    await ensure_playwright_installed()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        html = await page.content()
        await browser.close()
        return html

@app.get("/fetch")
async def read_item(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="URL must be provided.")
    html = await fetch_html(url)
    return {"html": html}
