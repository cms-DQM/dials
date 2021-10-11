## Start a new project on Django 

1. Copy the .s2i folder into project directory 
2. Create a virtual environment 
```python
pyhon -m venv mlp-env
source mlp-env/bin/activate
```
3. Install necessary packages (copy requirement.txt from similar projects)
```python
pip install -r requirements.txt
```
3. Run following commands for creating a new Django project. [See tutorial](https://docs.djangoproject.com/en/3.2/intro/tutorial01/)

```python
django-admin startproject mlp
```

4. For creating projects, run

```python
python manage.py startapp home
```
Few steps to follow 
 * add app to `urls.py` in `mlp/urls.py`
 * add app to `mlp/settings.py` in `INSTALLED_APPS` enivormnent variable

5. In project structure. Main folder will be `mlp`. It will contain 
    * `settings.py`
        * Dont forget to edit `BASE_DIR`, `ALLOWED_HOSTS`, `TEMPLATES`, `DATABASES`, `STATIC` etc. 
    * `urls.py`
    * `asgi.py` & `wsgi.py`

6. `manage.py` is outside the `mlp` directory. But inside the main repo directory. 
7. The main repo dir also contains `.gitignore` file 
8. Copy `openshift-start-up-script` from similar projects
9. Declare Enviroment variables in [Build](https://openshift.cern.ch/console/project/ml4dqm-playground/browse/builds) on Openshift platform 