FROM ubuntu:20.04

# Timezone Configuration
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && apt install -y    apt-utils \
                                    lsb-release \
                                    mesa-utils \
                                    gnupg2 \
                                    net-tools \
                                    build-essential \
                                    wget \
                                    unzip \
                                    curl \
                                    git \
                                    nano \
                                    iputils-ping \
                                    cmake \
                                    psmisc \
                                    python3-pip \
                                    python3-dev

RUN apt-get update
RUN curl -fsSL -s https://deb.nodesource.com/setup_19.x | bash /dev/stdin
RUN apt update && apt install -y nodejs
RUN npm install -g http-server
# RUN ln -s /usr/bin/nodejs /usr/bin/node

ENTRYPOINT http-server /web -p 8080