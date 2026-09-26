# IoT Dashboard — ESP32 Sensor (Temperature & Humidity)

A complete pipeline: ESP32 with a DHT22 sensor → FastAPI backend →
web dashboard with a real-time chart.

## Structure

```
firmware/
└── esp32_sensor.ino   # real firmware, flashed onto the ESP32 (Arduino IDE)
backend/
├── app/
│   ├── main.py          # API that receives and serves sensor readings
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── requirements.txt
└── simulate_esp32.py    # "virtual ESP32" — test everything without hardware
dashboard/
└── index.html            # opens directly in the browser, no extra server needed
```

## Try it right now, with no hardware at all

```bash
# 1. Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Start the backend
uvicorn app.main:app --reload
```

With the backend running, open **two** more terminals:

**Terminal 2** — open `dashboard/index.html` directly in the browser
(just double-click the file).

**Terminal 3** — run the virtual ESP32 to simulate incoming readings:
```bash
cd backend
python simulate_esp32.py
```

Back in the browser, the chart should start filling in on its own,
every few seconds, with realistic (but simulated) temperature and
humidity data.

## Using it with a real ESP32

1. Open `firmware/esp32_sensor.ino` in the Arduino IDE.
2. Install the libraries listed at the top of the file.
3. Replace `WIFI_SSID`, `WIFI_PASSWORD`, and `SERVER_URL` with your
   own values (`SERVER_URL` must point to the IP address of the
   computer running the backend on your local network — **do not**
   use `127.0.0.1` here, since that would point back at the ESP32
   itself).
4. Wire the circuit: DHT22 → VCC (3.3V), GND (GND), DATA (GPIO 4).
5. Flash the firmware and open the Serial Monitor (115200 baud) to
   watch the readings being sent.
6. The dashboard will now display real data instead of simulated
   data — no backend or dashboard code needs to change.

## Roadmap

- [x] Phase 1 — ESP32 reading the sensor + sending data over HTTP + basic dashboard
- [ ] Phase 2 — Replace HTTP with MQTT (closer to the industry standard)
- [ ] Phase 3 — Automatic alerts when readings cross a configurable threshold
- [ ] Phase 4 — Persist data in PostgreSQL (reusing the student-api project)
