import ast, importlib.util, os
from behave import given, when, then

def load_solution(context):
    path = context.config.userdata.get(
        "solution_path",
        os.path.join(os.path.dirname(__file__), "../../solution.py")
    )
    spec = importlib.util.spec_from_file_location("solution", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

@given("first tuple {tuple1}")
def step_given_first_tuple(context, tuple1):
    context.tuple1 = ast.literal_eval(tuple1)

@given("second tuple {tuple2}")
def step_given_second_tuple(context, tuple2):
    context.tuple2 = ast.literal_eval(tuple2)

@when("I compute similar elements")
def step_when_compute(context):
    context.result = load_solution(context).similar_elements(
        context.tuple1, context.tuple2
    )

@then("the result should be {expected}")
def step_then_result(context, expected):
    expected_val = ast.literal_eval(expected)
    assert context.result == expected_val, (
        f"Expected {expected_val}, got {context.result}"
    )