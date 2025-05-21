FROM python:3.13-slim

WORKDIR /app

COPY src/SpotifyAnalyzer/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/SpotifyAnalyzer/ .

RUN mkdir -p /app/uploads

COPY .env /app/

ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["python", "main.py"]
