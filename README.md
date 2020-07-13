# qqbot-for-github-webhook
## 介绍

这是一个用于接受`github webhooks`的QQ机器人。基于`Mirai`项目和`Python Mirai `SDK。

## 截图

![photo_2020-07-12_10-08-27](https://allwens-work.oss-cn-beijing.aliyuncs.com/bed/photo_2020-07-12_10-08-27.jpg)

## 使用

> 推荐在服务器上使用。

1. 根据自己平台选择下载[MiraiOK](https://github.com/LXY1226/MiraiOK)并运行。

2. 结束运行，将[Mirai-api-http](https://github.com/project-mirai/mirai-api-http/releases)的`.jar`文件移动到`MiraiOK`根路径下的`plugins`文件夹。

3. 重新运行，进行账号登录：

   ```
   login 账号 密码
   ```

4. 安装机器人所需的依赖：

   ```bash
   pip install kuriyama webhook_listener
   ```

5. 参考注释修改机器人账号，`auth key`，`Mirai-api-http`运行地址。

6. 运行机器人。

7. 为你的项目设置`webhooks`

   ![image-20200712102440422](https://allwens-work.oss-cn-beijing.aliyuncs.com/bed/image-20200712102440422.png)

## 参考

+ [python Mirai文档](https://mirai-py.originpages.com/)
+ [对python Mirai的同步调用](https://github.com/NatriumLab/python-mirai/issues/87)