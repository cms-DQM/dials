import imp
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django_tables2 import RequestConfig
from django_filters import rest_framework as filters
from rest_framework import generics

from lumisection_histos2D.models import LumisectionHisto2D
from lumisection_histos2D.filters import LumisectionHistos2DFilter
from lumisection_histos2D.tables import LumisectionHistos2DTable
from lumisection_histos2D.serializers import LumisectionHisto2DSerializer

import pandas as pd

def listLumisectionHistos2D(request):
    """
    View to list the filtered 2D histograms for Lumisections
    """
    context = {}
    lumisectionHistos2D_list = LumisectionHisto2D.objects.all()
    lumisectionHistos2D_filter = LumisectionHistos2DFilter(request.GET, queryset=lumisectionHistos2D_list)
    lumisectionHistos2D_table = LumisectionHistos2DTable(lumisectionHistos2D_filter.qs[:50])

    RequestConfig(request).configure(lumisectionHistos2D_table)

    context["lumisectionHistos2D_table"] = lumisectionHistos2D_table
    context["filter"] = lumisectionHistos2D_filter
    return render(request, "lumisection_histos2D/listLumisectionHistos2D.html", context)

class listLumisectionHistos2DAPI(generics.ListAPIView):
    queryset = LumisectionHisto2D.objects.all()
    serializer_class = LumisectionHisto2DSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LumisectionHistos2DFilter