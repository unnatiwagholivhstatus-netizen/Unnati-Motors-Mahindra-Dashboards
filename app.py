import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# =================================================
# BASIC CONFIG
# =================================================

BASE_DIR = Path(__file__).resolve().parent
PORT = int(os.getenv("PORT", "8000"))

COMPANY_NAME = "UNNATI MOTORS"

# YOUR LIVE RENDER DASHBOARDS
DASHBOARDS = [
    {
        "key": "spare",
        "name": "Spare Ageing",
        "url": "https://spare-ageing-1-lr4x.onrender.com"
    },
    {
        "key": "openro",
        "name": "Open RO",
        "url": "https://open-ro-9ke9.onrender.com"
    },
    {
        "key": "maxi",
        "name": "Maxi Care",
        "url": "https://maxi-care.onrender.com"
    },
]

# =================================================
# APP SETUP
# =================================================

app = FastAPI(title="Unnati Motors - Common Dashboard")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# =================================================
# ROUTES
# =================================================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "company_name": COMPANY_NAME,
            "dashboards": DASHBOARDS
        }
    )

@app.get("/go/{dash_key}")
def open_dashboard(dash_key: str):
    dash = next((d for d in DASHBOARDS if d["key"] == dash_key), None)
    if not dash:
        return RedirectResponse("/", status_code=302)
    return RedirectResponse(dash["url"], status_code=302)

@app.get("/health")
def health():
    return {"status": "ok"}
