import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.anthropic import AnthropicChatCompletion

load_dotenv()


def build_kernel() -> Kernel:
    kernel = Kernel()
    kernel.add_service(
        AnthropicChatCompletion(
            ai_model_id=os.getenv("MODEL_ID", "claude-sonnet-4-6"),
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
    )
    return kernel


def get_model_id() -> str:
    load_dotenv()
    return os.getenv("MODEL_ID", "claude-sonnet-4-6")


def get_api_key() -> str:
    load_dotenv()
    return os.getenv("ANTHROPIC_API_KEY", "")
