import argparse

from py_version_from_tag import utils


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="py_version_from_tag",
        description="Writes name of the tag to version field of python setup file.",
    )

    parser.add_argument("-p", "--path", required=False, default="pyproject.toml")
    parser.add_argument("-l", "--latest", required=False, action="store_true")
    parser.add_argument("-g", "--git", required=False, default="git")

    args = parser.parse_args()

    tag_func = utils.get_latest_tag if args.latest else utils.get_current_tag

    tag_name = tag_func(args.git)
    utils.replace_version(args.path, utils.get_version_from_tag(tag_name))


if __name__ == "__main__":
    main()
