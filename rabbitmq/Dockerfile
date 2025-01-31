# rabbitmq/Dockerfile
FROM rabbitmq:3.13.4-management-alpine

RUN apk update \
    && apk add --no-cache curl

COPY rabbitmq_health_checkout.sh /usr/local/bin/rabbitmq_health_checkout.sh
RUN chmod +x /usr/local/bin/rabbitmq_health_checkout.sh