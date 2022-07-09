# Dialect map: Pub/Sub job ⚙️

[![CI/CD Status][ci-status-badge]][ci-status-link]
[![Coverage Status][cov-status-badge]][cov-status-link]
[![MIT license][mit-license-badge]][mit-license-link]
[![Code style][code-style-badge]][code-style-link]


### About
This repository contains the data-ingestion job to propagate Pub/Sub data to the database.

It relies on [Dialect map IO][dialect-map-io], which provides PubSub / API connection capabilities,
and [Dialect map schemas][dialect-map-schemas], which provides data (de)serialization capabilities,
in order to send validated records to the [Dialect map private API][dialect-map-private-api].


### Dependencies
Python dependencies are specified on the multiple files within the `reqs` directory.

In order to install all the development packages, as well as the defined commit hooks:

```shell
make install-dev
```


### Formatting
All Python files are formatted using [Black][web-black], and the custom properties defined
in the `pyproject.toml` file.

```shell
make check
```


### Testing
Project testing is performed using [Pytest][web-pytest]. In order to run the tests:

```shell
make test
```


### CLI 🚀
The project contains a [main.py][main-module] module exposing a CLI with several commands:

```shell
python3 src/main.py [OPTIONS] [COMMAND] [ARGS]...
```


#### Command: `data-diff-job`
This command starts a [Google Pub/Sub][google-pub-sub] subscription reading job, that dispatches _data-diff_
message records coming from the [Dialect map data][dialect-map-data] repository, to the Dialect map _private_ API.

| ARGUMENT       | ENV VARIABLE           | REQUIRED | DESCRIPTION                              |
|----------------|------------------------|----------|------------------------------------------|
| --gcp-project  | -                      | Yes      | GCP project name                         |
| --gcp-pubsub   | -                      | Yes      | GCP Pub/Sub subscription name            |
| --gcp-key-path | -                      | Yes      | GCP Service account key path             |
| --api-url      | -                      | Yes      | Private API base URL                     |


[ci-status-badge]: https://github.com/dialect-map/dialect-map-job-pubsub/actions/workflows/ci.yml/badge.svg?branch=main
[ci-status-link]: https://github.com/dialect-map/dialect-map-job-pubsub/actions/workflows/ci.yml?query=branch%3Amain
[code-style-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[code-style-link]: https://github.com/psf/black
[cov-status-badge]: https://codecov.io/gh/dialect-map/dialect-map-job-pubsub/branch/main/graph/badge.svg
[cov-status-link]: https://codecov.io/gh/dialect-map/dialect-map-job-pubsub
[mit-license-badge]: https://img.shields.io/badge/License-MIT-blue.svg
[mit-license-link]: https://github.com/dialect-map/dialect-map-job-pubsub/blob/main/LICENSE

[dialect-map-data]: https://github.com/dialect-map/dialect-map-data
[dialect-map-io]: https://github.com/dialect-map/dialect-map-io
[dialect-map-private-api]: https://github.com/dialect-map/dialect-map-private-api
[dialect-map-schemas]: https://github.com/dialect-map/dialect-map-schemas
[google-pub-sub]: https://cloud.google.com/pubsub/docs/overview
[main-module]: src/main.py
[web-black]: https://black.readthedocs.io/en/stable/
[web-pytest]: https://docs.pytest.org/en/latest/#
