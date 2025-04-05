FROM python:3.10-slim

WORKDIR /app

COPY ./controller /app/controller
COPY ./utils /app/utils
COPY ./requirements.txt /app

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["uvicorn", "controller.main:app", "--host", "0.0.0.0", "--port", "8000"]

