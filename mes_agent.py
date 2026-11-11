
import os
import json
import httpx

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

MES_API_URL = "http://127.0.0.1:8000"
MODEL = "gpt-4.1-mini"

def get_production_lines(status=None):

    params = {}

    if status:
        params["status"] = status

    response = httpx.get(
        f"{MES_API_URL}/lines",
        params=params,
        timeout=10.0
    )

    response.raise_for_status()

    return response.json()

def get_active_downtime():
    response = httpx.get(
        f"{MES_API_URL}/downtime/active",
        timeout=10.0
    )

    response.raise_for_status()
    return response.json()


def get_downtime_summary():
    response = httpx.get(
        f"{MES_API_URL}/downtime/summary",
        timeout=10.0
    )

    response.raise_for_status()
    return response.json()

tools = [
    {
        "type": "function",
        "name": "get_production_lines",
        "description": (
            "Get current production line statuses. "
            "Use this to find which lines are RUNNING or DOWN."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": ["string", "null"],
                    "enum": ["RUNNING", "DOWN", None],
                    "description": "Filter by status, or null for all lines."
                }
            },
            "required": ["status"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_active_downtime",
        "description": (
            "Get currently DOWN production lines and "
            "how long each has been down."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_downtime_summary",
        "description": (
            "Get historical downtime event counts, "
            "total completed downtime, and average "
            "completed downtime for each line. "
            "Active downtime durations are excluded."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    },

    {
    "type": "function",
    "name": "investigate_production_line",
    "description": (
        "Investigate downtime incidents for a specific "
        "production line. Returns downtime events, "
        "equipment alarms, alarm severity, and affected "
        "production lots. Use this tool when asked why "
        "a line stopped, what alarms occurred, or which "
        "production lots were affected. Alarm data is "
        "evidence, not a confirmed root cause."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "line_id": {
                "type": "string",
                "description": (
                    "Production line ID, for example LINE-24"
                )
            }
        },
        "required": ["line_id"],
        "additionalProperties": False
    },
    "strict": True
    }

]

def investigate_production_line(line_id):
    line_id = line_id.strip().upper()

    response = httpx.get(
        f"{MES_API_URL}/investigate/{line_id}",
        timeout=10.0
    )

    response.raise_for_status()

    return response.json()



def ask_agent(question):

    INVESTIGATION_INSTRUCTIONS = """
    You are a manufacturing systems investigation assistant
    working with a simulated semiconductor MES.

    Always use available tools to retrieve current manufacturing
    data. Never invent downtime events, alarms, lot IDs, or metrics.

    When investigating a production line:
    1. Identify the relevant downtime event and its status.
    2. Report the equipment alarm code and severity, if available.
    3. Identify affected production lots, if available.
    4. Explain possible causes based on the available evidence.
    5. Recommend practical investigation steps for engineers.

    An equipment alarm is not proof of the root cause.
    Clearly distinguish observed facts from hypotheses.

    If data is missing, state that it is unavailable.
    Do not claim a line is currently down based solely on
    a historical downtime event.
    """ 

    input_messages = [
        {"role": "user", "content": question}
    ]

    max_rounds = 5

    for round_number in range(max_rounds):

        response = client.responses.create(
            model=MODEL,
            instructions=INVESTIGATION_INSTRUCTIONS,
            tools=tools,
            input=input_messages
        )

        input_messages.extend(response.output)

        tool_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        # No more tools needed: return the answer
        if not tool_calls:
            return response.output_text

        # Execute every tool requested by the model
        for item in tool_calls:

            arguments = json.loads(item.arguments)

            print(
                f"[TOOL CALLED] {item.name}: {arguments}"
            )

            try:
                if item.name == "get_production_lines":
                    result = get_production_lines(
                        arguments.get("status")
                    )

                elif item.name == "get_active_downtime":
                    result = get_active_downtime()

                elif item.name == "get_downtime_summary":
                    result = get_downtime_summary()

                elif item.name == "investigate_production_line":
                    result = investigate_production_line(
                        arguments["line_id"]
                    )
                else:
                    result = {
                        "error": f"Unknown tool: {item.name}"
                    }

            except (httpx.HTTPError, ValueError) as error:
                result = {
                    "error": str(error)
                }

            input_messages.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(result)
            })

    return (
        "Unable to complete the request within "
        "the maximum number of tool-calling rounds."
    )


if __name__ == "__main__":

    print("MES-AI Agent started!")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        try:
            answer = ask_agent(question)
            print(f"\nAI Agent: {answer}\n")

        except Exception as e:
            print(f"\nError: {e}\n")

