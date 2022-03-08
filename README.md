# DQM Playground

[![Build Status](https://app.travis-ci.com/XavierAtCERN/MLplayground.svg?branch=master)](https://app.travis-ci.com/XavierAtCERN/MLplayground)

The goal of the DQM Playground is to serve information from various sources (OMS, Run Registry, DQM GUI, static files from the ML4DQM effort) in order to ease model development and to provide a place to compare the predictions of the various models.

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
DIR_PATH_EOS_CMSML4DC
 ```
