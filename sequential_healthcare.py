"""Sequential workflow: research agent → policy agent → provider agent.

All servers must be running:
  Terminal 1: uv run python a2a_policy_agent.py
  Terminal 2: uv run python a2a_research_agent.py
  Terminal 3: uv run python a2a_provider_agent.py
Then: uv run python sequential_healthcare.py "your question"
"""

import asyncio
import logging
import os
import sys
import warnings

warnings.filterwarnings("ignore")
logging.getLogger("google.adk").setLevel(logging.ERROR)

from dotenv import load_dotenv
from google.adk.agents import SequentialAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.runners import InMemoryRunner

async def main(prompt: str) -> None:
    host = os.getenv("AGENT_HOST", "localhost")
    policy_port = os.getenv("POLICY_AGENT_PORT", "9999")
    research_port = os.getenv("RESEARCH_AGENT_PORT", "9998")
    provider_port = os.getenv("PROVIDER_AGENT_PORT", "9997")

    research_agent = RemoteA2aAgent(
        name="health_research_agent",
        agent_card=f"http://{host}:{research_port}",
    )
    policy_agent = RemoteA2aAgent(
        name="policy_agent",
        agent_card=f"http://{host}:{policy_port}",
    )
    provider_agent = RemoteA2aAgent(
        name="provider_agent",
        agent_card=f"http://{host}:{provider_port}",
    )

    root_agent = SequentialAgent(
        name="root_agent",
        description="Healthcare Routing Agent",
        sub_agents=[research_agent, policy_agent, provider_agent],
    )

    runner = InMemoryRunner(root_agent)
    for event in await runner.run_debug(prompt, quiet=True):
        if event.is_final_response() and event.content:
            print(event.content.parts[0].text)


if __name__ == "__main__":
    load_dotenv(override=True)
    q = sys.argv[1] if len(sys.argv) > 1 else "How can I get mental health therapy?"
    asyncio.run(main(q))
