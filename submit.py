import os
import json
import hmac
import hashlib
from datetime import datetime, timezone
import requests

url = "https://b12.io/apply/submission"

run_link = \
    f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}"

body_dict = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "name": "Kirill Levin",
    "email": "levinkirillkirilllevin@example.com",
    "resume_link": "https://www.linkedin.com/in/levin-kirill/",
    "repository_link": "https://github.com/Kirill-Levin-dev/",
    "action_run_link": run_link
}

body = json.dumps(
    body_dict,
    separators=(',', ':'),
    sort_keys=True
)

secret = os.environ["SIGNING_SECRET"].encode()

signature = hmac.new(
    secret,
    body.encode("utf-8"),
    hashlib.sha256
).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}"
}

response = requests.post(url, data=body, headers=headers)

print("=== SUBMISSION START ===")
print("Request body:", body_dict)
print("Status:", response.status_code)
print("Response:", response.text)
print("=== SUBMISSION END ===")
