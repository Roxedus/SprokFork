FROM lsiobase/alpine.python3

LABEL maintainer="Roxedus"


COPY / /app

RUN apk add --no-cache --virtual=build-dependencies  --update gcc musl-dev

RUN \
    python3 -m pip install -r /app/requirements.txt && \
    chown -R abc:abc \
    /config \
    /app

RUN apk del build-dependencies

WORKDIR /app

CMD ln -sf /app/data /config && python3 /app/bot.py

VOLUME /config
