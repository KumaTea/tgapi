import os
import base64


def read_file(filename, encrypt=False):
    if encrypt:
        with open(filename, 'rb') as f:
            return base64.b64decode(f.read()).decode('utf-8')
    else:
        with open(filename, 'r') as f:
            return f.read()


def write_file(filename, encrypt=False, content=None):
    if not content:
        raise SystemError
    else:
        if encrypt:
            with open(filename, 'wb') as f:
                f.write(base64.b64encode(content.encode('utf-8')))
            return True
        else:
            with open(filename, 'w') as f:
                f.write(content)
            return True


def new_token():
    token = input(
        'Please input your bot API.\nIt should start with \"bot\", include \":\" and without \"/\".\n')
    if token.startswith('bot') and ':' in token:
        return token
    else:
        return False


def query_token(item=None):
    if not item:
        if os.path.isfile('token_bot.txt'):
            return read_file('token_bot.txt', True)
        else:
            token = new_token()
            while not token:
                print('Illegal token, please retry.')
                token = new_token()
            id_end = token.find(':')
            if not os.path.isfile('token_' + token[3:id_end]):
                write_file('token_' + token[3:id_end], True, token)
            return token
    else:
        if type(item) == int:  # Bot id
            if os.path.isfile('token_' + str(item)):
                return read_file('token_' + str(item), True)
            else:
                token = new_token()
                while not token:
                    print('Illegal token, please retry.')
                    token = new_token()
                id_end = token.find(':')
                write_file('token_' + token[3:id_end], True, token)
                return token
        else:
            if os.path.isfile(item):  # token_12345
                return read_file(item, True)
            else:
                id_end = item.find(':')
                if not os.path.isfile('token_' + item[3:id_end]):
                    write_file('token_' + item[3:id_end], True, item)
                return item
