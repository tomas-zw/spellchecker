FROM python:3.8.3-slim-buster

WORKDIR /src

COPY . /src

RUN pip install -r requirements.txt

CMD ["python", "spellchecker.py"]

