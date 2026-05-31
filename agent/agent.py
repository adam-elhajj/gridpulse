import time
from tinydb import TinyDB
import os

db_path = '/home/adamelhajj54321/gridpulse/gridpulse_db.json'

print("🧠 GridPulse AI Agent Online. Monitoring telemetry for anomalies...")

while True:
    if os.path.exists(db_path):
        db = TinyDB(db_path)
        data = db.table('telemetry').all()
        if data:
            temp = data[0].get('temperature', 0)
            if temp > 65.0:
                print(f"⚠️ [ALERT] Temp is {temp}°C! Triggering Emergency Relay Trip.")
            elif temp > 55.0:
                print(f"⚖️ [NOTICE] Temp is {temp}°C. Throttling power.")
            else:
                print(f"✅ [STATUS] Temp {temp}°C. Nominal.")
    time.sleep(2)
