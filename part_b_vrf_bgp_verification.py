import requests
import urllib3

# Disable warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
CONTROLLER = "https://35.200.176.139"
USERNAME = "admin"
PASSWORD = "root@123"
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

def check_vrf_bgp(csrf_token):
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
        "Referer": CONTROLLER,
        "Cookie": f"csrftoken={csrf_token}; avi-sessionid={session.cookies.get('avi-sessionid')}"
    }

    print("\n🔍 Fetching VRF Contexts for BGP settings...")
    resp = session.get(f"{CONTROLLER}/api/vrfcontext", headers=headers, verify=VERIFY_SSL)
    if resp.status_code != 200:
        print("❌ Failed to fetch VRF contexts.")
        print(resp.text)
        return

    vrfs = resp.json().get("results", [])
    if not vrfs:
        print("ℹ️ No VRF contexts found.")
        return

    for vrf in vrfs:
        print(f"\n✅ VRF: {vrf.get('name')}")
        bgp = vrf.get("bgp_profile")
        if bgp:
            print("  - BGP Configuration Found:")
            print(f"    • local_as: {bgp.get('local_as')}")
            print(f"    • ibgp: {bgp.get('ibgp')}")
            print(f"    • shutdown: {bgp.get('shutdown')}")
        else:
            print("  - ℹ️ No BGP profile configured for this VRF.")

# Run Part B
if __name__ == "__main__":
    csrf = login()
    check_vrf_bgp(csrf)
