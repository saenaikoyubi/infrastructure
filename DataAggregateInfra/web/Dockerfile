FROM python:3.9-slim

ENV TZ Asia/Tokyo

WORKDIR /web

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]