FROM nginx:alpine
MAINTAINER Antoine Mercadal <antoine@nuagenetworks.net>

ADD ./app /usr/share/nginx/html
# ADD ./certs /etc/nginx/certs
ADD ./nginx.conf /etc/nginx/
ADD ./run.sh /

CMD sh /run.sh architect
