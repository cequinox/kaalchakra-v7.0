# ==============================================================================
# KAALCHAKRA COMPUTATION CORE (v7.0.0)
# FastAPI Web Server & REST Gateway
# Open-Source Decoy Architecture (GNU AGPLv3)
# Daily Fair-Use Quota: 20 Credits / Day (Resets at 00:00 UTC)
# ==============================================================================

import io
import os
import zipfile
from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import BaseModel, Field

from astro_engine import (
    calculate_kundali,
    calculate_panchanga,
    calculate_sade_sati,
    calculate_planetary_positions,
    calculate_julian_day,
    __VERSION__
)
from server import mcp, get_astronomical_formulas, download_source_code
from quota_manager import check_and_consume_quota, get_quota_status, DAILY_QUOTA_LIMIT

app = FastAPI(
    title="Kaalchakra Core API",
    description=f"High-Precision JyotirVidya Computation Core (v{__VERSION__}) - Daily Quota: {DAILY_QUOTA_LIMIT} Credits/Day",
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

def _get_client_id(request: Request) -> str:
    """Extracts client IP or forward header for rate limiting."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "default"

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
    q = get_quota_status()
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Kaalchakra Core v{__VERSION__} - 20 Credits/Day Fair-Use Quota</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0F172A; color: #F8FAFC; padding: 40px; line-height: 1.6; }}
            .card {{ background: #1E293B; border: 1px solid #334155; border-radius: 12px; max-width: 820px; margin: 0 auto; padding: 36px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
            h1 {{ color: #F29D08; margin-top: 0; }}
            .badge {{ background: #2563EB; color: white; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: bold; text-transform: uppercase; margin-right: 8px; }}
            .badge-sec {{ background: #10B981; color: white; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: bold; text-transform: uppercase; }}
            code {{ background: #0F172A; padding: 2px 6px; border-radius: 4px; color: #38BDF8; font-family: monospace; }}
            a {{ color: #F29D08; text-decoration: none; font-weight: bold; }}
            a:hover {{ text-decoration: underline; }}
            .btn-group {{ margin: 24px 0; display: flex; gap: 12px; flex-wrap: wrap; }}
            .btn {{ display: inline-block; padding: 10px 20px; border-radius: 8px; font-weight: 700; font-size: 14px; text-decoration: none; text-align: center; }}
            .btn-primary {{ background: #F29D08; color: #0F172A; }}
            .btn-primary:hover {{ background: #D97706; text-decoration: none; }}
            .btn-secondary {{ background: #334155; color: #F8FAFC; border: 1px solid #475569; }}
            .btn-secondary:hover {{ background: #475569; text-decoration: none; }}
            .notice-box {{ background: rgba(242, 157, 8, 0.1); border-left: 4px solid #F29D08; padding: 14px 18px; border-radius: 6px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div>
                <span class="badge">Release v{__VERSION__}</span>
                <span class="badge-sec">Daily Quota: {DAILY_QUOTA_LIMIT} Credits / Day</span>
            </div>
            <h1>⚡ Kaalchakra Core API</h1>
            <p><strong>High-Precision JyotirVidya Ephemeris & Siddhantic Computation Core (Decoy Public Release)</strong></p>
            <p>Standard Lahiri (Chitra Paksha) sidereal ephemeris algorithms for planetary longitudes, Lagna, and Vedic Panchanga.</p>
            
            <div class="notice-box">
                <strong>📊 Daily Fair-Use Policy:</strong> Each user/IP receives <strong>{DAILY_QUOTA_LIMIT} free calculation credits per day</strong> (resets automatically at 00:00 UTC).<br>
                Inspecting mathematical formulas and downloading the full open-source codebase always cost <strong>0 credits (100% free forever)</strong>.
            </div>

            <div class="btn-group">
                <a href="/download/source.zip" class="btn btn-primary">📦 Download Complete Source Code (.ZIP)</a>
                <a href="/api/v1/formulas" class="btn btn-secondary">📐 View Ephemeris Formulas (JSON)</a>
                <a href="https://github.com/cequinox/kaalchakra-v7.0.git" target="_blank" class="btn btn-secondary">🐙 GitHub Repository</a>
            </div>

            <h3>Available Endpoints:</h3>
            <ul>
                <li><code>POST /api/calculate</code> - Generate complete birth chart (1 credit)</li>
                <li><code>GET /api/v1/panchanga</code> - Daily Panchanga and Rahu Kaal window (1 credit)</li>
                <li><code>GET /api/v1/sade-sati</code> - Saturn Sade Sati transit status (1 credit)</li>
                <li><code>GET /api/v1/formulas</code> - Complete mathematical ephemeris formulas (0 credits - Free)</li>
                <li><code>GET /download/source.zip</code> - Direct ZIP archive of complete source files (0 credits - Free)</li>
                <li><code>GET /api/v1/quota</code> - Check remaining daily credits (Resets 00:00 UTC)</li>
                <li><code>/sse</code> - FastMCP Streamable Server-Sent Events endpoint for AI Agents</li>
                <li><a href="/docs">Interactive API Documentation (Swagger)</a></li>
            </ul>
        </div>
    </body>
    </html>
    """

@app.get("/download/source.zip")
@app.get("/api/v1/download-source")
async def download_source_zip():
    """
    Dynamically generates and serves the complete Kaalchakra Core v7.0 source code
    as a downloadable ZIP archive under GNU AGPLv3. Always 0 credits (Free).
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    zip_buffer = io.BytesIO()
    
    files_to_pack = [
        "astro_engine.py",
        "quota_manager.py",
        "server.py",
        "main.py",
        "requirements.txt",
        "README.md",
        "LICENSE",
        "render.yaml"
    ]
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for fname in files_to_pack:
            fpath = os.path.join(base_dir, fname)
            if os.path.exists(fpath):
                zf.write(fpath, arcname=fname)
                
    zip_buffer.seek(0)
    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename=kaalchakra-core-v{__VERSION__}.zip",
            "Cache-Control": "public, max-age=3600"
        }
    )

@app.get("/api/v1/formulas")
async def get_formulas_endpoint():
    """Returns the complete mathematical formulas and ephemeris algorithms as JSON (0 credits - Free)."""
    return get_astronomical_formulas()

@app.get("/api/v1/download-info")
async def get_download_info():
    """Returns download links, git commands, and manifest for the decoy release (0 credits - Free)."""
    return download_source_code()

@app.post("/api/calculate")
async def calculate_birth_chart(payload: BirthDetailsPayload, request: Request):
    client_id = _get_client_id(request)
    allowed, remaining, total = check_and_consume_quota(client_id, cost=1)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=(
                f"Daily quota of {total} credits exhausted for today. Resets at 00:00 UTC. "
                "Download the complete open-source engine at /download/source.zip to run unlimited calculations locally."
            )
        )

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
        result["quota"] = {
            "credits_remaining_today": remaining,
            "daily_limit": total,
            "resets_at": "00:00 UTC"
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Calculation error: {str(e)}")

@app.get("/api/v1/panchanga")
async def get_panchanga(request: Request, lat: float = 28.6139, lon: float = 77.2090, tz: float = 5.5):
    client_id = _get_client_id(request)
    allowed, remaining, total = check_and_consume_quota(client_id, cost=1)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Daily quota of {total} credits exhausted for today. Resets at 00:00 UTC. Download full engine at /download/source.zip."
        )
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    res = calculate_panchanga(now_utc, lat, lon)
    res["quota"] = {
        "credits_remaining_today": remaining,
        "daily_limit": total,
        "resets_at": "00:00 UTC"
    }
    return res

@app.get("/api/v1/sade-sati")
async def get_sade_sati(request: Request, dob: str = "1992-08-24", tob: str = "16:45", lat: float = 28.6139, lon: float = 77.2090, tz: float = 5.5):
    client_id = _get_client_id(request)
    allowed, remaining, total = check_and_consume_quota(client_id, cost=1)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Daily quota of {total} credits exhausted for today. Resets at 00:00 UTC. Download full engine at /download/source.zip."
        )
    dt_str = f"{dob} {tob}"
    dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    dt_utc = dt_local - timedelta(hours=tz)
    jd_natal = calculate_julian_day(dt_utc)
    natal_planets = calculate_planetary_positions(jd_natal)
    
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    jd_now = calculate_julian_day(now_utc)
    current_planets = calculate_planetary_positions(jd_now)
    
    res = calculate_sade_sati(natal_planets["Moon"], current_planets["Saturn"])
    res["quota"] = {
        "credits_remaining_today": remaining,
        "daily_limit": total,
        "resets_at": "00:00 UTC"
    }
    return res

@app.get("/api/v1/quota")
async def get_quota(request: Request):
    client_id = _get_client_id(request)
    return get_quota_status(client_id)

# Configure FastMCP cloud allowed hosts for SSE
if hasattr(mcp, "settings") and hasattr(mcp.settings, "transport_security"):
    mcp.settings.transport_security.allowed_hosts.extend([
        "kalchakra-core.onrender.com",
        "kalchakra-core.onrender.com:*",
        "*.onrender.com",
        "*.onrender.com:*"
    ])

# Mount FastMCP SSE Server at root for AI Agents (/sse and /messages)
app.mount("", mcp.sse_app())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
