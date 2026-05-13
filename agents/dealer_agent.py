from typing import NamedTuple

from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, ToolMessage

from config import get_llm
from tools.card_tools import draw_card

DEALER_SYSTEM_PROMPT = (
    "You are a Blackjack dealer. Draw cards for players only when explicitly asked.\n"
    "Always call draw_card with the exact player name from the request.\n"
    "Keep your response short: state the card value drawn."
)


class DrawResult(NamedTuple):
    message: str             # dealer's natural-language reply (for display)
    card_value: int | None   # None if the agent failed to draw a card


class DealerAgent:
    def __init__(self):
        llm = get_llm(temperature=0.1)
        self.agent = create_agent(
            model=llm,
            tools=[draw_card],
        )

    def handle_request(self, request: str) -> DrawResult:
        result = self.agent.invoke({"messages": [
            SystemMessage(content=DEALER_SYSTEM_PROMPT),
            ("human", request),
        ]})

        card_value: int | None = None
        for msg in result["messages"]:
            if isinstance(msg, ToolMessage) and msg.name == "draw_card":
                card_value = int(msg.content)
                break

        return DrawResult(message=result["messages"][-1].content, card_value=card_value)


def build_dealer_agent() -> DealerAgent:
    return DealerAgent()
