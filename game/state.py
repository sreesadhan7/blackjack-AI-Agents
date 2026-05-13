from dataclasses import dataclass, field


@dataclass
class PlayerState:
    name: str
    cards: list[int] = field(default_factory=list)
    is_human: bool = False

    @property
    def total(self) -> int:
        return sum(self.cards)

    @property
    def is_bust(self) -> bool:
        return self.total > 21

    @property
    def card_count(self) -> int:
        return len(self.cards)


@dataclass
class GameState:
    players: list[PlayerState] = field(default_factory=list)
    current_turn: int = 0
    game_over: bool = False

    def get_player(self, name: str) -> PlayerState | None:
        return next((p for p in self.players if p.name == name), None)
