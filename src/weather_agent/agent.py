from .constants import MAX_TURNS, MAX_TOKENS
from .provider_client import get_client_and_model
from .prompts import build_system_prompt
from .schemas import TOOL_MENU
from .tools import TOOL_FUNCTIONS
import json

def run_agent_turns(messages: list, max_turns: int = MAX_TURNS) -> str:
    client, model, _ = get_client_and_model()

    working = [
        {
            "role": "system",
            "content": build_system_prompt(),
        },
        *messages
    ]

    for _ in range(max_turns):
        response = client.chat.completions.create(
            model=model,
            messages=working,
            tools=TOOL_MENU,
            max_tokens=MAX_TOKENS,
        )

        message = response.choices[0].message

        if not message.tool_calls:
            answer = message.content or ""
            messages.append({
                "role": "assistant",
                "content": answer
            })
            return answer

        # make a tool call
        working.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": json.dumps(call.function.arguments)
                    }
                } for call in message.tool_calls
            ]
        })

        # make actual tool call
        for call in message.tool_calls:
            name = call.function.name
            if name not in TOOL_FUNCTIONS:
                result = f"Unknown tool: {name}"

            else:
                arguments = json.loads(call.function.arguments)
                tool_result = TOOL_FUNCTIONS[name](**arguments) #make the actual tool call

            working.append({
                "role": "tool",
                "content": str(tool_result),
                "tool_call_id": call.id,
            })

    fallback = "Stopped after hitting the max_turns without a final answer"
    messages.append({
        "role": "assistant",
        "content": fallback
    })
    return fallback