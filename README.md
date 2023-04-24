# DQM Playground

[![Django CI - Updated](https://github.com/CMSTrackerDPG/MLplayground/actions/workflows/django.yml/badge.svg)](https://github.com/CMSTrackerDPG/MLplayground/actions/workflows/django.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


The goal of the DQM Playground is to serve information from various
sources (OMS, Run Registry, DQM GUI, static files from the ML4DQM effort)
in order to ease model development and to provide a place to compare the
predictions of the various models.

## Requirements

- A `postgresql` database.
- A `ROOT` installation.
- An `.env` file which contains the variables listed [below](#environmental-variables).

## Environmental variables

All must be stored in a file named `.env`:

```python3
DJANGO_DATABASE_ENGINE
DJANGO_DEBUG
DJANGO_DATABASE_NAME
DJANGO_DATABASE_PASSWORD
DJANGO_DATABASE_USER
DJANGO_DATABASE_HOST
DJANGO_DATABASE_PORT
DJANGO_SECRET_KEY
DIR_PATH_DQMIO_STORAGE
```
### `DIR_PATH_DQMIO_STORAGE` (`str`)

List of directories to look into for DQM files (csv, nanoDQMIO). Separate
multiple directories with a colon (`:`), e.g.:

``` python3
DIR_PATH_DQMIO_STORAGE = "/dir/to/dqm/files:/this/is/another/dir"
```


## Behavior

## Management Commands

### `histograms`

- `exctract_lumisections_histos1D_csv`: Given a CSV containing 1D
Lumisection Histograms, this command will parse the file's
contents and create appropriate entries in the `LumisectionHistogram1D`
table.
- `exctract_lumisections_histos2D_csv`: Given a CSV containing 2D
Lumisection Histograms, this command will parse the file's contents
and create appropriate entries in the `LumisectionHistogram2D` table.

## Authentication

### External applications

To query the API from a third-party application, you will need to
generate a token (from the admin dashboard)

## Development

### Database

For storing histograms, the `ArrayField` is used, so a PostgreSQL database is
recommended for running the project locally.

Installing `pgadmin4` is also recommended for easier interfacing with the DB.

### API access via JS

Accessing the API via a rendered HTML page requires session authentication of
the DRF. This is done by:

1. Requiring the user to login to the page that contains the JS that does the requests
2. Configuring DRF to accept `SessionAuthentication`
3. Adding the `X-CSRF-TOKEN` header to the API request and setting its value to
the CSRF token which you can get by accessing the cookies stored in the current
page. [https://docs.djangoproject.com/en/4.0/ref/csrf/#ajax]

[https://www.django-rest-framework.org/topics/ajax-csrf-cors/]


### Building the Dockerfile locally

If outside the CERN GPN, you will need to create a bridge (via, e.g. `sshuttle`) first.

Then, `cd` into the directory where the `Dockerfile` is and run:

```bash
sudo docker build . --build-arg ROOT_TAG_NAME=v6-24-08 --network="host"
```
