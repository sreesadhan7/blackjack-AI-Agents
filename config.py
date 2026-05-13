import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")


def get_llm(temperature: float = 0.3):
    """Return the configured LLM instance."""
    if LLM_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model="claude-haiku-4-5-20251001", temperature=temperature)
    elif LLM_PROVIDER in ("google", "google-genai"):
        from langchain_core.rate_limiters import InMemoryRateLimiter
        from langchain_google_genai import ChatGoogleGenerativeAI
        # gemini-3.1-flash-lite free tier = 5 RPM. so added limiter at 4/min (1 per 15s)
        # to stay under API limit.
        rate_limiter = InMemoryRateLimiter(requests_per_second=4 / 60)
        return ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite",
            temperature=temperature,
            rate_limiter=rate_limiter,
        )
    else:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-4o-mini", temperature=temperature)
