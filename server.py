# ==============================================================================
# KAALCHAKRA COMPUTATION CORE (v7.0.0)
# FastMCP Model Context Protocol Server for AI Agents
# Standard Lahiri (Chitra Paksha) Sidereal Engine
# Open-Source Decoy Architecture (GNU AGPLv3)
# Daily Fair-Use Quota: 20 Credits / Day (Resets at 00:00 UTC)
# ==============================================================================

import os
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

try:
    from mcp.server.fastmcp import FastMCP
except (ImportError, ModuleNotFoundError):
    try:
        from mcp.server.mcpserver import MCPServer as FastMCP
    except Exception:
        from mcp.server import Server as FastMCP

from astro_engine import (
    calculate_kundali,
    calculate_panchanga,
    calculate_sade_sati,
    calculate_planetary_positions,
    calculate_julian_day,
    __VERSION__
)
from quota_manager import check_and_consume_quota, get_quota_status, DAILY_QUOTA_LIMIT

# Initialize FastMCP Server
mcp = FastMCP("kaalchakra-core-v7")

def _quota_exhausted_payload() -> Dict[str, Any]:
    q = get_quota_status()
    return {
        "status": "error",
        "error_code": "DAILY_QUOTA_EXHAUSTED",
        "message": (
            f"⛔ DAILY QUOTA EXHAUSTED: You have utilized all {DAILY_QUOTA_LIMIT} free calculation credits for today ({q['date_utc']}).\n"
            "Your 20 daily credits will automatically reset at 00:00 UTC.\n\n"
            "💡 TO RUN UNLIMITED CALCULATIONS:\n"
            "Download the complete open-source engine and run locally without limits:\n"
            "📦 Direct ZIP: https://kalchakra-core.onrender.com/download/source.zip\n"
            "🐙 Git Clone: git clone https://github.com/cequinox/kaalchakra-v7.0.git\n"
            "📫 Enterprise Inquiries: enterprise@kaalchakra.com"
        ),
        "quota": q,
        "source_download": "https://kalchakra-core.onrender.com/download/source.zip"
    }

@mcp.tool(name="show_welcome_and_language_menu")
def show_welcome_and_language_menu(user_name: Optional[str] = None) -> str:
    """
    Displays the official Kaalchakra Core v7.0 first-contact welcome banner,
    pathway options, daily quota status (20 credits/day), and system status.
    """
    name_str = f" {user_name.strip().upper()}" if user_name else ""
    q = get_quota_status()
    return (
        "================================================================================\n"
        f"🙏 NAMASTE{name_str} & WARM WELCOME | KAALCHAKRA CORE v7.0\n"
        "================================================================================\n"
        "Welcome to Kaalchakra Core v7.0 (Official Decoy Release).\n"
        "Standard Lahiri (Chitra Paksha) Sidereal Ephemeris Engine.\n\n"
        "🌟 Available Pathways:\n"
        "  [ 1 ] Full Birth Chart (D1 Rashi & D9 Navamsha on Lahiri)\n"
        "  [ 2 ] Real-Time Daily Panchanga (5 Limbs of Time) & Rahu Kaal\n"
        "  [ 3 ] Saturn Sade Sati Transit Analysis\n"
        "  [ 4 ] Core Astronomical Formulas & Full Source Code Download\n\n"
        f"⚡ System Status: Active & Online (Kaalchakra Core v{__VERSION__})\n"
        f"📊 Daily Fair-Use Quota: {q['credits_remaining']} / {q['daily_limit']} Credits Remaining Today (Resets 00:00 UTC)\n"
        "📫 Customer Support: support@kaalchakra.com | Enterprise: enterprise@kaalchakra.com\n"
        "================================================================================"
    )

