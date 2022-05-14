FROM python:3.9
WORKDIR /datacenter
LABEL maintainer="Jundong Xu <xu.jundong@aliyun.com>"
ENV DOCKER=true
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . .