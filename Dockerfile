# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /eth_get_block_by_number
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV CLOUDFLARE_URL=https://cloudflare-eth.com
ENV CAPACITY=10
ENV BASE_PATH=/eth_get_block_by_number
CMD ["flask", "run", "--host=0.0.0.0"]
