from .bot import Bot


__version__ = '0.3.3.1'


def bot(token=None):
    return Bot(token)
