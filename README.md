# Dialect map: static-data job ⚙️

[![CI/CD Status][ci-status-badge]][ci-status-link]
[![Coverage Status][cov-status-badge]][cov-status-link]
[![MIT license][mit-license-badge]][mit-license-link]
[![Code style][code-style-badge]][code-style-link]


### About
This repository contains the data-ingestion job to propagate _static_ data to the database.
The _static_ term makes reference to the [Dialect map data][dialect-map-data] slow change pace.

It relies on [Dialect map IO][dialect-map-io], which provides PubSub / API connection capabilities,
and [Dialect map schemas][dialect-map-schemas], which provides data (de)serialization capabilities,
in order to send validated records to the [Dialect map private API][dialect-map-private-api] component.


### Dependencies
Python dependencies are specified within the `requirements.txt` and `requirements-dev.txt` files.

In order to install the development packages, as well as the defined commit hooks:
```sh
make install-dev
```


### Formatting
All Python files are formatted using [Black][web-black], and the custom properties defined
in the `pyproject.toml` file.
```sh
make check
```


### Testing
Project testing is performed using [Pytest][web-pytest]. In order to run the tests:
```sh
make test
```


### CLI 🚀
The project contains a [main.py][main-module] module exposing a CLI with several commands:
```sh
python3 src/main.py [OPTIONS] [COMMAND] [ARGS]...
```

The top-level options are:

| OPTION         | ENV VARIABLE           | DEFAULT          | REQUIRED | DESCRIPTION                              |
|----------------|------------------------|------------------|----------|------------------------------------------|
| --api-url      | DIALECT_MAP_API_URL    | -                | Yes      | Private API base URL                     |
| --log-level    | DIALECT_MAP_LOG_LEVEL  | INFO             | No       | Log messages level                       |


#### Command: `pubsub-job`
This command starts a [GCP Pub/Sub][google-pub-sub] reading job, that dispatches message encoded
data records to the Dialect Map _private_ API, until no more messages are available.

The command arguments are:

| ARGUMENT       | ENV VARIABLE           | DEFAULT          | REQUIRED | DESCRIPTION                              |
|----------------|------------------------|------------------|----------|------------------------------------------|
| --gcp-project  | -                      | -                | Yes      | GCP project name                         |
| --gcp-pubsub   | -                      | -                | Yes      | GCP Pub/Sub subscription name            |
| --gcp-key-path | -                      | -                | Yes      | GCP Service account key path             |


[ci-status-badge]: https://github.com/dialect-map/dialect-map-job-static/actions/workflows/ci.yml/badge.svg?branch=main
[ci-status-link]: https://github.com/dialect-map/dialect-map-job-static/actions/workflows/ci.yml?query=branch%3Amain
[code-style-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[code-style-link]: https://github.com/psf/black
[cov-status-badge]: https://codecov.io/gh/dialect-map/dialect-map-job-static/branch/main/graph/badge.svg
[cov-status-link]: https://codecov.io/gh/dialect-map/dialect-map-job-static
[mit-license-badge]: https://img.shields.io/badge/License-MIT-blue.svg
[mit-license-link]: https://github.com/dialect-map/dialect-map-job-static/blob/main/LICENSE

[dialect-map-data]: https://github.com/dialect-map/dialect-map-data
[dialect-map-io]: https://github.com/dialect-map/dialect-map-io
[dialect-map-private-api]: https://github.com/dialect-map/dialect-map-private-api
[dialect-map-schemas]: https://github.com/dialect-map/dialect-map-schemas
[google-pub-sub]: https://cloud.google.com/pubsub/docs/overview
[main-module]: src/main.py
[web-black]: https://black.readthedocs.io/en/stable/
[web-pytest]: https://docs.pytest.org/en/latest/#
