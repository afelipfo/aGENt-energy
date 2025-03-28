import openai
import time
import base64
from typing import List, Union

from simulation_engine.settings import *

openai.api_key = OPENAI_API_KEY


# ============================================================================
# #######################[SECTION 1: HELPER FUNCTIONS] #######################
# ============================================================================

def print_run_prompts(prompt_input: Union[str, List[str]], 
                      prompt: str, 
                      output: str) -> None:
  print (f"=== START =======================================================")
  print ("~~~ prompt_input    ----------------------------------------------")
  print (prompt_input, "\n")
  print ("~~~ prompt    ----------------------------------------------------")
  print (prompt, "\n")
  print ("~~~ output    ----------------------------------------------------")
  print (output, "\n") 
  print ("=== END ==========================================================")
  print ("\n\n\n")


def generate_prompt(prompt_input: Union[str, List[str]], 
                    prompt_lib_file: str) -> str:
  """Generate a prompt by replacing placeholders in a template file with 
     input."""
  if isinstance(prompt_input, str):
    prompt_input = [prompt_input]
  prompt_input = [str(i) for i in prompt_input]

  with open(prompt_lib_file, "r") as f:
    prompt = f.read()

  for count, input_text in enumerate(prompt_input):
    prompt = prompt.replace(f"!<INPUT {count}>!", input_text)

  if "<commentblockmarker>###</commentblockmarker>" in prompt:
    prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]

  return prompt.strip()


# ============================================================================
# ####################### [SECTION 2: SAFE GENERATE] #########################
# ============================================================================

def gpt_request(prompt: str, 
                model: str = "gpt-4o", 
                max_tokens: int = 1500) -> str:
  """Make a request to OpenAI's GPT model."""
  if model == "o1-preview": 
    try:
      client = openai.OpenAI(api_key=OPENAI_API_KEY)
      response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
      )
      return response.choices[0].message.content
    except Exception as e:
      return f"GENERATION ERROR: {str(e)}"

  try:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
      model=model,
      messages=[{"role": "user", "content": prompt}],
      max_tokens=max_tokens,
      temperature=0.7
    )
    return response.choices[0].message.content
  except Exception as e:
    return f"GENERATION ERROR: {str(e)}"


def gpt4_vision(messages: List[dict], max_tokens: int = 1500) -> str:
  """Make a request to OpenAI's GPT-4 Vision model."""
  try:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
      model="gpt-4o",
      messages=messages,
      max_tokens=max_tokens,
      temperature=0.7
    )
    return response.choices[0].message.content
  except Exception as e:
    return f"GENERATION ERROR: {str(e)}"


def chat_safe_generate(prompt_input: Union[str, List[str]], 
                       prompt_lib_file: str,
                       gpt_version: str = "gpt-4o", 
                       repeat: int = 1,
                       fail_safe: str = "error", 
                       func_clean_up: callable = None,
                       verbose: bool = False,
                       max_tokens: int = 1500,
                       file_attachment: str = None,
                       file_type: str = None) -> tuple:
    """Generate a response using GPT models with error handling & retries."""
    import base64
    import time
    from simulation_engine.settings import DEBUG  # Ensure DEBUG is imported

    if file_attachment and file_type:
        prompt = generate_prompt(prompt_input, prompt_lib_file)
        messages = [{"role": "user", "content": prompt}]

        if file_type.lower() == 'image':
            with open(file_attachment, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please refer to the attached image."},
                    {"type": "image_url", "image_url": 
                     {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            })
            response = gpt4_vision(messages, max_tokens)  # Assuming this is defined elsewhere

        elif file_type.lower() == 'pdf':
            pdf_text = extract_text_from_pdf_file(file_attachment)  # Assuming this is defined
            pdf = f"PDF attachment in text-form:\n{pdf_text}\n\n"
            instruction = generate_prompt(prompt_input, prompt_lib_file)
            prompt = f"{pdf}"
            prompt += f"<End of the PDF attachment>\n=\nTask description:\n{instruction}"
            response = gpt_request(prompt, gpt_version, max_tokens)  # Assuming this is defined

    else:
        prompt = generate_prompt(prompt_input, prompt_lib_file)
        messages = [{"role": "user", "content": prompt}]
        for i in range(repeat):
            try:
                # Use chat_completion_with_backoff or direct API call for openai==0.28.0
                response = chat_completion_with_backoff(messages=messages, model=gpt_version, max_tokens=max_tokens)
                print("Raw API Response:", response)  # Debug: Log raw response
                if response and response != "GENERATION ERROR":
                    break
            except Exception as e:
                print(f"API Call Failed (Attempt {i+1}/{repeat}):", str(e))
                response = "GENERATION ERROR"
            time.sleep(2**i)
        else:
            response = fail_safe
            print("All retries failed, returning fail_safe:", fail_safe)

    # Ensure response is not None before passing to func_clean_up
    if func_clean_up:
        if response is None or response == "GENERATION ERROR":
            print("Warning: Response is None or errored before cleanup:", response)
            response = fail_safe
        else:
            try:
                response = func_clean_up(response, prompt=prompt)
            except Exception as e:
                print("Cleanup failed:", str(e))
                response = fail_safe

    if verbose or DEBUG:
        print_run_prompts(prompt_input, prompt, response)

    return response, prompt, prompt_input, fail_safe


def chat_completion_with_backoff(messages, model, max_tokens=1500):
    """Helper function for retries with exponential backoff (for openai==0.28.0)."""
    import openai
    from simulation_engine.settings import OPENAI_API_KEY
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )
        return response.choices[0].message["content"]  # Extract content for old API
    except Exception as e:
        print("Chat completion error:", str(e))
        return "GENERATION ERROR"


# ============================================================================
# #################### [SECTION 3: OTHER API FUNCTIONS] ######################
# ============================================================================

def get_text_embedding(text: str, 
                       model: str = "text-embedding-3-small") -> List[float]:
  """Generate an embedding for the given text using OpenAI's API."""
  if not isinstance(text, str) or not text.strip():
    raise ValueError("Input text must be a non-empty string.")

  text = text.replace("\n", " ").strip()
  response = openai.embeddings.create(
    input=[text], model=model).data[0].embedding
  return response









