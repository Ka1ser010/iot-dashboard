

import argparse
import math
import random
import time
import requests

SERVER_URL = "http://127.0.0.1:8000/readings/"


def generate_reading(step: int) -> dict:
    base_temp = 24 + 3 * math.sin(step / 10)
    base_humidity = 55 + 8 * math.sin(step / 15 + 1)

    temperature = round(base_temp + random.uniform(-0.4, 0.4), 1)
    humidity = round(base_humidity + random.uniform(-1.5, 1.5), 1)

    return {"temperature": temperature, "humidity": humidity}


def main():
    parser = argparse.ArgumentParser(description="Simula um ESP32 enviando leituras.")
    parser.add_argument("--count", type=int, default=20, help="Número de leituras a enviar")
    parser.add_argument("--interval", type=float, default=2.0, help="Segundos entre leituras")
    parser.add_argument("--url", type=str, default=SERVER_URL, help="URL do endpoint /readings/")
    args = parser.parse_args()

    print(f"ESP32 -> sending {args.count} readings to {args.url}\n")

    for step in range(args.count):
        reading = generate_reading(step)
        try:
            response = requests.post(args.url, json=reading, timeout=5)
            status = "OK" if response.status_code == 201 else f"error {response.status_code}"
            print(f"[{step + 1}/{args.count}] Temp={reading['temperature']}C "
                  f"Humidity={reading['humidity']}% -> {status}")
        except requests.exceptions.ConnectionError:
            print("Could not connect to the backend. Is it running? "
                  "(uvicorn app.main:app --reload)")
            return

        if step < args.count - 1:
            time.sleep(args.interval)

    print("\nSimulação concluída.")


if __name__ == "__main__":
    main()
