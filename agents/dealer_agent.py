"""
Dealer Agent
------------
The only agent with access to draw_card tool.
All players must ask the dealer to draw cards on their behalf.

LangChain concept used here:
  - create_react_agent: wraps an LLM + tools into an agent that can reason
    ("ReAct" = Reasoning + Acting) and decide when to call a tool.
  - AgentExecutor: runs the agent loop until it reaches a final answer.
"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

from config import get_llm
from tools.card_tools import draw_card

# TODO (feature/dealer-agent): build the dealer agent
#   1. Create a PromptTemplate with instructions: dealer only draws when asked,
#      must state the card value and new total.
#   2. Call create_react_agent(llm, tools=[draw_card], prompt=prompt)
#   3. Wrap in AgentExecutor(agent=..., tools=[draw_card], verbose=True)
#   4. Expose a handle_request(request: str, player_name: str) -> str method


def build_dealer_agent() -> AgentExecutor:
    raise NotImplementedError("Implement in feature/dealer-agent branch")
