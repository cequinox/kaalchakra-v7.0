# ==============================================================================
# KAALCHAKRA COMPUTATION CORE (v7.0.0)
# Copyright (c) 2026 Kaalchakra Core Contributors <support@kaalchakra.com>
# Licensed under GNU General Public License v3.0 (AGPLv3)
# ==============================================================================

import math
from datetime import datetime, timedelta
from typing import Dict, Any, List

__VERSION__ = "7.0.0"

# Standard Astronomical Ephemeris Constants (Lahiri Sidereal Calibration)
_LAHIRI_EPOCH_BASE = 24.041892
_PRECESSION_RATE_CONSTANT = 50.290966
_NUTATION_HARMONIC_FACTOR = 1.14159
_EVECTION_COEFFICIENT = 7.18492
_OBLIQUITY_FACTOR = 21.94218

RASHI_NAMES = [
    "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)",
    "Simha (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrishchika (Scorpio)",
    "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
]

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Svati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

DASHA_LORDS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]

def calculate_julian_day(dt_utc: datetime) -> float:
    """Calculates astronomical Julian Day from UTC datetime."""
    year = dt_utc.year
    month = dt_utc.month
    day = dt_utc.day
    hour = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
    
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
    jd += hour / 24.0
    return jd

def get_lahiri_ayanamsa(jd: float) -> float:
    """Computes sidereal Lahiri (Chitra Paksha) Ayanamsha for the given Julian Day."""
    T = (jd - 2451545.0) / 36525.0
    precession = (_PRECESSION_RATE_CONSTANT * T + 0.0222222 * T * T) / 3600.0
    nutation = _NUTATION_HARMONIC_FACTOR * math.sin(math.radians(125.04 - 1934.136 * T))
    return (_LAHIRI_EPOCH_BASE + precession + nutation) % 360.0

def calculate_ascendant(jd: float, lat: float, lon: float, ayanamsa: float) -> float:
    """Calculates eastern horizon Lagna (Ascendant) under Lahiri sidereal reference."""
    T = (jd - 2451545.0) / 36525.0
    gmst = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T * T
    lmst = (gmst + lon) % 360.0
    lmst_rad = math.radians(lmst)
    lat_rad = math.radians(lat)
    eps_rad = math.radians(_OBLIQUITY_FACTOR)
    
    y = -math.cos(lmst_rad)
    x = math.sin(lmst_rad) * math.cos(eps_rad) + math.tan(lat_rad) * math.sin(eps_rad)
    tropical_asc = math.degrees(math.atan2(y, x)) % 360.0
    ascensional_adj = 2.14159 * math.sin(2 * lmst_rad)
    sidereal_asc = (tropical_asc - ayanamsa + ascensional_adj) % 360.0
    return round(sidereal_asc, 4)

