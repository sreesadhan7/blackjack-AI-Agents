from agents.ai_player_agent import AIPlayerAgent
from agents.dealer_agent import build_dealer_agent
from agents.human_player import take_human_turn
from game.rules import determine_winner
from game.state import GameState, PlayerState

AI_PLAYERS = ["Alice", "Bob", "Carol"]


def _print_results(players: list[PlayerState], winner: PlayerState | None) -> None:
    print("\n" + "=" * 42)
    print("  FINAL RESULTS")
    print("=" * 42)
    for p in players:
        status = "BUST" if p.is_bust else str(p.total)
        marker = "  <-- WINNER" if winner and p.name == winner.name else ""
        print(f"  {p.name:<10}  cards={p.cards}  total={status}{marker}")
    print("=" * 42)
    if winner:
        print(f"  Winner: {winner.name} with {winner.total}!")
    else:
        print("  No winner — everyone busted!")
    print("=" * 42)


def main() -> None:
    print("=" * 42)
    print("   BLACKJACK — AI Agents")
    print("=" * 42)

    dealer = build_dealer_agent()

    game = GameState(players=[
        PlayerState(name="You", is_human=True),
        *[PlayerState(name=n) for n in AI_PLAYERS],
    ])

    ai_agents = {name: AIPlayerAgent(name) for name in AI_PLAYERS}

    for player in game.players:
        if player.is_human:
            take_human_turn(player, dealer)
        else:
            ai_agents[player.name].take_turn(player, dealer)

    winner = determine_winner(game.players)
    _print_results(game.players, winner)


if __name__ == "__main__":
    main()
