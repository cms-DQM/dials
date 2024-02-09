###############################
# BUILDER IMAGE
###############################

FROM node:20.11-bookworm as builder

WORKDIR /usr/src/app

COPY . /usr/src/app/

RUN yarn install

###############################
# FINAL IMAGE
###############################

FROM node:20.11-bookworm

# Deleting base node user with UID and GID 1000
# If someone uses a different UID/GID he can specify as build args
# this will ensure that the new user has the same permissions
# as the host running the container
# therefore the bind mount will not be a problem
RUN userdel node && rm -rf /home/node

ARG UID=1000
ARG GID=1000

ENV USERNAME=app
ENV HOME=/home/$USERNAME
ENV APP_HOME=$HOME/web

RUN mkdir -p $HOME
RUN mkdir $APP_HOME
RUN groupadd --system $USERNAME --gid $GID && adduser --system --group $USERNAME --uid $UID

WORKDIR $APP_HOME

COPY --from=builder /usr/src/app/node_modules $APP_HOME/node_modules

COPY . $APP_HOME
RUN chown -R $USERNAME:$USERNAME $HOME
RUN chown -R $USERNAME:$USERNAME /opt/yarn-*

USER $USERNAME

EXPOSE 3000
