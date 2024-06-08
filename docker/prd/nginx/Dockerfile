FROM nginx:1.23.3-alpine

RUN apk add --no-cache nginx-mod-http-geoip

RUN rm /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx.conf /etc/nginx/nginx.conf

COPY ./default.conf /etc/nginx/conf.d/default.conf
