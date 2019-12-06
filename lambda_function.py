from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import LineBotApiError,InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage,StickerMessage,StickerSendMessage
import json
import logging
import os
import pprint
import sys

from message_controller import LineBotTextMassageHandler

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
        message_handler = LineBotTextMassageHandler(line_event)
        reply = message_handler.reply()
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

