# Architecture

This project is organized around a simple Linux provisioning workflow that keeps risky system changes behind an explicit apply flag.

```text
sample_users.txt
      |
      v
load_user_records()
      |
      v
parse_user_record()
      |
      v
UserRecord objects
      |
      v
build_useradd_command()
      |
      v
Dry-run output or explicit apply mode
```

## Design Goals

- Keep the default workflow safe by printing commands instead of executing them.
- Validate input before generating Linux system commands.
- Keep parsing logic separate from command-building logic so each piece can be tested.
- Provide a clear path for future improvements such as logging, secure password handling, and richer account policies.

## Safety Notes

The script does not set plaintext passwords. The `password` field is parsed because it exists in the input format, but production-style password handling should use a secure process such as one-time password reset flows, locked accounts, or a secrets management workflow.

The `--apply` flag should only be used inside a controlled Linux VM or test environment.