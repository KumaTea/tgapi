import requests


class Get:

    def __init__(self, url, data):
        self.url = url
        self.data = data

    def chat(self, item='id'):
        if 'message' in self.data:
            chat_item = self.data['message']['chat'][item]
        elif 'edited_message' in self.data:
            chat_item = self.data['edited_message']['chat'][item]
        elif 'channel_post' in self.data:
            chat_item = self.data['channel_post']['chat'][item]
        elif 'edited_channel_post' in self.data:
            chat_item = self.data['edited_channel_post']['chat'][item]
        elif 'channel_post' in self.data:
            chat_item = self.data['left_chat_member']['chat'][item]
        else:
            chat_item = 0
        return chat_item

    def message(self, item='text'):
        if 'text' in item or 'message' in item:
            return self.data['message']['text']
        elif item == 'id':
            if 'message' in self.data:
                msg_id = self.data['message']['message_id']
            elif 'result' in self.data:
                msg_id = self.data['result']['message_id']
            else:
                msg_id = self.data['message']['message_id']
            return msg_id
        elif item == 'type':
            if 'message' in self.data:
                if 'new_chat_member' in self.data['message']:
                    return 'new chat member'
                elif 'text' in self.data['message']:
                    return 'text'
                elif 'photo' in self.data['message']:
                    return 'photo'
                elif 'video' in self.data['message']:
                    return 'video'
                elif 'sticker' in self.data['message']:
                    return 'sticker'
                elif 'animation' in self.data['message']:
                    return 'gif'
                elif 'document' in self.data['message']:
                    return 'file'
                elif 'edited_message' in self.data:
                    return 'edited'
                else:
                    return 'unknown'
            elif 'channel_post' or 'edited_channel_post' in self.data:
                return 'channel post'
            elif 'left_chat_member' in self.data:
                return 'left chat member'
            else:
                return 'undefined'
        else:
            return self.data['message'][item]

    def text(self):
        return self.message('text')

    def msgid(self):
        return self.message('id')

    def type(self):
        return self.message('type')

    def caption(self):
        return self.message('caption')

    def reply(self, item='text'):
        if 'reply_to_message' in self.data['message']:
            self.data = self.data['reply_to_message']
            if 'id' in item:
                reply = self.message('id')
            elif item == 'user':
                reply = self.user('id')
            elif 'text' in item or 'message' in item:
                reply = self.message('text')
            elif item == 'type':
                reply = self.message('type')
            elif 'file' in item:
                reply = self.file('file_id')
            elif 'first' in item:
                reply = self.data['message']['from']['first_name']
            elif 'last' in item:
                reply = self.data['message']['from'].get('last_name', '')
            elif 'username' in item:
                reply = self.data['message']['from'].get('username', 'No username')
            else:
                reply = 0
        else:
            reply = 0
        return reply

    def file(self, item='file_id', media_type=None):
        if item == 'id':
            item = 'file_id'
        if media_type:
            if 'photo' in media_type:
                return self.data['message']['photo'][-1][item]
            else:
                return self.data['message'][media_type][item]
        else:
            if 'photo' in self.data['message']:
                return self.data['message']['photo'][-1][item]
            elif 'video' in self.data['message']:
                return self.data['message']['video'][item]
            elif 'sticker' in self.data['message']:
                return self.data['message']['sticker'][item]
            elif 'animation' in self.data['message']:
                return self.data['message']['animation'][item]
            elif 'document' in self.data['message']:
                return self.data['message']['document'][item]
            else:
                return 'Unknown Type'

    def photo(self, item='file_id'):
        return self.file(item, media_type='photo')

    def video(self, item='file_id'):
        return self.file(item, media_type='video')

    def sticker(self, item='file_id'):
        return self.file(item, media_type='sticker')

    def animation(self, item='file_id'):
        return self.file(item, media_type='animation')

    def gif(self, item='file_id'):
        return self.file(item, media_type='animation')

    def document(self, item='file_id'):
        return self.file(item, media_type='document')

    def user(self, item='id'):
        if item == 'id':
            user_info = self.data['message']['from']['id']
        elif 'first' in item:
            user_info = self.data['message']['from']['first_name']
        elif 'last' in item:
            user_info = self.data['message']['from'].get('last_name', 'No last name')
        elif item == 'username':
            user_info = self.data['message']['from'].get('username', 'No username')
        elif 'lang' in item:
            user_info = self.data['message']['from'].get('language_code', 'zh-Hans')
        elif item == 'bot':
            user_info = self.data['message']['from']['is_bot']
        else:
            user_info = 'Unknown argument'
        return user_info

    def group_admin(self, chat_id):
        if type(chat_id) == dict:
            chat_id = self.chat('id')
        answer = {
            "chat_id": chat_id,
        }
        get_admin = f'{self.url}getChatAdministrators'
        admins = requests.post(get_admin, data=answer).json()
        admin_list = []
        for admin_user in admins['result']:
            admin_list.append(admin_user['user']['id'])
        return admin_list


