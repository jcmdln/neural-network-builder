FROM python:3.7
COPY . /app
RUN pip install -r requirements.txt
