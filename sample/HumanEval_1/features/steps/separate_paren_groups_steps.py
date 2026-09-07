import ast, importlib.util, os
from behave import given, when, then, use_step_matcher

use_step_matcher("re")

def load_solution(context):
    path = context.config.userdata.get(
        "solution_path",
        os.path.join(os.path.dirname(__file__), "../../solution.py")
    )
    spec = importlib.util.spec_from_file_location("solution", path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

@given('a paren string "(?P<paren_string>.*)"')
def step_given(context, paren_string):
    context.paren_string = paren_string

@when("I separate the paren groups")
def step_when(context):
    context.result = load_solution(context).separate_paren_groups(
        context.paren_string
    )

@then('the result should be (?P<expected>.*)')
def step_then(context, expected):
    expected_val = ast.literal_eval(expected)
    assert context.result == expected_val, (
        f"Expected {expected_val!r}, got {context.result!r}"
    )