import ast

def parse_code(code: str) -> dict:
    """
    Parses Python code and extracts structure using AST.
    Returns a dict with functions, classes, imports, and issues.
    """
    result = {
        "functions": [],
        "classes": [],
        "imports": [],
        "issues": []
    }

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        result["issues"].append(f"Syntax error: {e}")
        return result

    for node in ast.walk(tree):

        # Extract functions
        if isinstance(node, ast.FunctionDef):
            func_info = {
                "name": node.name,
                "args": [arg.id if isinstance(arg, ast.Name) else arg.arg 
                         for arg in node.args.args],
                "lineno": node.lineno,
                "has_docstring": ast.get_docstring(node) is not None
            }
            result["functions"].append(func_info)

        # Extract classes
        elif isinstance(node, ast.ClassDef):
            result["classes"].append({
                "name": node.name,
                "lineno": node.lineno
            })

        # Extract imports
        elif isinstance(node, ast.Import):
            for alias in node.names:
                result["imports"].append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            result["imports"].append(f"{node.module}")

    # Basic issue detection
    for func in result["functions"]:
        if not func["has_docstring"]:
            result["issues"].append(
                f"Function '{func['name']}' at line {func['lineno']} is missing a docstring"
            )

    return result


# Test it
if __name__ == "__main__":
    sample_code = """
import os
import sys

class Calculator:
    def add(self, a, b):
        return a + b
    
    def divide(self, a, b):
        return a / b

def greet(name):
    print("Hello " + name)
"""

    result = parse_code(sample_code)
    print("=== AST PARSER OUTPUT ===")
    print(f"Functions found: {result['functions']}")
    print(f"Classes found:   {result['classes']}")
    print(f"Imports found:   {result['imports']}")
    print(f"Issues found:    {result['issues']}")