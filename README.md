# ML Playground

## Setup the environment

```
conda create -n ml_playground
conda activate ml_playground

conda install pip

git clone https://github.com/CMSTrackerDPG/MLplayground

cd MLplayground
pip install -r requirements.txt
```

## Environment variables

Create a .env file with the following content:
```
DJANGO_DATABASE_ENGINE=django.db.backends.sqlite3
DJANGO_DEBUG=True
DJANGO_DATABASE_NAME=db.sqlite3
DJANGO_SECRET_KEY=(%g65bg+&9rbnt+h&txlxw$+lkq=g=yrp!6@v+7@&$a%9^yt-!
```

## Run website locally

Setup your local database
```
python manage.py migrate
python manage.py createsuperuser
```

Run the website
```
python manage.py runserver
```

## Adding new apps

When adding new apps, it might be necessary to do the following:
```
python manage.py makemigrations new_app
python manage.py migrate new_app
```

## Filling the database using the Django management

The Django core management tool allows to interact with the database using scripts which can be scheduled. In order to fill the database, the runs and run_histos apps contain specific scripts which can be triggered from the scripts folder.

To test adding runs to the database:
```
cd scripts
source step1_extract_runs.sh
```

To test adding run-level histograms (entries, mean, rms, skewness, kurtosis) to the database:
```
cd scripts
source step2_extract_run_histos.sh
```

To add everything, just uncomment the command in the loop. 
