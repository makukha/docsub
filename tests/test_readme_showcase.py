from subprocess import check_output


def test_readme_showcase(data_path, python, monkeypatch):
    monkeypatch.chdir(data_path)
    result = check_output(
        args=[python, '-m', 'docsub', 'sync', '__input__.md'],
        text=True,
    )
    assert result == (data_path / '__result__.md').read_text()
