# Manufacturing MES AI Agent

**An AI-powered manufacturing monitoring and downtime investigation prototype built with Python, FastAPI, SQLite, and OpenAI function calling.**

This project demonstrates how a Large Language Model (LLM) can be integrated with manufacturing execution system (MES) data to monitor production lines, analyze equipment downtime, investigate alarms, and identify affected production lots through natural-language queries.

The system uses **synthetic manufacturing data** and is designed as a proof of concept for AI-enabled manufacturing systems integration.

## Key Features

- **Production Line Monitoring:** Simulates 35 production lines with dynamically changing operational statuses.
- **Equipment Downtime Tracking:** Records downtime events, recovery timestamps, and downtime durations.
- **Equipment Alarm Simulation:** Generates equipment alarms with severity levels and links them to downtime incidents.
- **Production Lot Tracking:** Identifies production lots affected by equipment downtime and places them on hold.
- **REST API Integration:** Provides manufacturing data through FastAPI endpoints.
- **SQL-Based Investigation:** Uses relational database queries and SQL JOINs to connect downtime events, alarms, and production lots.
- **AI Agent with Function Calling:** Uses OpenAI's API to select appropriate tools, retrieve manufacturing data, and generate investigation summaries.
- **Natural-Language Interface:** Allows users to ask questions about production conditions without writing SQL queries.

## System Architecture

```text
                  Manufacturing Engineer
                           |
                  Natural Language Query
                           |
                           v
                 +--------------------+
                 |     AI Agent       |
                 |   OpenAI API       |
                 |  Function Calling  |
                 +--------------------+
                           |
                    HTTP Requests
                           |
                           v
                 +--------------------+
                 |    FastAPI         |
                 |    REST API        |
                 +--------------------+
                           |
                    SQL Queries
                           |
                           v
                 +--------------------+
                 |   SQLite Database  |
                 |--------------------|
                 | production_lines   |
                 | downtime_events    |
                 | equipment_alarms   |
                 | production_lots    |
                 +--------------------+
                           ^
                           |
                 +--------------------+
                 | Manufacturing      |
                 | Simulator          |
                 | Python             |
                 +--------------------+
```

The AI agent accesses manufacturing data through the API layer rather than connecting directly to the database.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development and manufacturing simulation |
| SQLite | Relational database for manufacturing records |
| SQL | Data aggregation, filtering, and incident investigation |
| FastAPI | REST API development |
| Uvicorn | ASGI application server |
| OpenAI API | LLM-based reasoning and function calling |
| HTTPX | HTTP communication between the agent and API |
| python-dotenv | Environment variable management |

## Project Structure

```text
MES_AI_Agent/
├── main.py
├── mes_agent.py
├── equipment_simulator.py
├── create_database.py
├── create_lines.py
├── create_manufacturing_tables.py
├── insert_data.py
├── investigate_downtime.py
├── query_equipment.py
├── test_openai.py
├── data/
│   └── mes.db                 # Generated locally
├── .env                       # Local API credentials
├── .gitignore
└── README.md
```

The SQLite database and `.env` file are excluded from version control.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/manufacturing-mes-ai-agent.git
cd manufacturing-mes-ai-agent
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn openai httpx python-dotenv
```

### 4. Configure the OpenAI API key

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
```

An OpenAI API key with available API credits is required for the AI agent.

**Never commit API keys or other credentials to GitHub.**

### 5. Initialize the database

Create the local database directory:

```bash
mkdir -p data
```

Run the database initialization scripts:

```bash
python create_database.py
python insert_data.py
python create_lines.py
python create_manufacturing_tables.py
```

These scripts create the SQLite database and populate the initial manufacturing records.

### 6. Start the REST API

In Terminal 1:

```bash
python -m uvicorn main:app --reload
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

### 7. Start the manufacturing simulator

In Terminal 2:

```bash
python equipment_simulator.py
```

The simulator continuously generates synthetic equipment downtime events, alarms, and production lot impacts.

### 8. Start the AI agent

In Terminal 3:

```bash
python mes_agent.py
```

Enter natural-language manufacturing questions in the terminal.

## Example Queries

The AI agent supports questions such as:

**Production monitoring**

```text
Which production lines are currently down?
```

**Active downtime investigation**

```text
Show me all active downtime events and their durations.
```

**Historical downtime analysis**

```text
Which production lines have experienced the most downtime?
```

**Equipment incident investigation**

```text
Investigate LINE-24 and summarize its recent downtime events.
```

**Maintenance investigation**

```text
Based on LINE-24's equipment alarms and downtime history,
what should the maintenance engineer investigate first?
```

The agent selects relevant tools, retrieves structured manufacturing data, and generates a response based on the available records.

## REST API Endpoints

| Endpoint | Description |
|---|---|
| `GET /equipment` | Retrieve equipment records |
| `GET /lines` | Retrieve production line statuses |
| `GET /downtime` | Retrieve recent downtime events |
| `GET /downtime/active` | Retrieve active downtime incidents |
| `GET /downtime/summary` | Retrieve aggregated downtime statistics |
| `GET /investigate/{line_id}` | Retrieve incident details, alarms, and affected lots |

## AI Agent Design

The AI agent uses OpenAI function calling to interact with manufacturing data through predefined tools.

The available tools are:

1. `get_production_lines`
2. `get_active_downtime`
3. `get_downtime_summary`
4. `investigate_production_line`

When a user submits a question, the LLM determines which tool is appropriate. The Python application executes the requested tool, retrieves data from FastAPI, and returns the result to the LLM.

The LLM then generates a natural-language response grounded in the retrieved manufacturing records.

This approach separates language-model reasoning from database access and business logic.

## Engineering Considerations

This project demonstrates several concepts relevant to manufacturing systems integration:

- **Separation of concerns:** Independent modules for simulation, database queries, APIs, and AI orchestration.
- **Data integrity:** Relational links between downtime events, alarms, and affected production lots.
- **API-based integration:** Structured communication between the AI agent and manufacturing data services.
- **Traceability:** Incident identifiers connect related manufacturing records.
- **Human-in-the-loop investigation:** The agent suggests investigation priorities without automatically changing equipment or production status.

## Current Limitations

This project is a local proof of concept rather than a production-ready MES application.

- Manufacturing data is simulated rather than collected from actual equipment or MES infrastructure.
- SQLite is used for local development rather than high-throughput industrial data processing.
- Equipment alarms are synthetic and do not establish confirmed failure causes.
- The agent does not perform automated equipment control or production release decisions.
- Production deployment would require authentication, authorization, monitoring, robust error handling, and additional data-quality controls.

## Potential Future Improvements

- Integration with real MES databases or equipment data interfaces.
- Real-time event streaming using Kafka or MQTT.
- Predictive maintenance using machine learning models.
- Anomaly detection using equipment sensor data.
- Manufacturing dashboards for downtime and equipment KPIs.
- Role-based access control, audit logging, and production monitoring.
- Deployment using containerized cloud infrastructure.

## Project Purpose

This project was developed to explore how AI agents can support manufacturing engineers by connecting natural-language interfaces with structured production data.

The primary focus is on **manufacturing systems integration, SQL-based data analysis, REST API development, and practical AI agent orchestration**, rather than training a custom language model.

The project demonstrates an approach to making manufacturing data more accessible while