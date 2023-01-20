import subprocess
import toml

def main():
    try:
        tag_name = subprocess.run("git describe --tags --abbrev=0", stdout=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as exc:
        if exc.returncode == 128:
            raise RuntimeError("No tags found in git history.") from exc
        raise exc

    tag_name = tag_name.stdout.decode("utf8").split("\n")[0]

    with open("pyproject.toml", "r", encoding="utf8") as file:
        pyproject_toml = toml.load(file)

    pyproject_toml["project"]["version"] = tag_name

    with open("pyproject.toml", "w", encoding="utf8") as file:
        toml.dump(pyproject_toml, file)


if __name__ == "__main__":
    main()
