# Blackjack AI Agents

A command-line Blackjack simulation using LangChain AI agents.

## Architecture

```
main.py                  ← game loop & orchestrator
├── agents/
│   ├── dealer_agent.py  ← only agent with draw_card tool (LangChain ReAct agent)
│   ├── ai_player_agent.py  ← 3 AI players (LLM decides hit/stand, asks dealer)
│   └── human_player.py  ← human turn via CLI input
├── game/
│   ├── state.py         ← PlayerState, GameState dataclasses
│   └── rules.py         ← bust check, winner logic
├── tools/
│   └── card_tools.py    ← draw_card() LangChain @tool (random 2–11)
└── config.py            ← LLM provider setup (OpenAI or Anthropic)
```

### How agents communicate

```
Human / AI player
      │  "Please draw a card for Alice"
      ▼
  Dealer Agent  ──uses tool──▶  draw_card("Alice")  ──▶  random int 2–11
      │
      ▼
  Returns: "I drew a 7 for Alice. Her total is now 14."
```

Players **cannot** call `draw_card` directly — all card drawing goes through the dealer.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API key
python main.py
```

## LangChain concepts used

| Concept | Where | What it does |
|---|---|---|
| `@tool` | `tools/card_tools.py` | Wraps a Python function so an LLM can call it |
| `create_react_agent` | `agents/dealer_agent.py` | Builds a ReAct agent (Reason → Act loop) |
| `AgentExecutor` | `agents/dealer_agent.py` | Runs the agent loop until a final answer |
| LCEL (`prompt \| llm`) | `agents/ai_player_agent.py` | Chains prompt + LLM into a single callable |

## Game rules

- Each player draws up to **3 cards**.
- Cards are worth their face value (2–11, no suits).
- Highest score **≤ 21** wins.
- All busts → no winner.
