import requests
import argparse

class DirScanner:
    def __init__(self, base_url: str, wordlist_path: str):
        self.base_url = base_url.rstrip("/") + "/"
        self.wordlist_path = wordlist_path
        self.directories = self.load_wordlist()

    def load_wordlist(self) -> list:
        try:
            with open(self.wordlist_path, "r", encoding="utf-8") as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"[ERR] Wordlist file not found: {self.wordlist_path}")
            return []

    def scan(self):
        print(f"[+] Starting scan: {self.base_url}")
        print("-" * 50)

        for path in self.directories:
            full_url = self.base_url + path
            try:
                response = requests.get(full_url, timeout=5)
                status = response.status_code

                if status == 200:
                    print(f"[200] ✅ Found: {full_url}")
                elif status == 403:
                    print(f"[403] 🚫 Forbidden: {full_url}")
                elif status == 401:
                    print(f"[401] 🔒 Unauthorized: {full_url}")
                elif status in (301, 302):
                    print(
                        f"[{status}] 🔁 Redirect: {full_url} → {response.headers.get('Location')}"
                    )
                elif status == 404:
                    print(f"[404] ❌ Not Found: {full_url}")
                else:
                    print(f"[{status}] ℹ️ Other: {full_url}")

            except requests.exceptions.RequestException as e:
                print(f"[ERR] ⚠️ Error on {full_url} — {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Directory scanner tool")
    parser.add_argument("url", help="URL from scan")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist file")

    args = parser.parse_args()

    scanner = DirScanner(base_url=args.url, wordlist_path=args.wordlist)
    scanner.scan()
