from .bot import Bot


__version__ = '0.3.2.8.2'


def bot(token=None):
    return Bot(token)
