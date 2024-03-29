FROM python:3.10

WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg \
    libsm6 \
    libxext6 \
    libglib2.0-0

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY weights weights
COPY setup.cfg setup.cfg
COPY app.py app.py
COPY tests tests
COPY config config
COPY src src
COPY Makefile Makefile

ENV PYTHONPATH /app
ENV API_PORT 5000
ENV HOST 0.0.0.0

CMD python app.py
