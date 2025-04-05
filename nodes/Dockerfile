FROM python:3.10-slim

WORKDIR /app
COPY . /app
RUN pip install fastapi uvicorn requests python-multipart

ENV NODE_PORT=9001
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $NODE_PORT"]
