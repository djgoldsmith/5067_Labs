#FROM cueh/flask
FROM python:3-slim

RUN apt-get update && apt-get install -y --no-install-recommends ncat

#Install the Selenium Driver
COPY REQUIREMENTS.txt /tmp/REQUIREMENTS.txt
RUN pip install -r /tmp/REQUIREMENTS.txt

#RUN useradd -r flask
#USER flask
WORKDIR /opt
ADD ./app /opt/app

CMD ["flask", "run", "--host=0.0.0.0"]