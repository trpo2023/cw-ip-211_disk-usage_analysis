import pytest

from main import show_command_list, remove_files, Cleaner


def test_show_command_list(capsys):
    show_command_list()
    captured = capsys.readouterr()
    assert "\033[94mList of commands:\n" in captured.out
    assert "\033[34ma - \033[37mAdd a folder to explore\n" in captured.out
    assert "\033[34md - \033[37mDelete selected file/folder\n" in captured.out
    assert "\033[34mg - \033[37mShow disk-usage analysis\n" in captured.out
    assert "\033[34mh - \033[37mShow list of commands\n" in captured.out
    assert "\033[34mq - \033[37mQuit" in captured.out


def test_Cleaner_convert_file_size():
    cleaner = Cleaner()
    assert cleaner.convert_file_size(1023) == "1023.00 B"
    assert cleaner.convert_file_size(1024) == "1.00 KB"
    assert cleaner.convert_file_size(1024**2) == "1.00 MB"
    assert cleaner.convert_file_size(1024**3) == "1.00 GB"
    assert cleaner.convert_file_size(1024**4) == "1.00 TB"


@pytest.fixture
def test_dir(tmp_path):
    test_file1 = tmp_path / "test_file1.txt"
    test_file1.write_text("test")
    test_subdir = tmp_path / "test_subdir"
    test_subdir.mkdir()
    test_file2 = test_subdir / "test_file2.txt"
    test_file2.write_text("test")
    return tmp_path


def test_Cleaner_get_directory_sizes(test_dir):
    cleaner = Cleaner()
    result = cleaner.get_directory_sizes(test_dir)
    assert "test_subdir: 4.00 B" in result
    assert "test_file1.txt: 4.00 B" in result


def test_remove_files_accept(test_dir, capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda x: 'y')
    remove_files(test_dir)
    captured = capsys.readouterr()
    assert "\033[94mDelete this file(s)?\033[37m\n" in captured.out
    assert "test_file1.txt\n" in captured.out
    assert "test_subdir\n" in captured.out
    assert "\033[31m'y' - yes\n" in captured.out
    assert "'n' - no\n" in captured.out
    assert "\033[93mSuccessfully cleaned!\n" in captured.out


def test_remove_files_reject(test_dir, capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda x: 'n')
    remove_files(test_dir)
    captured = capsys.readouterr()
    assert "Delete this file(s)?" in captured.out
    assert "test_file1.txt" in captured.out
    assert "test_subdir" in captured.out
    assert "'y' - yes" in captured.out
    assert "'n' - no" in captured.out
    assert "Successfully cleaned!" not in captured.out
