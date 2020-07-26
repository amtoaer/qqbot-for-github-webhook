from mirai import Mirai, Plain, MessageChain, Friend
import asyncio
import threading
import webhook_listener
import json
# 你的bot的qq号
qq = 123456789
# 你的auth_key
authKey = 'INITKEY6QQze5JY'
# mirai api地址
mirai_api_http_locate = 'localhost:5742/'

app = Mirai(f"mirai://{mirai_api_http_locate}?authKey={authKey}&qq={qq}")

'''
推送或者强制推送的信息，如：

[tsp:master] 1 new commit by amtoaer:
   d38b512:[修复填写表格时出现的错误]

'''
pushInfo = '[{}:{}] {} new commit by {} {}:'
commitMessage = '\n   {}:[{}]'

'''
创建或者删除分支的信息，如：

[tsp:ant] amtoaer delete this branch

'''
branchInfo = '[{}:{}] {} {} this branch'


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
    printContent = 'init content'
    # 如果是创建/删除分支
    if content['created'] or content['deleted']:
        action = 'create'
        if content['deleted']:
            action = 'delete'
        printContent = branchInfo.format(content['repository']['name'],
                                         content['ref'].split('/')[-1],
                                         content['pusher']['name'],
                                         action)
    else:
        isForced = ''
        # 如果是强制推送
        if content['forced']:
            isForced = 'via force push'
        printContent = pushInfo.format(content['repository']['name'],
                                       content['ref'].split('/')[-1],
                                       len(content['commits']),
                                       content['pusher']['name'],
                                       isForced)
        for item in content['commits']:
            # 取commit哈希前七位
            printContent += commitMessage.format(
                item['id'][0:7], item['message'])
    # 私聊通知给某位好友
    asyncio.run_coroutine_threadsafe(app.sendFriendMessage(
        # 好友的QQ号
        123456789,
        [Plain(text=printContent)]
    ), loop)
    '''
    如果你需要给群组发送通知，那么应修改为
    asyncio.run_coroutine_threadsafe(app.sendGroupMessage(
        # QQ群号
        123456789,
        [Plain(text=printContent)]
    ), loop)
    '''


def main():
    webhooks = webhook_listener.Listener(
        # webhook的监听端口
        handlers={"POST": handleWebhook}, port=12345)
    webhooks.start()


if __name__ == '__main__':
    main()
    thread.run()
