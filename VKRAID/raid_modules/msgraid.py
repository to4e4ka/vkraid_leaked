import time
import vk_api
import random
import requests
import traceback
from raid_utils import jsonreader
from threading import Thread
from python3_anticaptcha import ImageToTextTask
from vk_api.longpoll import VkLongPoll, VkEventType, VkChatEventType


class MsgRaid(Thread):
    def __init__(self, token, captcha_key, chat, call):
        Thread.__init__(self)
        self.token = token
        self.captcha_key = captcha_key
        self.chat = chat
        self.call = call

    def run(self):
        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.captcha_key, save_format='const') \
                .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])
        vk_session = vk_api.VkApi(token=self.token, captcha_handler=captcha_handler)
        vk = vk_session.get_api()
        vk.messages.send(
            chat_id=self.chat,
            random_id=random.randint(1, 999999),
            message=self.call
        )


class AddFriend(Thread):
    def __init__(self, token, captcha_key, ids):
        Thread.__init__(self)
        self.token = token
        self.captcha_key = captcha_key
        self.ids = ids

    def run(self):
        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.captcha_key, save_format='const') \
                .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])
        vk_session = vk_api.VkApi(token=self.token, captcha_handler=captcha_handler)
        vk = vk_session.get_api()
        params = {
            'v': '5.92',
            'access_token': self.token
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Connection': 'keep-alive'
        }
        url = 'https://api.vk.com/method/users.get'
        a = requests.get(url=url, params=params, headers=headers).json()
        name = a['response'][0]['first_name']
        surname = a['response'][0]['last_name']
        print(f'{name} {surname} ?????????????????? ?? ????????????')
        for user_id in self.ids:
            try:
                vk.friends.add(user_id=user_id)
            except KeyError:
                print('???????????? ?????? ???????????????? ????????????')
            except:
                print('???????????????? ???????????? ?? ????????????')
        else:
            print(f'{name} {surname} ?????????????? ?? ????????????!')


class AntiKick(Thread):
    def __init__(self, token):
        Thread.__init__(self)
        self.token = token

    def run(self):
        vk_session = vk_api.VkApi(token=self.token)
        vk = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        while True:
            try:
                for event in longpoll.listen():
                    if event.type_id == VkChatEventType.USER_KICKED:
                        vk.messages.addChatUser(
                            chat_id=event.chat_id,
                            user_id=event.info['user_id']
                        )
            except:
                pass


class SpamLs(Thread):
    def __init__(self, token, user_id, media, ms, captcha_key, n, delmsg, theme):
        Thread.__init__(self)
        self.token = token
        self.user_id = user_id
        self.media = media
        self.ms = ms
        self.captcha_key = captcha_key
        self.n = n
        self.delmsg = delmsg
        self.theme = theme

    def run(self):
        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.captcha_key, save_format='const') \
                .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])
        k = 1
        vk = vk_api.VkApi(token=self.token, captcha_handler=captcha_handler).get_api()
        while True:
            try:
                if self.ms == 1:
                    a = open('args.txt', encoding='utf8')
                    msg = a.read().split('\n')
                    a.close()
                    if self.delmsg == 1:
                        vk.messages.send(
                            user_id=self.user_id,
                            message=random.choice(msg),
                            attachment=self.media,
                            random_id=random.randint(1, 999999)
                        )
                    if self.delmsg == 2:
                        vk.messages.send(
                            user_id=self.user_id,
                            message=random.choice(msg),
                            attachment=self.media,
                            random_id=random.randint(1, 999999),
                            expire_ttl=60
                        )
                elif self.ms == 2:
                    msg = jsonreader.get_json_param('msg').split('\n')[0]
                    if self.delmsg == 1:
                        vk.messages.send(
                            user_id=self.user_id,
                            message=msg,
                            attachment=self.media,
                            random_id=random.randint(1, 999999)
                        )
                    if self.delmsg == 2:
                        vk.messages.send(
                            user_id=self.user_id,
                            message=msg,
                            attachment=self.media,
                            random_id=random.randint(1, 999999),
                            expire_ttl=60
                        )
                if self.theme == 2:
                    themes = ["emerald", "midnight", "new_year", "frost", "halloween_violet", "halloween_orange", "unicorn", "twilight", "sunset", "retrowave", "marine", "lagoon", "disco", "crimson", "candy"]
                    vk.messages.setConversationStyle(
                        style=random.choice(themes),
                        peer_id=self.user_id
                    )
                print(f'[LS RAID] {k} ???????????????????? ?? {self.n} ????????????????!')
                k += 1
            except KeyError:
                print('???????????? ?????? ???????????????? ????????????')
                break
            except:
                print('???????????? ?????? ???????????????? ??????????????????.')
                break
            time.sleep(random.randint(1, 3))


