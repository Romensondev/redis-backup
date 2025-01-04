FROM debian:12-slim

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY run.bash /app/run.bash
COPY send-s3.py /app/send-s3.py

WORKDIR /app

RUN chmod +x run.bash

ENTRYPOINT ["./run.bash"]