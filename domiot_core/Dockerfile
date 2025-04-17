ARG BUILD_FROM
FROM $BUILD_FROM


WORKDIR /app
EXPOSE 8888

RUN apk update && apk add --no-cache python3 py3-pip build-base python3-dev nginx

RUN mkdir -p /run/nginx

COPY . /app/

# Set permissions for nginx
RUN chown -R :www-data /app

RUN bash build.sh

RUN chmod +x ./run.sh
CMD [ "./run.sh" ]