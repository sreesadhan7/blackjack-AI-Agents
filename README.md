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
config.py                    ← LLM provider (OpenAI, Anthropic, or Google Gemini)
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
cp .env.example .env        # add your API key and set LLM_PROVIDER
python main.py
```

Supported providers (set `LLM_PROVIDER` in `.env`):

| Provider | `LLM_PROVIDER` value | Model used |
|---|---|---|
| OpenAI | `openai` | `gpt-4o-mini` |
| Anthropic | `anthropic` | `claude-haiku-4-5` |
| Google Gemini | `google-genai` | `gemini-2.5-flash` |

## LangChain / LangGraph concepts used

| Concept | File | What it does |
|---|---|---|
| `@tool` | `tools/card_tools.py` | Wraps a Python function so an LLM can call it |
| `create_react_agent` (LangGraph) | `agents/dealer_agent.py` | ReAct loop: Thought → Action → Observation → Final Answer |
| `ToolMessage` | `agents/dealer_agent.py` | Carries the raw tool return value (card int) back through the message chain |
| LCEL `prompt \| llm \| parser` | `agents/ai_player_agent.py` | Chains prompt + LLM + output parser into one callable |
| `ChatPromptTemplate` | `agents/ai_player_agent.py` | Structured system + human message prompt |
| `StrOutputParser` | `agents/ai_player_agent.py` | Converts LLM response object to a plain string |

## Game rules

- Each player draws up to **3 cards**.
- Cards are worth their face value (random 2–11).
- Highest score **≤ 21** wins. All busts → no winner.
- Ties go to the player who acted first (turn order: You → Alice → Bob → Carol).
