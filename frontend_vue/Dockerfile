FROM node:16-bullseye

ARG BASE_DIR=/opt/honeysuckle/frontend

RUN mkdir -p ${BASE_DIR}
WORKDIR ${BASE_DIR}

COPY . .

RUN npm --registry https://registry.npm.taobao.org install
RUN npm run build

COPY ./build/dist /usr/share/nginx/html