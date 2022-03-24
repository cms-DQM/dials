cd ..
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# rm -rf runs/migrations
# rm -rf run_histos/migrations 
# rm -rf data__certification/migrations

# rm -rf lumisections/migrations
# rm -rf lumisection_histos1D/migrations
# rm -rf lumisection_histos2D/migrations
# rm -rf lumisection_certification/migrations
