FROM mysql:latest
ENV MYSQL_ROOT_PASSWORD Honeysuckle@123!
ENV MYSQL_DATABASE honeysuckle_db
ENV WORK_PATH /usr/local/work
ENV MYSQL_USER honeysuckle
ENV MYSQL_PASSWORD honeysuckle123

COPY my.cnf /etc/mysql/conf.d/my.cnf

COPY ./init.sql /docker-entrypoint-initdb.d/

#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
#RUN apt-get update && apt-get install -y tzdata
