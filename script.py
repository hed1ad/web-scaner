import requests

wordlist = [
    "admin",
    "login",
    "dashboard",
    "auth",
    "panel",
    "config",
    "uploads",
    "api",
    "images",
    "js"
]

def scan_directories(base_url, wordlist):
    if not base_url.endswith('/'):
        base_url += '/'

    print(f"[+] Сканирование сайта: {base_url}")
    print("-" * 50)

    for path in wordlist:
        url = base_url + path.strip()
        try:
            response = requests.get(url, timeout=5)
            status = response.status_code

            if status == 200:
                print(f"[200] ✅ Найдено: {url}")
            elif status == 403:
                print(f"[403] 🚫 Доступ запрещен: {url}")
            elif status == 401:
                print(f"[401] 🔒 Требуется авторизация: {url}")
            elif status == 500:
                print(f"[500] 💥 Ошибка сервера: {url}")
            elif status in (301, 302):
                print(f"[{status}] 🔁 Перенаправление: {url} → {response.headers.get('Location')}")
            elif status == 404:
                print(f"[404] ❌ Не найдено: {url}")
            else:
                print(f"[{status}] ℹ️ Прочее: {url}")

        except requests.exceptions.RequestException as e:
            print(f"[ERR] ⚠️ Ошибка при запросе {url} — {e}")

# 🖐 Запрос URL у пользователя
if __name__ == "__main__":
    base_url = input("Введите URL для сканирования: ").strip()
    scan_directories(base_url, wordlist)
