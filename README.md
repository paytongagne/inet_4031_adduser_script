# Linux User Provisioning Automation

A Linux-focused automation project for working with structured user account records. This repository is being prepared as a portfolio-ready systems administration project that demonstrates file-based user input, account metadata, group assignment concepts, and future automation around Linux user provisioning.

## Overview

The project uses colon-delimited user records that follow a format commonly used in systems administration exercises:

```text
username:password:last_name:first_name:group
```

The current repository includes sample user records that can be used as input for a future provisioning script. The next stage is to add a Python or shell-based automation layer that validates records, handles malformed lines, and safely prepares Linux user creation commands.

## Tech Focus

- Linux system administration
- User and group management concepts
- Python or shell automation
- Input validation
- Command-line tooling
- Safe dry-run workflow design

## Example Input

```text
user04:pass04:Last04:First04:group01
user05:pass05:Last05:First05:group02
user06:pass06:Last06:First06:group01,group02
```

## Planned Features

- Parse user records from an input file
- Validate required fields
- Skip comments and malformed lines
- Support users with one group, multiple groups, or no group
- Generate Linux user creation commands
- Add a dry-run mode before making system changes
- Add logging for created, skipped, and failed users
- Add unit tests for record parsing

## Proposed Command Flow

```bash
python provision_users.py --input create-users.txt --dry-run
python provision_users.py --input create-users.txt --apply
```

## Workplace Relevance

This project is meant to show practical automation skills that apply to IT, DevOps, system administration, and infrastructure support roles. The finished version should demonstrate safe scripting, validation, documentation, and repeatable Linux account setup workflows.

## Portfolio Status

This repository is currently in cleanup mode. The next commits should add the actual provisioning script, tests, a safer file name for the input data, and screenshots or terminal output examples.