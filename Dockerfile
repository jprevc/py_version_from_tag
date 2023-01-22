FROM python:3.10-slim

RUN apt-get -y update
RUN apt-get -y install git

WORKDIR /app

COPY py_version_from_tag py_version_from_tag
COPY setup.py .
COPY pyproject.toml .
COPY README.md .

VOLUME app/root

ENV PYVERSION_ROOT="/app/root"

RUN ["python3", "-m", "pip", "install", "-e", "."]

ENTRYPOINT ["python3", "-m", "py_version_from_tag"]
