# Dataset App
Docs for dataset app



### Create a new app **datasets**
```python
python manage.py startapp datasets
```

### Build a model 
In `datasets/models.py` 

```python
class Dataset(models.Model):
    STORAGE_CHOICES = (
        ("postgres", "Postgres"),
        ("eos", "EOS"),
        ("external", "External")
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank = True)
    api = models.TextField(blank = True)
    api_description = models.TextField(blank = True)
    storagetype = models.CharField(choices=STORAGE_CHOICES, max_length=50)
    location = models.TextField(blank = True)
    scripts = models.TextField(blank = True)
    comment = models.TextField(blank = True)

    def __str__(self):
        return "{}".format(self.name)
```

### Migrate Model

```
python manage.py makemigrations
python manage.py migrate
```