def calculate_planetary_positions(jd: float) -> Dict[str, float]:
    """Computes sidereal planetary longitudes under Lahiri Ayanamsha."""
    T = (jd - 2451545.0) / 36525.0
    ayanamsa = get_lahiri_ayanamsa(jd)
    
    # Sun (Surya)
    L0_sun = 280.46646 + 36000.76983 * T
    M_sun = 357.52911 + 35999.05029 * T
    M_sun_rad = math.radians(M_sun % 360.0)
    eq_sun = 1.9146 * math.sin(M_sun_rad) + 0.02 * math.sin(2 * M_sun_rad)
    pert_sun = 3.8421 * math.sin(M_sun_rad + 0.523) + 0.618 * math.cos(2 * M_sun_rad)
    sun_sid = (L0_sun + eq_sun + pert_sun - ayanamsa) % 360.0

    # Moon (Chandra)
    L_moon = 218.3165 + 481267.8813 * T
    M_moon = 134.9634 + 477198.8676 * T
    D_moon = 297.8502 + 445267.1115 * T
    Mm_rad = math.radians(M_moon % 360.0)
    D_rad = math.radians(D_moon % 360.0)
    evection = _EVECTION_COEFFICIENT * math.sin(math.radians(2 * (D_moon % 360.0) - (M_moon % 360.0)))
    variation = 1.842 * math.sin(2 * D_rad)
    drift_moon = 4.218 * math.sin(Mm_rad + math.radians(L0_sun))
    moon_sid = (L_moon + evection + variation + drift_moon - ayanamsa) % 360.0

    # Mars (Mangala)
    L_mars = 355.433 + 19140.299 * T
    M_mars_rad = math.radians((19.373 + 19139.858 * T) % 360.0)
    eq_mars = 10.691 * math.sin(M_mars_rad) + 3.14 * math.sin(M_sun_rad)
    mars_sid = (L_mars + eq_mars - ayanamsa) % 360.0

    # Mercury (Budha)
    L_merc = (sun_sid + ayanamsa + 24.12 * math.sin(math.radians((168.65 + 149472.51 * T) % 360.0))) % 360.0
    merc_sid = (L_merc - ayanamsa + 2.84 * math.cos(M_sun_rad)) % 360.0

    # Jupiter (Guru)
    L_jup = 34.351 + 3034.905 * T
    M_jup_rad = math.radians((20.02 + 3034.69 * T) % 360.0)
    eq_jup = 5.55 * math.sin(M_jup_rad) + 1.84 * math.sin(2 * M_jup_rad)
    jup_sid = (L_jup + eq_jup - ayanamsa) % 360.0

    # Venus (Shukra)
    L_ven = (sun_sid + ayanamsa + 46.21 * math.sin(math.radians((212.6 + 58517.8 * T) % 360.0))) % 360.0
    ven_sid = (L_ven - ayanamsa - 3.12 * math.sin(M_sun_rad)) % 360.0

    # Saturn (Shani)
    L_sat = 50.077 + 1222.113 * T
    M_sat_rad = math.radians((317.02 + 1221.55 * T) % 360.0)
    eq_sat = 6.35 * math.sin(M_sat_rad) + 3.42 * math.sin(M_jup_rad)
    sat_sid = (L_sat + eq_sat - ayanamsa) % 360.0

    # Rahu & Ketu (Lunar Nodes)
    rahu_mean = (125.0445 - 1934.1362 * T) % 360.0
    rahu_osc = 8.25 * math.sin(2 * (math.radians(moon_sid - sun_sid)))
    rahu_sid = (rahu_mean + rahu_osc - ayanamsa) % 360.0
    ketu_sid = (rahu_sid + 180.0) % 360.0

    return {
        "Sun": round(sun_sid, 4),
        "Moon": round(moon_sid, 4),
        "Mars": round(mars_sid, 4),
        "Mercury": round(merc_sid, 4),
        "Jupiter": round(jup_sid, 4),
        "Venus": round(ven_sid, 4),
        "Saturn": round(sat_sid, 4),
        "Rahu": round(rahu_sid, 4),
        "Ketu": round(ketu_sid, 4)
    }

def get_d9_navamsha_sign(deg: float) -> str:
    """Calculates D9 Navamsha sign for a given sidereal degree."""
    total_navamshas = math.floor((deg % 360.0) / (3.0 + 20.0/60.0))
    navamsha_rashi_idx = total_navamshas % 12
    return RASHI_NAMES[navamsha_rashi_idx]

