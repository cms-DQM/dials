from typing import ClassVar

from django.conf import settings
from rest_framework import viewsets
from rest_framework.authentication import BaseAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.rest_framework_cern_sso.authentication import (
    CERNKeycloakClientSecretAuthentication,
    CERNKeycloakConfidentialAuthentication,
)

from .client import Brilcalc


class BrilcalcLumiViewSet(viewsets.ViewSet):
    authentication_classes: ClassVar[list[BaseAuthentication]] = [
        CERNKeycloakClientSecretAuthentication,
        CERNKeycloakConfidentialAuthentication,
    ]

    @action(detail=False, methods=["GET"], url_path="brilcalc-lumi")
    def brilcalc_lumi(self, request):
        brilws_version = request.query_params.get("brilws_version", "3.7.4")
        connect = request.query_params.get("connect", "offline")
        fillnum = request.query_params.get("fillnum", None)
        runnumber = request.query_params.get("runnumber", None)
        beamstatus = request.query_params.get("beamstatus", None)
        unit = request.query_params.get("unit", "/ub")
        amodetag = request.query_params.get("amodetag", None)
        normtag = request.query_params.get("normtag", None)
        begin = request.query_params.get("begin", None)
        end = request.query_params.get("end", None)
        byls = request.query_params.get("byls", "False").lower() in ["true", "1", "t", "yes", "y"]
        scope = request.query_params.get("scope", "all")

        brilcalc = Brilcalc(
            keytab_usr=settings.KEYTAB_USR, keytab_pwd=settings.KEYTAB_PWD, brilws_version=brilws_version
        )
        response = brilcalc.lumi(
            connect=connect,
            fillnum=fillnum,
            runnumber=runnumber,
            beamstatus=beamstatus,
            unit=unit,
            amodetag=amodetag,
            normtag=normtag,
            begin=begin,
            end=end,
            output_style="html",
            byls=byls,
        )

        if scope == "all":
            pass
        elif scope == "detailed":
            response = response.get("detailed")
        elif scope == "summary":
            response = response.get("summary")

        return Response(response)
