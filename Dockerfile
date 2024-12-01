FROM python:3.12-slim

RUN mkdir /app

COPY requirements.txt /app/
COPY create_tables.sql /app/

COPY src /app/

RUN python -m pip install -r /app/requirements.txt

WORKDIR /app

# Открываем порт
EXPOSE 5000

ENTRYPOINT ["python", "app.py"]