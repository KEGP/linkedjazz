FROM python:3


COPY ../playingbringtogether /app/
WORKDIR /app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8888
CMD uvicorn backend:app --host 0.0.0.0 --port 8888
