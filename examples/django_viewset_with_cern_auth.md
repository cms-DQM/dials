# Creating a Django ViewSet protected by CERN Auth

This example depicts the train of thoughts to complete the TODO's item: "Create viewset for BadFileIndex model".

## REST Api routes and DRF ViewSets

The [Djando Rest Framework (DRF)](https://www.django-rest-framework.org/) is a good framework for creating a REST api on top on Django, there are many methods (APIView, GenericAPIView, ViewSet, ...) that simplifies the process of creating REST api's views. Here are going to use some `mixins` and the `GenericViewSet` abstract to create an api endpoint that only has `list` and `get` methods, since the `BadFileIndex` model is object representation of the database table for storing files that couldn't even open when trying to extract metadata for indexing for now we only need to list all files and maybe get a specific one by his id.

In the [`viewsets.py`](/backend/dqmio_file_indexer/viewsets.py) we can add the following block of code representing our viewset:

```python
class BadFileIndexViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = BadFileIndex.objects.all().order_by("st_itime")
    serializer_class = BadFileIndexSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BadFileIndexFilter
```

The mixins `RetrieveModelMixin` and `ListModelMixin` are used to recycle `get` and `list` methods and the `GenericViewSet` is used to inherit the ViewSet specification for our new class. You can see a bunch of class attributes:

* `queryset` is the actual data (lazy queried) model that the viewsets methods will interact
* `serializer_class` serialization class used to parse queryset's output
* `filter_backends` specify (per ViewSet in our case) the filter backend to be used
* `filterset_class` filterable fields and methods are defined in that class

Naturally you have to create the serializer and filterset classes according to your needs, in that case put in the [`serializers.py`](/backend/dqmio_file_indexer/serializers.py) the following block,

```python
class BadFileIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadFileIndex
        fields = "__all__"
```

and for the [`filters.py`](/backend/dqmio_file_indexer/filters.py) the following block:

```python
class BadFileIndexFilter(filters.FilterSet):
    path_contains = filters.CharFilter(label="File path contains", field_name="file_path", lookup_expr="contains")
    era = filters.CharFilter(label="Data era", field_name="data_era", lookup_expr="exact")
    min_size = filters.NumberFilter(label="Minimum file size", field_name="st_size", lookup_expr="gte")

    class Meta:
        model = BadFileIndex
        fields = ["path_contains", "era", "min_size"]
```

## Protecting our ViewSet with CERN SSO

In any viewset is possible to specify an `authentication_classes` attribute that lists which authentication methods any built-in method of the viewset will have. In our case we want to integrate with the CERN SSO, that is easy since custom authentication classes are defined in [`rest_framework_cern_sso`](backend/utils/rest_framework_cern_sso/authentication.py) (don't get confused, CERN SSO uses Keycloak underneath!). Than we just need tho append the following line in our ViewSet:

```python
class BadFileIndexViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    ...
    authentication_classes = [CERNKeycloakClientSecretAuthentication, CERNKeycloakBearerAuthentication]
```

## Exposing our ViewSet as an REST Api method

Now that the new viewset is created and protected, we need to expose it as an endpoint. You need to navigate to [`routers.py`](/backend/dqmio_file_indexer/routers.py) and append the following line:

```python
router.register(f"bad-file-index", BadFileIndexViewSet, basename="bad-file-index")
```

This will integrate the viewset as an api endpoint under the basename `bad-file-index`. Note: This router is automatically imported and unpacked in the actual exposed application's `urlpatterns` you can see it [here](/backend/dials/urls.py).
