import os
import logging
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger("llm_service")


def _require_env(*names: str) -> dict:
    values = {name: os.environ.get(name) for name in names}
    missing = [name for name, val in values.items() if not val]
    if missing:
        raise RuntimeError(
            f"LLMService init failed — missing required environment variable(s): {', '.join(missing)}"
        )
    return values


class LLMService:
    def __init__(self):
        env = _require_env("AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_KEY", "AZURE_OPENAI_DEPLOYMENT")

        self.client = OpenAI(
            base_url=env["AZURE_OPENAI_ENDPOINT"].rstrip("/") + "/",
            api_key=env["AZURE_OPENAI_KEY"],
        )
        self.deployment = env["AZURE_OPENAI_DEPLOYMENT"]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def _call_with_retry(self, messages: list[dict], temperature: float):
        return self.client.responses.create(
            model=self.deployment,
            input=messages,
            temperature=temperature,
        )

    def chat(self, messages: list[dict], temperature: float = 0.3) -> dict:
        try:
            response = self._call_with_retry(messages, temperature)
            usage = getattr(response, "usage", None)
            tokens_used = usage.total_tokens if usage else 0

            logger.info("llm_call_completed", extra={
                "tokens_used": tokens_used,
                "model": self.deployment
            })

            return {"text": response.output_text, "tokens_used": tokens_used}
        except Exception as e:
            logger.error(f"LLM call failed after retries: {e}")
            return {"text": "I'm having trouble processing that request right now.", "tokens_used": 0}

    def simple_ask(self, prompt: str) -> str:
        result = self.chat([{"role": "user", "content": prompt}])
        return result["text"]