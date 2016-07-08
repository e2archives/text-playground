FROM node:6
MAINTAINER eterna2 <eterna2@hotmail.com>

EXPOSE 80
WORKDIR /app
RUN npm install pm2 -g

COPY package.json /app/package.json
RUN npm install

COPY ./modules /app/modules
COPY ./routes /app/routes
COPY ./conf.json /app/conf.json
COPY ./index.js /app/index.js

CMD pm2 start index.js --no-daemon