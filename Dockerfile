FROM python:latest

RUN apt update && apt upgrade -y && \
    apt install -y bash git which && \
    rm -rf /var/lib/apt/lists/*

# RUN git clone https://github.com/20xygen/MIPTpay.git --branch checkpoint_3 /MIPTpay
COPY . .
# WORKDIR /MIPTpay

RUN python3 -m venv .venv
RUN /bin/bash -c "source .venv/bin/activate && pip install poetry"
RUN .venv/bin/pip install poetry

RUN .venv/bin/poetry lock
RUN .venv/bin/poetry install

# RUN python src/miptpaydj/manage.py makemigrations
# RUN python src/miptpaydj/manage.py migrate
# RUN .venv/bin/poetry run setup

RUN . .venv/bin/activate && \
    python src/miptpaydj/manage.py makemigrations && \
    python src/miptpaydj/manage.py migrate && \
    poetry run setup

EXPOSE 8000

CMD . .venv/bin/activate && \
    python src/miptpaydj/manage.py runserver 0.0.0.0:8000
