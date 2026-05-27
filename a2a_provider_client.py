"""Microsoft Agent Framework A2A client for the HealthcareProviderAgent server.

Server must be running: `uv run python a2a_provider_agent.py`
Then: `uv run python a2a_provider_client.py "your question"`
"""

import asyncio
import os
import sys

from agent_framework.a2a import A2AAgent
from dotenv import load_dotenv


async def ask(prompt: str) -> str:
    host = os.getenv("AGENT_HOST", "localhost")
    port = os.getenv("PROVIDER_AGENT_PORT", "9997")
    base_url = f"http://{host}:{port}"

    agent = A2AAgent(
        name="HealthcareProviderAgent",
        url=base_url,
    )

    print(f"→ Connecting to: {base_url}")
    print(f"→ Sending: {prompt!r}\n")

    result = await agent.run(prompt)
    return result.text


def main() -> None:
    load_dotenv(override=True)
    prompt = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "I'm based in Austin, TX. Are there any Psychiatrists near me?"
    )
    answer = asyncio.run(ask(prompt))
    print("─" * 60)
    print(answer)


if __name__ == "__main__":
    main()
