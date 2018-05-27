FROM ubuntu:16.04

RUN apt-get update

RUN apt-get install -y libldns-dev git build-essential

RUN apt-get install -y python python-pip

RUN git clone https://github.com/blechschmidt/massdns.git

COPY app /app

RUN pip install -r /app/requirements.txt

WORKDIR /massdns/

RUN make

ENTRYPOINT ["python", "/app/run.py"]
