FROM python:3.10 as production

WORKDIR app

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
