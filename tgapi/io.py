import requests


class Get:

    def __init__(self, url, data):
        self.url = url
        self.data = data

    def chat(self, item='id', data=None):
        if not data:
            data = self.data
        if 'message' in data:
            chat_item = data['message']['chat'][item]
        elif 'edited_message' in data:
            chat_item = data['edited_message']['chat'][item]
        elif 'channel_post' in data:
            chat_item = data['channel_post']['chat'][item]
        elif 'edited_channel_post' in data:
            chat_item = data['edited_channel_post']['chat'][item]
        elif 'channel_post' in data:
            chat_item = data['left_chat_member']['chat'][item]
        else:
            chat_item = 0
        return chat_item

    def message(self, item, prefix='message'):
        if item == 'text':
            return self.data[prefix]['text']
        elif item == 'id':
            if 'message' in self.data:
                msg_id = self.data['message']['message_id']
            elif 'result' in self.data:
                msg_id = self.data['result']['message_id']
            else:
                msg_id = self.data[prefix]['message_id']
            return msg_id
        elif item == 'type':
            if 'photo' in self.data[prefix]:
                return 'photo'
            elif 'video' in self.data[prefix]:
                return 'video'
            elif 'sticker' in self.data[prefix]:
                return 'sticker'
            elif 'document' in self.data[prefix]:
                return 'document'
            elif 'text' in self.data[prefix]:
                return 'text'
            else:
                return 'Unknown Type'
        return 'Undefined item'

    def reply(self, item):
        if 'reply_to_message' in self.data['message']:
            if item == 'id' or 'msgid':
                reply = self.data['message']['reply_to_message']['message_id']
            elif item == 'user':
                reply = self.data['message']['reply_to_message']['from']['id']
            elif item == 'text':
                reply = self.data['message']['reply_to_message']['text']
            elif item == 'type':
                reply = self.message('type', 'reply_to_message')
            elif item == 'fileid':
                reply = self.file('file_id', 'reply_to_message')
            elif item == 'first':
                reply = self.data['message']['reply_to_message']['from']['first_name']
            elif item == 'last':
                reply = self.data['message']['reply_to_message']['from'].get('last_name', '')
            elif item == 'username':
                reply = self.data['message']['reply_to_message']['from'].get('username', 'No username')
            else:
                reply = 0
        else:
            reply = 0
        return reply

    def file(self, item='file_id', prefix='message'):
        if item == 'id':
            item = 'file_id'
        if 'photo' in self.data[prefix]:
            file_item = self.data[prefix]['photo'][-1][item]
            return file_item
        elif 'video' in self.data[prefix]:
            file_item = self.data[prefix]['video'][item]
            return file_item
        elif 'sticker' in self.data[prefix]:
            file_item = self.data[prefix]['sticker'][item]
            return file_item
        elif 'document' in self.data[prefix]:
            file_item = self.data[prefix]['document'][item]
            return file_item
        else:
            return 'Unknown Type'

    def user(self, item):
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
            chat_id = self.chat('id', chat_id)
        answer = {
            "chat_id": chat_id,
        }
        get_admin = self.url + 'getChatAdministrators'
        admin_json = requests.post(get_admin, json=answer)
        admins = admin_json.json()
        admin_list = []
        for admin_user in admins['result']:
            admin_list.append(admin_user['user']['id'])
        return admin_list


# POST

class Send:

    def __init__(self, url, chat_id):
        self.url = url
        self.chat_id = chat_id

    def text(self, text, reply_to=None, parse=None):
        answer = {
            "chat_id": self.chat_id,
            "text": text,
        }
        if reply_to:
            answer['reply_to_message_id'] = reply_to
        if parse:
            answer['parse_mode'] = parse
        msg_url = self.url + 'sendMessage'
        result = requests.post(msg_url, json=answer)
        return result.json()

    def sticker(self, file_id, reply_to=None):
        answer = {
            "chat_id": self.chat_id,
            "sticker": file_id,
        }
        if reply_to:
            answer['reply_to_message_id'] = reply_to
        msg_url = self.url + 'sendSticker'
        result = requests.post(msg_url, json=answer)
        return result.json()

    def photo(self, photo, reply_to=False, upload=False):
        if upload:
            with open(photo, 'rb') as fl:
                sending = {'photo': fl}
                if reply_to:
                    msg_url = self.url + 'sendPhoto?chat_id=' + str(self.chat_id) + '&' + str(reply_to)
                else:
                    msg_url = self.url + 'sendPhoto?chat_id=' + str(self.chat_id)
                result = requests.post(msg_url, files=sending)
            return result.json()
        else:
            answer = {
                "chat_id": self.chat_id,
                "photo": photo,
            }
            if reply_to:
                answer['reply_to_message_id'] = reply_to
            msg_url = self.url + 'sendPhoto'
            result = requests.post(msg_url, json=answer)
            return result.json()

    def video(self, video, reply_to=False, upload=False):
        if upload:
            with open(video, 'rb') as fl:
                sending = {'video': fl}
                if reply_to:
                    msg_url = self.url + 'sendVideo?chat_id=' + str(self.chat_id) + '&' + str(reply_to)
                else:
                    msg_url = self.url + 'sendVideo?chat_id=' + str(self.chat_id)
                result = requests.post(msg_url, files=sending)
            return result.json()
        else:
            answer = {
                "chat_id": self.chat_id,
                "video": video,
            }
            if reply_to:
                answer['reply_to_message_id'] = reply_to
            msg_url = self.url + 'sendVideo'
            result = requests.post(msg_url, json=answer)
            return result.json()

    def gif(self, gif, reply_to=False, upload=False):
        if upload:
            with open(gif, 'rb') as fl:
                sending = {'animation': fl}
                if reply_to:
                    msg_url = self.url + 'sendAnimation?chat_id=' + str(self.chat_id) + '&' + str(reply_to)
                else:
                    msg_url = self.url + 'sendAnimation?chat_id=' + str(self.chat_id)
                result = requests.post(msg_url, files=sending)
            return result.json()
        else:
            answer = {
                "chat_id": self.chat_id,
                "animation": gif,
            }
            if reply_to:
                answer['reply_to_message_id'] = reply_to
            msg_url = self.url + 'sendAnimation'
            result = requests.post(msg_url, json=answer)
            return result.json()

    def file(self, file, reply_to=False, upload=False):
        if upload:
            with open(file, 'rb') as fl:
                sending = {'document': fl}
                if reply_to:
                    msg_url = self.url + 'sendDocument?chat_id=' + str(self.chat_id) + '&' + str(reply_to)
                else:
                    msg_url = self.url + 'sendDocument?chat_id=' + str(self.chat_id)
                result = requests.post(msg_url, files=sending)
            return result.json()
        else:
            answer = {
                "chat_id": self.chat_id,
                "document": file,
            }
            if reply_to:
                answer['reply_to_message_id'] = reply_to
            msg_url = self.url + 'sendDocument'
            result = requests.post(msg_url, json=answer)
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
        edit_text = self.url + 'editMessageText'
        result = requests.post(edit_text, json=answer)
        return result.json()


class Delete:

    def __init__(self, url, chat_id, msg_id):
        self.url = url
        self.chat_id = chat_id
        self.msg_id = msg_id

    def message(self):
        answer = {
            "chat_id": self.chat_id,
            "message_id": self.msg_id,
        }
        del_msg = self.url + 'deleteMessage'
        result = requests.post(del_msg, json=answer)
        return result.json()
