FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y telnet net-tools vim 

COPY server.py .
EXPOSE 5151

ENTRYPOINT [ "python", "./server.py" ]
