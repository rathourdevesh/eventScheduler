FROM python

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /srv/eventScheduler

COPY requirements.txt /srv/eventScheduler/
RUN apt update && apt upgrade

RUN pip install -r requirements.txt
COPY . /srv/eventScheduler/
ENTRYPOINT ["python", "run.py"]