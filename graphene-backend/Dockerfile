FROM python:3.11-slim

WORKDIR /usr/src/

COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

COPY . .


CMD ["python", "app/main.py"]


EXPOSE 8000
