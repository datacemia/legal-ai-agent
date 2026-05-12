import json
from typing import Any

from openai import OpenAI

from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def call_json_ai(
    prompt: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.1,
) -> dict[str, Any]:
    """
    Centralized OpenAI JSON caller.

    Keeps all model calls consistent and avoids duplicated OpenAI logic
    across the contract agent.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict JSON engine. "
                    "Return only valid JSON. Do not include markdown."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content or "{}"
    return json.loads(content)
