FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/code

#SERVEUR SUR LE PORT 80
EXPOSE 80

#serveur uvicorn utilisé pour python
CMD ["uvicorn", "code.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

