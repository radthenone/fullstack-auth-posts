FROM node:21-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm ci
RUN npm cache clean --force

COPY . .

EXPOSE 3000

CMD ["npm", "run", "docker"]
