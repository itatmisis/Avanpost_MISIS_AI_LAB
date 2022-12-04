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

RUN pip3 install flask pika pymongo requests peewee
RUN pip3 install pandas pickle5 statistics numpy
RUN pip3 install seaborn scipy scikit-learn
RUN pip3 install torch==1.13.0
RUN pip3 install torchvision 
RUN pip3 install numpy matplotlib Pillow tqdm
RUN pip3 install tensorflow
RUN pip3 install psycopg2-binary peewee
ENV PYTHONPATH "${PYTHONPATH}:/ml/"
WORKDIR /app