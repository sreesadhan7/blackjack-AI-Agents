from typing import NamedTuple

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

from config import get_llm
from tools.card_tools import draw_card

# Required placeholders for create_react_agent:
#   {tools}            — formatted list of tool name + description
#   {tool_names}       — comma-separated tool names (used in "Action must be one of")
#   {input}            — the player's request message
#   {agent_scratchpad} — where the Thought/Action/Observation loop is appended
DEALER_PROMPT = PromptTemplate.from_template(
    "You are a Blackjack dealer. Draw cards for players only when explicitly asked.\n"
    "Always call draw_card with the exact player name from the request.\n"
    "Keep your Final Answer short: state the card value drawn.\n\n"
    "Available tools:\n{tools}\n\n"
    "Format to follow strictly:\n"
    "Question: the incoming request\n"
    "Thought: your reasoning\n"
    "Action: tool name — must be one of [{tool_names}]\n"
    "Action Input: the input for that tool\n"
    "Observation: the tool result\n"
    "Thought: what I now know\n"
    "Final Answer: your reply to the player\n\n"
    "Begin!\n\n"
    "Question: {input}\n"
    "Thought:{agent_scratchpad}"
)


class DrawResult(NamedTuple):
    message: str    # dealer's natural-language reply (for display)
    card_value: int  # raw int returned by draw_card (for game state)


class DealerAgent:
    def __init__(self):
        llm = get_llm(temperature=0.1)
        agent = create_react_agent(llm=llm, tools=[draw_card], prompt=DEALER_PROMPT)
        self.executor = AgentExecutor(
            agent=agent,
            tools=[draw_card],
            verbose=True,
            return_intermediate_steps=True,
            handle_parsing_errors=True,
            max_iterations=3,
        )

    def handle_request(self, request: str) -> DrawResult:
        result = self.executor.invoke({"input": request})

        card_value = 0
        for action, observation in result.get("intermediate_steps", []):
            if getattr(action, "tool", None) == "draw_card":
                card_value = int(observation)
                break

        return DrawResult(message=result["output"], card_value=card_value)


def build_dealer_agent() -> DealerAgent:
    return DealerAgent()