# POST

class Query:

    def __init__(self, url, chat_id):
        self.url = url
        self.chat_id = chat_id

    def chat(self, item=None, raw=False):
        answer = {
            "chat_id": self.chat_id,
        }
        get_chat = f'{self.url}getChat'
        chat = requests.post(get_chat, data=answer).json()
        if raw:
            return chat
        else:
            if item:
                return chat[item] if item in chat else None
            else:
                return chat['id'] if str(self.chat_id).startswith('@') else chat['username']

    def group_admin(self, chat_id, raw=False):
        answer = {
            "chat_id": chat_id,
        }
        get_admin = f'{self.url}getChatAdministrators'
        admins = requests.post(get_admin, data=answer).json()
        if raw:
            return admins
        else:
            admin_list = []
            for admin_user in admins['result']:
                admin_list.append(admin_user['user']['id'])
            return

    def chat_administrators(self, chat_id, raw=False):
        return self.group_admin(chat_id, raw)


class Send:

    def __init__(self, url, chat_id):
        self.url = url
        self.chat_id = chat_id

    def text(self, text, reply_to=None, parse=None, no_preview=True, **kwargs):
        answer = {
            "chat_id": self.chat_id,
            "text": text,
            "disable_web_page_preview": no_preview,
        }
        if reply_to:
            answer['reply_to_message_id'] = reply_to
        if parse:
            answer['parse_mode'] = parse
        if kwargs:
            for key, value in kwargs.items():
                answer[key] = value
        msg_url = f'{self.url}sendMessage'
        result = requests.post(msg_url, data=answer)
        return result.json()

    def message(self, text, reply_to=None, parse=None, no_preview=True, **kwargs):
        return self.text(text, reply_to, parse, no_preview, **kwargs)

    def markdown(self, text, reply_to=None, no_preview=True, **kwargs):
        return self.text(text, reply_to, 'Markdown', no_preview, **kwargs)

    def sticker(self, file_id, reply_to=None):
        answer = {
            "chat_id": self.chat_id,
            "sticker": file_id,
        }
        if reply_to:
            answer['reply_to_message_id'] = reply_to
        msg_url = f'{self.url}sendSticker'
        result = requests.post(msg_url, data=answer)
        return result.json()

    def photo(self, photo, caption=None, reply_to=False, upload=False):
        msg_url = f'{self.url}sendPhoto'
        answer = {
            "chat_id": self.chat_id,
        }
        if reply_to:
            answer['reply_to_message_id'] = reply_to
        if caption:
            answer['caption'] = caption
        if upload:
            with open(photo, 'rb') as fl:
                sending = {'photo': fl}
                result = requests.post(msg_url, data=answer, files=sending)
        else:
            answer['photo'] = photo
            result = requests.post(msg_url, data=answer)
        return result.json()

    def video(self, video, caption=None, reply_to=False, upload=False):
        msg_url = f'{self.url}sendVideo'
        answer = {
            "chat_id": self.chat_id,
        }
        if reply_to:
            answer['reply_to_message_id'] = reply_to
        if caption:
            answer['caption'] = caption
        if upload:
            with open(video, 'rb') as fl:
                sending = {'video': fl}
                result = requests.post(msg_url, data=answer, files=sending)
        else:
            answer['video'] = video
            result = requests.post(msg_url, data=answer)
        return result.json()

    def gif(self, gif, caption=None, reply_to=False, upload=False):
        msg_url = f'{self.url}sendAnimation'
        answer = {
            "chat_id": self.chat_id,
        }
        if reply_to:
            answer['reply_to_message_id'] = reply_to
        if caption:
            answer['caption'] = caption
        if upload:
            with open(gif, 'rb') as fl:
                sending = {'animation': fl}
                result = requests.post(msg_url, data=answer, files=sending)
        else:
            answer['animation'] = gif
            result = requests.post(msg_url, data=answer)
        return result.json()

    def animation(self, gif, caption=None, reply_to=False, upload=False):
        return self.gif(gif, caption, reply_to, upload)

    def mediagroup(self, album, reply_to=False, upload=False):
        """
        album = [
            {'type': 'photo', 'media': ''},
            {'type': 'photo', 'media': ''},
            ]
        """
        if type(album) != list:
            raise TypeError

        msg_url = f'{self.url}sendMediaGroup'
        answer = {
            "chat_id": self.chat_id,
        }
        if reply_to:
            answer['reply_to_message_id'] = reply_to
        if upload:
            album_files = {}
            for i in range(len(album)):
                print('album', album)
                album_files[i] = open(album[i]['media'], 'rb')
                print('album_files', album_files)
                album[i]['media'] = album_files[i]
            sending = {'media': album}
            print(sending)
            result = requests.post(msg_url, files=sending, data=answer)
            for i in range(len(album)):
                album_files[i].close()
        else:
            answer['media'] = album
            result = requests.post(msg_url, data=answer)
        return result.json()

    def album(self, album, reply_to=False, upload=False):
        return self.mediagroup(album, reply_to, upload)

    def file(self, file, caption=None, reply_to=False, upload=False):
        msg_url = f'{self.url}sendDocument'
        answer = {
            "chat_id": self.chat_id,
        }
        if reply_to:
            answer['reply_to_message_id'] = reply_to
        if caption:
            answer['caption'] = caption
        if upload:
            with open(file, 'rb') as fl:
                sending = {'document': fl}
                result = requests.post(msg_url, data=answer, files=sending)
        else:
            answer['document'] = file
            result = requests.post(msg_url, data=answer)
        return result.json()

    def custom(self, command, **kwargs):
        answer = {}
        for key, value in kwargs.items():
            answer[key] = value
        msg_url = self.url + f'send{command}'
        result = requests.post(msg_url, data=answer)
        return result.json()


