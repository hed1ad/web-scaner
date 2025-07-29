import questionary
from dir_scanner import DirScanner


def handle_selection(choice):
    if choice.startswith("1"):
        print("[!] Запуск SQL Injection (заглушка)")
    elif choice.startswith("2"):
        print("[!] Запуск XSS (заглушка)")
    elif choice.startswith("3"):
        print("[*] Запуск Directory Traversal...")
        base_url = questionary.text("Введите URL для сканирования (например https://site.com):").ask()
        if base_url:
            scanner = DirScanner(base_url)
            scanner.scan()
        else:
            print("[!] URL не введён.")
    elif choice.startswith("4"):
        print("[!] Проверка заголовков (заглушка)")
    elif choice.startswith("5"):
        print("[!] Поиск админок (заглушка)")
    elif choice.startswith("6"):
        print("[*] Запуск всего сразу (заглушка)")
    elif choice.startswith("7"):
        print("[?] Пока не реализовано (ввод по номерам)")


def main():
    choice = questionary.select(
        "Выбери пункт для сканирования:",
        choices=[
            "1. SQL Injection (SQLi)",
            "2. Cross-Site Scripting (XSS)",
            "3. Directory Traversal",
            "4. Insecure Headers",
            "5. Exposed Admin Panels",
            "6. Все пункты",
            "7. Комбинация (например 1+2+3)"
        ]
    ).ask()

    if choice:
        handle_selection(choice)
    else:
        print("Ничего не выбрано.")


if __name__ == "__main__":
    main()
