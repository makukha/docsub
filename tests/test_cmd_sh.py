from subprocess import check_output


def test_sh(data_path, python, monkeypatch):
    monkeypatch.chdir(data_path)
    result = check_output([python, '-m', 'docsub', 'input.md'], text=True)
    assert result == (data_path / 'result.md').read_text()
