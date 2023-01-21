import pathlib
import subprocess
from typing import Generator, Callable

import pytest
import toml

from py_version_from_tag import utils
from tests import mocks


@pytest.mark.parametrize(
    "tag_name,expected",
    (("v3.2.1", "3.2.1"), ("3.2.1", "3.2.1"), ("v1.2", "1.2"), ("v0.2_alpha", "0.2_alpha"), ("v1.2_v", "1.2_v")),
)
def test_get_version_from_tag_removes_v_prefix(tag_name: str, expected: str):
    assert utils.get_version_from_tag(tag_name) == expected


@pytest.mark.parametrize("cli_stdout, expected", [(b"v3.1.0\n", "v3.1.0"), (b"v3.1.0\nv4.1.3\n", "v3.1.0")])
@pytest.mark.parametrize("get_tag_func", [utils.get_current_tag, utils.get_latest_tag])
def test_get_tag(monkeypatch, cli_stdout, expected, get_tag_func):
    mock_subprocess_run_func = mocks.create_mock_subprocess_return_object(cli_stdout)
    monkeypatch.setattr(subprocess, "run", mock_subprocess_run_func)

    assert get_tag_func() == expected


@pytest.fixture(name="toml_path")
def toml_path_fixture() -> pathlib.Path:
    return pathlib.Path(__file__).parent / "res" / "test_pyproject.toml"


@pytest.fixture(name="restore_toml")
def restore_toml_fixture(toml_path: pathlib.Path) -> Generator:
    with open(toml_path, "r", encoding="utf8") as file:
        toml_content = toml.load(file)

    yield

    with open(toml_path, "w", encoding="utf8") as file:
        toml.dump(toml_content, file)


@pytest.mark.parametrize("new_string", ["new_test_string", "v3.2.4", "3.2.4", "1.2.3_alpha"])
def test_replace_version(
    toml_path: pathlib.Path, restore_toml: Callable, new_string: str  # pylint: disable=unused-argument
) -> None:
    utils.replace_version(toml_path, "new_test_string")

    with open(toml_path, "r", encoding="utf8") as file:
        toml_content = toml.load(file)

    assert toml_content["project"]["version"] == "new_test_string"


def test_get_current_tag_raises_error_if_there_is_no_tag(monkeypatch):
    mock_subprocess_run_func = mocks.create_mock_subprocess_return_object(b"")
    monkeypatch.setattr(subprocess, "run", mock_subprocess_run_func)

    with pytest.raises(RuntimeError):
        utils.get_current_tag()
