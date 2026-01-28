import os
import http
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Serve HTML files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Your Gemini API key
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # <--- Replace this

# Home page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Gemini API endpoint
@app.post("/gemini")
async def gemini_api(data: dict):
    user_input = data.get("message", "")

    # Make request to Gemini API
    async with http.AsyncClient() as client:
        response = await client.post(
            "https://api.gemini.com/v1/generate",  # Replace with real Gemini endpoint
            headers={
                "Authorization": f"Bearer {GEMINI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "prompt": user_input,
                "max_tokens": 100  # Example parameter
            }
        )
        result = response.json()

    # Return Gemini reply
    return JSONResponse(content={"reply": result.get("text", "No response")})
