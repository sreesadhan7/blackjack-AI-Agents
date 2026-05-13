"""
Human Player
------------
Reads commands from stdin and translates them into requests for the dealer.
Natural input like "deal me a card" or "hit" should be understood.
"""

from game.state import PlayerState
from game.rules import can_draw

# TODO (feature/human-player): implement human turn
#   1. Print current hand and total.
#   2. Accept freeform input ("hit", "deal me a card", "stand", "I'm good").
#   3. Use a small LLM call OR simple keyword matching to classify intent.
#   4. If hit: return request string for the dealer agent.
#   5. If stand / bust: end the human turn.


def take_human_turn(player_state: PlayerState, dealer_agent) -> None:
    raise NotImplementedError("Implement in feature/human-player branch")
