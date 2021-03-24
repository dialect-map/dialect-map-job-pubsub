# Dialect map: static-data job ⚙️

### About
This repository contains the data-ingestion job to propagate _static_ data to the database.
The _static_ term makes reference to the [Dialect map data][dialect-map-data] slow change pace.

It will be used in combination with the [Dialect map IO][dialect-map-io] package, which provides the file parsing
and API connection capabilities, as well as the [Dialect map private API][dialect-map-api], which is the component
exposing a way of inserting records into the underlying database.


### Dependencies
Python dependencies are specified within the `requirements.txt` and `requirements-dev.txt` files.

In order to install the development packages, as well as the defined commit hooks:
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



[black-web]: https://black.readthedocs.io/en/stable/
[dialect-map-data]: https://github.com/dialect-map/dialect-map-data
[dialect-map-io]: https://github.com/dialect-map/dialect-map-io
[dialect-map-api]: https://github.com/dialect-map/dialect-map-private-api
[google-pub-sub]: https://cloud.google.com/pubsub/docs/overview
[main-module]: src/main.py
[pytest-web]: https://docs.pytest.org/en/latest/#
