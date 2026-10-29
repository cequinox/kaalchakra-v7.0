# ==============================================================================
# KAALCHAKRA COMPUTATION CORE (v7.0.0)
# FastAPI Web Server & REST Gateway
# ==============================================================================

from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from astro_engine import (
    calculate_kundali,
    calculate_panchanga,
    calculate_sade_sati,
    calculate_planetary_positions,
    calculate_julian_day,
    __VERSION__
)

app = FastAPI(
    title="Kaalchakra Core API",
    description="High-Precision JyotirVidya Computation Core (v7.0.0)",
    version=__VERSION__
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BirthDetailsPayload(BaseModel):
    name: Optional[str] = "Seeker"
    dob: str = Field(..., description="Date of birth: YYYY-MM-DD", example="1992-08-24")
    tob: str = Field(..., description="Time of birth: HH:MM or HH:MM:SS", example="16:45")
    lat: float = Field(..., description="Latitude", example=28.6139)
    lon: float = Field(..., description="Longitude", example=77.2090)
    tz: float = Field(5.5, description="Timezone offset from UTC in hours", example=5.5)

@app.get("/healthz")
async def health_check():
    return {"status": "healthy", "service": "Kaalchakra Core", "version": __VERSION__}

@app.get("/", response_class=HTMLResponse)
async def root_index():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Kaalchakra Core v{__VERSION__}</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0F172A; color: #F8FAFC; padding: 40px; line-height: 1.6; }}
            .card {{ background: #1E293B; border: 1px solid #334155; border-radius: 12px; max-width: 800px; margin: 0 auto; padding: 32px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
            h1 {{ color: #F29D08; margin-top: 0; }}
            .badge {{ background: #2563EB; color: white; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: bold; text-transform: uppercase; }}
            code {{ background: #0F172A; padding: 2px 6px; border-radius: 4px; color: #38BDF8; font-family: monospace; }}
            a {{ color: #F29D08; text-decoration: none; font-weight: bold; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">Release v{__VERSION__}</span>
            <h1>Kaalchakra Core API</h1>
            <p><strong>High-Precision JyotirVidya Ephemeris & Siddhantic Computation Core</strong></p>
            <p>Kaalchakra Core provides astronomical planetary longitudes, Lagna derivations, and Vedic Panchanga computation.</p>
            
            <h3>Available Endpoints:</h3>
            <ul>
                <li><code>POST /api/calculate</code> - Generate complete birth chart (D1, D9, Nakshatra, Lagna)</li>
                <li><code>GET /api/v1/panchanga</code> - Daily Panchanga and Rahu Kaal window</li>
                <li><code>GET /api/v1/sade-sati</code> - Saturn Sade Sati transit status</li>
                <li><code>GET /api/v1/quota</code> - System quota status</li>
                <li><a href="/docs">Interactive API Documentation (Swagger)</a></li>
            </ul>
        </div>
    </body>
    </html>
    """

@app.post("/api/calculate")
async def calculate_birth_chart(payload: BirthDetailsPayload):
    try:
        dt_str = f"{payload.dob} {payload.tob}"
        try:
            dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            
        tz_offset = timedelta(hours=payload.tz)
        dt_utc = dt_local - tz_offset
        
        result = calculate_kundali(dt_utc, payload.lat, payload.lon)
        result["seeker_name"] = payload.name
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Calculation error: {str(e)}")

@app.get("/api/v1/panchanga")
async def get_panchanga(lat: float = 28.6139, lon: float = 77.2090, tz: float = 5.5):
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    return calculate_panchanga(now_utc, lat, lon)

@app.get("/api/v1/sade-sati")
async def get_sade_sati(dob: str = "1992-08-24", tob: str = "16:45", lat: float = 28.6139, lon: float = 77.2090, tz: float = 5.5):
    dt_str = f"{dob} {tob}"
    dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    dt_utc = dt_local - timedelta(hours=tz)
    jd_natal = calculate_julian_day(dt_utc)
    natal_planets = calculate_planetary_positions(jd_natal)
    
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    jd_now = calculate_julian_day(now_utc)
    current_planets = calculate_planetary_positions(jd_now)
    
    return calculate_sade_sati(natal_planets["Moon"], current_planets["Saturn"])

@app.get("/api/v1/quota")
async def get_quota():
    return {
        "status": "active",
        "version": __VERSION__,
        "available_quota": "UNLIMITED",
        "rate_limit": "None (Self-Hosted)"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
