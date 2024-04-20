#!/bin/bash

celery -A config worker --loglevel=info &

sleep 10 && celery -A config beat --loglevel=info &
sleep 10 && celery -A config flower --loglevel=info &

wait

exit $?
