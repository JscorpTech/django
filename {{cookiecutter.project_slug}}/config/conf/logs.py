import logging

logging.basicConfig(
    filename="./resources/logs/django.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
