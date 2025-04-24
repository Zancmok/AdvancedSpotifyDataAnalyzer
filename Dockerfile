FROM python:3.13-slim

WORKDIR /app

COPY ./src /app/src
COPY requirements.txt /app/

# Create the database folder and file in a single RUN statement
RUN mkdir -p /app/database && touch /app/database/database.db

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5000

CMD ["python", "/app/src/main.py"]
