from __future__ import annotations

import subprocess
import pathlib

import toml


def get_latest_tag(git_path: str = "git") -> str:
    """
    Obtains the latest tag name (counting from the current commit) by running a git command on CLI.

    :raises RuntimeError: If no tags could be found in git history.
    :raises subprocess.CalledProcessError: If some unknown issue occured when running git command on CLI.
    """
    try:
        tag_name = subprocess.run(f"{git_path} describe --tags --abbrev=0", stdout=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as exc:
        if exc.returncode == 128:
            raise RuntimeError("No tags found in git history.") from exc
        raise exc

    return tag_name.stdout.decode("utf8").split("\n")[0]


def get_current_tag(git_path: str = "git") -> str:
    """
    Returns tag of the current commit. If there are more than one tags on the commit, only the first one found will be
    returned.

    :return: Tag name of the current commit.

    :raises RuntimeError: If no tags could be found on the current commit.
    """
    tag_name_raw = subprocess.run(f"{git_path} tag --points-at HEAD", stdout=subprocess.PIPE, check=True)

    tag_name = tag_name_raw.stdout.decode("utf8").split("\n")[0]

    if tag_name == "":
        raise RuntimeError("Could not find any tags on the current commit.")

    return tag_name


def get_version_from_tag(tag: str) -> str:
    """
    Obtains version string from tag name.

    :param tag: Tag string from which version string will be obtained.

    :return: Version string in form "X.Y.Z"
    """

    if tag.startswith("v"):
        return tag[1:]

    return tag


def replace_version(setup_file_path: str | pathlib.Path, new_string: str) -> None:
    """
    Replaces version string in python setup file.

    :param setup_file_path: Path to pyproject.toml file.
    :param new_string: New string to be written to 'version' field.
    """
    with open(setup_file_path, encoding="utf8") as file:
        pyproject_toml = toml.load(file)

    pyproject_toml["project"]["version"] = new_string

    with open(setup_file_path, "w", encoding="utf8") as file:
        toml.dump(pyproject_toml, file)
