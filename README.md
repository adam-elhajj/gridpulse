# GridPulse: Autonomous EVSE Monitoring & Fault Mitigation System

**GridPulse** is a high-availability telemetry monitoring and autonomous fault-mitigation framework designed for Electric Vehicle Supply Equipment (EVSE). Built as a decoupled, multi-process distributed system, GridPulse simulates real-world charging hardware, analyzes telemetry data for thermal anomalies, and executes automated safety protocols to ensure grid stability and infrastructure longevity.

## 🎯 Engineering Objectives
In modern EV charging networks, hardware failures caused by thermal runaway and voltage surges result in significant operational downtime. GridPulse was engineered to:

* **Decouple Data Production & Consumption:** Ensure the simulator remains independent from the decision-making agent.
* **Implement Autonomous Fault-Detection:** Utilize an AI-driven agent to move from "reactive monitoring" to "proactive mitigation."
* **Real-time Visualization:** Provide situational awareness for operators via a live-streamed dashboard.

## 🏗 System Architecture
The system employs a producer-consumer model to maximize scalability and fault isolation:

| Component | Technology | Responsibility |
| :--- | :--- | :--- |
| **Data Simulator** | Python/TinyDB | Generates high-fidelity electrical telemetry (Voltage/Current/Temp). |
| **Logic Agent** | Python | Analyzes data streams, identifies threshold breaches, and triggers relay logic. |
| **Dashboard** | Streamlit | Real-time diagnostic interface for system health monitoring. |

## 🚀 Key Technical Challenges Solved
* **Asynchronous Data Handling:** Managed concurrent read/write operations using a lightweight TinyDB document store, optimizing for edge-compute constraints.
* **Cross-Origin Networking:** Implemented robust WebSocket communication layers to bypass environment-specific origin restrictions in containerized deployments.
* **Modular Architecture:** Designed the agent and simulator as independent services, allowing for hot-swapping logic without system downtime.

## 🛠 Deployment Instructions
Ensure the environment is configured with Python 3.x.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/adam-elhajj/gridpulse.git](https://github.com/adam-elhajj/gridpulse.git)
   cd gridpulse
   ```
2. Initialize the Simulator:
   ```bash
   python3 simulator.py
3. Deploy the Agent:
   ```bash
   python3 agent/agent.py
4. Visualize Telemetry:
   ```bash
   streamlit run dashboard/app.py --server.enableCORS=false

## 🔋 Future Scalability
The current implementation serves as a functional MVP. Future iterations will focus on:
* **Cloud-Native Ingestion:** Migrating from local DB to MQTT/Kafka brokers for large-scale cluster data management.
* **Predictive Maintenance:** Integrating time-series machine learning models to predict component failure before threshold breaches occur.

---
*Developed for high-scale electrical infrastructure monitoring.*
   
      
