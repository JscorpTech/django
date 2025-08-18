FROM jscorptech/django:v0.5

ARG SCRIPT="entrypoint.sh"
ENV SCRIPT=$SCRIPT

WORKDIR /code

COPY ./ /code

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

RUN mv ./resources/scripts/$SCRIPT . && chmod +x $SCRIPT

CMD sh $SCRIPT
