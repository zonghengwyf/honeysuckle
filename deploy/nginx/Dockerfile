FROM nginx:stable-alpine

# RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

ARG APP_ENV
ENV APP_ENV=${APP_ENV}

ARG basedir=/opt/honeysuckle

RUN mkdir -p ${basedir}/nginx

ADD . ${basedir}/deploy/nginx

# 设置工作目录
WORKDIR ${basedir}/deploy/nginx

RUN chmod +x nginx-entrypoint.sh

CMD ["sh", "nginx-entrypoint.sh"]