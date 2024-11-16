FROM python:3.13-slim

WORKDIR /gate04

ENV TZ Asia/Tokyo

COPY /Copy/requirements.txt requirements.txt
COPY /Copy/__init__.py app/__init__.py
COPY /Copy/__main__.py app/__main__.py
RUN pip install -r requirements.txt

CMD ["python","-m", "app"]

# CMD ["python", "sleep.py"]
# CMD ["/bin/bash"]