class Edit:

    def __init__(self, url, chat_id, msg_id):
        self.url = url
        self.chat_id = chat_id
        self.msg_id = msg_id

    def text(self, text):
        answer = {
            "chat_id": self.chat_id,
            "message_id": self.msg_id,
            "text": text,
        }
        edit_text = f'{self.url}editMessageText'
        result = requests.post(edit_text, data=answer)
        return result.json()

    def message(self, text):
        return self.text(text)


class Delete:

    def __init__(self, url, chat_id, msg_id):
        self.url = url
        self.chat_id = chat_id
        self.msg_id = msg_id

    def message(self, msg_id=None):
        if self.msg_id:
            msg_id = self.msg_id
        answer = {
            "chat_id": self.chat_id,
            "message_id": msg_id,
        }
        del_msg = f'{self.url}deleteMessage'
        result = requests.post(del_msg, data=answer)
        return result.json()


class Set:

    def __init__(self, url, webhook=None):
        self.url = url
        self.webhook_url = webhook

    def webhook(self, webhook=None, source_type='url'):
        if 'rok' in source_type:
            webhook_url = requests.get('http://127.0.0.1:4040/api/tunnels').json()['tunnels'][0]['public_url']
        else:
            if self.webhook_url:
                webhook_url = self.webhook_url
            else:
                webhook_url = webhook
            start_https = webhook_url.find('//')
            if start_https == -1:
                webhook_url = f'https://{webhook_url}'
        answer = {
            "url": webhook_url
        }
        set_url = f'{self.url}setWebHook'
        result = requests.post(set_url, data=answer)
        return result.json()
