from fastapi import FastAPI, HTTPException
from playwright.async_api import async_playwright

app = FastAPI()

async def fetch_html(url: str):
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
