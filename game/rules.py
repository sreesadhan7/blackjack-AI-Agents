from game.state import PlayerState


MAX_CARDS = 3
BUST_THRESHOLD = 21


def can_draw(player: PlayerState) -> bool:
    """Return True if the player is allowed to draw another card."""
    return player.card_count < MAX_CARDS and not player.is_bust


def determine_winner(players: list[PlayerState]) -> PlayerState | None:
    """Return the player with the highest score at or under 21, or None if all bust."""
    valid = [p for p in players if not p.is_bust]
    if not valid:
        return None
    return max(valid, key=lambda p: p.total)
