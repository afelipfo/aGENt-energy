import openai

# Replace with your actual key from settings.py
openai.api_key = ""

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Match your settings.py LLM_VERS
        messages=[{"role": "user", "content": "Hello, can you hear me?"}]
    )
    print("API Response:", response.choices[0].message["content"])
except Exception as e:
    print("Error:", str(e))