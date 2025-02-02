# syntax=docker/dockerfile:1

FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN groupadd -g 2000 rekrutka && \
    useradd -u 2000 -g rekrutka rekrutka && \
    mkdir -p /rekrutka && \
    mkdir -p /home/rekrutka && \
    chown rekrutka:rekrutka -R /home/rekrutka


RUN apt-get update && apt-get install -y weasyprint gettext python3-dev && apt-get clean && \
     rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*


WORKDIR /rekrutka
COPY backend/requirements.txt /rekrutka/

USER 2000:2000

RUN pip install -U pip setuptools && pip install -r /rekrutka/requirements.txt

ENTRYPOINT ["/rekrutka/entrypoint.sh"]