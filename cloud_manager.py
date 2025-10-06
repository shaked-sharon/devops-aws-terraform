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
from datetime import datetime

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
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{ts} UTC | {msg}\n")

# for config help
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

def ask_os(prompt: str) -> str:
    allowed = {"ubuntu", "centos", "windows", "macos"}
    while True:
        val = input(prompt).strip().lower()
        if val in allowed:
            return val
        print("Supported OS Only: Ubuntu, CentOS, Windows, MacOS. Boo!")

def ask_int(prompt: str, *, min_val=None, max_val=None) -> int:
    while True:
        raw = input(prompt).strip()
        if not re.fullmatch(r"-?\d+", raw):
            print("Please use whole numbers...")
            continue
        val = int(raw)
        if min_val is not None and val < min_val:
            print(f"Value needs to be ≥ {min_val}.")
            continue
        if max_val is not None and val > max_val:
            print(f"Value needs to be ≤ {max_val}.")
            continue
        return val

def ask_port(prompt: str) -> int:
    # Valid TCP ports: 1-65535
    return ask_int(prompt, min_val=1, max_val=65535)

def ask_yes_no(prompt: str, default=True) -> bool:
    # Default True > Y/n -- Default False > y/N
    hint = "Y/n" if default else "y/N"
    while True:
        raw = input(f"{prompt} [{hint}]: ").strip().lower()
        if raw == "" and default is not None:
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("Please answer y or n.")

# Local manage
def action_add_machine() -> None:
    print("\nAdd local machine record (will be stored in configs/instances.json files)")
    name = ask_str("Machine Name: ", min_len=1, max_len=40)
    os_type = ask_os("OS (Ubuntu, CentOS, Windows, MacOS): ")  # added OS prompt
    vcpu = ask_int("vCPUs (1-8): ", min_val=1, max_val=8)
    ram_gb = ask_int("RAM in GB (1-64): ", min_val=1, max_val=64)
    disk_gb = ask_int("Disk Size in GB (8-1024): ", min_val=8, max_val=1024)
    ssh_port = ask_port("SSH Port (Generally 22): ")
    backups = ask_yes_no("Do you want to enable backups?", default=True)

    rec = {
        "name": name,
        "os": os_type,  # store OS choice
        "vcpu": vcpu,
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
        print(f"Machine '{name}' successfully added!! Hooray!!")
    except Exception:
        print("Boo!! Error trying to save machine...")

def action_list_local() -> None:
    items = load_instances()
    if not items:
        print("\nNo local machines saved yet...")
        return
    print("\nLocal Machines:")
    print("-" * 60)
    for i, m in enumerate(items, 1):
        print(f"{i}. {m.get('name','')} | OS {m.get('os','')} | vCPU {m.get('vcpu')} | RAM {m.get('ram_gb')} GB | "
              f"Disk {m.get('disk_gb')} GB | SSH {m.get('ssh_port')} | Backup {m.get('enable_backup')}")
    print("-" * 60)

# ---------- AWS integration ----------
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
        print("Finished listing EC2 instances. Success!! Hooray!!")
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
            print("Thank You!! Goodbye!!")
            break
        else:
            print("Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted...Boo!! (but it’s okay!)")