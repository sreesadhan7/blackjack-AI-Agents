from agents.dealer_agent import DealerAgent
from game.rules import MAX_CARDS, can_draw
from game.state import PlayerState

_HIT_WORDS = {"hit", "draw", "card", "deal", "yes", "more", "give", "next"}
_STAND_WORDS = {"stand", "stop", "stay", "no", "pass", "enough", "done", "hold"}


def take_human_turn(player_state: PlayerState, dealer: DealerAgent) -> None:
    print("\n--- Your turn ---")

    while can_draw(player_state):
        print(f"  Your hand: {player_state.cards}  |  Total: {player_state.total}")
        print(f"  Cards you can still draw: {MAX_CARDS - player_state.card_count}")

        try:
            raw = input("  > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Standing.")
            break

        words = set(raw.split())

        if words & _STAND_WORDS or raw == "":
            print("  You stand.")
            break

        elif words & _HIT_WORDS:
            result = dealer.handle_request(f"Please draw a card for {player_state.name}.")
            if result.card_value is None:
                print("  Dealer couldn't draw. Try again.")
                continue
            player_state.cards.append(result.card_value)
            print(f"  Dealer drew {result.card_value}. New total: {player_state.total}")
            if player_state.is_bust:
                print("  You bust!")
                break

        else:
            print("  Say 'hit' / 'deal me a card' to draw, or 'stand' / 'stop' to hold.")

    if not player_state.is_bust and player_state.card_count == MAX_CARDS:
        print(f"  You've used all {MAX_CARDS} cards. Final total: {player_state.total}")
