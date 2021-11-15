FROM notudope/notubot:buster

ENV PIP_NO_CACHE_DIR 1
ENV PATH="/usr/src/app/bin:$PATH"
WORKDIR /usr/src/app

RUN git clone -b main https://github.com/notudope/notubot.git ./

COPY ./sample_config.env ./config.env* ./

RUN pip3 install --no-cache-dir -U -r requirements.txt

ENTRYPOINT ["/usr/bin/tini", "-s", "--"]
#CMD ["python3", "-m", "run", "--prod"]
CMD ["python3", "-m", "notubot"]
