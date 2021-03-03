# Dialect map: static-data job

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

The repositories defined as sub-modules will follow their own development pace.
For cases where the sub-module repositories has been updated on GitHub, and want
to propagate those changes to your local copy of the repositories:

```sh
git submodule update --remote
```


### Dependencies
Python dependencies are specified within the `requirements.txt` and `requirements-dev.txt` files.

In order to install the development packages, as long as the defined commit hooks:
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


### Data update
In order to ingest any data changes happening on the `dialect-map-data` submodule, this project needs
to compute the differences between one particular version of the JSON data files and the next.

For this purpose, a Golang / CLI tool called [jd][jd-github-repo] is used.

To simplify the _diff-computing_ operations, a set of scripts within the `scripts` folder have been defined.
These scripts have a specific order to be run (specified by their prefix), and a mandatory argument to receive,
indicating the name of the JSON file to compute the differences on.

```sh
echo "Computing JSON difference on jargons.json" && \
    ./scripts/1_copy_data.sh && \
    ./scripts/2_update_data.sh && \
    ./scripts/3_compute_diffs.sh -f "jargons.json"
```

### Run job
To propagate data differences into the database, the [main.py][main-module] module defines a `run` command:

```sh
python3 src/main.py run [OPTIONS]
```

This command accepts several options, from which the most relevant are:

| OPTION         | ENV VARIABLE             | DEFAULT      | REQUIRED | DESCRIPTION                        |
|----------------|--------------------------|--------------|----------|------------------------------------|
| --api-url      | DIALECT_MAP_API_URL      | ...          | No       | Private API base URL               |
| --key-path     | DIALECT_MAP_KEY_PATH     | ...          | No       | Path to the Service Account key    |
| --log-level    | DIALECT_MAP_LOG_LEVEL    | INFO         | No       | Log messages level                 |


[black-web]: https://black.readthedocs.io/en/stable/
[dialect-map-data]: https://github.com/dialect-map/dialect-map-data
[dialect-map-io]: https://github.com/dialect-map/dialect-map-io
[dialect-map-api]: https://github.com/dialect-map/dialect-map-private-api
[jd-github-repo]: https://github.com/josephburnett/jd
[main-module]: src/main.py
[pytest-web]: https://docs.pytest.org/en/latest/#
