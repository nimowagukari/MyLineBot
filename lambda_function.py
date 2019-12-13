#!/usr/bin/env python

import logging
import os
import sys

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (FollowEvent, JoinEvent, MessageEvent, TextMessage)

from responder import LineBotTextMassageHandler

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

channel_secret = os.getenv("LINE_CHANNEL_SECRET")
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if channel_secret is None:
    logger.error("Please define LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    logger.error(
        "Please define LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

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
        message_handler = LineBotTextMassageHandler(line_bot_api, line_event)
        message_handler.reply()

    @handler.add(JoinEvent)
    def reply_join(line_event):
        message_handler = LineBotTextMassageHandler(line_bot_api, line_event)
        if message_handler.check_item():
            msg = "ただいま～"
            message_handler.greeting(msg)
        else:
            msg = "よろしく～"
            message_handler.greeting(msg)
            message_handler.register_item()

    @handler.add(FollowEvent)
    def reply_follow(line_event):
        message_handler = LineBotTextMassageHandler(line_bot_api, line_event)
        if message_handler.check_item():
            msg = "ただいま～"
            message_handler.greeting(msg)
        else:
            msg = "よろしく～"
            message_handler.greeting(msg)
            message_handler.register_item()

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