class StickerSpamLs(Thread):
    def __init__(self, token, user_id, captcha_key, n, delmsg, theme):
        Thread.__init__(self)
        self.token = token
        self.user_id = user_id
        self.captcha_key = captcha_key
        self.n = n
        self.delmsg = delmsg
        self.theme = theme

    def run(self):
        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.captcha_key, save_format='const') \
                .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])
        k = 1
        vk = vk_api.VkApi(token=self.token, captcha_handler=captcha_handler).get_api()
        while True:
            try:
                if self.delmsg == 1:
                    vk.messages.send(
                        user_id=self.user_id,
                        random_id=random.randint(1, 999999),
                        sticker_id=random.randint(9008, 9047)
                    )
                if self.delmsg == 2:
                    vk.messages.send(
                        user_id=self.user_id,
                        random_id=random.randint(1, 999999),
                        sticker_id=random.randint(9008, 9047),
                        expire_ttl=60
                    )
                if self.theme == 2:
                    themes = ["emerald", "midnight", "new_year", "frost", "halloween_violet", "halloween_orange", "unicorn", "twilight", "sunset", "retrowave", "marine", "lagoon", "disco", "crimson", "candy"]
                    vk.messages.setConversationStyle(
                        style=random.choice(themes),
                        peer_id=self.user_id
                    )
                print(f'[LS RAID] {k} ???????????????????? ?? {self.n} ????????????????!')
                k += 1
            except KeyError:
                print('???????????? ?????? ???????????????? ????????????')
            except:
                print('???????????? ?????? ???????????????? ??????????????????. ?? ???????????? ??????????????')
                break
            time.sleep(random.randint(1, 3))


class SpamChat(Thread):
    def __init__(self, token, ms, captcha_key, n, call, title, edit, attach, edit_cf, delmsg, theme):
        Thread.__init__(self)
        self.token = token
        self.ms = ms
        self.captcha_key = captcha_key
        self.n = n
        self.call = call
        self.title = title
        self.edit = edit
        self.attach = attach
        self.edit_cf = edit_cf
        self.delmsg = delmsg
        self.theme = theme

    def run(self):
        AntiKick(self.token).start()

        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.captcha_key, save_format='const') \
                .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])
        vk_session = vk_api.VkApi(token=self.token, captcha_handler=captcha_handler)
        vk = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.text == self.call:
                k = 1
                while True:
                    try:
                        if self.edit == 1:
                            if self.ms == 1:
                                a = open('args.txt', encoding='utf8')
                                msg = a.read().split('\n')
                                a.close()
                                if self.delmsg == 1:
                                    msg_id = vk.messages.send(
                                        random_id=random.randint(1, 999999),
                                        chat_id=event.chat_id,
                                        message="????????????"
                                    )
                                if self.delmsg == 2:
                                    msg_id = vk.messages.send(
                                        random_id=random.randint(1, 999999),
                                        chat_id=event.chat_id,
                                        message="????????????",
                                        expire_ttl=60
                                    )
                                vk.messages.edit(
                                    peer_id=event.peer_id,
                                    message=random.choice(msg),
                                    message_id=msg_id,
                                    attachment=self.attach
                                )
                            elif self.ms == 2:
                                msg = jsonreader.get_json_param('msg').split('\n')[0]
                                if self.delmsg == 1:
                                    msg_id = vk.messages.send(
                                        random_id=random.randint(1, 999999),
                                        chat_id=event.chat_id,
                                        message="????????????"
                                    )
                                if self.delmsg == 2:
                                    msg_id = vk.messages.send(
                                        random_id=random.randint(1, 999999),
                                        chat_id=event.chat_id,
                                        message="????????????",
                                        expire_ttl=60
                                    )
                                vk.messages.edit(
                                    peer_id=event.peer_id,
                                    message=msg,
                                    message_id=msg_id,
                                    attachment=self.attach
                                )
                        if self.edit == 2:
                            if self.ms == 1:
                                a = open('args.txt', encoding='utf8')
                                msg = a.read().split('\n')
                                a.close()
                                if self.delmsg == 1:
                                    vk.messages.send(
                                        random_id=random.randint(1, 999999),
                                        chat_id=event.chat_id,
                                        message=random.choice(msg),
                                        attachment=self.attach
                                    )
                                if self.delmsg == 2:
                                    vk.messages.send(
                                        random_id=random.randint(1, 999999),
                                        chat_id=event.chat_id,
                                        message=random.choice(msg),
                                        attachment=self.attach,
                                        expire_ttl=60
                                    )
                            if self.ms == 2:
                                msg = jsonreader.get_json_param('msg').split('\n')[0]
                                if self.delmsg == 1:
                                    vk.messages.send(
                                        random_id=random.randint(1, 999999),
                                        chat_id=event.chat_id,
                                        message=msg,
                                        attachment=self.attach
                                    )
                                if self.delmsg == 2:
                                    vk.messages.send(
                                        random_id=random.randint(1, 999999),
                                        chat_id=event.chat_id,
                                        message=msg,
                                        attachment=self.attach,
                                        expire_ttl=60
                                    )
                        if self.edit_cf == 1:
                            titled = vk.messages.getChat(chat_id=event.chat_id)['title']
                            if titled != self.title:
                                vk.messages.editChat(chat_id=event.chat_id, title=self.title)
                                vk.messages.deleteChatPhoto(chat_id=event.chat_id)
                                vk.messages.unpin(peer_id=event.peer_id)
                        if self.theme == 2:
                            themes = ["emerald", "midnight", "new_year", "frost", "halloween_violet", "halloween_orange", "unicorn", "twilight", "sunset", "retrowave", "marine", "lagoon", "disco", "crimson", "candy"]
                            vk.messages.setConversationStyle(
                                style=random.choice(themes),
                                peer_id=event.peer_id
                            )

                        print(f'[CHAT] {k} ???????????????????? ?? {self.n} ????????????????!')
                        k += 1
                    except KeyError:
                        print('???????????? ?????? ???????????????? ????????????')
                    except:
                        print(traceback.format_exc())
                        print('???????????? ?????? ???????????????? ??????????????????')
                        break
                    time.sleep(random.randint(1, 3))


