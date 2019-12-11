# TGAPI

## TERMINATION
Due to various reasons, this project have been TERMINATED.

For the concern of projects using this, the module on `pypi` will not be deleted, but switching to a stable one is highly recommended.

Thank you for your support.

---

`tgapi`, A Python module for I/O of Telegram **bot** API

#### Disclaimer
This project is developed and maintained by unprofessional developer.

DO NOT use it in production environment.

## Install
```bash
pip install tgapi
```

## Tutorial
First, let's initialize a bot session:
```python
import tgapi

bot_token = 'bot123456789:AbCdEfGhIjKlMnOpQrStUvWxYz'
my_bot = tgapi.bot(bot_token)
```
Then, we can use `my_bot` to process data.

### Get
Imagine we've received a `json` text message from `flask` by:
```python
import flask

data = flask.request.json
```
Then we can do this to get the text:
```python
text_message = my_bot.get(data).message('text')
```

### Send, Edit and Delete
```python
chat_id = 123456789

# Send

my_bot.send(chat_id).photo('FileIDAaAaAa121212', 'This is a photo sent by tgapi')

# Edit

message_id = 1234

my_bot.edit(chat_id, message_id).text('Edited to this')

# Delete
# You can do:

my_bot.delete(chat_id, message_id).message()

# or:

my_bot.delete(chat_id).message(message_id)
```
