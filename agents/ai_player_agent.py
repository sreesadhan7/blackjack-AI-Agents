"""
AI Player Agent
---------------
Represents one AI-controlled player. Cannot call draw_card directly.
Instead it sends a natural-language request to the dealer agent.

LangChain concept used here:
  - A plain LLM call (ChatPromptTemplate + LLM) to decide hit or stand.
  - No tools — the player only reasons, never acts on card drawing itself.
"""

from langchain_core.prompts import ChatPromptTemplate

from config import get_llm
from game.state import PlayerState

# TODO (feature/ai-players): implement AI player decision loop
#   1. Build a ChatPromptTemplate: give the player its name, current cards,
#      total, and ask it to decide "hit" or "stand" with reasoning.
#   2. Chain: prompt | llm  (LangChain Expression Language / LCEL)
#   3. Parse the response to extract the decision.
#   4. If "hit", return a message string to send to the dealer agent,
#      e.g. "Please draw a card for Alice."
#   5. Repeat up to MAX_CARDS times or until player says "stand" / busts.


class AIPlayerAgent:
    def __init__(self, name: str):
        self.name = name

    def decide_action(self, player_state: PlayerState) -> str:
        raise NotImplementedError("Implement in feature/ai-players branch")
