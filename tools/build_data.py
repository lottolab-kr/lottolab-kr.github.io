#!/usr/bin/env python3
"""
Rebuilds data.json from data/draws.csv (the versioned source of truth).

Usage:
    python3 tools/build_data.py

Validates:
  - drwNo is a positive integer, dates are real calendar dates
  - each row has 6 distinct main numbers in 1-45 plus a bonus in 1-45
    that does not duplicate a main number
  - the round range has no gaps or duplicate rounds

Run this after editing data/draws.csv (e.g. after appending a new week's
result), then commit both files together.
"""
import csv
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "draws.csv"
JSON_PATH = ROOT / "data.json"


def load_rows(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, r in enumerate(reader, start=2):  # header is line 1
            try:
                drwno = int(r["drwNo"])
                date = r["date"]
                nums = [int(r[f"n{k}"]) for k in range(1, 7)]
                bonus = int(r["bonus"])
            except (KeyError, ValueError) as e:
                sys.exit(f"Line {i}: malformed row ({e})")

            try:
                datetime.date.fromisoformat(date)
            except ValueError:
                sys.exit(f"Line {i} (round {drwno}): bad date '{date}'")

            if len(set(nums)) != 6 or any(not (1 <= n <= 45) for n in nums):
                sys.exit(f"Line {i} (round {drwno}): main numbers must be 6 distinct values in 1-45")
            if not (1 <= bonus <= 45) or bonus in nums:
                sys.exit(f"Line {i} (round {drwno}): bonus must be 1-45 and not duplicate a main number")

            rows.append((drwno, date, tuple(sorted(nums)), bonus))
    return rows


def validate_continuity(rows):
    by_no = {}
    for r in rows:
        if r[0] in by_no and by_no[r[0]] != r:
            sys.exit(f"Round {r[0]} appears twice with different data")
        by_no[r[0]] = r
    nos = sorted(by_no.keys())
    missing = [n for n in range(nos[0], nos[-1] + 1) if n not in by_no]
    if missing:
        sys.exit(f"Missing rounds in range {nos[0]}-{nos[-1]}: {missing[:20]}")
    return [by_no[n] for n in nos]


def main():
    rows = load_rows(CSV_PATH)
    if not rows:
        sys.exit("No rows found in data/draws.csv")
    rows = validate_continuity(rows)

    counts = [0] * 46
    for _, _, nums, _ in rows:
        for n in nums:
            counts[n] += 1

    doc = {
        "counts": counts,
        "minDrwNo": rows[0][0],
        "maxDrwNo": rows[-1][0],
        "lastDate": rows[-1][1],
        "isComplete": rows[0][0] == 1,
        "asOf": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(),
        "strength": 2,
    }

    # preserve any existing ads config already in data.json
    if JSON_PATH.exists():
        try:
            existing = json.loads(JSON_PATH.read_text(encoding="utf-8"))
            if "ads" in existing:
                doc["ads"] = existing["ads"]
        except Exception:
            pass
    doc.setdefault("ads", {
        "top": {"enabled": False, "image": "", "link": ""},
        "bottom": {"enabled": False, "image": "", "link": ""},
    })

    JSON_PATH.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {JSON_PATH} — {len(rows)} rounds ({rows[0][0]}~{rows[-1][0]}), "
          f"complete={doc['isComplete']}, counts min={min(counts[1:])} max={max(counts[1:])}")


if __name__ == "__main__":
    main()
