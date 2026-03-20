from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
import os
from config import GROQ_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY if GROQ_API_KEY else ""


# --- Structured Output Schema ---
class ErrorExplanation(BaseModel):
    error_type: str           # e.g. "ZeroDivisionError"
    plain_english: str        # what went wrong in simple terms
    root_cause: str           # why it happened
    fix: str                  # exact fix with code
    prevention: str           # how to avoid this in future

# --- The Agent ---
model = GroqModel("llama-3.3-70b-versatile")

error_agent = Agent(
    model=model,
    output_type=ErrorExplanation,
    system_prompt="""
    You are a Python debugging expert who explains errors clearly.
    
    When given a Python traceback:
    - Identify the exact error type
    - Explain what went wrong in plain simple English
      (imagine explaining to a beginner)
    - Find the root cause precisely
    - Give an exact code fix
    - Suggest how to prevent this class of error in future
    
    Be clear, specific, and practical.
    Never use jargon without explaining it.
    """
)

def explain_error(traceback: str, code: str = "") -> ErrorExplanation:
    prompt = f"""
Explain this Python error:

TRACEBACK:
{traceback}

{"CODE:" if code else ""}
{code if code else ""}

Give a clear explanation and exact fix.
"""
    result = error_agent.run_sync(prompt)
    return result.output


# --- Test it ---
if __name__ == "__main__":
    
    # Test 1 — ZeroDivisionError
    traceback1 = """
Traceback (most recent call last):
  File "app.py", line 12, in <module>
    result = calculate_average([])
  File "app.py", line 5, in calculate_average
    return sum(numbers) / len(numbers)
ZeroDivisionError: division by zero
"""

    code1 = """
def calculate_average(numbers):
    return sum(numbers) / len(numbers)
"""

    # Test 2 — KeyError
    traceback2 = """
Traceback (most recent call last):
  File "app.py", line 8, in <module>
    print(user['email'])
KeyError: 'email'
"""

    code2 = """
user = {'name': 'Bhavya', 'age': 25}
print(user['email'])
"""

    for i, (tb, code) in enumerate([(traceback1, code1), (traceback2, code2)], 1):
        print(f"=== ERROR EXPLAINER — Test {i} ===")
        result = explain_error(tb, code)
        print(f"Error Type    : {result.error_type}")
        print(f"What happened : {result.plain_english}")
        print(f"Root Cause    : {result.root_cause}")
        print(f"Fix           : {result.fix}")
        print(f"Prevention    : {result.prevention}")
        print()
