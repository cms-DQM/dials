###############################
# DEPENDENCIES IMAGE
###############################

FROM python:3.10.13-bookworm AS dependencies

ENV POETRY_VERSION=1.7.1

WORKDIR /usr/src/dependencies

RUN pip3 install --upgrade pip
RUN pip3 install "poetry==$POETRY_VERSION"

COPY pyproject.toml /usr/src/dependencies/
COPY *poetry.lock /usr/src/dependencies/

RUN poetry export --with=backend --format=requirements.txt > requirements.txt

###############################
# BUILDER IMAGE
###############################

FROM python:3.10.13-alpine3.19 AS builder

WORKDIR /usr/src/build

COPY --from=dependencies /usr/src/dependencies/requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 wheel --no-cache-dir --no-deps --wheel-dir /usr/src/build/wheels -r requirements.txt

###############################
# RELEASE IMAGE
###############################

FROM python:3.10.13-alpine3.19 AS release

# This is to print directly to stdout instead of buffering output
ENV PYTHONUNBUFFERED 1

ARG UID=1000
ARG GID=1000

ENV USERNAME=app
ENV HOME=/home/$USERNAME
ENV APP_HOME=$HOME/backend

RUN mkdir -p $HOME
RUN mkdir $APP_HOME
RUN addgroup --system --gid $GID $USERNAME && adduser --system --ingroup $USERNAME --uid $UID $USERNAME

WORKDIR $APP_HOME

COPY --from=builder /usr/src/build/wheels /wheels
COPY --from=builder /usr/src/build/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache /wheels/*

COPY backend $APP_HOME

RUN chown -R $USERNAME:$USERNAME $APP_HOME

USER $USERNAME

RUN python -m compileall dials
RUN $APP_HOME/scripts/setup-django-production.sh

EXPOSE 8000

CMD ${APP_HOME}/scripts/run-django-production.sh
