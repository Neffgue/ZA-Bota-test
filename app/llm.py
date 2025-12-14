import asyncio

from openai import OpenAI


class OpenRouterClient:
    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        self._client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self._model = model

    async def complete(self, messages: list[dict], retries: int = 3) -> str:
        pause = 1.0
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(
                    self._client.chat.completions.create,
                    model=self._model,
                    messages=messages,
                )
                return (response.choices[0].message.content or "").strip()
            except Exception:
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(pause)
                pause *= 2
