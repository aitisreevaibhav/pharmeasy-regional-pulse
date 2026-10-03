import json
from datetime import datetime
from uuid import uuid4


AUDIT_PATH = "audit_log.jsonl"

VALID_DECISIONS = {"approve", "edit", "reject"}


def review_gate_v1(report, decision, reviewer_note=""):
    """
    Review a report and record the review decision.

    Allowed decisions:
    approve, edit, reject
    """

    if decision not in VALID_DECISIONS:
        raise ValueError(
            "Invalid decision. Use: approve, edit, or reject."
        )

    run_id = str(uuid4())

    # Try to get the region from the report
    if isinstance(report, dict):
        region = report.get("region", "multiple")
    else:
        region = "multiple"

    # Downstream use is allowed only when approved
    downstream_allowed = decision == "approve"

    result = {
        "report": report,
        "decision": decision,
        "reviewer_note": reviewer_note,
        "downstream_allowed": downstream_allowed,
        "run_id": run_id,
    }

    # Create one audit record
    audit_record = {
        "timestamp": datetime.now().isoformat(),
        "run_id": run_id,
        "region": region,
        "decision": decision,
        "reviewer_note": reviewer_note,
    }

    # Append audit record to JSONL file
    with open(AUDIT_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(audit_record) + "\n")

    return result


def main():

    # Small sample report for testing
    report = {
        "region": "Guntur",
        "context": "Guntur sales increased from April to May.",
        "insight": "April-to-May sales changed by 122.19%.",
        "implication": "The movement should be reviewed."
    }

    print("\n=== REVIEW GATE TEST ===")

    # 1. APPROVE
    print("\n--- APPROVE ---")
    before = report.copy()

    approved = review_gate_v1(
        report,
        "approve",
        "Numbers checked against SQL output."
    )

    print("Before:")
    print(before)

    print("After:")
    print(approved)

    # 2. EDIT
    print("\n--- EDIT ---")

    edited = review_gate_v1(
        report,
        "edit",
        "Please add category-level evidence."
    )

    print("Before:")
    print(report)

    print("After:")
    print(edited)

    # 3. REJECT
    print("\n--- REJECT ---")

    rejected = review_gate_v1(
        report,
        "reject",
        "Evidence needs further verification."
    )

    print("Before:")
    print(report)

    print("After:")
    print(rejected)

    # 4. Invalid decision test
    print("\n--- INVALID DECISION TEST ---")

    try:
        review_gate_v1(
            report,
            "pending",
            "Invalid decision test."
        )
    except ValueError as e:
        print("Correctly rejected:")
        print(e)


if __name__ == "__main__":
    main()