FROM python:3.13-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc iproute2 net-tools libssl-dev && rm -rf /var/lib/apt/lists/*
RUN pip install sslpsk3 cryptography scapy
CMD ["sleep", "infinity"]