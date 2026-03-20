from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from ast_parser import parse_code
import os
from config import GROQ_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY if GROQ_API_KEY else ""


# --- Structured Output Schema ---
class TestCase(BaseModel):
    test_name: str
    description: str
    code: str

class TestSuite(BaseModel):
    total_tests: int
    test_cases: list[TestCase]
    setup_notes: str

# --- The Agent ---
model = GroqModel("llama-3.3-70b-versatile")

test_agent = Agent(
    model=model,
    output_type=TestSuite,
    system_prompt="""
    You are a Python testing expert who writes clean Pytest unit tests.
    
    When given Python code:
    - Write comprehensive unit tests for every function
    - Cover happy path, edge cases, and error cases
    - Use descriptive test names (test_function_when_condition_returns_expected)
    - Use pytest.raises for exception testing
    - Keep tests simple, readable, and independent
    
    Return actual runnable pytest code for each test case.
    """
)

def write_tests(code: str) -> TestSuite:
    ast_result = parse_code(code)
    
    prompt = f"""
Write pytest unit tests for this Python code:
```python
{code}
```

Functions detected: {[f['name'] for f in ast_result['functions']]}

Write tests covering normal cases, edge cases, and error cases.
"""
    result = test_agent.run_sync(prompt)
    return result.output


# --- Test it ---
if __name__ == "__main__":
    sample_code = """
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def get_first(items):
    if not items:
        raise IndexError("List is empty")
    return items[0]

def calculate_average(numbers):
    if not numbers:
        raise ZeroDivisionError("Cannot average empty list")
    return sum(numbers) / len(numbers)
"""

    print("=== TEST WRITER AGENT ===")
    suite = write_tests(sample_code)
    print(f"Total tests generated: {suite.total_tests}")
    print(f"Setup notes: {suite.setup_notes}")
    print()
    for test in suite.test_cases:
        print(f"Test: {test.test_name}")
        print(f"Description: {test.description}")
        print(f"Code:\n{test.code}")
        print()