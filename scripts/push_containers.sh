# https://github.com/gabrielmscampos/dqm-ml4ad

docker login

docker build -f ./backend/Dockerfile -t gabrielmscampos/dqmdc-ml4ad-backend-base ./backend
docker build -f ./frontend/Dockerfile.prod -t gabrielmscampos/dqmdc-ml4ad-frontend ./frontend

docker push gabrielmscampos/dqmdc-ml4ad-backend-base
docker push gabrielmscampos/dqmdc-ml4ad-frontend
