from .bot import Bot


__version__ = '0.3.2.9'


def bot(token=None):
    return Bot(token)
