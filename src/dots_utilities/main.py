import logging


def hello(name: str):
    """

    Greets you nicely.

    :param str name:    What should we call you?

    :return None
    """
    log = logging.getLogger(__name__)
    log.debug(f"Hi {name}! May you live long and prosper 🖖")
