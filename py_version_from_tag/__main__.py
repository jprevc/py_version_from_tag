import argparse
import pathlib

from py_version_from_tag import utils


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="py_version_from_tag",
        description="Writes name of the tag to version field of python setup file.",
    )

    parser.add_argument("-p", "--path", required=False, default=utils.DEFAULT_PYPROJECT_PATH)
    parser.add_argument("-l", "--latest", required=False, action="store_true")
    parser.add_argument("-g", "--git", required=False, default="git")
    parser.add_argument("-r", "--root", required=False, default=utils.DEFAULT_ROOT)

    args = parser.parse_args()

    git_command_runner = utils.GitLatestTagCommandRunner if args.latest else utils.GitCurrentTagCommandRunner
    toml_path = pathlib.Path(args.root) / args.path

    tag_name = git_command_runner(args.git, args.root).run()
    utils.replace_version(toml_path, utils.get_version_from_tag(tag_name))


if __name__ == "__main__":
    main()
