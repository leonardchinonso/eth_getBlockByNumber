# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /eth_getBlockByNumber_with_docker
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV CLOUDFLARE_URL=https://cloudflare-eth.com
ENV CAPACITY=5
ENV BASE_PATH=/eth_getBlockByNumber_with_docker
CMD ["flask", "run", "--host=0.0.0.0"]
