from langchain_core.tools import tool


@tool
def calculate(expression: str) -> str:
    """Calculate a basic mathematical expression."""

    try:
        allowed = "0123456789+-*/(). "

        if not all(char in allowed for char in expression):
            return "Invalid mathematical expression."

        result = eval(expression, {"__builtins__": {}}, {})

        return str(result)

    except Exception:
        return "Could not calculate the expression."


@tool
def create_task_list(goal: str) -> str:
    """Break a user's goal into simple actionable tasks."""

    return f"""
Task breakdown for: {goal}

1. Understand the main goal.
2. Identify the required steps.
3. Arrange the steps in a logical order.
4. Execute or complete each step.
5. Review the final result.
"""


tools = [
    calculate,
    create_task_list
]