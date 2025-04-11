FROM node:lts-alpine

ARG basedir=/opt/honeysuckle
ARG APP_ENV

RUN npm config set registry https://registry.npmmirror.com
RUN yarn config set registry https://registry.npmmirror.com

# 创建应用目录
RUN mkdir -p ${basedir}/frontend
ARG workdir=${basedir}/frontend

ENV APP_ENV=${APP_ENV} BASE_DIR=${basedir} WORK_DIR=${workdir}

WORKDIR ${workdir}

COPY package*.json ./

RUN npm install -g pnpm

RUN pnpm install
COPY . .

# 赋予执行权限
RUN chmod +x frontend-entrypoint.sh

CMD ["sh", "frontend-entrypoint.sh"]
