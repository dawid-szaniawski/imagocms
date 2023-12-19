FROM python:3.12.1-alpine3.19
USER root

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt
RUN apk update && apk upgrade && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade "psycopg[binary,pool]" && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -f /requirements.txt && \
    addgroup appgroup && adduser -D -H appuser -G appgroup

WORKDIR /app
USER appuser

COPY --chown=appuser:appgroup imagocms /app/imagocms
EXPOSE 5050

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:5050", "imagocms.app:create_app()" ]
