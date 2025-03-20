import openai
from simulation_engine.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
try:
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Return a JSON object: {'test': 'success'}" }],
        response_format={"type": "json_object"}
    )
    print("API Response:", response.choices[0].message.content)
except Exception as e:
    print("API Error:", str(e))