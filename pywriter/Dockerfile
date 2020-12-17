FROM ubuntu:16.04
RUN apt-get update --fix-missing
RUN apt-get install -y python3
RUN apt-get install -y python3-dev
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-pycurl
RUN pip3 install sysv_ipc
RUN pip3 install kubernetes
COPY pywriter_kube.py /
COPY .kube /.kube 
CMD ["python3","/pywriter_kube.py"]
