from fastapi import FastAPI, HTTPException, Request
from playwright.async_api import async_playwright
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

class URLRequest(BaseModel):
    url: str

@app.get("/fetch")
async def fetch_page(request: Request):
    url: Optional[str] = request.query_params.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="Missing 'url' parameter")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()  # HTML content
        await browser.close()

    return {"html": content}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
