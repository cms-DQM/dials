# Dockerfile to augment the default Python image
# with extra packages. This image is then used as a base
# by Openshift to create the final S2I Python image for MLP
# Instructions followed:
# https://paas.docs.cern.ch/2._Deploy_Applications/Deploy_From_Git_Repository/4-add-oracle-client-to-s2i/

# A FROM line must be present but is ignored. It will be overridden by the --image-stream parameter in the BuildConfig
FROM registry.access.redhat.com/ubi8/python-38

# Temporarily switch to root user to install packages
USER root

# Install root dependencies
# For other packages, edit the second `dnf install` line appropriately.

RUN rpm --import https://linuxsoft.cern.ch/mirror/yum.oracle.com/RPM-GPG-KEY-oracle-ol8 \
 && dnf install -y http://linuxsoft.cern.ch/cern/centos/s8/CERN/x86_64/Packages/centos-gpg-keys-8-6.el8s.cern.noarch.rpm http://linuxsoft.cern.ch/cern/centos/s8/CERN/x86_64/Packages/centos-linux-repos-8-6.el8s.cern.noarch.rpm \
 && dnf install -y epel-release \
 && dnf install -y libzstd-devel avahi-compat-libdns_sd-devel avahi-devel binutils cfitsio-devel cmake3 davix-devel dcap-devel fftw-devel ftgl-devel gcc gcc-c++ gcc-gfortran gfal2-all gfal2-devel giflib-devel git gl2ps-devel glew-devel gnu-free-mono-fonts gnu-free-sans-fonts gnu-free-serif-fonts graphviz-devel gsl-devel jemalloc-devel krb5-devel libAfterImage-devel libX11-devel libXext-devel libXft-devel libXpm-devel libiodbc-devel libtiff-devel libxml2-devel lz4-devel make ncurses-libs openldap-devel openssl-devel pcre-devel readline-devel redhat-rpm-config sqlite-devel srm-ifce-devel unixODBC-devel urw-fonts xorg-x11-fonts-ISO8859-1-75dpi xrootd-server-devel xxhash-devel xz-devel zlib-devel pythia8-devel mesa-libGL-devel mesa-libGLU-devel glew-devel ftgl-devel libuuid-devel qt5-qtwebengine-devel R-devel R-Rcpp-devel R-RInside-devel \
 && dnf install -y redhat-lsb-core --setopt=tsflags=noscripts \
 && dnf update -y libarchive \
 && dnf clean all \
 && python3 -m pip install -U pip numpy
 # mysql-devel 

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

# ENTRYPOINT ["tail", "-f", "/dev/null"]