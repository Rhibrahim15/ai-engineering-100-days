
from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / "progress_state.json"
JSON_OUTPUT = ROOT / "progress.json"
MD_OUTPUT = ROOT / "PROGRESS.md"
TOTAL_DAYS = 100

SPRINTS = [
    ("Python and engineering foundations", 1, 10),
    ("Data handling and classical ML", 11, 20),
    ("Deep learning fundamentals", 21, 30),
    ("NLP and transformers", 31, 40),
    ("Reliable LLM applications", 41, 50),
    ("RAG and knowledge systems", 51, 60),
    ("AI agents and orchestration", 61, 70),
    ("Production infrastructure", 71, 80),
    ("Evaluation, testing, reliability", 81, 90),
    ("Capstone, deployment, portfolio", 91, 100),
]

VALID_STATUSES = {"Not started", "In progress", "Verified"}


def sprint_for_day(day: int) -> tuple[int, str, int, int]:
    for number, (name, start, end) in enumerate(SPRINTS, start=1):
        if start <= day <= end:
            return number, name, start, end

    raise ValueError(f"No sprint configured for day {day}")


def load_state() -> dict:
    if not STATE_FILE.exists():
        raise FileNotFoundError(
            "progress_state.json is missing. Create it before running this script."
        )

    with STATE_FILE.open("r", encoding="utf-8-sig") as file:
        state = json.load(file)

    if not isinstance(state, dict):
        raise ValueError("The progress state must be a JSON object.")

    days = state.get("days", {})

    if not isinstance(days, dict):
        raise ValueError("'days' in progress_state.json must be an object.")

    return days


def check_tests(day: int, evidence: list[str]) -> bool:
    """Run unittest discovery when test files are declared."""
    test_files = [
        ROOT / path
        for path in evidence
        if Path(path).name.startswith("test_")
        and Path(path).suffix == ".py"
    ]

    if not test_files:
        return False

    if any(not path.is_file() for path in test_files):
        return False

    code_folder = ROOT / f"day{day:02d}" / "code"

    if not code_folder.is_dir():
        return False

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(code_folder),
            "-p",
            "test_*.py",
            "-v",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.stdout:
        print(result.stdout, end="")

    if result.stderr:
        print(result.stderr, end="")

    return result.returncode == 0


def build_records(state_days: dict) -> list[dict]:
    records = []

    for day in range(1, TOTAL_DAYS + 1):
        key = str(day)
        folder = ROOT / f"day{day:02d}"
        entry = state_days.get(key, {})

        if not isinstance(entry, dict):
            raise ValueError(f"Day {day} must have an object as its record.")

        status = entry.get("status", "Not started")
        evidence = entry.get("evidence", [])
        verification = entry.get("verification", {})

        if status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status for Day {day}: {status!r}"
            )

        if not isinstance(evidence, list):
            raise ValueError(f"Evidence for Day {day} must be a list.")

        if not isinstance(verification, dict):
            raise ValueError(
                f"Verification for Day {day} must be an object."
            )

        if any(not isinstance(path, str) for path in evidence):
            raise ValueError(
                f"Every evidence path for Day {day} must be a string."
            )

        # Reject paths that escape the repository root.
        safe_evidence = []
        for relative_path in evidence:
            candidate = (ROOT / relative_path).resolve()

            if not candidate.is_relative_to(ROOT.resolve()):
                raise ValueError(
                    f"Evidence path for Day {day} escapes the repository."
                )

            safe_evidence.append(candidate)

        missing = [
            relative_path
            for relative_path, candidate in zip(evidence, safe_evidence)
            if not candidate.is_file()
        ]

        reflection = folder / "reflection.md"
        reflection_has_content = (
            reflection.is_file()
            and bool(reflection.read_text(encoding="utf-8-sig").strip())
        )

        tests_passed = False

        if status == "Verified" and not missing:
            tests_passed = check_tests(day, evidence)

        verified_requirements_met = (
            status == "Verified"
            and not missing
            and tests_passed
            and reflection_has_content
            and verification.get("reflection_reviewed") is True
            and verification.get("human_verified") is True
        )

        if status == "Verified" and not verified_requirements_met:
            status = "In progress"

        sprint_number, sprint_name, _, _ = sprint_for_day(day)

        if status == "Not started":
            detail = "No work recorded in progress state"
        elif status == "Verified":
            detail = (
                "Evidence exists; tests passed; reflection and human review recorded"
            )
        elif missing:
            detail = "Missing evidence: " + ", ".join(missing)
        elif not reflection_has_content:
            detail = "Reflection needs to be completed"
        elif not tests_passed and entry.get("status") == "Verified":
            detail = "Verification failed: tests did not pass"
        else:
            detail = "Work recorded; verification pending"

        records.append({
            "day": day,
            "topic": sprint_name,
            "sprint": sprint_number,
            "status": status,
            "evidence": evidence,
            "detail": detail,
            "tests_passed": tests_passed,
        })

    return records


