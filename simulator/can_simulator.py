import json, random, time, os
from datetime import datetime, timezone
from google.cloud import pubsub_v1

PROJECT_ID = os.environ.get("PROJECT_ID")
TOPIC_ID = "ev-telemetry-raw"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
STATIONS = [f"EVSE-{i:03d}" for i in range(1, 6)]

def generate_telemetry(station_id):
    fault = random.random() < 0.05
    return {
        "station_id": station_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "voltage_v": random.uniform(380, 420) if not fault else random.uniform(200, 340),
        "current_a": random.uniform(0, 32),
        "soc_pct": random.uniform(10, 100),
        "temp_c": random.uniform(20, 45) if not fault else random.uniform(65, 90),
        "fault_code": "F001_OVERHEAT" if fault and random.random() > 0.5 else ("F002_UNDERVOLT" if fault else None),
        "power_kw": random.uniform(0, 11),
        "session_active": random.choice([True, False])
    }

def publish_loop():
    print(f"Simulator streaming data to {topic_path}... Press Ctrl+C to stop.")
    while True:
        for station in STATIONS:
            payload = generate_telemetry(station)
            data = json.dumps(payload).encode("utf-8")
            publisher.publish(topic_path, data, station_id=station)
            print(f"→ Published: {station} | V={payload['voltage_v']:.1f}V | Temp={payload['temp_c']:.1f}C | Fault={payload['fault_code']}")
        time.sleep(2.0)

if __name__ == "__main__":
    publish_loop()
