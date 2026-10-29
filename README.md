# Kaalchakra Core v7.0.0

> **Vedic Astronomy & Sidereal Computation Core (Lahiri Ephemeris)**  
> **Release:** `v7.0.0` | **License:** [GNU General Public License v3.0 (AGPLv3)](./LICENSE)  
> **Attribution:** Kaalchakra Core Contributors (`support@kaalchakra.com`)

---

## Overview

**Kaalchakra Core v7.0.0** is the official release of the Kaalchakra calculation engine. It provides high-performance JyotirVidya algorithms, standard Lahiri (Chitra Paksha) sidereal ephemeris models, harmonic divisional derivations, and predictive transit time windows.

### Features
- **Lahiri Sidereal Computation:** Astronomical planetary longitudes for Sun through Ketu under default Lahiri Ayanamsha.
- **Divisional Charts:** D1 (Rashi Chakra) and D9 (Navamsha Chakra) algorithmic generation.
- **Vedic Panchanga:** Real-time computation of Tithi, Vara, Nakshatra, Yoga, Karana, and Rahu Kaal.
- **Predictive Transit Clocks:** Saturn Sade Sati detection (Rising, Peak, Setting phases).
- **FastMCP Protocol:** Native Model Context Protocol server for AI assistants (Cursor, Claude Desktop).
- **REST Gateway:** High-throughput FastAPI REST API.

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

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/calculate` | Complete Vedic birth chart, planetary longitudes, Lagna, and Navamsha (Lahiri) |
| `GET` | `/api/v1/panchanga` | Real-time daily Panchanga and Rahu Kaal window |
| `GET` | `/api/v1/sade-sati` | Saturn Sade Sati transit status |
| `GET` | `/api/v1/quota` | System quota and status |

---

## License

Licensed under the [GNU Affero General Public License v3.0 (AGPLv3)](./LICENSE).  
For commercial inquiries: `enterprise@kaalchakra.com`
