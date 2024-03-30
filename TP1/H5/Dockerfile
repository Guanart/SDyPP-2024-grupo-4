FROM node:19.0.0-alpine3.16
ENV NODE_ENV=production

WORKDIR /usr/src/app
ADD cliente_servidor.js cliente_servidor.js
ENTRYPOINT ["node", "cliente_servidor.js"]