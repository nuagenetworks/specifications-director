FROM garuda:latest

MAINTAINER Antoine Mercadal <antoine@nuagenetworks.net>

ADD . /app

RUN apt-get update && apt-get install -y --force-yes libsasl2-dev libldap2-dev && \
    cd /app/libs && \
    cp nuage.pem /etc/ssl/certs && \
    ln -s /etc/ssl/certs/nuage.pem /etc/ssl/certs/`cat nuage.pem | openssl x509 -hash -noout`.0 && \
    pip install specdk*.tar.gz && \
    cd /app && \
    pip install -r requirements.txt && \
    rm -rf /app/libs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 2000
WORKDIR /app/specsdirectorserver
CMD ./server.py --redis-host=redis --mongo-host=mongo

