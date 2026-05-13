# Blackjack AI Agents

A command-line Blackjack simulation using LangChain AI agents (Python 3.12+).

## How it works

```
You (human)          type "hit" / "deal me a card" / "stand"
Alice / Bob / Carol  LLM decides hit or stand each turn
        │
        │  natural-language request: "Please draw a card for Alice."
        ▼
  Dealer Agent  ── draw_card tool ──▶  random int 2–11
        │
        ▼
  DrawResult(message="I drew a 7 for Alice.", card_value=7)
```

Players **cannot** call `draw_card` directly — all card drawing goes through the dealer agent.

## Project structure

```
main.py                      ← game loop & results display
config.py                    ← LLM provider (OpenAI or Anthropic)
agents/
  dealer_agent.py            ← ReAct agent with draw_card tool
  ai_player_agent.py         ← LCEL chain decides hit/stand per turn
  human_player.py            ← CLI input with keyword matching
game/
  state.py                   ← PlayerState, GameState dataclasses
  rules.py                   ← bust check, winner logic
tools/
  card_tools.py              ← draw_card() LangChain @tool (random 2–11)
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env        # add your API key
python main.py
```

## LangChain concepts used

| Concept | File | What it does |
|---|---|---|
| `@tool` | `tools/card_tools.py` | Wraps a Python function so an LLM can call it |
| `create_react_agent` | `agents/dealer_agent.py` | ReAct loop: Thought → Action → Observation → Final Answer |
| `AgentExecutor` | `agents/dealer_agent.py` | Runs the loop, executes tool calls, stops at Final Answer |
| `return_intermediate_steps` | `agents/dealer_agent.py` | Exposes raw tool output so we get the int without parsing text |
| LCEL `prompt \| llm \| parser` | `agents/ai_player_agent.py` | Chains prompt + LLM + output parser into one callable |
| `ChatPromptTemplate` | `agents/ai_player_agent.py` | Structured system + human message prompt |

## Game rules

- Each player draws up to **3 cards**.
- Cards are worth their face value (random 2–11).
- Highest score **≤ 21** wins. All busts → no winner.
