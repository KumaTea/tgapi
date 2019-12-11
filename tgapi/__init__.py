from .bot import Bot


__version__ = '0.3.4'


def bot(token=None):
    return Bot(token)
