import os

app_name = os.getenv("APP_NAME", "builder")
app_port = os.getenv("APP_PORT", "5001")

print(f"app_name={app_name} app_port={app_port}")