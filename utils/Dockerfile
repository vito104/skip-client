FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    wget build-essential perl zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

RUN wget https://github.com/openssl/openssl/releases/download/openssl-3.5.0/openssl-3.5.0.tar.gz \
    && tar -xzf openssl-3.5.0.tar.gz \
    && cd openssl-3.5.0 \
    && ./config --prefix=/opt/openssl-custom --openssldir=/opt/openssl-custom/ssl \
    && make -j$(nproc) \
    && make install

ENV PATH="/opt/openssl-custom/bin:$PATH"

WORKDIR /work

CMD ["bash"]
