def show_banner():
    banner = r"""
     _______  ______  __    __ 
    |__   __||___  /  \ \  / / 
       | |     / /    \ \/ /  
       | |    / /      >  <   
       | |   / /__    / /\ \  
       |_|  /_____|  /_/  \_\  v1.0
    """
    
    print("\033[1;36m" + banner + "\033[0m")
    print("\033[1;32m{:=^60}\033[0m".format(" ZOV Vulnerability Scanner "))
    print("\033[1;33m• Author:\033[0m hed1ad, erz")
    print("\033[1;33m• GitHub:\033[0m github.com/hed1ad/zovscan")
    print("\033[1;33m• Supported Checks:\033[0m")
    print("  - SQL Injection (SQLi)")
    print("  - Cross-Site Scripting (XSS)")
    print("  - Directory Traversal")
    print("  - Insecure Headers")
    print("  - Exposed Admin Panels")
    print("\033[1;32m{:=^60}\033[0m".format(""))
    print("Usage: zovscan --target https://example.com --scan all\n")
    print("Press CTRL+C to stop scanning at any time")

from dir_scanner import DirScanner

if __name__ == "__main__":
    url = input("Enter URL to scan: ").strip()
    scanner = DirScanner(base_url=url, wordlist_path="wordlist.txt")
    scanner.scan()