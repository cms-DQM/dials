import imp
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django_tables2 import RequestConfig
from django_filters import rest_framework as filters
from rest_framework import generics

from lumisection_histos1D.models import LumisectionHisto1D
from lumisection_histos1D.filters import LumisectionHistos1DFilter
from lumisection_histos1D.tables import LumisectionHistos1DTable
from lumisection_histos1D.serializers import LumisectionHisto1DSerializer

import pandas as pd


def listLumisectionHistos1D(request):
    """
    View to list the filtered 1D histograms for Lumisections
    """
    context = {}
    lumisectionHistos1D_list = LumisectionHisto1D.objects.all()
    lumisectionHistos1D_filter = LumisectionHistos1DFilter(
        request.GET, queryset=lumisectionHistos1D_list
    )
    lumisectionHistos1D_table = LumisectionHistos1DTable(
        lumisectionHistos1D_filter.qs[:50]
    )

    RequestConfig(request).configure(lumisectionHistos1D_table)

    context["lumisectionHistos1D_table"] = lumisectionHistos1D_table
    context["filter"] = lumisectionHistos1D_filter
    return render(request, "lumisection_histos1D/listLumisectionHistos1D.html", context)


class listLumisectionHistos1DAPI(generics.ListAPIView):
    queryset = LumisectionHisto1D.objects.all()
    serializer_class = LumisectionHisto1DSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LumisectionHistos1DFilter