class StickerSpamChat(Thread):
    def __init__(self, token, captcha_key, n, call, title, edit_cf, delmsg):
        Thread.__init__(self)
        self.token = token
        self.captcha_key = captcha_key
        self.n = n
        self.call = call
        self.title = title
        self.edit_cf = edit_cf
        self.delmsg = delmsg

    def run(self):
        AntiKick(self.token).start()

        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.captcha_key, save_format='const') \
                .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])
        vk_session = vk_api.VkApi(token=self.token, captcha_handler=captcha_handler)
        vk = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.text == self.call:
                k = 1
                while True:
                    try:
                        if self.delmsg == 1:
                            vk.messages.send(
                                random_id=random.randint(1, 999999),
                                chat_id=event.chat_id,
                                sticker_id=random.randint(9008, 9047)
                            )
                        if self.delmsg == 2:
                            vk.messages.send(
                                random_id=random.randint(1, 999999),
                                chat_id=event.chat_id,
                                sticker_id=random.randint(9008, 9047),
                                expire_ttl=60
                            )
                        if self.edit_cf == 1:
                            titled = vk.messages.getChat(chat_id=event.chat_id)['title']
                            if titled != self.title:
                                vk.messages.editChat(chat_id=event.chat_id, title=self.title)
                                vk.messages.deleteChatPhoto(chat_id=event.chat_id)
                                vk.messages.unpin(peer_id=event.peer_id)
                        if self.theme == 2:
                            themes = ["emerald", "midnight", "new_year", "frost", "halloween_violet", "halloween_orange", "unicorn", "twilight", "sunset", "retrowave", "marine", "lagoon", "disco", "crimson", "candy"]
                            vk.messages.setConversationStyle(
                                style=random.choice(themes),
                                peer_id=event.peer_id
                            )
                        print(f'[CHAT] {k} ???????????????????? ?? {self.n} ????????????????!')
                        k += 1
                    except KeyError:
                        print('???????????? ?????? ???????????????? ????????????')
                    except:
                        print('???????????? ?????? ???????????????? ??????????????????')
                        break
                    time.sleep(random.randint(1, 3))


class ConfJoin(Thread):
    def __init__(self, tokens, link):
        Thread.__init__(self)
        self.tokens = tokens
        self.link = link

    def run(self):
        print('?????????? ?? ??????????...')
        for token in self.tokens:
            params = {
                'access_token': token,
                'v': '5.92',
                'link': self.link
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
                'Connection': 'keep-alive'
            }
            url = 'https://api.vk.com/method/messages.joinChatByInviteLink'
            requests.get(url=url, params=params, headers=headers)
        else:
            print('?????? ??????????!')


