import click
from docsub import Environment
from docsub.__main__ import sync


def test_tmpdir(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    env = Environment.load(click.Context(sync))
    tmp = env.get_temp_dir('testing')
    assert tmp.exists()
    assert tmp.is_dir()
    assert tmp == tmp_path / '.docsub' / 'tmp_testing'
