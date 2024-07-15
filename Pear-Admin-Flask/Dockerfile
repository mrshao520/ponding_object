# 拉取镜像
FROM flastdeploy


WORKDIR /app

COPY ./dev_requirements.txt /app

RUN pip install -r dev_requirements.txt &&\
    rm -rf /temp 

EXPOSE 5000
# 指定应用程序入口
# gunicorn -c gunicorn_config.py app:app
# CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]

LABEL maintainer="Shao <2632240096@qq.com>"