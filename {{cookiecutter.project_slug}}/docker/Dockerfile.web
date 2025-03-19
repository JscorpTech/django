FROM jscorptech/django:v0.5

WORKDIR /code

COPY ./ /code

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

CMD ["sh", "./resources/scripts/entrypoint.sh"]
