FROM jscorptech/django:v0.5

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

CMD ["sh", "./entrypoint.sh"]
