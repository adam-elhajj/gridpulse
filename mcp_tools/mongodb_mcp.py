import os
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta

client = MongoClient(os.environ["MONGO_URI"])
db = client["gridpulse"]

def query_telemetry(station_id=None, minutes=10):
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    query = {"ingested_at": {"$gte": cutoff.isoformat()}}
    if station_id:
        query["station_id"] = station_id
    return list(db["telemetry_readings"].find(query, {"_id": 0}))

def detect_anomalies(readings):
    anomalies = []
    for r in readings:
        issues = []
        if r.get("voltage_v", 400) < 350:
            issues.append(f"UNDERVOLT: {r['voltage_v']:.1f}V")
        if r.get("temp_c", 25) > 60:
            issues.append(f"OVERHEAT: {r['temp_c']:.1f}C")
        if r.get("fault_code"):
            issues.append(f"FAULT CODE DETECTED: {r['fault_code']}")
        if issues:
            anomalies.append({
                "station_id": r.get("station_id"),
                "timestamp": r.get("timestamp"),
                "issues": issues
            })
    return anomalies

def write_fault_event(station_id, issues, agent_recommendation):
    doc = {
        "station_id": station_id,
        "detected_at": datetime.now(timezone.utc).isoformat(),
        "issues": issues,
        "agent_recommendation": agent_recommendation,
        "status": "open"
    }
    result = db["fault_events"].insert_one(doc)
    return str(result.inserted_id)

def trigger_remediation(station_id, action):
    allowed = {"LOAD_SHED", "SOFT_RESET", "ISOLATE", "ALERT_OPERATOR"}
    if action not in allowed:
        return {"error": f"Unknown action: {action}"}
    doc = {
        "station_id": station_id,
        "action": action,
        "triggered_at": datetime.now(timezone.utc).isoformat()
    }
    db["agent_actions"].insert_one(doc)
    print(f"REMEDIATION EXECUTED: {action} -> {station_id}")
    return {"status": "dispatched", "action": action, "station": station_id}
