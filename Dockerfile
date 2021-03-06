FROM python:3.8

WORKDIR /app
COPY . .

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "main.py"]