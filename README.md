# Dialect map: static-data job ⚙️

### About
This repository contains the data-ingestion job to propagate _static_ data to the database.
The _static_ term makes reference to the [Dialect map data][dialect-map-data] slow change pace.

It will be used in combination with the [Dialect map IO][dialect-map-io] package, which provides the file parsing
and API connection capabilities, as well as the [Dialect map private API][dialect-map-api], which is the component
exposing a way of inserting records into the underlying database.


### Development
To install all the source code that is necessary to operate with this project:

```sh
git clone --recurse-submodules https://github.com/dialect-map/dialect-map-job-static
```

For cases where the project has already been cloned:

```sh
git submodule update --init --recursive
```

The repository defined as submodule will follow their own development pace.
For cases where the submodule repository has been updated on GitHub, and want
to propagate those changes to your local copy:

```sh
git submodule update --remote
```


### Dependencies
Python dependencies are specified within the `requirements.txt` and `requirements-dev.txt` files.
In terms of binary dependencies, the project depends on a Golang / CLI tool called [jd][jd-github-repo].
This tool is used to generate the differences (_diffs_) between consecutive versions of
the [dialect-map-data][dialect-map-data] submodule data files

In order to install the development packages, non-python dependencies and commit hooks:
```sh
make install-dev
```


### Formatting
All Python files are formatted using [Black][black-web], and the custom properties defined
in the `pyproject.toml` file.
```sh
make check
```


### Testing
Project testing is performed using [Pytest][pytest-web]. In order to run the tests:
```sh
make test
```


### Run
The project contains a [main.py][main-module] module exposing a CLI. Although this CLI contains several commands
that can be executed in a separated manner, the `Makefile` defines a rule to execute them in the standard order.
```sh
export DIALECT_MAP_API_URL="<URL>"
export DIALECT_MAP_KEY_PATH="<PATH>"
make run
```

This high level rule can be configured with the following env. variables

| ENV VARIABLE             | DEFAULT            | REQUIRED | DESCRIPTION                                   |
|--------------------------|--------------------|----------|-----------------------------------------------|
| DIALECT_MAP_API_URL      | -                  | Yes      | Private API base URL                          |
| DIALECT_MAP_KEY_PATH     | -                  | Yes      | Path to the Service Account key               |
| DIALECT_MAP_LOG_LEVEL    | INFO               | No       | Log messages level                            |


[black-web]: https://black.readthedocs.io/en/stable/
[dialect-map-data]: https://github.com/dialect-map/dialect-map-data
[dialect-map-io]: https://github.com/dialect-map/dialect-map-io
[dialect-map-api]: https://github.com/dialect-map/dialect-map-private-api
[jd-github-repo]: https://github.com/josephburnett/jd
[main-module]: src/main.py
[pytest-web]: https://docs.pytest.org/en/latest/#
