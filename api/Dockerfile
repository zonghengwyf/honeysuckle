FROM python:3.10

ARG basedir=/opt/honeysuckle

RUN mkdir -p ${basedir}/api

ADD . ${basedir}/api

WORKDIR ${basedir}/api

RUN cp /etc/apt/sources.list /etc/apt/sources.list.backup

RUN echo "deb http://mirrors.aliyun.com/debian/ bullseye main contrib non-free" > /etc/apt/sources.list
RUN echo "deb-src http://mirrors.aliyun.com/debian/ bullseye main contrib non-free" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg libasound2-dev libsndfile-dev

RUN pip install --upgrade pip wheel && pip install uwsgi -i https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=200 \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=200 \
    && rm requirements.txt

RUN chmod +x start.sh

CMD ["sh", "start.sh"]

# ===============================================frontend=======================================
RUN apt-get install -y nodejs npm
RUN mkdir -p ${basedir}/frontend/assets
WORKDIR ${basedir}/frontend

COPY package.json ${basedir}/frontend/
COPY package-lock.json ${basedir}/frontend/
RUN npm install --registry=https://registry.npmmirror.com

COPY . .

RUN npm run build
