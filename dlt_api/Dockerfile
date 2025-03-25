
FROM python:latest
WORKDIR /app

COPY requirements.txt .

# install dependencies for pipeline
RUN pip install --no-cache-dir -r requirements.txt

COPY chit_pipeline.py .  

CMD ["python", "chit_pipeline.py"]


