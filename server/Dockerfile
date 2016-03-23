FROM monolithe/garuda

MAINTAINER Antoine Mercadal <antoine@nuagenetworks.net>

ADD . /app

RUN apt-get update && apt-get install -y --force-yes libsasl2-dev libldap2-dev && \
    cd /app && \
    pip install -r requirements.txt && \
    monogen -f specs -L python && \
    cd codegen/python && python setup.py sdist && pip install dist/specdk-1.0.tar.gz && cd - && \
    rm -rf codegen specs&& \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 1984
WORKDIR /app/specsdirectorserver
CMD ./server.py
