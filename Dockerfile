# Dockerfile to augment the default Python image
# with extra packages. This image is then used as a base
# by Openshift to create the final S2I Python image for MLP
# Instructions followed:
# https://paas.docs.cern.ch/2._Deploy_Applications/Deploy_From_Git_Repository/4-add-oracle-client-to-s2i/

# A FROM line must be present but is ignored. It will be overridden by the --image-stream parameter in the BuildConfig
FROM registry.access.redhat.com/ubi8/python-38

# The following installs most CERN Centos Stream 8 repos including Oracle drivers and EPEL. More repos can be added if needed.
ARG EXTRA_REPOS="http://linuxsoft.cern.ch/cern/centos/s8/CERN/x86_64/Packages/centos-gpg-keys-8-6.el8s.cern.noarch.rpm http://linuxsoft.cern.ch/cern/centos/s8/CERN/x86_64/Packages/centos-linux-repos-8-6.el8s.cern.noarch.rpm http://linuxsoft.cern.ch/cern/centos/s8/CERN/x86_64/Packages/epel-release-8-11.2.el8s.cern.noarch.rpm http://linuxsoft.cern.ch/cern/centos/s8/CERN/x86_64/Packages/oracle-release-1.2-1.el8s.cern.noarch.rpm"

# Temporarily switch to root user to install packages
USER root

# Install root dependencies
RUN rpm --import https://linuxsoft.cern.ch/mirror/yum.oracle.com/RPM-GPG-KEY-oracle-ol8 \
 && dnf install -y ${EXTRA_REPOS} \
 && dnf install -y epel-release \
 && dnf install -y git make cmake gcc-c++ gcc binutils libX11-devel libXpm-devel libXft-devel libXext-devel openssl-devel \
 && dnf install -y gcc-gfortran pcre-devel mesa-libGL-devel mesa-libGLU-devel glew-devel ftgl-devel fftw-devel cfitsio-devel graphviz-devel libuuid-devel avahi-compat-libdns_sd-devel openldap-devel python3-numpy libxml2-devel gsl-devel readline-devel R-devel R-Rcpp-devel R-RInside-devel xrootd-client\
 && dnf install -y redhat-lsb-core --setopt=tsflags=noscripts \
 && dnf update -y libarchive \
 && dnf clean all \
 && python3 -m pip install -U pip numpy

# Build argument specifying ROOT version
ARG ROOT_TAG_NAME

# Build ROOT
RUN mkdir -p /opt/app-root/src/root/ /usr/src/root \
 && cd /tmp \
 && git clone --branch "$ROOT_TAG_NAME" --depth=1 https://github.com/root-project/root /usr/src/root \
 && cmake -DCMAKE_INSTALL_PREFIX=/opt/app-root/src/root/ /usr/src/root -DPython3_ROOT_DIR=`which python3` \
 && cmake --build . --target install -j 1 \
 && rm -rf /usr/src/root /tmp/*

# Run the final image as unprivileged user.
# This is the base image's `default` user, but S2I requires a numerical user ID.
USER 1001