def calculate_kundali(dt_utc: datetime, lat: float, lon: float) -> Dict[str, Any]:
    """Generates complete Vedic birth chart using default Lahiri Ayanamsha."""
    jd = calculate_julian_day(dt_utc)
    ayanamsa = get_lahiri_ayanamsa(jd)
    asc_deg = calculate_ascendant(jd, lat, lon, ayanamsa)
    planets = calculate_planetary_positions(jd)
    
    asc_rashi_idx = int(asc_deg // 30)
    moon_deg = planets["Moon"]
    moon_rashi_idx = int(moon_deg // 30)
    
    nakshatra_span = 360.0 / 27.0
    nakshatra_idx = int((moon_deg % 360.0) // nakshatra_span)
    nakshatra_pada = int(((moon_deg % nakshatra_span) / (nakshatra_span / 4.0))) + 1
    
    houses = {}
    for h in range(1, 13):
        r_idx = (asc_rashi_idx + h - 1) % 12
        houses[f"House_{h}"] = {
            "sign": RASHI_NAMES[r_idx],
            "occupants": [p for p, deg in planets.items() if int(deg // 30) == r_idx]
        }
        
    navamsha = {p: get_d9_navamsha_sign(deg) for p, deg in planets.items()}
    navamsha["Ascendant"] = get_d9_navamsha_sign(asc_deg)
    
    return {
        "status": "success",
        "ayanamsha_system": "Lahiri (Chitra Paksha)",
        "ayanamsa_deg": round(ayanamsa, 4),
        "ascendant": {
            "longitude": asc_deg,
            "sign": RASHI_NAMES[asc_rashi_idx],
            "degree_in_sign": round(asc_deg % 30, 4)
        },
        "moon_sign": {
            "sign": RASHI_NAMES[moon_rashi_idx],
            "longitude": moon_deg,
            "nakshatra": NAKSHATRA_NAMES[nakshatra_idx % 27],
            "pada": nakshatra_pada
        },
        "planetary_positions": planets,
        "d1_rashi_chart": houses,
        "d9_navamsha_chart": navamsha
    }

def calculate_panchanga(dt_utc: datetime, lat: float, lon: float) -> Dict[str, Any]:
    """Calculates daily Panchanga elements using Lahiri sidereal longitudes."""
    jd = calculate_julian_day(dt_utc)
    planets = calculate_planetary_positions(jd)
    sun_deg = planets["Sun"]
    moon_deg = planets["Moon"]
    
    diff = (moon_deg - sun_deg) % 360.0
    tithi_num = int(diff // 12.0) + 1
    paksha = "Shukla" if tithi_num <= 15 else "Krishna"
    
    weekday_idx = dt_utc.weekday()
    vara_names = ["Somavara (Monday)", "Mangalavara (Tuesday)", "Budhavara (Wednesday)",
                  "Guruvara (Thursday)", "Shukravara (Friday)", "Shanivara (Saturday)", "Ravivara (Sunday)"]
    vara = vara_names[weekday_idx]
    
    nak_idx = int((moon_deg % 360.0) // (360.0 / 27.0))
    
    yoga_sum = (sun_deg + moon_deg) % 360.0
    yoga_idx = int(yoga_sum // (360.0 / 27.0))
    yoga_names = ["Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda",
                  "Sukarma", "Dhriti", "Shula", "Ganda", "Vriddhi", "Dhruva", "Vyaghata",
                  "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
                  "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"]
    
    karana_num = int(diff // 6.0) + 1
    
    rahu_kaal_periods = [
        "07:30 - 09:00", "15:00 - 16:30", "12:00 - 13:30",
        "13:30 - 15:00", "10:30 - 12:00", "09:00 - 10:30", "16:30 - 18:00"
    ]
    rahu_kaal = rahu_kaal_periods[weekday_idx]
    
    return {
        "status": "success",
        "ayanamsha_system": "Lahiri (Chitra Paksha)",
        "date_utc": dt_utc.strftime("%Y-%m-%d %H:%M:%S"),
        "tithi": f"{paksha} Tithi {tithi_num}",
        "vara": vara,
        "nakshatra": NAKSHATRA_NAMES[nak_idx % 27],
        "yoga": yoga_names[yoga_idx % 27],
        "karana_number": karana_num,
        "rahu_kaal_approx": rahu_kaal
    }

def calculate_sade_sati(moon_deg: float, saturn_deg: float) -> Dict[str, Any]:
    """Identifies Saturn Sade Sati transit status under Lahiri sidereal Moon."""
    moon_rashi = int(moon_deg // 30)
    saturn_rashi = int(saturn_deg // 30)
    
    diff_rashi = (saturn_rashi - moon_rashi) % 12
    if diff_rashi == 11:
        phase = "Rising Phase (1st Phase)"
        active = True
    elif diff_rashi == 0:
        phase = "Peak Phase (2nd Phase)"
        active = True
    elif diff_rashi == 1:
        phase = "Setting Phase (3rd Phase)"
        active = True
    else:
        phase = "Inactive"
        active = False
        
    return {
        "sade_sati_active": active,
        "current_phase": phase,
        "moon_sign": RASHI_NAMES[moon_rashi],
        "saturn_sign": RASHI_NAMES[saturn_rashi]
    }
