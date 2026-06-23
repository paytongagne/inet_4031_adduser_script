"""Linux user provisioning command generator.

This tool reads colon-delimited user records and generates safe Linux account
creation commands. It defaults to dry-run behavior so commands are printed
instead of executed.
"""

from __future__ import annotations

import argparse
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class UserRecord:
    username: str
    password: str
    last_name: str
    first_name: str
    groups: List[str]

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


def parse_user_record(line: str) -> UserRecord | None:
    """Parse one colon-delimited user record.

    Expected format:
        username:password:last_name:first_name:group1,group2

    Blank lines and comment lines return None. Malformed lines raise ValueError.
    """
    stripped = line.strip()

    if not stripped or stripped.startswith("#"):
        return None

    parts = stripped.split(":")
    if len(parts) != 5:
        raise ValueError(f"Invalid record format: {line.rstrip()}")

    username, password, last_name, first_name, raw_groups = [part.strip() for part in parts]

    required = {
        "username": username,
        "password": password,
        "last_name": last_name,
        "first_name": first_name,
    }
    missing = [field for field, value in required.items() if not value]
    if missing:
        raise ValueError(f"Missing required fields {missing}: {line.rstrip()}")

    groups = [] if raw_groups in {"", "-"} else [group.strip() for group in raw_groups.split(",") if group.strip()]

    return UserRecord(
        username=username,
        password=password,
        last_name=last_name,
        first_name=first_name,
        groups=groups,
    )


def load_user_records(path: Path) -> List[UserRecord]:
    """Load and validate user records from a file."""
    records: List[UserRecord] = []

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        try:
            record = parse_user_record(line)
        except ValueError as exc:
            raise ValueError(f"Line {line_number}: {exc}") from exc

        if record is not None:
            records.append(record)

    return records


def build_useradd_command(record: UserRecord) -> List[str]:
    """Build a Linux useradd command without executing it."""
    command = [
        "sudo",
        "useradd",
        "-m",
        "-c",
        record.full_name,
    ]

    if record.groups:
        command.extend(["-G", ",".join(record.groups)])

    command.append(record.username)
    return command


def shell_join(command: Iterable[str]) -> str:
    """Return a safely quoted shell command string."""
    return " ".join(shlex.quote(part) for part in command)


def apply_commands(records: Iterable[UserRecord]) -> None:
    """Execute provisioning commands.

    This intentionally does not set plaintext passwords. Password handling should
    be implemented with a secure process before this is used outside a lab VM.
    """
    for record in records:
        command = build_useradd_command(record)
        subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Linux user provisioning commands from structured records.")
    parser.add_argument("--input", default="sample_users.txt", help="Path to colon-delimited user records")
    parser.add_argument("--apply", action="store_true", help="Execute commands instead of printing dry-run output")
    args = parser.parse_args()

    input_path = Path(args.input)
    records = load_user_records(input_path)

    if not records:
        print("No valid user records found.")
        return

    if args.apply:
        apply_commands(records)
        print(f"Applied provisioning commands for {len(records)} users.")
        return

    print("Dry run: generated Linux user creation commands")
    for record in records:
        print(shell_join(build_useradd_command(record)))


if __name__ == "__main__":
    main()
