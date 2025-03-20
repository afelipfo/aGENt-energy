from pathlib import Path

OPENAI_API_KEY = "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"
KEY_OWNER = "Felipe"

DEBUG = False

MAX_CHUNK_SIZE = 4

LLM_VERS = "gpt-4o-mini"

BASE_DIR = f"{Path(__file__).resolve().parent.parent}"

POPULATIONS_DIR = f"{BASE_DIR}/agent_bank/populations"
LLM_PROMPT_DIR = f"{BASE_DIR}/simulation_engine/prompt_template"