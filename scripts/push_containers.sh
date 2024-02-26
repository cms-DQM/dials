docker login

docker build -f ./backend/Dockerfile -t gabrielmscampos/dials-backend-base ./backend
docker build -f ./frontend/Dockerfile.prod -t gabrielmscampos/dials-frontend ./frontend

docker push gabrielmscampos/dials-backend-base
docker push gabrielmscampos/dials-frontend
