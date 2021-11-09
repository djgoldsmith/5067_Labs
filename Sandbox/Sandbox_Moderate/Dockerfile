FROM cueh/flask



USER root
ADD REQUIREMENTS.txt /tmp
RUN pip install -r /tmp/REQUIREMENTS.txt

USER flask
WORKDIR /opt
ADD ./opt /opt
