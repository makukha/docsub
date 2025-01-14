import re
import shlex
from subprocess import check_output


def test_readme_docsubfile_apply(data_path, python, monkeypatch):
    monkeypatch.chdir(data_path)
    result = check_output(
        args=[python, '-m', 'docsub', 'apply', '__input__.md'],
        text=True,
    )
    expected = (data_path / '__result__.md').read_text()
    assert result == expected


def strip_docsub(string: str) -> str:
    return re.sub(r'^<!-- docsub: .*-->\n', '', string, flags=re.MULTILINE)


def test_readme_docsubfile_x(data_path, python, monkeypatch):
    monkeypatch.chdir(data_path)
    input_md = (data_path / '__input__.md').read_text()
    match = re.search(r'^<!-- docsub: x (?P<cmd>.+) -->$', input_md, flags=re.MULTILINE)
    result = check_output(
        args=[python, '-m', 'docsub', 'x', *shlex.split(match.group('cmd'))],
        text=True,
    )
    expected = strip_docsub((data_path / '__result__.md').read_text())
    assert result == expected
