FROM python:3.8-slim-buster

ARG basedir=/opt/honeysuckle
ARG model_path=/var/model

ENV MODEL_PATH=${model_path} BASE_DIR=${basedir}

RUN mkdir -p ${basedir}/backend
RUN mkdir -p /var/run/honeysuckle
RUN chown www-data:www-data /var/run/honeysuckle

ADD . ${basedir}/backend

WORKDIR ${basedir}/backend

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
  sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends build-essential python3-distutils vim iputils-ping telnet wget ffmpeg libsndfile1 libasound2-dev libsndfile-dev libhdf5-dev

RUN pip install celery==5.1.2 -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install --upgrade pip wheel setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install gunicorn uvicorn -i https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=600 && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=600 && \
    rm requirements.txt

RUN mkdir -p ${model_path}/2stems ${model_path}/4stems ${model_path}/5stems

#COPY 2stems.tar.gz /tmp/2stems.tar.gz
RUN wget -O /tmp/2stems.tar.gz https://github.com/deezer/spleeter/releases/download/v1.4.0/2stems.tar.gz && \
    tar -xvzf /tmp/2stems.tar.gz -C ${model_path}/2stems/ && \
    touch ${model_path}/2stems/.probe

#COPY 4stems.tar.gz /tmp/4stems.tar.gz
RUN wget -O /tmp/4stems.tar.gz https://github.com/deezer/spleeter/releases/download/v1.4.0/4stems.tar.gz && \
    tar -xvzf /tmp/4stems.tar.gz -C ${model_path}/4stems/ && \
    touch ${model_path}/4stems/.probe

#COPY 5stems.tar.gz /tmp/5stems.tar.gz
RUN  wget -O /tmp/5stems.tar.gz https://github.com/deezer/spleeter/releases/download/v1.4.0/5stems.tar.gz && \
    tar -xvzf /tmp/5stems.tar.gz -C ${model_path}/5stems/ && \
    touch ${model_path}/5stems/.probe

RUN apt-get remove --purge -y build-essential && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod +x entrypoint.sh

CMD ["sh", "entrypoint.sh"]

