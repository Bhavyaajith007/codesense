from groq import Groq
from config import GROQ_API_KEY

# Configure Groq client
client = Groq(api_key=GROQ_API_KEY)

def ask_ai(prompt: str) -> str:
    """
    Sends a prompt to Groq and returns the response.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling Groq: {e}"


# Test it
if __name__ == "__main__":
    test_prompt = """
You are a code review expert. Review this Python code and list any bugs or issues:

def divide(a, b):
    return a / b

Be specific and concise.
"""
    print("=== GROQ RESPONSE ===")
    result = ask_ai(test_prompt)
    print(result)