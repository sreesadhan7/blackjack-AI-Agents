import random
from langchain_core.tools import tool


@tool
def draw_card(player_name: str) -> int:
    """Draw a card for the given player. Returns a random value between 2 and 11."""
    value = random.randint(2, 11)
    return value
