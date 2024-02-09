FROM rootproject/root:6.30.02-ubuntu22.04

# The ROOT installed in the base image was compiled against python3 in ubuntu22.04 base image
# ROOT's team just installed the latest python version (3.10.x) at build time
#
# So in order to control python version (same as development version)
# we are going to install python 3.10.13 manually
#
# Note: Using this base image we can't change python's minor version
# since root is pre-compiled for python 3.10.x, i.e. we should compile root manually
# for a different python minor version if we need a different minor version
ARG PYTHON_VERSION=3.10.13

RUN apt-get update -y && apt-get install netcat -y

RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz \
    && tar xzvf Python-${PYTHON_VERSION}.tgz \
    && rm Python-${PYTHON_VERSION}.tgz \
    && cd Python-${PYTHON_VERSION} \
    && ./configure \
    && make -j$(( $(nproc --all) - 2 )) \
    && make install \
    && cd .. \
    && rm -rf Python-${PYTHON_VERSION}

WORKDIR /api

# set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
RUN pip3 install poetry==1.7.1

COPY . .

RUN sed -i 's/\r$//g' /api/scripts/entrypoint.sh
RUN chmod +x /api/scripts/entrypoint.sh

RUN poetry install --no-root

EXPOSE 8000

ENTRYPOINT ["/api/scripts/entrypoint.sh"]
