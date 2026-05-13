"""
Blackjack AI Agents — entry point.

Game flow:
  1. Build dealer agent (has draw_card tool).
  2. Create AI player agents (Alice, Bob, Carol) + human player.
  3. Each player takes their turn:
       - AI player: LLM decides hit/stand → asks dealer → dealer draws card.
       - Human player: freeform CLI input → asks dealer → dealer draws card.
  4. After all turns, determine and display winner.

Run:
    python main.py
"""

# TODO (feature/game-loop): wire everything together
#   1. Import and build dealer_agent via build_dealer_agent()
#   2. Create GameState with PlayerState for each player (3 AI + 1 human)
#   3. Loop through players, calling their turn functions
#   4. Print results and call determine_winner()


def main():
    print("=== Blackjack AI Agents ===")
    print("Game loop not yet implemented.")
    print("See TODO comments in main.py and each agents/ file.")


if __name__ == "__main__":
    main()
