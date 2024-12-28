from subprocess import check_output


def test_cat(data_path, python, monkeypatch):
    monkeypatch.chdir(data_path)
    # stdout
    result = check_output([python, '-m', 'docsub', 'README.md'], text=True)
    assert result == (data_path / 'result.md').read_text()
    # in-place
    check_output([python, '-m', 'docsub', '-i', 'README.md'])
    assert (data_path / 'README.md').read_text() == (data_path / 'RESULT.md').read_text()
