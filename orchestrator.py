from bug_detector import detect_bugs, BugReport
from quality_scorer import score_quality, QualityReport
from error_explainer import explain_error, ErrorExplanation
from test_writer import write_tests, TestSuite
from pydantic import BaseModel

class CodeAnalysisResult(BaseModel):
    bug_report: BugReport
    quality_report: QualityReport
    test_suite: TestSuite
    error_explanation: ErrorExplanation | None = None

def analyze_code(code: str, traceback: str = "") -> CodeAnalysisResult:
    print("🔍 Detecting bugs...")
    bug_report = detect_bugs(code)
    
    print("📊 Scoring quality...")
    quality_report = score_quality(code)
    
    print("✅ Writing tests...")
    test_suite = write_tests(code)
    
    error_explanation = None
    if traceback:
        print("💡 Explaining error...")
        error_explanation = explain_error(traceback, code)

    return CodeAnalysisResult(
        bug_report=bug_report,
        quality_report=quality_report,
        test_suite=test_suite,
        error_explanation=error_explanation
    )


# --- Test it ---
if __name__ == "__main__":
    sample_code = """
def divide(a, b):
    return a / b

def get_first(items):
    return items[0]

def calculate_average(numbers):
    return sum(numbers) / len(numbers)
"""

    print("=== CODESENSE ORCHESTRATOR ===\n")
    result = analyze_code(sample_code)
    
    print(f"\n=== RESULTS ===")
    print(f"Bugs Found      : {result.bug_report.total_bugs}")
    print(f"Verdict         : {result.bug_report.overall_verdict}")
    print(f"Quality Score   : {result.quality_report.overall_score}/100 ({result.quality_report.grade})")
    print(f"Tests Generated : {result.test_suite.total_tests}")
    print(f"\nTop Strength    : {result.quality_report.top_strength}")
    print(f"Top Improvement : {result.quality_report.top_improvement}")