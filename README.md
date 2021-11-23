# Anomaly Detection Playground

## Setup the environment

```bash
conda create -n ml_playground
conda activate ml_playground

conda install pip

git clone https://github.com/XavierAtCERN/MLplayground

cd MLplayground
pip install -r requirements.txt
```

## Environment variables

Create a .env file with the following content:
```bash
DJANGO_DATABASE_ENGINE=django.db.backends.sqlite3
DJANGO_DEBUG=True
DJANGO_DATABASE_NAME=db.sqlite3
DJANGO_SECRET_KEY=(%g65bg+&9rbnt+h&txlxw$+lkq=g=yrp!6@v+7@&$a%9^yt-!
```

## Run website locally

Setup your local database
```bash
python manage.py migrate
python manage.py createsuperuser
```

Run the website
```bash
python manage.py runserver
```

## Adding new apps

When adding new apps, it might be necessary to do the following:
```bash
python manage.py makemigrations new_app
python manage.py migrate new_app
```

## Filling the database with run information

The Django core management tool allows to interact with the database using scripts which can be scheduled. In order to fill the database, the runs and run_histos apps contain specific scripts which can be triggered from the scripts folder.

To test adding runs to the database:
```bash
cd scripts
source step1_extract_runs.sh
```

To test adding run-level histograms (entries, mean, rms, skewness, kurtosis) to the database:
```bash
cd scripts
source step2_extract_run_histos.sh
```

To add everything, just uncomment the command in the loop.

## Prototyping data extraction and views using jupyter

In order to prototype the scripts for data extraction and the views, it is possible to use some notebooks.
```bash
pip install jupyter django-extensions
python manage.py shell_plus --notebook
```

On lxplus, some lines can be added to settings.py in order to specify the IP adress and the port to be used as well as the no-browser option in order to forward the notebook.

## Current class structure

The main current class structure is the following:
![Graph of class structure](./images/ad_project_classes.png?raw=true "Graph of class structure")

Uniqueness should be established by the use of UniqueConstraint. Runs as well as the combinations of run+dataset+histogram and run+lumisection are unique.

## Building a REST API

The project can be split in two parts. The first goal is to move from many data sources to a database which can be queried by anyone. The second goal is to provide a framework to compare various approaches to anomaly detection. In order to fulfill the first goal while working towards the second, a REST API can be created which will allow users to access the relevant information from the database without modifying the project.

In order to build the REST API, install the Django REST framework.
```bash
pip install djangorestframework
```
and add it to the list of installed apps.

We then need to add a serializer.py file in each app we want to make accessible through the API. Starting with runs.

## Run certification

In progress

## Filling the database with lumisection information

Lumisection information from the ML4DQM dataset are 1D and 2D histograms. In order to add this information to the database, the run and lumisection they are related to need to have been created. The creation of run / lumisection is done when needed using a get_or_create for both as can be seen [here](https://github.com/XavierAtCERN/MLplayground/blob/master/lumisection_histos2D/management/commands/extract_lumisections_histos2D.py#L35-L44).

A script to add lumisections can be ran as follow:
```bash
cd scripts
source step4_extract_lumisections.sh
```

However, this script is of limited interest and will mostly be useful to test the code once tests will be added. Two more useful scripts can be ran to add 1D and 2D histogram information for every run/lumisection.

```bash
cd scripts
source step5_extract_lumisection_histos1D.sh
```

Alternatively:

```bash
cd scripts
source step6_extract_lumisection_histos2D.sh
```

## Adding tests

Due to the increasing complexity of the project, now is a good time to start adding tests. Django helps running tests by creating a TestCase class which will be used to create the tests for each app. The test development benefits from the very useful book [Test-Driven Development with Python](https://www.obeythetestinggoat.com/).

To run all the tests:
````bash
python manage.py test
```

To run all tests for a specific app:
````bash
python manage.py test app
```
