FROM jscorptech/django:v0.2

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

CMD ["sh", "./scripts/entrypoint.sh"]
