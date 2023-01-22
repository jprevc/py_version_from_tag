import argparse
import pathlib

from py_version_from_tag import utils


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="py_version_from_tag",
        description="Writes name of the tag to version field of python setup file.",
    )

    parser.add_argument(
        "-p",
        "--path",
        required=False,
        default=utils.DEFAULT_PYPROJECT_PATH,
        help="Path to pyproject.toml file, if not provided, it will be assumed that the file is placed in the current"
        "working directory, or in 'root', if that option was used.",
    )
    parser.add_argument(
        "-l",
        "--latest",
        required=False,
        action="store_true",
        help="If used, the latest tag in git history will be used. If this option is not used, the tag on the current "
        "commit will be used and the program will fail if current commit is not tagged.",
    )
    parser.add_argument(
        "-g",
        "--git",
        required=False,
        default="git",
        help="Path to git executable. If not provided, it will be assumed that git is placed on environment PATH.",
    )
    parser.add_argument(
        "-r",
        "--root",
        required=False,
        default=utils.DEFAULT_ROOT,
        help="Root of the project repository, this will be used for searching for pyproject.toml and for finding tags "
        "in the repository.",
    )
    parser.add_argument(
        "-i",
        "--ignore-pep",
        required=False,
        action="store_true",
        help="If used, version written to pyproject.toml will be the same string as used as a tag name. Otherwise, "
        "version written to pyproject.toml will be a parsed version of input tag and it will conform to PEP440 rules "
        "for python packaging versioning. ",
    )

    args = parser.parse_args()

    git_command_runner = utils.GitLatestTagCommandRunner if args.latest else utils.GitCurrentTagCommandRunner
    toml_path = pathlib.Path(args.root) / args.path

    tag_name = git_command_runner(args.git, args.root).run()
    utils.replace_version(toml_path, utils.get_version_from_tag(tag_name, args.ignore_pep))


if __name__ == "__main__":
    main()
