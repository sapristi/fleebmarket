FROM debian:stable-slim

# decides which arch to choose in meilisearch releases
ARG MEILISEARCH_ARCH=amd64

WORKDIR /usr/local

RUN apt-get update && apt-get install --no-install-recommends -y \
    wget \
    ca-certificates
RUN wget --quiet -O meilisearch https://github.com/meilisearch/MeiliSearch/releases/download/v0.24.0/meilisearch-linux-${MEILISEARCH_ARCH} \
    && chmod +x meilisearch

ENV MEILI_HTTP_ADDR 0.0.0.0:7700
EXPOSE 7700/tcp

CMD ./meilisearch
