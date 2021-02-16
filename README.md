# Dialect map: static-data job

### About
This repository contains the data-ingestion job to propagate _static_ data to the database.
The _static_ term makes reference to the [Dialect map data][dialect-map-data] slow change pace.

It will be used in combination with the [Dialect map IO][dialect-map-io] package, which provides the file parsing
and API connection capabilities, as well as the [Dialect map private API][dialect-map-api], which is the component
exposing a way of inserting records into the underlying database.


### Development
To install all the source code that is necessary to operate with this project:

```shell script
git clone --recurse-submodules https://github.com/dialect-map/dialect-map-job-static
```

For cases where the project has already been cloned:

```shell script
git submodule update --init --recursive
```

The repositories defined as sub-modules will follow their own development pace.
For cases where the sub-module repositories has been updated on GitHub, and want
to propagate those changes to your local copy of the repositories:

```shell script
git submodule update --remote
```


### Dependencies
Python dependencies are specified within the `requirements.txt` and `requirements-dev.txt` files.

In order to install the development packages, as long as the defined commit hooks:
```sh
make install-dev
```


### Formatting
All Python files are formatted using [Black][black-web],  and the custom properties defined
in the `pyproject.toml` file.
```sh
make check
```


[black-web]: https://black.readthedocs.io/en/stable/
[dialect-map-data]: https://github.com/dialect-map/dialect-map-data
[dialect-map-io]: https://github.com/dialect-map/dialect-map-io
[dialect-map-api]: https://github.com/dialect-map/dialect-map-private-api
