# Python | builder_client.py

## What This Script Does

- Reads 2 environment variables: `APP_NAME` (defaults to "builder") & `APP_PORT` (defaults to "5001")
- Prints them as single line, then exits
- Small script used to test Docker & Jenkins pipeline

## How to Use

- `Dockerfile` in project root copies script into a Docker container
- Jenkins runs pipeline > builds container > runs script inside it > pushes image to Docker Hub
- CI/CD flow works E2E

## Files

- **builder_client.py** – the actual Python script
- **README.md** – this file

---

_Last update: Feb. 2026_
