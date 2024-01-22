FROM python:3.10

ENV PYTHONBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

COPY . /code

COPY entrypoint.sh /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

CMD ["/code/entrypoint.sh"]

