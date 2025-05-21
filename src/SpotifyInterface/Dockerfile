FROM python:3.13-slim

WORKDIR /app

COPY src/SpotifyInterface/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/SpotifyInterface/ .

RUN mkdir -p /app/uploads

COPY .env /app/

ENV PYTHONPATH=/app

CMD ["python", "main.py"]
