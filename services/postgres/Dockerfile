from postgres:13.3

COPY init_scripts /docker-entrypoint-initdb.d

RUN cat /etc/locale.gen
RUN echo fr_FR.UTF-8 UTF-8 >> /etc/locale.gen; echo en_US.UTF-8 UTF-8 >> /etc/locale.gen; locale-gen
