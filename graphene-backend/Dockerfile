FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt


COPY . .

# Set the PYTHONPATH to ensure Python can find your module
ENV PYTHONPATH /usr/src/app

CMD ["flask", "--app", "app.main", "run", "--host", "0.0.0.0", "--port", "8000", "--debug"]

EXPOSE 8000
