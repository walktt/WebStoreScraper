FROM python

RUN mkdir -p /app
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

VOLUME ["/app/data"]

CMD ["python", "main.py"]