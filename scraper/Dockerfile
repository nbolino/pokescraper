FROM python:3.10

ENV ENV local
COPY . /tmp/scraper
WORKDIR /tmp/scraper
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]