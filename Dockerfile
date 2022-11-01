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

RUN dnf install -y http://linuxsoft.cern.ch/cern/centos/s8/CERN/x86_64/Packages/centos-gpg-keys-8-6.el8s.cern.noarch.rpm http://linuxsoft.cern.ch/cern/centos/s8/CERN/x86_64/Packages/centos-linux-repos-8-6.el8s.cern.noarch.rpm http://linuxsoft.cern.ch/cern/centos/s8/CERN/x86_64/Packages/oracle-release-1.2-1.el8s.cern.noarch.rpm \
 && sed -i 's|gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-oracle-ol8||' /etc/yum.repos.d/dbclients8.repo \
 && dnf install -y make cmake gcc-c++ gcc binutils libX11-devel libXpm-devel libXft-devel libXext-devel \
 && dnf clean all 

# Build ROOT
RUN echo $ROOT_TAG_NAME \
 && cmake --version \
 && which cmake \
 &&	mkdir -p /opt/app-root/src/root/root_build /opt/app-root/src/root/root_install \
 &&	git clone --branch "v6-26-06" --depth=1 https://github.com/root-project/root.git /opt/app-root/src/root/root_src \
 && cd /opt/app-root/src/root/root_build \
 && cmake -DCMAKE_INSTALL_PREFIX=../root_install ../root_src \
 && cmake --build . -- install -j4 

# Run the final image as unprivileged user.
# This is the base image's `default` user, but S2I requires a numerical user ID.
USER 1001