"""A2A client for the PolicyAgent server.

Server must be running: `uv run python a2a_policy_agent.py`
Then: `uv run python a2a_policy_client.py "your question"`
"""

import asyncio
import os
import sys

import httpx
from a2a.client import Client, ClientConfig, ClientFactory, create_text_message_object
from a2a.types import Artifact, Message, Task
from a2a.utils.message import get_message_text
from dotenv import load_dotenv


async def ask(prompt: str) -> str:
    host = os.getenv("AGENT_HOST", "localhost")
    port = os.getenv("POLICY_AGENT_PORT", "9999")
    base_url = f"http://{host}:{port}"

    async with httpx.AsyncClient(timeout=100.0) as http:
        client: Client = await ClientFactory.connect(
            base_url, client_config=ClientConfig(httpx_client=http)
        )

        card = await client.get_card()
        print(f"→ Connected to: {card.name} ({card.url})")
        print(f"  Skills: {[s.id for s in card.skills]}\n")

        message = create_text_message_object(content=prompt)
        print(f"→ Sending: {prompt!r}\n")

        text = ""
        async for response in client.send_message(message):
            if isinstance(response, Message):
                text = get_message_text(response)
            elif isinstance(response, tuple):
                task: Task = response[0]
                if task.artifacts:
                    artifact: Artifact = task.artifacts[0]
                    text = get_message_text(artifact)

        return text


def main() -> None:
    load_dotenv(override=True)
    prompt = (
        sys.argv[1] if len(sys.argv) > 1 else "How much for mental health therapy?"
    )
    answer = asyncio.run(ask(prompt))
    print("─" * 60)
    print(answer)


if __name__ == "__main__":
    main()
