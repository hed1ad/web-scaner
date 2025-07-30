#!/usr/bin/env python3
"""Directory scanner tool to discover hidden paths on a web server."""

import argparse
import sys
import requests


class DirScanner:
    """Scans a web server for directories using a wordlist."""

    def __init__(self, base_url: str, wordlist_path: str, filter_codes: list = None):
        """Initialize the scanner with target URL, wordlist, and optional status code filter.

        Args:
            base_url (str): Target URL to scan.
            wordlist_path (str): Path to the wordlist file.
            filter_codes (list, optional): List of HTTP status codes to filter. Defaults to None.
        """
        self.base_url = base_url.rstrip("/") + "/"
        self.wordlist_path = wordlist_path
        self.filter_codes = filter_codes if filter_codes else []
        self.directories = self.load_wordlist()

    def load_wordlist(self) -> list:
        """Load and parse the wordlist file.

        Returns:
            list: List of directory paths to scan.

        Raises:
            SystemExit: If the wordlist file is not found.
        """
        try:
            with open(self.wordlist_path, "r", encoding="utf-8") as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"[ERR] Wordlist file not found: {self.wordlist_path}")
            sys.exit(1)

    def scan(self):
        """Scan the target URL and print discovered paths based on HTTP status codes."""
        print(f"[+] Starting scan: {self.base_url}")
        if self.filter_codes:
            print(f"[+] Filtering status codes: {', '.join(map(str, self.filter_codes))}")
        print("-" * 50)

        for path in self.directories:
            full_url = self.base_url + path
            try:
                response = requests.get(full_url, timeout=5)
                status = response.status_code

                if self.filter_codes and status not in self.filter_codes:
                    continue

                if status == 200:
                    print(f"[200] ✅ Found: {full_url}")
                elif status == 403:
                    print(f"[403] 🚫 Forbidden: {full_url}")
                elif status == 401:
                    print(f"[401] 🔒 Unauthorized: {full_url}")
                elif status in (301, 302):
                    location = response.headers.get("Location")
                    print(f"[{status}] 🔁 Redirect: {full_url} → {location}")
                elif status == 404:
                    print(f"[404] ❌ Not Found: {full_url}")
                else:
                    print(f"[{status}] ℹ️ Other: {full_url}")

            except requests.exceptions.RequestException as e:
                print(f"[ERR] ⚠️ Error on {full_url} — {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Directory scanner tool")
    parser.add_argument("url", help="URL to scan")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist file")
    parser.add_argument("--codes", help="Filter status codes (e.g., '200,403,301')")

    args = parser.parse_args()

    status_codes = []
    if args.codes:
        try:
            status_codes = [int(code.strip()) for code in args.codes.split(",")]
        except ValueError:
            print("[ERR] Invalid status codes format.('200,403').")
            sys.exit(1)

    scanner = DirScanner(base_url=args.url, wordlist_path=args.wordlist, filter_codes=status_codes)
    scanner.scan()
