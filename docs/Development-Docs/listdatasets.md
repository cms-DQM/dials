# Dataset App
Docs for dataset app



### Create a new app **datasets**
```python
python manage.py startapp listdatasets
```

### Build a model 
In `listdatasets/models.py` 

```python
class Dataset(models.Model):
    STORAGE_CHOICES = (
        ("postgres", "Postgres"),
        ("eos", "EOS"),
        ("external", "External")
    )

    GRANULAR_CHOICES = (
        ("fill", "Fill"),
        ("run", "Run"),
        ("lumi", "Lumisection")
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank = True)
    api = models.TextField(blank = True)
    api_description = models.TextField(blank = True)
    storagetype = models.CharField(choices=STORAGE_CHOICES, max_length=50)
    location = models.TextField(blank = True)
    scripts = models.TextField(blank = True)
    comment = models.TextField(blank = True)
    granularity = models.CharField(choices=GRANULAR_CHOICES, max_length=50)

    def __str__(self):
        return "{}".format(self.name)
```

### Migrate Model

```
python manage.py makemigrations
python manage.py migrate
```