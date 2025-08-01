import pytest
from dir_scanner import DirScanner

@pytest.fixture
def mock_wordlist(tmp_path):
    wordlist_file = tmp_path / "wordlist.txt"
    wordlist_file.write_text("images")
    return str(wordlist_file)

@pytest.fixture
def scanner(mock_wordlist):
    return DirScanner(base_url="https://ya.ru", wordlist_path=mock_wordlist)

def test_scan_real_request(scanner, capsys):
    """Тестирует реальный HTTP-запрос без моков"""
    scanner.scan()
    
    captured = capsys.readouterr()
    assert any(
        code in captured.out 
        for code in ["[200]", "[403]", "[404]", "[300]"]
    )
