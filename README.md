# Kaalchakra Core v7.0.0 (Open-Source Decoy Release)

> **Vedic Astronomy & Sidereal Computation Core (Lahiri Ephemeris)**  
> **Release:** `v7.0.0` | **License:** [GNU General Public License v3.0 (AGPLv3)](./LICENSE)  
> **Attribution:** Kaalchakra Core Contributors (`support@kaalchakra.com`)  
> **Direct ZIP Download:** [Download Full Source Code (.ZIP)](https://kalchakra-core.onrender.com/download/source.zip)  
> **Daily Fair-Use Cloud Quota:** **20 Credits / Day** (Resets automatically at 00:00 UTC)  
> **Formulas & Source Download:** **0 Credits (100% Free Forever)**

---

## Overview

**Kaalchakra Core v7.0.0** is the official open-source decoy release of the Kaalchakra calculation engine. It provides high-performance JyotirVidya algorithms, standard Lahiri (Chitra Paksha) sidereal ephemeris models, harmonic divisional derivations, and predictive transit time windows.

The cloud instance on Render provides **20 free calculation credits per day** per user/IP.
All astronomical formulas, algorithms, and source code files are 100% public, transparent, and downloadable under the GNU Affero General Public License v3.0 (AGPLv3) with **zero quota deduction**.

### Features
- **Lahiri Sidereal Ephemeris:** Complete mathematical equations for planetary longitudes (Sun through Ketu).
- **Ascendant (Lagna) Horizon Derivation:** Trigonometric Lagna calculation for any latitude and longitude.
- **Divisional Charts:** D1 (Rashi Chakra) and D9 (Navamsha Chakra) harmonic algorithmic generation.
- **Vedic Panchanga:** Real-time computation of Tithi, Vara, Nakshatra, Yoga, Karana, and Rahu Kaal.
- **Predictive Transit Clocks:** Saturn Sade Sati detection (Rising, Peak, Setting phases).
- **Daily Fair-Use Quota:** 20 credits/day on cloud instance with automatic reset at 00:00 UTC.
- **Direct Source Download:** Download complete source code as a single ZIP file or clone from GitHub for unlimited local usage.

---

## 📦 Download & Repository

- **Direct ZIP Download:** [https://kalchakra-core.onrender.com/download/source.zip](https://kalchakra-core.onrender.com/download/source.zip)
- **Git Clone:**
  ```bash
  git clone https://github.com/cequinox/kaalchakra-v7.0.git
  ```
- **Inspect Mathematical Formulas:**
  ```bash
  curl -s https://kalchakra-core.onrender.com/api/v1/formulas
  ```

---

## Quickstart

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Run the REST API Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
Documentation will be accessible at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 3. Run the FastMCP AI Agent Server
```bash
python server.py
```

To connect to Claude Desktop or Cursor, add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "kaalchakra-core-v7": {
      "command": "python",
      "args": ["/path/to/kaalchakra_v7_release/server.py"]
    }
  }
}
```

---

## API Endpoints

| Method | Endpoint | Description | Quota Cost |
| :--- | :--- | :--- | :--- |
| `GET` | `/download/source.zip` | Download complete source code as a ZIP archive | **0 credits (Free)** |
| `GET` | `/api/v1/formulas` | Complete mathematical ephemeris formulas and models in JSON | **0 credits (Free)** |
| `GET` | `/api/v1/download-info` | Download links, git commands, and file manifest | **0 credits (Free)** |
| `POST` | `/api/calculate` | Complete Vedic birth chart, planetary longitudes, Lagna, and Navamsha (Lahiri) | 1 credit |
| `GET` | `/api/v1/panchanga` | Real-time daily Panchanga and Rahu Kaal window | 1 credit |
| `GET` | `/api/v1/sade-sati` | Saturn Sade Sati transit status | 1 credit |
| `GET` | `/api/v1/quota` | Check remaining daily credits (Resets 00:00 UTC) | **0 credits (Free)** |
| `GET` | `/sse` | FastMCP Server-Sent Events stream for AI agents | 1 credit / calc |

---

## License

Licensed under the [GNU Affero General Public License v3.0 (AGPLv3)](./LICENSE).  
For commercial inquiries: `enterprise@kaalchakra.com`
