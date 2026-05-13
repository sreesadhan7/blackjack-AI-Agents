from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from agents.dealer_agent import DealerAgent
from config import get_llm
from game.rules import MAX_CARDS, can_draw
from game.state import PlayerState


class AIPlayerAgent:
    def __init__(self, name: str):
        self.name = name
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are {name}, a Blackjack player. Make smart decisions.\n"
             "Rules: draw up to 3 cards total, bust if total exceeds 21.\n"
             "Respond with exactly one word: 'hit' or 'stand'."),
            ("human",
             "Your hand: {cards}\nTotal: {total}\nCards you can still draw: {cards_left}\nDecision?"),
        ])
        self.chain = prompt | get_llm(temperature=0) | StrOutputParser()

    def take_turn(self, player_state: PlayerState, dealer: DealerAgent) -> None:
        print(f"\n--- {self.name}'s turn ---")

        while can_draw(player_state):
            print(f"  Hand: {player_state.cards}  |  Total: {player_state.total}")

            raw = self.chain.invoke({
                "name": self.name,
                "cards": player_state.cards,
                "total": player_state.total,
                "cards_left": MAX_CARDS - player_state.card_count,
            }).strip().lower()
            decision = raw.split()[0].strip(".,!?;:\"'()[]{}") if raw else "stand"

            print(f"  {self.name} decides: {decision}")

            if not decision.startswith("hit"):
                print(f"  {self.name} stands.")
                break

            result = dealer.handle_request(f"Please draw a card for {self.name}.")
            if result.card_value is None:
                print(f"  Dealer failed to draw. {self.name} stands.")
                break

            player_state.cards.append(result.card_value)
            print(f"  Dealer drew {result.card_value}. New total: {player_state.total}")

            if player_state.is_bust:
                print(f"  {self.name} busts!")
                break

        if not player_state.is_bust and player_state.card_count == MAX_CARDS:
            print(f"  {self.name} reached the card limit. Final total: {player_state.total}")
