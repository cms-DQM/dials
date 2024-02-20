# TODO

## General

* Staging deployment

## Backend

* Remove file from BadFileIndex table when it is fixed/removed in/from filesystem
* Create viewset for BadFileIndex model
* Check etl job queue for dead process (worker have shutdown for whatever reason and left the file unprocessed)
* Add h1d and h2d filter for source data file era and filepath contains


## Frontend

* Add copyright notice on the home page at the footer
* Create card with bad files count
* Add bad files count bar to `Indexed file by status` bar plot
* Add filter in `Indexed files` tab to look for bad files (note that is a different api request)
* Create card with min, max and avg job queues processing time
* Fix eslint warnings
* Fix wrapped plotly components overflowing in 
