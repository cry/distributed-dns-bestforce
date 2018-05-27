FROM ubuntu:16.04

RUN apt-get update

RUN apt-get install -y libldns-dev git build-essential

RUN apt-get install -y python

RUN git clone https://github.com/blechschmidt/massdns.git

WORKDIR /massdns/

RUN make

ENTRYPOINT ["./bin/massdns"]
