# ==============================================================================
# KAALCHAKRA COMPUTATION CORE (v7.0.0)
# FastMCP Model Context Protocol Server for AI Agents
# Standard Lahiri (Chitra Paksha) Sidereal Engine
# ==============================================================================

import os
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

from mcp.server.fastmcp import FastMCP
from astro_engine import (
    calculate_kundali,
    calculate_panchanga,
    calculate_sade_sati,
    calculate_planetary_positions,
    calculate_julian_day,
    __VERSION__
)

# Initialize FastMCP Server
mcp = FastMCP("kaalchakra-core-v7")

@mcp.tool(name="show_welcome_and_language_menu")
def show_welcome_and_language_menu(user_name: Optional[str] = None) -> str:
    """
    Displays the official Kaalchakra Core v7.0 first-contact welcome banner,
    pathway options, and system status.
    """
    name_str = f" {user_name.strip().upper()}" if user_name else ""
    return (
        "================================================================================\n"
        f"🙏 NAMASTE{name_str} & WARM WELCOME | KAALCHAKRA CORE v7.0\n"
        "================================================================================\n"
        "Welcome to Kaalchakra Core v7.0 (Official Release).\n"
        "Standard Lahiri (Chitra Paksha) Sidereal Ephemeris Engine.\n\n"
        "🌟 Available Pathways:\n"
        "  [ 1 ] Full Birth Chart (D1 Rashi & D9 Navamsha on Lahiri)\n"
        "  [ 2 ] Real-Time Daily Panchanga (5 Limbs of Time) & Rahu Kaal\n"
        "  [ 3 ] Saturn Sade Sati Transit Analysis\n"
        "  [ 4 ] Core Astronomical & Mathematical Architecture\n\n"
        f"⚡ System Status: Active (Kaalchakra Core v{__VERSION__})\n"
        "📊 License: GNU AGPLv3 | Ephemeris: Lahiri Sidereal Baseline\n"
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
    Powered by Kaalchakra Core v7.0.
    """
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
    """
    dt_str = f"{dob} {tob}"
    try:
        dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        
    dt_utc = dt_local - timedelta(hours=timezone_offset)
    chart = calculate_kundali(dt_utc, latitude, longitude)
    chart["seeker_name"] = name
    chart["engine_version"] = f"Kaalchakra Core v{__VERSION__}"
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
    """
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    res = calculate_panchanga(now_utc, latitude, longitude)
    res["engine_version"] = f"Kaalchakra Core v{__VERSION__}"
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
    """
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
    """
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
        )
    }

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
