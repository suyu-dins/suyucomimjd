import logging
import re
import datetime
import time
from telegram.ext import Updater, CommandHandler

# 设置日志等级
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# 填写您的Telegram Bot Token
TOKEN = '6250704511:AAGsffiXivAtCnGBqmDbIwb4ESsOwoS0diM'

# 创建一个Updater对象
updater = Updater(TOKEN, use_context=True)

# 创建一个CommandHandler处理器，处理/start命令
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="您好！请发送频道链接来获取频道ID。")

# 创建一个CommandHandler处理器，处理/channel命令
def channel(update, context):
    # 获取用户发送的频道链接
    channel_link = update.message.text
    # 使用正则表达式从链接中提取ID
    channel_id = re.search(r't.me/(.+)', channel_link).group(1)
    # 发送频道ID给用户
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"频道ID为：{channel_id}")

# 创建一个CommandHandler处理器，处理/stop命令
def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="再见！")
    updater.stop()

# 创建一个Dispatcher对象，并添加CommandHandler处理器
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('channel', channel))
dispatcher.add_handler(CommandHandler('stop', stop))

# 启动机器人
updater.start_polling()

# 添加异常处理
def error(update, context):
    logging.error(f"Update {update} caused error {context.error}")

# 添加错误处理器
dispatcher.add_error_handler(error)

# 添加定时器，每天晚上10点自动停止机器人
def job():
    now = datetime.datetime.now()
    if now.hour == 22:
        stop(None, None)

while True:
    job()
    time.sleep(60)