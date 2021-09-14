FROM cueh/flask

USER root
RUN apt-get update && apt-get install -y --no-install-recommends ncat

#Install the Selenium Driver
COPY REQUIREMENTS.txt /tmp/REQUIREMENTS.txt
RUN pip install -r /tmp/REQUIREMENTS.txt

USER flask
WORKDIR /opt
ADD ./RequestsTrainer /opt/RequestsTrainer/