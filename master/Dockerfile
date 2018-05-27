FROM ubuntu:16.04

RUN apt-get update

RUN apt-get install -y libldns-dev git build-essential

RUN apt-get install -y python python-pip

COPY app /app

WORKDIR /app/

RUN pip install -r /app/requirements.txt

ENTRYPOINT ["python", "/app/run.py"]
