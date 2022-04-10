FROM python:3.10.4-slim-buster
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py"]