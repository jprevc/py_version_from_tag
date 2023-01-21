# py_version_from_tag
py_version_from_tag is a simple CLI tool that will obtain the tag name of the current commit, extract version from it
and write it to python setup file.

This can be very useful in automatic build processes, so you don't need to manually update version string in setup files
when you have already written it as a tag name.

Usage
----------

Prerequisites:
- Your working directory should be placed on a valid git repository
- The current commit (HEAD) should be tagged


    python -m pip install py_version_from_tag -p {path to pyproject.toml}
    python -m pip py_version_from_tag

Alternatively, if the current commit is not tagged, but you want to use the latest commit as version,
you can use the *-l* switch, like this:

    python -m pip py_version_from_tag -l

For full list of available options, run

    python -m pip py_version_from_tag -h

Notes
----------
- Currently, only pyproject.toml file is supported as a setup file
- Tag name should contain a valid version information, for example: "v3.1.2", "1.2.3", "v4.5.6_alpha" are all examples
of valid tag version names
