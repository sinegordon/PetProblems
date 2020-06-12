FROM python:3.8-alpine
LABEL maintainer="sinegordon@gmail.com"
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt --no-cache-dir
COPY . .
ENV PYTHONUNBUFFERED=1
STOPSIGNAL SIGINT
CMD ["python3", "./service.py"]