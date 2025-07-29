import requests


class DirScanner:
    def __init__(self, base_url: str, wordlist_path: str = "wordlist.txt"):
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
        print(f"[+] Scanning: {self.base_url}")
        print("-" * 50)

        for path in self.directories:
            url = self.base_url + path
            try:
                response = requests.get(url, timeout=5)
                status = response.status_code

                if status == 200:
                    print(f"[200] ✅ Found: {url}")
                elif status == 403:
                    print(f"[403] 🔒 Forbidden: {url}")
                elif status == 404:
                    print(f"[404] ❌ Not Found: {url}")
                else:
                    print(f"[{status}] ℹ️  {url}")
            except requests.RequestException as e:
                print(f"[ERR] Failed to request {url} — {e}")
