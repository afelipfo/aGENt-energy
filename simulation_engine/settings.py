from pathlib import Path

OPENAI_API_KEY = ""
KEY_OWNER = "Felipe"

DEBUG = True

MAX_CHUNK_SIZE = 4

LLM_VERS = "gpt-3.5-turbo"

BASE_DIR = f"{Path(__file__).resolve().parent.parent}"

POPULATIONS_DIR = f"{BASE_DIR}/agent_bank/populations"
LLM_PROMPT_DIR = f"{BASE_DIR}/simulation_engine/prompt_template"