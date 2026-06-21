#!/usr/bin/env python3
"""
Automated KPI Updater.
Runs check_kpis.py --update, checks for changes in docs/kpi-tracker.md,
commits and pushes them, and sleeps for a randomized duration between 32 minutes and 2 hours.
"""
from __future__ import annotations

import random
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_kpi_update() -> bool:
    print("Running KPI update check...")
    # Run the check_kpis.py script with --update
    res = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_kpis.py"), "--update"],
        capture_output=True,
        text=True,
    )
    if res.returncode != 0:
        print(
            f"Error updating KPIs: {res.stderr or res.stdout}",
            file=sys.stderr,
        )
        return False
    print("KPIs updated locally.")
    return True


def git_commit_and_push() -> None:
    # Check if there are changes in docs/kpi-tracker.md
    res = subprocess.run(
        ["git", "status", "--porcelain", "docs/kpi-tracker.md"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if not res.stdout.strip():
        print("No changes in KPI tracker. Skipping git push.")
        return

    print("Changes detected. Committing and pushing...")
    # Add
    subprocess.run(
        ["git", "add", "docs/kpi-tracker.md"], cwd=str(ROOT), check=True
    )
    # Commit
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "chore: auto-update KPI tracker [skip ci]",
        ],
        cwd=str(ROOT),
        check=True,
    )
    # Push
    subprocess.run(["git", "push"], cwd=str(ROOT), check=True)
    print("KPI tracker pushed successfully.")


def main() -> None:
    print("Starting automated KPI updater...")
    while True:
        try:
            if run_kpi_update():
                git_commit_and_push()
        except Exception as e:
            print(f"Error in update cycle: {e}", file=sys.stderr)

        # Calculate random sleep duration: between 32 minutes and 2 hours
        min_sec = 32 * 60
        max_sec = 120 * 60
        sleep_time = random.randint(min_sec, max_sec)

        minutes = sleep_time // 60
        seconds = sleep_time % 60
        print(f"Next update scheduled in {minutes}m {seconds}s.")
        time.sleep(sleep_time)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKPI updater stopped.")
