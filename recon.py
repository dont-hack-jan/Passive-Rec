import os
import sys
import requests
import shodan
import json
from urllib.parse import quote

#Do not forget to change this API part
SHODAN_API_KEY = "shodan_api_key"
GITHUB_TOKEN = "github_api_token"

def save_output(output_dir, filename, data):
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
        f.write(data)

def run_cmd(command, output_path):
    result = os.popen(command).read()
    save_output(*output_path, result)

def run_whois(target, output_dir):
    run_cmd(f"whois {target}", (output_dir, "whois.txt"))

def run_dns(target, output_dir):
    print("[*] Running dig and host lookups...")
    run_cmd(f"dig {target} ANY +noall +answer", (output_dir, "dig.txt"))
    run_cmd(f"host -t mx {target}", (output_dir, "host-mx.txt"))
    run_cmd(f"host -t txt {target}", (output_dir, "host-txt.txt"))

def run_amass(target, output_dir):
    print("[*] Running Amass (passive)...")
    run_cmd(f"amass enum -passive -d {target}", (output_dir, "amass.txt"))

def run_subfinder(target, output_dir):
    print("[*] Running Subfinder...")
    run_cmd(f"subfinder -d {target} -silent", (output_dir, "subfinder.txt"))

def get_crtsh(target, output_dir):
    print("[*] Fetching crt.sh...")
    url = f"https://crt.sh/?q=%25.{quote(target)}&output=json"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            names = {entry['name_value'] for entry in r.json()}
            save_output(output_dir, "crtsh.txt", "\n".join(sorted(names)))
    except Exception as e:
        print(f"[!] crt.sh error: {e}")

def get_wayback(target, output_dir):
    print("[*] Fetching Wayback Machine URLs...")
    url = f"http://web.archive.org/cdx/search/cdx?url=*{quote(target)}/*&output=text&fl=original&collapse=urlkey"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            save_output(output_dir, "wayback.txt", r.text)
    except Exception as e:
        print(f"[!] Wayback error: {e}")

def run_shodan(target, output_dir):
    print("[*] Querying Shodan...")
    try:
        api = shodan.Shodan(SHODAN_API_KEY)
        results = api.search(f"hostname:{target}")
        with open(os.path.join(output_dir, "shodan.json"), "w", encoding='utf-8') as f:
            json.dump(results, f, indent=2)
    except Exception as e:
        print(f"[!] Shodan error: {e}")

def github_search(target, output_dir):
    print("[*] Searching GitHub code...")
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/search/code?q={target}+in:file"
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            save_output(output_dir, "github.json", json.dumps(r.json(), indent=2))
        else:
            save_output(output_dir, "github.txt", f"Status {r.status_code}: {r.text}")
    except Exception as e:
        print(f"[!] GitHub API error: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 recon.py <target-domain>")
        sys.exit(1)

    target = sys.argv[1]
    output_dir = f"{target}"
    os.makedirs(output_dir, exist_ok=True)

    print(f"[+] Starting passive recon on: {target}\nOutput: {output_dir}")

    run_whois(target, output_dir)
    run_dns(target, output_dir)
    run_amass(target, output_dir)
    run_subfinder(target, output_dir)
    get_crtsh(target, output_dir)
    get_wayback(target, output_dir)
    run_shodan(target, output_dir)
    github_search(target, output_dir)

    print(f"[✓] Recon complete. Results saved in {output_dir}/")

if __name__ == "__main__":
    main()