class AddConf:
    def __init__(self, token, ids, call):
        self.token = token
        self.ids = ids
        self.call = call

    def go(self):
        h = int(input('???????????? ???? ???????????? ???????? ?????????????\n1.????\n2.??????\n'))
        print(
            '?????????????? ?????? - ?????? ??????????????, ?? ???????????????? ?????? ???????? ???????????????????? ???????? ?? ??????????\n'
            '???????????????????? ?????? ?????????? ?? ???????????? ?? ???????????? ????????????')
        vk = vk_api.VkApi(token=self.token).get_api()
        if h == 1:
            chat = input('?????????????? ???????? ????????????: ')
            print('????????????')
            for user in self.ids:
                try:
                    vk.messages.addChatUser(chat_id=chat, user_id=user)
                except:
                    pass
            else:
                print('?????? ????????????????????!')
        if h == 2:
            print('?????????????????? ???????????? ???????? ?? ???????????????? ????????????????')
            vk_session = vk_api.VkApi(token=self.token)
            vk = vk_session.get_api()
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.text == self.call:
                    print('???????? ???????????? - ', event.chat_id)
                    for user in self.ids:
                        try:
                            vk.messages.addChatUser(chat_id=event.chat_id, user_id=user)
                        except:
                            pass
                        time.sleep(random.randint(1, 5))
                    else:
                        print('?????? ????????????????????!')


class ScreenshotSpamChat(Thread):
    def __init__(self, token, captcha_key, n, call, title, edit_cf):
        Thread.__init__(self)
        self.token = token
        self.captcha_key = captcha_key
        self.n = n
        self.call = call
        self.title = title
        self.edit_cf = edit_cf

    def run(self):
        AntiKick(self.token).start()

        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(
                anticaptcha_key=self.captcha_key, save_format='const') \
                .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])
        vk_session = vk_api.VkApi(token=self.token, captcha_handler=captcha_handler)
        vk = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.text == self.call:
                k = 1
                while True:
                    try:
                        vk.messages.sendService(
                            action_type="chat_screenshot",
                            peer_id=event.peer_id
                        )
                        if self.edit_cf == 1:
                            titled = vk.messages.getChat(chat_id=event.chat_id)['title']
                            if titled != self.title:
                                vk.messages.editChat(chat_id=event.chat_id, title=self.title)
                                vk.messages.deleteChatPhoto(chat_id=event.chat_id)
                                vk.messages.unpin(peer_id=event.peer_id)
                        print(f'[CHAT] {k} ???????????????????? ?? {self.n} ????????????????!')
                        k += 1
                    except KeyError:
                        print('???????????? ?????? ???????????????? ????????????')
                    except:
                        print('???????????? ?????? ???????????????? ??????????????????')
                        break


class ThemeSpamChat(Thread):
    def __init__(self, token, n, call, title, edit_cf):
        Thread.__init__(self)
        self.token = token
        self.n = n
        self.call = call
        self.title = title
        self.edit_cf = edit_cf

    def run(self):
        themes = ["emerald", "midnight", "new_year", "frost", "halloween_violet", "halloween_orange", "unicorn", "twilight", "sunset", "retrowave", "marine", "lagoon", "disco", "crimson", "candy"]
        AntiKick(self.token).start()
        vk_session = vk_api.VkApi(token=self.token)
        vk = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.text == self.call:
                k = 1
                while True:
                    try:
                        vk.messages.setConversationStyle(
                            style=random.choice(themes),
                            peer_id=event.peer_id
                        )
                        if self.edit_cf == 1:
                            titled = vk.messages.getChat(chat_id=event.chat_id)['title']
                            if titled != self.title:
                                vk.messages.editChat(chat_id=event.chat_id, title=self.title)
                                vk.messages.deleteChatPhoto(chat_id=event.chat_id)
                                vk.messages.unpin(peer_id=event.peer_id)
                        print(f'[CHAT] {k} ???????????????????? ?? {self.n} ????????????????!')
                        k += 1
                    except KeyError:
                        print('???????????? ?????? ???????????????? ????????????')
                    except Exception as e:
                        print('???????????? ?????? ???????????????? ??????????????????')
                        print(e)
                        break
                    time.sleep(random.randint(3, 5))
