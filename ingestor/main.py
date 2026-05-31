import base64, json, os
from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime, timezone

app = Flask(__name__)
client = MongoClient(os.environ["MONGO_URI"])
db = client["gridpulse"]
col = db["telemetry_readings"]

@app.route("/ingest", methods=["POST"])
def ingest():
    envelope = request.get_json(silent=True)
    if not envelope:
        return "Bad Request", 400
    message = envelope.get("message", {})
    data = base64.b64decode(message.get("data", "")).decode("utf-8")
    payload = json.loads(data)
    payload["ingested_at"] = datetime.now(timezone.utc).isoformat()
    col.insert_one(payload)
    print(f"Successfully Ingested Telemetry for: {payload.get('station_id')}")
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
