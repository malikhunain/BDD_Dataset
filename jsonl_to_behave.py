"""
jsonl_to_behave.py

Converts records from bdd_dataset.jsonl into runnable per-problem Behave
directory structures -- the same layout as sample/, one folder per problem:

    <output_dir>/<id>/
        features/
            <id>.feature
            steps/
                <id>_steps.py
        solution.py

Usage:
    # Explode the full dataset
    python jsonl_to_behave.py --input bdd_dataset.jsonl --output_dir ./exploded

    # Explode just one source
    python jsonl_to_behave.py --input bdd_dataset_humanEval.jsonl --output_dir ./exploded

    # Explode a specific subset by id
    python jsonl_to_behave.py --input bdd_dataset.jsonl --output_dir ./exploded --ids HumanEval_0 MBPP_1

    # Explode only the first N (useful for a quick smoke test)
    python jsonl_to_behave.py --input bdd_dataset.jsonl --output_dir ./exploded --limit 10

After exploding, run behave against any problem individually:
    cd exploded/HumanEval_0 && behave features/

...or against everything at once from the output directory:
    behave exploded/ --include ".*\\.feature"

"""

import argparse
import json
from pathlib import Path


def load_records(path, ids=None, limit=None):
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if ids and rec.get("id") not in ids:
                continue
            records.append(rec)
            if limit and len(records) >= limit:
                break
    return records


def explode_record(record, output_dir):
    rid = record.get("id")
    if not rid:
        return None

    problem_dir = output_dir / rid
    features_dir = problem_dir / "features"
    steps_dir = features_dir / "steps"
    steps_dir.mkdir(parents=True, exist_ok=True)

    (features_dir / f"{rid}.feature").write_text(
        record.get("feature_text", ""), encoding="utf-8"
    )
    (steps_dir / f"{rid}_steps.py").write_text(
        record.get("steps_text", ""), encoding="utf-8"
    )
    (problem_dir / "solution.py").write_text(
        record.get("solution_text", ""), encoding="utf-8"
    )
    return problem_dir


def main():
    parser = argparse.ArgumentParser(
        description="Explode bdd_dataset.jsonl into runnable per-problem Behave folders."
    )
    parser.add_argument("--input", required=True, help="Path to a bdd_dataset*.jsonl file")
    parser.add_argument("--output_dir", required=True, help="Directory to write exploded problems into")
    parser.add_argument("--ids", nargs="*", default=None,
                         help="Only explode these specific problem ids (space-separated)")
    parser.add_argument("--limit", type=int, default=None,
                         help="Only explode the first N matching records")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    records = load_records(args.input, ids=set(args.ids) if args.ids else None, limit=args.limit)
    print(f"Loaded {len(records)} record(s) from {args.input}")

    written = 0
    for record in records:
        result = explode_record(record, output_dir)
        if result:
            written += 1

    print(f"Wrote {written} problem folder(s) to {output_dir}/")
    if written:
        example_id = records[0].get("id")
        print(f"\nTry it:\n  cd {output_dir}/{example_id} && behave features/")


if __name__ == "__main__":
    main()