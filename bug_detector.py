from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from ast_parser import parse_code

import os
from config import GROQ_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY if GROQ_API_KEY else ""

# --- Structured Output Schema ---
class Bug(BaseModel):
    line: str
    severity: str        # "low", "medium", "high"
    description: str
    fix: str

class BugReport(BaseModel):
    total_bugs: int
    bugs: list[Bug]
    overall_verdict: str  # "clean", "needs work", "critical"

# --- The Agent ---
model = GroqModel("llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

bug_detector = Agent(
    model=model,
    output_type=BugReport,
    system_prompt="""
    You are an expert Python code reviewer specializing in bug detection.
    
    When given code and its AST analysis, identify all bugs including:
    - Logic errors
    - Edge cases (division by zero, null checks, etc.)
    - Security issues
    - Type errors
    
    For each bug provide:
    - The line or function where it occurs
    - Severity: low / medium / high
    - Clear description of the problem
    - A concrete fix
    
    Be specific and practical. Only report real bugs, not style issues.
    """
)

def detect_bugs(code: str) -> BugReport:
    # First parse with AST
    ast_result = parse_code(code)
    
    # Build prompt with both code and AST info
    prompt = f"""
Review this Python code for bugs:
```python
{code}
```

AST Analysis found:
- Functions: {ast_result['functions']}
- Imports: {ast_result['imports']}
- Basic issues: {ast_result['issues']}

Identify all bugs and return a structured bug report.
"""
    result = bug_detector.run_sync(prompt)
    return result.output


# --- Test it ---
if __name__ == "__main__":
    sample_code = """
def divide(a, b):
    return a / b

def get_first(items):
    return items[0]

def read_file(path):
    f = open(path, 'r')
    content = f.read()
    return content

def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)
"""

    print("=== BUG DETECTOR AGENT ===")
    report = detect_bugs(sample_code)
    print(f"Total bugs found: {report.total_bugs}")
    print(f"Overall verdict: {report.overall_verdict}")
    print()
    for i, bug in enumerate(report.bugs, 1):
        print(f"Bug {i}:")
        print(f"  Line/Location : {bug.line}")
        print(f"  Severity      : {bug.severity}")
        print(f"  Problem       : {bug.description}")
        print(f"  Fix           : {bug.fix}")
        print()