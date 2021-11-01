#!/bin/bash

cd ..

./manage.py graph_models -a -g -o images/ad_project.png
./manage.py graph_models -a -I Run,RunHisto,RunCertification,Lumisection,LumisectionHisto2D -o images/ad_project_classes.png
