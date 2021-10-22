FROM notudope/notubot:buster

ENV DEBIAN_FRONTEND noninteractive

ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# hadolint ignore=DL3008
RUN apt-get -qq -y install --no-install-recommends \
    tini \
    tzdata \
    locales \
    && dpkg-reconfigure -f noninteractive tzdata \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

RUN apt-get -qq -y purge --auto-remove && apt-get -qq -y clean \
    && find /var/lib/apt/lists \
    /var/cache/apt/archives \
    /etc/apt/sources.list.d \
    /usr/share/man \
    /usr/share/doc \
    /var/log \
    -type f -exec rm -f {} +

ENV PATH="/usr/src/app/bin:$PATH"
WORKDIR /usr/src/app

RUN git clone -b main https://github.com/notudope/notubot.git ./

COPY ./sample_config.env ./config.env* ./

ENTRYPOINT ["/usr/bin/tini", "--"]
#CMD ["python3", "-m", "run", "--prod"]
CMD ["python3", "-m", "notubot"]
