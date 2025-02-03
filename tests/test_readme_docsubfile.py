import re
import shlex

from click.testing import CliRunner

from docsub.__main__ import cli


def test_readme_docsubfile_apply(data_path, python, monkeypatch):
    monkeypatch.chdir(data_path)
    result = CliRunner(mix_stderr=False).invoke(cli, ['apply', '__input__.md'])
    assert not result.stderr
    assert result.exit_code == 0
    expected = (data_path / '__result__.md').read_text()
    assert result.stdout == expected


def strip_docsub(string: str) -> str:
    return re.sub(r'^<!-- docsub: .*-->\n', '', string, flags=re.MULTILINE)


def test_readme_docsubfile_x(data_path, python, monkeypatch):
    monkeypatch.chdir(data_path)
    src = (data_path / '__input__.md').read_text()
    match = re.search(r'^<!-- docsub: x (?P<cmd>.+) -->$', src, flags=re.MULTILINE)
    assert match is not None
    args = shlex.split(match.group('cmd'))
    result = CliRunner(mix_stderr=False).invoke(cli, ['x', *args])
    assert not result.stderr
    assert result.exit_code == 0
    expected = strip_docsub((data_path / '__result__.txt').read_text())
    assert result.stdout == expected


def test_readme_docsubfile_log_hello(data_path, python, monkeypatch):
    monkeypatch.chdir(data_path)
    result = CliRunner(mix_stderr=False).invoke(cli, ['x', 'log-hello', 'Alice', 'Bob'])
    assert not result.stderr
    assert result.exit_code == 0
    logged = (data_path / '.docsub/tmp_log_hello/hello.log').read_text().strip()
    assert logged == "said hello to ('Alice', 'Bob')"
