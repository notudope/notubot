FROM notudope/notubot:buster

ENV PATH="/usr/src/app/bin:$PATH"
WORKDIR /usr/src/app

RUN git clone -b main https://github.com/notudope/notubot.git ./

COPY ./sample_config.env ./config.env* ./

ENTRYPOINT ["/usr/bin/tini", "--"]
#CMD ["python3", "-m", "run", "--prod"]
CMD ["python3", "-m", "notubot"]
