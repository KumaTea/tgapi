from .tools import query_token
from .io import *


class Bot:

    def __init__(self, token=None):
        bot_token = 'bot' + query_token(token)
        api_url = f'https://api.telegram.org/{bot_token}/'
        self.url = api_url

    def get(self, data):
        return Get(self.url, data)

    def send(self, chat_id):
        return Send(self.url, chat_id)

    def edit(self, chat_id=None, msg_id=None):
        return Edit(self.url, chat_id, msg_id)

    def delete(self, chat_id, msg_id=None):
        return Delete(self.url, chat_id, msg_id)

    def query(self, chat_id):
        return Query(self.url, chat_id)

    def set(self, webhook=None):
        return Set(self.url, webhook)
