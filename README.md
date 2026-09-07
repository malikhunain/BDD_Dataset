# BDD_Dataset

**A Python/Behave Behavior-Driven Development (BDD) dataset for code generation benchmarks, translated from HumanEval and MBPP, fully execution-verified.**

This repository hosts the dataset described in *"A Behavior-Driven Dataset for Python Code Generation Benchmarks"* (Murtaza & Hesenius, MSR 2027 Data and Tool Showcase Track). The dataset generation pipeline that produced this data is released separately: [BDD-Dataset-Generation](https://github.com/malikhunain/BDD-Dataset-Generation).

---

## What this is

`BDD_Dataset` contains **1,132 problems** from HumanEval and MBPP, each translated into Gherkin BDD format with executable Python [Behave](https://behave.readthedocs.io/) step definitions, paired with the **original, human-authored HumanEval/MBPP canonical reference solution** (not a model-generated artifact). Every problem is execution-verified: all scenarios pass against the reference solution via `behave`.

No prior BDD dataset targets Python. GWT (Alcântara Júnior & Montandon, MSR'26), the only prior large-scale BDD dataset, covers Java/JavaScript/Ruby, is mined rather than executed, and explicitly names Python/Behave as future work. This dataset closes that gap.

## Dataset statistics

| Attribute | Value |
|---|---|
| Total problems | 1,132 |
| HumanEval-derived | 160 |
| MBPP-derived | 972 |
| Scenarios / problem (mean, median) | 5.39, 5.0 |
| Steps / problem (mean, median) | 18.43, 18.0 |
| Reference solution LOC (mean, median) | 8.19, 6.0 |
| Reference solution cyclomatic complexity (mean, median) | 2.92, 2.0 |
| Execution verification | 100% (via `behave`) |
| Static analysis (Tier 1, AST-based) | 0/14 flagged candidates confirmed as defects |
| License (HumanEval / MBPP) | MIT / CC-BY-4.0 |

Full construction methodology, verification process, and quality analysis are described in the paper (link added once published).

## Schema

Each record in `bdd_dataset.jsonl` is a single JSON object with these fields:

| Field | Type | Description |
|---|---|---|
| `id` | string | Problem identifier, e.g. `HumanEval_0`, `MBPP_1` |
| `source` | string | `HumanEval` or `MBPP` |
| `feature_text` | string | The Gherkin feature file (scenarios in Given/When/Then form) |
| `steps_text` | string | Executable Python Behave step-definition module |
| `solution_text` | string | The original, unmodified HumanEval/MBPP canonical reference implementation |
| `num_scenarios` | int | Number of scenarios, correctly counting `Scenario Outline`/`Examples` expansion |
| `num_steps` | int | Number of executed steps, same expansion rule |
| `function_signature` | string | The target function's signature, AST-extracted from `solution_text` |

`solution_text` is included so each problem is immediately runnable end-to-end (feature → step definitions → reference solution) without a separate lookup into the source benchmarks.

## Worked example: `HumanEval_0`

**`feature_text`:**
```gherkin
Feature: Detecting close numbers in a list
  As a data validation system
  I want to check whether any two numbers in a list are closer than a threshold
  So that I can flag lists with suspiciously similar values

  Scenario: No two numbers are within the threshold
    Given a list of numbers [1.0, 2.0, 3.0]
    When I check for close elements with threshold 0.5
    Then the result should be False

  Scenario: Two numbers are within the threshold
    Given a list of numbers [1.0, 2.8, 3.0, 4.0, 5.0, 2.0]
    When I check for close elements with threshold 0.3
    Then the result should be True

  Scenario: Single element list has no pairs to compare
    Given a list of numbers [1.0]
    When I check for close elements with threshold 0.1
    Then the result should be False

  Scenario: Duplicate values are closer than any positive threshold
    Given a list of numbers [1.0, 1.0]
    When I check for close elements with threshold 0.1
    Then the result should be True

  Scenario: Exact threshold boundary is not considered closer than threshold
    Given a list of numbers [1.0, 2.0]
    When I check for close elements with threshold 1.0
    Then the result should be False
```

**`steps_text` (excerpt):**
```python
@given("a list of numbers {numbers}")
def step_given(context, numbers):
    context.numbers = ast.literal_eval(numbers)

@when("I check for close elements with threshold {threshold}")
def step_when(context, threshold):
    context.result = load_solution(context).has_close_elements(
        context.numbers, float(threshold))

@then("the result should be {expected}")
def step_then(context, expected):
    assert context.result == ast.literal_eval(expected), (
        f"Expected {expected}, got {context.result}")
```

**`solution_text`:** the unmodified canonical `has_close_elements` implementation from HumanEval.

A fully runnable version of this and 4 other example problems is in [`sample/`](./sample) — real `.feature` files and step-definition modules you can run directly with `behave`, not JSON.

## Repository structure

```
BDD_Dataset/
├── bdd_dataset.jsonl      # the full dataset -- 1,132 records, one per line
├── sample/                # 4 problems as runnable Behave files (browsable, not the full corpus)
│   ├── HumanEval_0/
│   │   ├── HumanEval_0.feature
│   │   ├── steps/
│   │   │   └── HumanEval_0_steps.py
│   │   └── solution.py
│   ├── HumanEval_...
│   ├── MBPP_.../
│   └── MBPP_.../
├── README.md               # this file
└── LICENSE                 # CC-BY-4.0 notice (see Licensing below)
```

`sample/` is illustrative only — 5 of the 1,132 problems, included so you can browse and run real Behave files without first writing a script to explode the jsonl. The full dataset is `bdd_dataset.jsonl`.

## Loading the dataset

```python
import json

records = []
with open("bdd_dataset.jsonl", encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))

print(len(records))          # 1132
print(records[0]["id"])      # e.g. "HumanEval_0"
```

## Licensing and attribution

HumanEval is [MIT-licensed](https://github.com/openai/human-eval/blob/master/LICENSE);
MBPP is [CC-BY-4.0-licensed](https://huggingface.co/datasets/google-research-datasets/mbpp).
Both licenses permit derivative works with attribution. This dataset, as a derivative work, is released under **CC-BY-4.0** (the more restrictive of the two source licenses). See [`LICENSE`](./LICENSE).

If you use this dataset, please retain attribution to both source benchmarks:

> This dataset derives from HumanEval (Chen et al., 2021, MIT License) and
> MBPP (Austin et al., 2021, CC-BY-4.0 License).

## Citation

```bibtex
@inproceedings{murtaza2027bdddataset,
  author    = {Murtaza, Hunain and Hesenius, Marc},
  title     = {A Behavior-Driven Dataset for Python Code Generation Benchmarks},
  booktitle = {Proceedings of the 24th International Conference on Mining Software Repositories -- Data and Tool Showcase Track (MSR '27)},
  year      = {2027},
  publisher = {ACM},
  doi       = {10.1145/nnnnnnn.nnnnnnn}
}
```
*(DOI to be updated once assigned.)*

## Related resources

- **Generation pipeline (code):** [BDD-Dataset-Generation](https://github.com/malikhunain/BDD-Dataset-Generation)
- **Paper:** link added once published
- **Zenodo archive (persistent DOI):** link added once published

## Limitations

Briefly: Python only; inherits HumanEval/MBPP's distributional biases toward short, self-contained algorithmic functions; Gherkin-formatted specifications for algorithmic problems is a narrower use of BDD than its original stakeholder-collaboration purpose; not protected against training-data contamination (HumanEval/MBPP are widely present in LLM training corpora). Full discussion in the paper, Section 8.