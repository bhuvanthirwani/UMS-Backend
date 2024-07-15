FROM python:3.11.1-slim

USER root

RUN apt-get update && \
    apt-get -y install procps net-tools wget htop curl vim nginx supervisor bash --no-install-recommends && \
    apt-get clean

ARG FLASK_MODE=staging
ENV APP_PATH=/usr/src/app
ENV FLASK_ENV=${FLASK_MODE}
ENV PYTHONPATH=${APP_PATH}

WORKDIR $APP_PATH

# Add application files
COPY . /usr/src/app/

RUN mkdir -p $APP_PATH /var/log/ums /var/log/supervisord /var/log/gunicorn && \
    # install poetry and dependencies
    python3 -m pip install --no-cache-dir poetry==1.7.1 && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi && \
    # Remove the default Nginx configuration
    rm /etc/nginx/sites-enabled/default && \
    # settings environment variables.
    test -e .env.production && \
    cp .env.production /usr/src/app/.env || true

# Copy the Nginx configuration file
COPY config/nginx.conf /etc/nginx/sites-available/
COPY config/supervisord.ini /etc/supervisor/conf.d/

RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/ && \
    echo "files = /etc/supervisor/conf.d/*.ini" >> /etc/supervisor/supervisord.conf

# Health check must be on gunicorn port.
HEALTHCHECK --interval=60s --timeout=10s --retries=1 CMD curl -f http://localhost:8000/ || exit 1
EXPOSE 5000
# run server
CMD ["supervisord", "--nodaemon", "-c", "/etc/supervisor/supervisord.conf"]
