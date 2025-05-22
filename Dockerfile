FROM python:3.13-slim

WORKDIR /app

COPY ./src /app/src

COPY requirements.txt /app/

COPY .env /app/

RUN mkdir -p /app/uploads

RUN mkdir -p /app/database && touch /app/database/database.db

RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONPATH=/app/src

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "src.main:app", "--workers=2", "--threads=4"]
