import time
import random
import json
from tinydb import TinyDB

# Path to your database
db = TinyDB('/home/adamelhajj54321/gridpulse/gridpulse_db.json')
telemetry_table = db.table('telemetry')

print("⚡ GridPulse Telemetry Simulator Started...")

try:
    while True:
        # Generate metrics
        voltage = round(random.uniform(238.0, 242.0), 2)
        current = round(random.uniform(31.0, 33.0), 2)
        power = round((voltage * current) / 1000, 2)
        
        # This will randomly hit up to 75.0, triggering your alerts
        temperature = round(random.uniform(40.0, 75.0), 1)

        # Write to DB
        telemetry_table.truncate()
        telemetry_table.insert({
            'voltage': voltage,
            'current': current,
            'power': power,
            'temperature': temperature
        })

        print(f"[LOG] Telemetry Updated -> {voltage}V | {current}A | {power}kW | {temperature}°C")
        time.sleep(1)
except KeyboardInterrupt:
    print("Simulator stopped.")
