#!/usr/bin/env python3

"""
Cloud Manager (Local & AWS)
- Local: Adds/lists simple VM records > configs/instances.json
- AWS: Lists actual EC2 instances via AWS/python/list_ec2.py

"""

from __future__ import annotations
import json
import os
import re
import sys
import subprocess
from pathlib import Path

# Paths (relates > initial root project) 
PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_DIR = PROJECT_ROOT / "configs"
CONFIG_FILE = CONFIG_DIR / "instances.json"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "app.log"
AWS_LISTER = PROJECT_ROOT / "AWS" / "python" / "list_ec2.py"

# for logs input
def log(msg: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    from datetime import datetime, timezone
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{ts} | {msg}\n")

#config help
def ensure_config() -> None:
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if not CONFIG_FILE.exists():
            CONFIG_FILE.write_text(json.dumps({"instances": []}, indent=2), encoding="utf-8")
    except Exception as e:
        log(f"ERROR creating config: {e}")
        print("Error preparing configuration... Boo!!")
        raise

def load_instances() -> list[dict]:
    ensure_config()
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        return data.get("instances", [])
    except Exception as e:
        log(f"ERROR reading config: {e}")
        print("Error reading configuration... Boo!!")
        return []

def save_instances(items: list[dict]) -> None:
    ensure_config()
    try:
        data = {"instances": items}
        CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception as e:
        log(f"ERROR saving config: {e}")
        print(f"Error saving configuration... Boo!! ({e})")
        raise

# User input validations 
# (from previous project, instructor noted, validations should be immediate and not at the end)
def ask_str(prompt: str, *, min_len=1, max_len=40) -> str:
    while True:
        val = input(prompt).strip()
        if not val:
            print(f"Please enter at least {min_len} letters...")
            continue
        if len(val) > max_len:
            print(f"Please keep it under {max_len} letters...")
            continue
        return val

def ask_int(prompt: str, *, min_val=None, max_val=None) -> int:
    while True:
        raw = input(prompt).strip()
        if not re.fullmatch(r"-?\d+", raw):
            print("Please use whole numbers...")
            continue
        val = int(raw)
        if min_val is not None and val < min_val:
            print(f"Value needs to be a minimum of {min_val}.")
            continue
        if max_val is not None and val > max_val:
            print(f"Value needs to be a maximum of {max_val}.")
            continue
        return val

# Local manage
def action_add_machine() -> None:
    print("\nLocal machine added! (Record of machine stored in configs/instances.json files)")
    name = ask_str("Machine Name: ", min_len=1, max_len=40)

    # sets defaults for local machine simulator & relative AWS instance
    cpu      = 8
    ram_gb   = 16
    disk_gb  = 24
    ssh_port = 22
    backups  = True

    rec = {
        "name": name,
        "cpu": cpu,
        "ram_gb": ram_gb,
        "disk_gb": disk_gb,
        "ssh_port": ssh_port,
        "enable_backup": backups,
    }

    try:
        items = load_instances()
        items.append(rec)
        save_instances(items)
        log(f"Added local machine: {name}")
        print("\n" + "=" * 60)
        print(f"Machine '{name}' successfully added!! Hooray!!")
        print("=" * 60 + "\n")
    except Exception:
        print("\nBoo!! Error trying to save machine...\n")

def action_list_local() -> None:
    items = load_instances()
    if not items:
        print("\nNo local machines saved yet...")
        return
    print("\nLocal Machines:")
    print("-" * 60)
    for i, m in enumerate(items, 1):
        print(f"{i}. {m.get('name','')} | CPU {m.get('cpu')} | RAM {m.get('ram_gb')} GB | "
              f"Disk {m.get('disk_gb')} GB | SSH {m.get('ssh_port')} | Backup {m.get('enable_backup')}")
    print("-" * 60)

# Integration of AWS
def require_aws_env() -> bool:
    missing = [k for k in ("AWS_ACCESS_KEY_ID","AWS_SECRET_ACCESS_KEY","AWS_DEFAULT_REGION") if not os.getenv(k)]
    if missing:
        print("\nAWS Mode requires environment variables to be set in the terminal:")
        print('  export AWS_ACCESS_KEY_ID="..."')
        print('  export AWS_SECRET_ACCESS_KEY="..."')
        print('  export AWS_DEFAULT_REGION="eu-central-1"')
        print("Missing environment variables... Boo!")
        return False
    return True

def action_list_aws() -> None:
    print("\nListing real EC2 instances (AWS mode):")
    if not require_aws_env():
        return
    if not AWS_LISTER.exists():
        print(f"Could not find lister script: {AWS_LISTER} ... Boo!")
        return
    try:
        # Use same Python interpreter to run lister
        subprocess.run([sys.executable, str(AWS_LISTER)], check=False)
        log("Ran AWS EC2 listing...")
    except Exception as e:
        print(f"Error running AWS lister... Boo! ({e})")
        log(f"ERROR running AWS lister: {e}")

# ---------- menu ----------
def main() -> None:
    print("=== Cloud Manager (Local + AWS) ===")
    try:
        ensure_config()
    except Exception:
        # ensure_config already printed/logged failure
        pass

    while True:
        print("\nMenu")
        print("1) Add local machine")
        print("2) List local machines")
        print("3) AWS: List EC2 instances")
        print("4) Exit")
        choice = input("Choose [1-4]: ").strip()
        if choice == "1":
            action_add_machine()
        elif choice == "2":
            action_list_local()
        elif choice == "3":
            action_list_aws()
        elif choice == "4":
            print("\nThank You!! Goodbye!!\n")
            break
        else:
            print("Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted...Boo!! (but it’s okay!)")