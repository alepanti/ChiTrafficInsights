FROM kestra/kestra:latest
USER root

RUN pip install --no-cache-dir \
    requests \
    google-cloud-storage \
    pytz \
    dlt[bigquery,filesystem]>=1.6.1 \
    google-cloud-bigquery-storage 

RUN dlt --non-interactive init filesystem bigquery
RUN rm -f .dlt/secrets.toml