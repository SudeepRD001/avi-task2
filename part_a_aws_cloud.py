import requests
import urllib3

# Disable warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
CONTROLLER = "https://35.200.176.139"
USERNAME = "hiring-2"
PASSWORD = "hiring-2"
CLOUD_NAME = "aws-cloud-sudeepdoddamani51"
VERIFY_SSL = False

# Start session
session = requests.Session()

def login():
    url = f"{CONTROLLER}/login"
    resp = session.post(url, json={"username": USERNAME, "password": PASSWORD}, verify=VERIFY_SSL)
    if resp.status_code != 200:
        print("❌ Login failed.")
        exit()
    print("✅ Logged in successfully.")
    return session.cookies.get("csrftoken")

def create_aws_cloud(csrf_token):
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
        "Referer": CONTROLLER,
        "Cookie": f"csrftoken={csrf_token}; avi-sessionid={session.cookies.get('avi-sessionid')}"
    }

    payload = {
        "name": CLOUD_NAME,
        "vtype": "CLOUD_AWS",
        "aws_configuration": {
            "access_key_id": "dummy-access-key",
            "secret_access_key": "dummy-secret-key",
            "region": "us-west-1",
            "vpc_id": "vpc-dummy"
        }
    }

    resp = session.post(f"{CONTROLLER}/api/cloud", headers=headers, json=payload, verify=VERIFY_SSL)
    if resp.status_code in [200, 201]:
        print(f"✅ AWS Cloud '{CLOUD_NAME}' created.")
    elif resp.status_code == 409:
        print(f"ℹ️ Cloud '{CLOUD_NAME}' already exists.")
    else:
        print(f"❌ Failed to create cloud: {resp.status_code}\n{resp.text}")

def verify_cloud_status(csrf_token):
    headers = {
        "Content-Type": "application/json",
        "Referer": CONTROLLER,
        "Cookie": f"csrftoken={csrf_token}; avi-sessionid={session.cookies.get('avi-sessionid')}"
    }

    resp = session.get(f"{CONTROLLER}/api/cloud", headers=headers, verify=VERIFY_SSL)
    if resp.status_code != 200:
        print("❌ Failed to fetch cloud list.")
        return

    clouds = resp.json().get("results", [])
    for cloud in clouds:
        if cloud["name"] == CLOUD_NAME:
            print(f"\n✅ Found cloud: {cloud['name']}")
            print(f"  - Type: {cloud['vtype']}")
            print(f"  - State: {cloud.get('cloud_state', 'Unknown')}")
            return
    print("❌ Cloud not found.")

# Execute Part A
if __name__ == "__main__":
    csrf = login()
    create_aws_cloud(csrf)
    verify_cloud_status(csrf)
