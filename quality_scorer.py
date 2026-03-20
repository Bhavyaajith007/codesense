from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from ast_parser import parse_code
from config import GROQ_API_KEY
import os



# --- Structured Output Schema ---
class CategoryScore(BaseModel):
    category: str
    score: int        # out of 100
    feedback: str

class QualityReport(BaseModel):
    overall_score: int        # out of 100
    grade: str                # A, B, C, D, F
    categories: list[CategoryScore]
    top_strength: str
    top_improvement: str

# --- The Agent ---
model = GroqModel("llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

quality_agent = Agent(
    model=model,
    output_type=QualityReport,
    system_prompt="""
    You are a senior software engineer specializing in code quality assessment.
    
    Score Python code across these categories:
    - Readability (naming, formatting, clarity)
    - Structure (organization, separation of concerns)
    - Efficiency (algorithmic complexity, unnecessary operations)
    - Error Handling (edge cases, exceptions, validation)
    - Documentation (docstrings, comments, self-explanatory code)
    
    For each category give:
    - A score from 0 to 100
    - Specific, actionable feedback
    
    Overall score is the weighted average.
    Grade: A (90+), B (75+), C (60+), D (45+), F (below 45)
    
    Be honest and precise. Good code should score high, bad code should score low.
    """
)

def score_quality(code: str) -> QualityReport:
    ast_result = parse_code(code)
    
    prompt = f"""
Score the quality of this Python code:
```python
{code}
```

AST Analysis:
- Functions: {ast_result['functions']}
- Classes: {ast_result['classes']}
- Imports: {ast_result['imports']}
- Issues: {ast_result['issues']}

Return a detailed quality report with scores for each category.
"""
    result = quality_agent.run_sync(prompt)
    return result.output


# --- Test it ---
if __name__ == "__main__":
    sample_code = """
import os

def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)

def read_file(path):
    f = open(path, 'r')
    content = f.read()
    return content

class UserManager:
    def __init__(self):
        self.users = []
    
    def add(self, u):
        self.users.append(u)
    
    def get(self, id):
        for u in self.users:
            if u['id'] == id:
                return u
"""

    print("=== CODE QUALITY SCORER ===")
    report = score_quality(sample_code)
    print(f"Overall Score : {report.overall_score}/100")
    print(f"Grade         : {report.grade}")
    print()
    print("Category Breakdown:")
    for cat in report.categories:
        bar = "█" * (cat.score // 10) + "░" * (10 - cat.score // 10)
        print(f"  {cat.category:<20} {bar} {cat.score}/100")
        print(f"  └─ {cat.feedback}")
        print()
    print(f"Top Strength    : {report.top_strength}")
    print(f"Top Improvement : {report.top_improvement}")