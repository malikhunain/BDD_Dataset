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

@given("a cost matrix {matrix}")
def step_given_matrix(context, matrix):
    context.matrix = ast.literal_eval(matrix)

@given("target row {m} and column {n}")
def step_given_target(context, m, n):
    context.m = int(m)
    context.n = int(n)

@when("I compute the minimum cost")
def step_when_compute(context):
    context.result = load_solution(context).min_cost(
        context.matrix, context.m, context.n
    )

@then("the result should be {expected}")
def step_then_result(context, expected):
    assert context.result == int(expected), (
        f"Expected {expected}, got {context.result}"
    )