FROM python:3.12.0-slim-bullseye
user root

EXPOSE 5050

RUN apt-get update && apt-get upgrade

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade "psycopg[binary,pool]"
RUN pip install --no-cache-dir -r requirements.txt && rm -f /requirements.txt

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY imagocms /app/imagocms

RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app

RUN chown -R app:app /app/imagocms/static/images
USER app

CMD exec gunicorn -w 4 -b 0.0.0.0:5050 'imagocms.app:create_app()'