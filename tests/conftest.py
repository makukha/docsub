from pathlib import Path
import shutil
import sys

from pytest import fixture


@fixture
def data_path(tmp_path, request) -> Path:
    filename = Path(request.module.__file__).resolve()
    test_dir = filename.parent / filename.stem
    if test_dir.is_dir():
        shutil.copytree(test_dir, tmp_path, dirs_exist_ok=True)

    return tmp_path


@fixture(scope='session')
def python() -> str:
    """
    Fixture returns path to current Python executable.
    """
    return sys.executable
