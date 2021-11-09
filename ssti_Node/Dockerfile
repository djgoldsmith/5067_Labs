FROM node:buster-slim

#RUN apt-get update && apt-get install -y ncat

WORKDIR /opt/app

#Requirements
ADD ./app /opt/app/

RUN npm install
EXPOSE 3000


ADD flag.txt /

CMD ["node", "server.js"]