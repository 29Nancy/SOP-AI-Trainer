import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

key = os.getenv("GROQ_API_KEY")
if not key:
    print("ERROR: Key is None")
else:
    print(f"Key loaded OK: {key[:12]}...")

try:
    client = Groq(api_key=key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Say hello in one sentence."}],
        max_tokens=50,
    )
    print("API WORKS! Response:", response.choices[0].message.content)
except Exception as e:
    print(f"API FAILED: {str(e)}")