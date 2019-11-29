from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import LineBotApiError,InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage,StickerMessage,StickerSendMessage
import json
import logging
import os
import pprint
import random
import sys

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

channel_secret = os.getenv("LINE_CHANNEL_SECRET")
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if channel_secret is None:
    logger.error("Please define LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
    pass
if channel_access_token is None:
    logger.error("Please define LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)
    pass

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

print('Loading function')

def lambda_handler(event, context):
    signature = event["headers"]["X-Line-Signature"]
    body = event["body"]
    ok_json = {"isBase64Encoded": False,
               "statusCode": 200,
               "headers": {},
               "body": ""}
    error_json = {"isBase64Encoded": False,
                  "statusCode": 403,
                  "headers": {},
                  "body": "Error"}

    @handler.add(MessageEvent, message=TextMessage)
    def reply_from_textmessage(line_event):
        text = line_event.message.text
        if text == "さよなら！":
            line_bot_api.reply_message(line_event.reply_token, StickerSendMessage(package_id='1',sticker_id='3'))
            source_type = line_event.source.type
            if source_type == "group":
                gid = line_event.source.group_id
                line_bot_api.leave_group(gid)
            elif source_type == "room":
                rid = line_event.source.room_id
                line_bot_api.leave_room(rid)
            else:
                uid = line_event.source.user_id
                reply = "個人トークからは抜けられません"
                line_bot_api.push_message(uid, TextSendMessage(text=reply))
        elif "しりとり" in text:
            reply = "実装予定です"
            line_bot_api.reply_message(line_event.reply_token, TextSendMessage(text=reply))
        else:
            reply = random.choice(["へぇ","すごいですね","なるほど","わかります","いいですね"])
            line_bot_api.reply_message(line_event.reply_token, TextSendMessage(text=reply))

    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        logger.error("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            logger.error("  %s: %s" % (m.property, m.message))
        return error_json
    except InvalidSignatureError:
        return error_json

    return ok_json

