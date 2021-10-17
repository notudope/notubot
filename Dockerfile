# Using Python Slim-Buster
FROM notudope/notubot:buster

# Clone repo and prepare working directory
RUN git clone -b main https://github.com/notudope/notubot /home/notubot/ \
    && chmod 777 /home/notubot \
    && mkdir /home/notubot/bin/

# Copies config.env (if exists)
COPY ./sample_config.env ./config.env* /home/notubot/

# Setup Working Directory
WORKDIR /home/notubot/

# Finalization
CMD ["python3","-m","userbot"]
