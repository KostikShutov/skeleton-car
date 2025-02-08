import logging
import sys


def configureLogger() -> None:
    logging.basicConfig(
        stream=sys.stdout,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        level=logging.INFO,
    )
