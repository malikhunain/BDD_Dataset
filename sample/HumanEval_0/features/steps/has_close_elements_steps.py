import ast, importlib.util, os
from behave import given, when, then

def load_solution(context):
    path = context.config.userdata.get(
        "solution_path",
        os.path.join(os.path.dirname(__file__), "../../solution.py")
    )
    spec = importlib.util.spec_from_file_location("solution", path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

@given("a list of numbers {numbers}")
def step_given(context, numbers):
    context.numbers = ast.literal_eval(numbers)

@when("I check for close elements with threshold {threshold}")
def step_when(context, threshold):
    context.result = load_solution(context).has_close_elements(
        context.numbers, float(threshold)
    )

@then("the result should be {expected}")
def step_then(context, expected):
    assert context.result == ast.literal_eval(expected), (
        f"Expected {expected}, got {context.result}"
    )