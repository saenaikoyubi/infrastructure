FROM python:3.9-slim

WORKDIR /gate

ENV TZ Asia/Tokyo

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
# CMD ["/bin/bash"]