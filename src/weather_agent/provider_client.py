from dataclasses import dataclass
from .config import GROQ_API_KEY
from openai import OpenAI
import os

@dataclass(frozen=True)
class Provider:
    name: str
    env_var: str
    base_url: str
    model:str

PROVIDERS = [
    Provider(
        name = "Groq",
        env_var = "GROQ_API_KEY",
        base_url = "https://api.groq.com/openai/v1",
        model = "openai/gpt-oss-20b"
    )
]

def select_provider() -> Provider:
    for provider in PROVIDERS:
        if os.getenv(provider.env_var):
            return provider

    raise RuntimeError("No provider found")

def get_client_and_model() -> tuple[OpenAI, str, Provider]:
    provider = select_provider()
    api_key = os.getenv(provider.env_var)

    client = OpenAI(
        api_key=api_key,
        base_url=provider.base_url
    )

    return client, provider.model, provider