from mirai import Mirai, Plain, MessageChain, Friend
import asyncio
import threading
import webhook_listener
import json
# your QQ robot
qq = 123456789
# your auth_key
authKey = 'INITKEY6QQze5JY'
# mirai api http locate
mirai_api_http_locate = 'localhost:5742/'

app = Mirai(f"mirai://{mirai_api_http_locate}?authKey={authKey}&qq={qq}")

text = '[{}:{}] {} new commit by {}:'
commitMessage = '\n   {}:[{}]'


class MiraiThread(threading.Thread):
    def __init__(self, loop):
        super(MiraiThread, self).__init__()
        self.loop = loop
        self.setDaemon(True)

    def run(self):
        app.run(loop=self.loop)


loop = asyncio.get_event_loop()
thread = MiraiThread(loop)


def handleWebhook(request, *args, **kwargs):
    tmpContent = request.body.read(int(request.headers['Content-Length'])) if int(
        request.headers.get('Content-Length', 0)) > 0 else ''
    content = json.loads(tmpContent.decode('utf-8'))
    printContent = text.format(content['repository']['name'],
                               content['ref'].split('/')[-1],
                               len(content['commits']),
                               content['pusher']['name'])
    for item in content['commits']:
        printContent += commitMessage.format(item['id'][0:7], item['message'])
    asyncio.run_coroutine_threadsafe(app.sendFriendMessage(
        # receiver's QQ
        123456789,
        [Plain(text=printContent)]
    ), loop)


def main():
    webhooks = webhook_listener.Listener(
        # webhook's listen port
        handlers={"POST": handleWebhook}, port=12345)
    webhooks.start()


if __name__ == '__main__':
    main()
    thread.run()
