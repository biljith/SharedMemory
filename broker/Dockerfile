FROM ubuntu:18.04
RUN apt-get update --fix-missing
RUN apt-get install -y python
RUN apt-get install -y python-dev
RUN apt-get install -y python-pip
RUN pip install sysv_ipc
RUN pip install flask
RUN pip install redis
COPY broker_api.py /
CMD ["python", "/broker_api.py"]
