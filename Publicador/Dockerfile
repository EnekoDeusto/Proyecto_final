FROM python:3.12.3

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir pandas paho-mqtt

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
