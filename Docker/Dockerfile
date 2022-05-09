FROM ubuntu:20.04 as builder

ENV TZ=US/Central
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /dependencies

RUN apt-get update && \
    apt-get install -y \
        git cmake vim wget curl\
        python3-dev python3-pip clang libc++-dev libc++abi-dev 


COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

# instatiate with docker run --rm -it -v $"$PWD":/root -w /root {tag}

ENTRYPOINT [ "bash" ]