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
        'Please input your bot API.\nIt should include \":\", can start with \"bot\", but without \"/\".\n')
    if token.startswith('bot') and ':' in token:
        return token[3:]
    else:
        return token


def query_token(item=None):
    if not item:
        if os.path.isfile('token_bot.txt'):
            return read_file('token_bot.txt', True)
        else:
            token = new_token()
            id_end = token.find(':')
            if not os.path.isfile('token_' + token[:id_end]):
                write_file('token_' + token[:id_end], True, token)
            return token
    else:
        if os.path.isfile(item):  # token_12345.txt
            return read_file(item, True)
        elif os.path.isfile(f'token_{item}'):  # token_12345.txt
            return read_file(f'token_{item}', True)
        else:
            if ':' in str(item):  # Bot token
                id_end = item.find(':')
                write_file('token_' + item[:id_end], True, item)
                return item
            else:  # Bot id
                token = new_token()
                id_end = token.find(':')
                write_file('token_' + token[:id_end], True, token)
                return token



def set_proxy(ip='127.0.0.1', port='1080', protocol='http'):
    proxy = f'{protocol}://{ip}:{port}'
    os.environ['http_proxy'] = proxy
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
    return proxy
