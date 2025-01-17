from docsub import Environment


def test_tmpdir(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    env = Environment.from_config_file(None)
    tmp = env.provide_temp_dir('testing')
    assert tmp.exists()
    assert tmp.is_dir()
    assert tmp == tmp_path / '.docsub' / 'tmp_testing'