def main() -> None:
    state_days = load_state()
    records = build_records(state_days)

    verified = sum(
        record["status"] == "Verified" for record in records
    )
    in_progress = sum(
        record["status"] == "In progress" for record in records
    )
    not_started = sum(
        record["status"] == "Not started" for record in records
    )

    current = next(
        (record for record in records if record["status"] != "Verified"),
        records[-1],
    )

    sprint_number, sprint_name, _, _ = sprint_for_day(current["day"])

    dashboard = {
        "title": "100-Day AI Engineering Streak",
        "updated": date.today().isoformat(),
        "total_days": TOTAL_DAYS,
        "verified_days": verified,
        "in_progress_days": in_progress,
        "not_started_days": not_started,
        "completion_percent": round(
            verified / TOTAL_DAYS * 100, 1
        ),
        "current_day": current["day"],
        "current_sprint": sprint_number,
        "current_sprint_name": sprint_name,
        "days": records,
    }

    JSON_OUTPUT.write_text(
        json.dumps(dashboard, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# 100-Day AI Engineering Streak - Progress",
        "",
        "**Start date:** 15-10-2026  ",
        f"**Last updated:** {date.today().isoformat()}  ",
        "**Daily commitment:** 4 hours  ",
        "**Repository:** https://github.com/Rhibrahim15/ai-engineering-100-days",
        "",
        "## Overall Progress",
        "",
        f"- **Verified days:** {verified}/{TOTAL_DAYS}",
        f"- **Completion:** {verified / TOTAL_DAYS * 100:.1f}%",
        f"- **In progress:** {in_progress}",
        f"- **Not started:** {not_started}",
        f"- **Current day:** Day {current['day']:02d}",
        f"- **Current sprint:** Sprint {sprint_number} - {sprint_name}",
        "",
        "## Status Definitions",
        "",
        "- `Not started` - No work recorded in progress state.",
        "- `In progress` - Work is recorded but verification is incomplete.",
        "- `Verified` - Evidence, passing tests, and human review are required.",
        "",
        "## Daily Tracker",
        "",
        "| Day | Sprint topic | Status | Evidence |",
        "|---|---|---|---|",
    ]

    for record in records:
        evidence = (
            ", ".join(f"`{path}`" for path in record["evidence"]) or "-"
        )
        lines.append(
            f"| {record['day']:02d} | {record['topic']} | "
            f"{record['status']} | {evidence} |"
        )

    lines.extend([
        "",
        "## Sprint Summary",
        "",
        "| Sprint | Days | Focus | Status |",
        "|---|---|---|---|",
    ])

    for number, (name, start, end) in enumerate(SPRINTS, start=1):
        sprint_records = records[start - 1:end]
        sprint_verified = sum(
            record["status"] == "Verified"
            for record in sprint_records
        )

        if sprint_verified == len(sprint_records):
            status = "Complete"
        elif any(
            record["status"] == "In progress"
            for record in sprint_records
        ):
            status = "In progress"
        else:
            status = "Not started"

        lines.append(
            f"| {number} | {start:02d}-{end:02d} | "
            f"{name} | {status} |"
        )

    lines.extend([
        "",
        "## Latest Milestone",
        "",
        f"- **Current task:** Review Day {current['day']:02d}.",
        "- **Next action:** Complete the implementation, checks, and reflection.",
        "",
        "<!-- Generated by scripts/update_progress.py. Do not edit generated statistics manually. -->",
        "",
    ])

    MD_OUTPUT.write_text(
        "\n".join(lines),
        encoding="utf-8-sig",
    )

    print("Progress report updated:", MD_OUTPUT)
    print("Dashboard data updated:", JSON_OUTPUT)
    print(
        f"Verified: {verified} | In progress: {in_progress} | "
        f"Not started: {not_started}"
    )
    print(f"Current day: {current['day']:02d}")


if __name__ == "__main__":
    main()
