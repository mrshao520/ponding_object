# 拉取镜像
FROM nvidia/cuda:11.2.2-cudnn8-devel-ubuntu20.04

ENV NVIDIA_VISIBLE_DEVICES=all NVIDIA_CAPABILITIES=compute,utility \
    LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64

ENV TZ=Asia/Shanghai \
    DEBIAN_FRONTEND=noninteractive

# 修改源地址
RUN cp /etc/apt/sources.list /etc/apt/sources_backup.list && \
    sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
    sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
    # 更新软件
    apt-get update && \
    apt-get upgrade -y --fix-missing &&\
    apt-get install -y locales && \
    apt-get install -y wget build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev \
    libreadline-dev libffi-dev libsqlite3-dev libbz2-dev liblzma-dev &&\
    # 安装所需要的软件
    apt-get install -y net-tools vim git cmake libglib2.0-dev &&\
    locale-gen zh_CN && \
    locale-gen zh_CN.utf8 && \
    apt-get install -y ttf-wqy-microhei ttf-wqy-zenhei xfonts-wqy &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /temp

# 下载python
RUN wget https://www.python.org/ftp/python/3.9.10/Python-3.9.10.tgz && \
    tar -xvf Python-3.9.10.tgz &&\
    # 编译&安装python
    cd Python-3.9.10 && \
    ./configure --enable-optimizations && \
    make && \
    make install &&\
    ln -s /usr/local/bin/python3 /usr/local/bin/python && \
    ln -s /usr/local/bin/pip3 /usr/local/bin/pip

# 下载FastDeploy库
RUN git clone -b release/1.0.7 https://github.com/PaddlePaddle/FastDeploy.git 

# python版本支持
# 不支持 compute_35
COPY ./cuda.cmake FastDeploy/cmake/cuda.cmake
# COPY ./CMakeLists.cmake FastDeploy/CMakeLists.cmake

RUN pip install wheel &&\
    cd FastDeploy/python &&\
    export ENABLE_PADDLE_BACKEND=ON &&\
    export ENABLE_TEXT=ON &&\
    export WITH_GPU=ON &&\
    python setup.py build &&\
    python setup.py bdist_wheel &&\
    cd dist &&\
    ls -al 
# 有时候编译的是fastdeploy_gpu_python，有时候是fastdeploy_python

RUN cd FastDeploy/python/dist &&\
    pip install fastdeploy_gpu_python-1.0.7-cp39-cp39-linux_x86_64.whl

# python 缺少的链接文件位置
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/nvidia/nsight-compute/2022.2.1/host/linux-desktop-glibc_2_11_3-x64/Mesa

# # cpp 版本编译
# 手动修改CMakeLists.txt文件
# COPY ./CMakeLists.txt FastDeploy/CMakeLists.txt

# RUN cd FastDeploy &&\
#     mkdir build && cd build &&\
#     cmake .. &&\
#     make -j12 &&\
#     make install

# # c++ 缺少的链接文件位置
# ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/third_libs/install/paddle_inference/paddle/lib/:/usr/local/third_libs/install/fast_tokenizer/lib

# WORKDIR /app

# # COPY ./app.py /app
# # COPY ./config.json /app
# # COPY ./JsonParser.py /app
# # COPY ./Longitude.py /app
# # COPY ./PondingTable.py /app
# # COPY ./UIE_Model.py /app
# # COPY ./UIE_Model2.py /app
# # COPY ./model_best /app/model_best
# COPY ./dev_requirements.txt /app

# RUN pip install -r dev_requirements.txt &&\
#     rm -rf /temp 

# EXPOSE 5000
# # 指定应用程序入口
# CMD ["python","gunicorn", "-c", "gunicorn_config.py" ,"app:app"]

# LABEL maintainer="Shao <2632240096@qq.com>"