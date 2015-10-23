FROM python:2.7

MAINTAINER Antoine Mercadal <antoine@nuagenetworks.net>

ADD . /app

RUN cd /app/libs && \
    pip install bambou*.tar.gz && \
    pip install monolithe*.tar.gz && \
    pip install garuda*.tar.gz && \
    pip install specdk*.tar.gz && \
    cd /app && \
    pip install -r requirements.txt && \
    rm -rf /app/libs

EXPOSE 2000
WORKDIR /app/specsdirectorserver
CMD ./specsdirectorsserver.py --redis-host=redis --mongo-host=mongo

