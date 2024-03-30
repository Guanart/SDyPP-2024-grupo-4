FROM node:19.0.0-alpine3.16
ENV NODE_ENV=production

WORKDIR /usr/src/app
ADD servidor.js servidor.js
EXPOSE 8003
ENTRYPOINT ["node", "servidor.js"]