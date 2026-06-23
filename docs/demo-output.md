# Demo Output

Run the project in dry-run mode:

```bash
python provision_users.py --input sample_users.txt
```

Expected output format:

```text
Dry run: generated Linux user creation commands
sudo useradd -m -c 'First04 Last04' -G group01 user04
sudo useradd -m -c 'First05 Last05' -G group02 user05
sudo useradd -m -c 'First06 Last06' -G group01,group02 user06
sudo useradd -m -c 'First07 Last07' user07
```

This file can be replaced later with a screenshot or copied terminal output from a Linux VM.