@mcp.tool(name="calculate_vedic_chart")
def calculate_vedic_chart(
    dob: Optional[str] = None,
    tob: Optional[str] = None,
    city: str = "Delhi",
    name: str = "Seeker",
    format: str = "full",
    language: str = "en",
    date_of_birth: Optional[str] = None,
    time_of_birth: Optional[str] = None,
    place: Optional[str] = None,
    chart_style: str = "north",
    email: Optional[str] = None,
    code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculates comprehensive Vedic birth chart using default Lahiri Ayanamsha.
    Consumes 1 daily credit from your 20 credits/day quota.
    """
    allowed, remaining, total = check_and_consume_quota(cost=1)
    if not allowed:
        return _quota_exhausted_payload()

    dob_val = dob or date_of_birth or "1992-08-24"
    tob_val = tob or time_of_birth or "16:45"
    city_val = place or city or "Delhi"
    
    # Default lat/lon for common queries (New Delhi standard)
    lat, lon, tz = 28.6139, 77.2090, 5.5
    
    dt_str = f"{dob_val} {tob_val}"
    try:
        dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        
    dt_utc = dt_local - timedelta(hours=tz)
    chart = calculate_kundali(dt_utc, lat, lon)
    chart["seeker_name"] = name
    chart["city"] = city_val
    chart["engine_version"] = f"Kaalchakra Core v{__VERSION__}"
    chart["quota"] = {
        "credits_remaining_today": remaining,
        "daily_limit": total,
        "resets_at": "00:00 UTC"
    }
    chart["telemetry_footer"] = f"📊 Daily Quota: {remaining} / {total} Credits Remaining (Resets at 00:00 UTC) | Support: support@kaalchakra.com"
    return chart

@mcp.tool(name="calculate_kundali")
def calculate_kundali_tool(
    name: str = "Seeker",
    dob: str = "1992-08-24",
    tob: str = "16:45",
    latitude: float = 28.6139,
    longitude: float = 77.2090,
    timezone_offset: float = 5.5
) -> Dict[str, Any]:
    """
    Calculate full Vedic birth chart (Lagna, Rashi, Nakshatra, D1 Rashi, D9 Navamsha)
    using default Lahiri (Chitra Paksha) sidereal ephemeris.
    Consumes 1 credit from your 20 credits/day quota.
    """
    allowed, remaining, total = check_and_consume_quota(cost=1)
    if not allowed:
        return _quota_exhausted_payload()

    dt_str = f"{dob} {tob}"
    try:
        dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        
    dt_utc = dt_local - timedelta(hours=timezone_offset)
    chart = calculate_kundali(dt_utc, latitude, longitude)
    chart["seeker_name"] = name
    chart["engine_version"] = f"Kaalchakra Core v{__VERSION__}"
    chart["quota"] = {
        "credits_remaining_today": remaining,
        "daily_limit": total,
        "resets_at": "00:00 UTC"
    }
    chart["telemetry_footer"] = f"📊 Daily Quota: {remaining} / {total} Credits Remaining (Resets at 00:00 UTC) | Support: support@kaalchakra.com"
    return chart

@mcp.tool(name="calculate_panchanga")
def calculate_panchanga_tool(
    latitude: float = 28.6139,
    longitude: float = 77.2090,
    timezone_offset: float = 5.5
) -> Dict[str, Any]:
    """
    Calculate real-time Vedic Panchanga (Tithi, Vara, Nakshatra, Yoga, Karana, Rahu Kaal)
    using default Lahiri sidereal reference.
    Consumes 1 credit from your 20 credits/day quota.
    """
    allowed, remaining, total = check_and_consume_quota(cost=1)
    if not allowed:
        return _quota_exhausted_payload()

    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    res = calculate_panchanga(now_utc, latitude, longitude)
    res["engine_version"] = f"Kaalchakra Core v{__VERSION__}"
    res["quota"] = {
        "credits_remaining_today": remaining,
        "daily_limit": total,
        "resets_at": "00:00 UTC"
    }
    res["telemetry_footer"] = f"📊 Daily Quota: {remaining} / {total} Credits Remaining (Resets at 00:00 UTC) | Support: support@kaalchakra.com"
    return res

@mcp.tool(name="calculate_sade_sati")
def calculate_sade_sati_tool(
    dob: str = "1992-08-24",
    tob: str = "16:45",
    latitude: float = 28.6139,
    longitude: float = 77.2090,
    timezone_offset: float = 5.5
) -> Dict[str, Any]:
    """
    Determine Saturn Sade Sati transit phase for a given birth chart
    under default Lahiri sidereal Moon.
    Consumes 1 credit from your 20 credits/day quota.
    """
    allowed, remaining, total = check_and_consume_quota(cost=1)
    if not allowed:
        return _quota_exhausted_payload()

    dt_str = f"{dob} {tob}"
    dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    dt_utc = dt_local - timedelta(hours=timezone_offset)
    jd_natal = calculate_julian_day(dt_utc)
    natal_planets = calculate_planetary_positions(jd_natal)
    
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    jd_now = calculate_julian_day(now_utc)
    current_planets = calculate_planetary_positions(jd_now)
    
    res = calculate_sade_sati(natal_planets["Moon"], current_planets["Saturn"])
    res["engine_version"] = f"Kaalchakra Core v{__VERSION__}"
    res["quota"] = {
        "credits_remaining_today": remaining,
        "daily_limit": total,
        "resets_at": "00:00 UTC"
    }
    res["telemetry_footer"] = f"📊 Daily Quota: {remaining} / {total} Credits Remaining (Resets at 00:00 UTC) | Support: support@kaalchakra.com"
    return res

@mcp.tool(name="ask_kundali_contextual_query")
def ask_kundali_contextual_query(
    dob: str,
    tob: str,
    city: str = "New Delhi",
    query_category: Optional[str] = "CAREER_PIVOT",
    name: str = "Seeker"
) -> Dict[str, Any]:
    """
    Evaluates contextual astrological queries on Kaalchakra Core v7.0.
    Consumes 1 credit from your 20 credits/day quota.
    """
    allowed, remaining, total = check_and_consume_quota(cost=1)
    if not allowed:
        return _quota_exhausted_payload()

    dt_str = f"{dob} {tob}"
    try:
        dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        
    dt_utc = dt_local - timedelta(hours=5.5)
    chart = calculate_kundali(dt_utc, 28.6139, 77.2090)
    
    return {
        "status": "success",
        "engine_version": f"Kaalchakra Core v{__VERSION__}",
        "seeker": name,
        "query_category": query_category,
        "ayanamsha_system": "Lahiri (Chitra Paksha)",
        "ascendant": chart["ascendant"],
        "moon_sign": chart["moon_sign"],
        "analysis": (
            f"Under Kaalchakra Core v{__VERSION__} (Lahiri Sidereal), Lagna is at {chart['ascendant']['longitude']}° ({chart['ascendant']['sign']}) "
            f"and Moon is at {chart['moon_sign']['longitude']}° ({chart['moon_sign']['sign']} - Nakshatra {chart['moon_sign']['nakshatra']}). "
            f"Planetary longitudes: {chart['planetary_positions']}."
        ),
        "quota": {
            "credits_remaining_today": remaining,
            "daily_limit": total,
            "resets_at": "00:00 UTC"
        },
        "telemetry_footer": f"📊 Daily Quota: {remaining} / {total} Credits Remaining (Resets at 00:00 UTC) | Support: support@kaalchakra.com"
    }

@mcp.tool(name="get_astronomical_formulas")
def get_astronomical_formulas(topic: Optional[str] = "all") -> Dict[str, Any]:
    """
    Returns the exact mathematical formulas, ephemeris equations, and computational
    algorithms powering Kaalchakra Core v7.0 under GNU AGPLv3.
    Always 100% Free with ZERO quota deduction (0 credits).
    """
    return {
        "status": "success",
        "engine_version": f"Kaalchakra Core v{__VERSION__}",
        "license": "GNU Affero General Public License v3.0 (AGPLv3)",
        "quota_cost": "0 Credits (Free Open Access)",
        "source_repository": "https://github.com/cequinox/kaalchakra-v7.0.git",
        "zip_download_url": "https://kalchakra-core.onrender.com/download/source.zip",
        "formulas": {
            "julian_day": {
                "name": "Astronomical Julian Day (JD)",
                "formula": "JD = floor(365.25 * (Y + 4716)) + floor(30.6001 * (M + 1)) + D + B - 1524.5 + (H/24.0)",
                "description": "Calculates Julian Day from UTC datetime with Gregorian century leap correction B = 2 - A + floor(A/4), where A = floor(Y/100)."
            },
            "lahiri_ayanamsa": {
                "name": "Sidereal Lahiri (Chitra Paksha) Ayanamsha",
                "formula": "Ayanamsha = (24.041892 + (50.290966 * T + 0.0222222 * T^2) / 3600.0 + 1.14159 * sin(125.04° - 1934.136° * T)) mod 360°",
                "epoch": "J2000.0 standard where T = (JD - 2451545.0) / 36525.0 (centuries from J2000)."
            },
            "ascendant_lagna": {
                "name": "Eastern Horizon Ascendant (Lagna)",
                "formula": "Lagna = (arctan2(-cos(LMST), sin(LMST)*cos(ε) + tan(φ)*sin(ε)) - Ayanamsha + 2.14159*sin(2*LMST)) mod 360°",
                "parameters": "LMST = Local Mean Sidereal Time (GMST + Lon), ε = Obliquity of Ecliptic (21.94218°), φ = Observer Latitude."
            },
            "planetary_longitudes": {
                "sun": "L_sun = (280.46646° + 36000.76983°*T + 1.9146°*sin(M_sun) + 0.02°*sin(2*M_sun) + 3.8421°*sin(M_sun + 0.523) + 0.618°*cos(2*M_sun) - Ayanamsha) mod 360°",
                "moon": "L_moon = (218.3165° + 481267.8813°*T + Evection + Variation + Drift - Ayanamsha) mod 360°",
                "mars": "L_mars = (355.433° + 19140.299°*T + 10.691°*sin(M_mars) + 3.14°*sin(M_sun) - Ayanamsha) mod 360°",
                "mercury": "L_merc = (Sun_Tropical + 24.12°*sin(168.65° + 149472.51°*T) - Ayanamsha + 2.84°*cos(M_sun)) mod 360°",
                "jupiter": "L_jup = (34.351° + 3034.905°*T + 5.55°*sin(M_jup) + 1.84°*sin(2*M_jup) - Ayanamsha) mod 360°",
                "venus": "L_ven = (Sun_Tropical + 46.21°*sin(212.6° + 58517.8°*T) - Ayanamsha - 3.12°*sin(M_sun)) mod 360°",
                "saturn": "L_sat = (50.077° + 1222.113°*T + 6.35°*sin(M_sat) + 3.42°*sin(M_jup) - Ayanamsha) mod 360°",
                "rahu": "L_rahu = ((125.0445° - 1934.1362°*T) + 8.25°*sin(2*(Moon - Sun)) - Ayanamsha) mod 360°",
                "ketu": "L_ketu = (L_rahu + 180.0°) mod 360°"
            },
            "d9_navamsha": {
                "name": "D9 Navamsha Harmonic Division",
                "formula": "Navamsha_Index = floor((Degree mod 360°) / (3.333333°)) mod 12",
                "sign_span": "Each 30° Rashi is partitioned into 9 equal harmonic arcs of 3° 20' each."
            },
            "panchanga_limbs": {
                "tithi": "Tithi = floor(((Moon - Sun) mod 360°) / 12°) + 1 (1-15 Shukla, 16-30 Krishna)",
                "vara": "Vara = Weekday derived from Gregorian Julian calendar date",
                "nakshatra": "Nakshatra = floor((Moon mod 360°) / (13.333333°)) (0-26 across 27 Nakshatras)",
                "yoga": "Yoga = floor(((Sun + Moon) mod 360°) / (13.333333°)) (0-26 across 27 Nitya Yogas)",
                "karana": "Karana = floor(((Moon - Sun) mod 360°) / 6°) + 1 (Half of a Tithi)"
            },
            "sade_sati": {
                "name": "Saturn Sade Sati Transit Window",
                "formula": "Diff_Rashi = (Saturn_Rashi - Moon_Rashi) mod 12 -> 11: Rising (12th), 0: Peak (1st), 1: Setting (2nd)"
            }
        }
    }

@mcp.tool(name="download_source_code")
def download_source_code(include_files: bool = False) -> Dict[str, Any]:
    """
    Provides complete download access, ZIP archive endpoints, and GitHub repository details
    for the open-source Kaalchakra Core v7.0 decoy release.
    Always 100% Free with ZERO quota deduction (0 credits).
    """
    res = {
        "status": "success",
        "engine_version": f"Kaalchakra Core v{__VERSION__}",
        "license": "GNU Affero General Public License v3.0 (AGPLv3)",
        "quota_cost": "0 Credits (Free Open Access)",
        "github_repository": "https://github.com/cequinox/kaalchakra-v7.0.git",
        "zip_download_url": "https://kalchakra-core.onrender.com/download/source.zip",
        "git_clone_command": "git clone https://github.com/cequinox/kaalchakra-v7.0.git",
        "file_manifest": [
            "astro_engine.py",
            "quota_manager.py",
            "server.py",
            "main.py",
            "requirements.txt",
            "README.md",
            "LICENSE",
            "render.yaml"
        ],
        "message": (
            "Kaalchakra Core v7.0 is 100% free and open-source under GNU AGPLv3. "
            "You can clone via git clone https://github.com/cequinox/kaalchakra-v7.0.git or "
            "download the complete ZIP archive at https://kalchakra-core.onrender.com/download/source.zip."
        )
    }
    if include_files:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        contents = {}
        for fn in ["astro_engine.py", "quota_manager.py", "server.py", "main.py", "requirements.txt", "README.md", "LICENSE", "render.yaml"]:
            fp = os.path.join(this_dir, fn)
            if os.path.exists(fp):
                try:
                    with open(fp, "r", encoding="utf-8") as f:
                        contents[fn] = f.read()
                except Exception as e:
                    contents[fn] = f"Error reading {fn}: {e}"
        res["files"] = contents
    return res

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Kaalchakra Core v7.0 MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse", "streamable-http", "http"], default=os.getenv("MCP_TRANSPORT", "stdio"))
    parser.add_argument("--host", default=os.getenv("HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8000")))
    args, _ = parser.parse_known_args()

    mcp.settings.host = args.host
    mcp.settings.port = args.port

    if args.transport in ["sse", "http"]:
        mcp.run(transport="sse")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
