#!/usr/bin/env python3
"""Directory scanner tool to discover hidden paths on a web server."""

import argparse
import sys
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


class DirScanner:
    def __init__(self, base_url: str, wordlist_path: str, filter_codes: list = None, threads: int = 20):
        self.base_url = base_url.rstrip("/") + "/"
        self.wordlist_path = wordlist_path
        self.filter_codes = filter_codes if filter_codes else []
        self.threads = threads
        self.directories = self.load_wordlist()

    def load_wordlist(self) -> list:
        try:
            with open(self.wordlist_path, "r", encoding="utf-8") as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"[ERR] Wordlist file not found: {self.wordlist_path}")
            sys.exit(1)

    def scan(self):
        print(f"[+] Starting threaded scan: {self.base_url}")
        if self.filter_codes:
            print(f"[+] Filtering status codes: {', '.join(map(str, self.filter_codes))}")
        print(f"[+] Threads: {self.threads}")
        print("-" * 50)

        def scan_path(path):
            full_url = self.base_url + path
            try:
                response = requests.get(full_url, timeout=5)
                status = response.status_code

                if self.filter_codes and status not in self.filter_codes:
                    return

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

        start = time.time()
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(scan_path, path) for path in self.directories]
            for _ in as_completed(futures):
                pass
        end = time.time()

        elapsed = end - start
        total = len(self.directories)
        speed = total / elapsed if elapsed > 0 else 0

        print(f"100% | {'█'*50}| {total}/{total}  {elapsed:.2f} sec, {speed:.2f}it/s]")




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Directory scanner tool")
    parser.add_argument("url", help="URL to scan")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist file")
    parser.add_argument("--codes", help="Filter status codes (e.g., '200,403,301')")
    parser.add_argument("--threads", type=int, default=20, help="Number of threads (default: 20)")

    args = parser.parse_args()

    status_codes = []
    if args.codes:
        try:
            status_codes = [int(code.strip()) for code in args.codes.split(",")]
        except ValueError:
            print("[ERR] Invalid status codes format.('200,403').")
            sys.exit(1)

    scanner = DirScanner(
        base_url=args.url,
        wordlist_path=args.wordlist,
        filter_codes=status_codes,
        threads=args.threads
    )
    scanner.scan()
