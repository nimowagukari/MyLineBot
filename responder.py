#!/usr/bin/env python

import boto3
import datetime
import random
import sys

from decimal import Decimal
from linebot.models import TextSendMessage


class LineBotTextMassageHandler(object):
    def __init__(self, line_bot_api, line_event):
        self.line_bot_api = line_bot_api
        self.line_event = line_event
        self.type = line_event.type
        self.source_type = line_event.source.type
        _tdelta = datetime.timedelta(hours=9)
        _tz = datetime.timezone(_tdelta, name='JST')
        _ts = int(int(line_event.timestamp) / 1000)
        _utc_dt = datetime.datetime.fromtimestamp(
            _ts, datetime.timezone.utc)
        self.timestamp = _utc_dt.astimezone(_tz).isoformat()

        if self.type in {"follow", "join", "message"}:
            self.reply_token = line_event.reply_token

        if self.type in {"follow", "message"}:
            self.userid = line_event.source.user_id

        if self.type in {"message"}:
            self.text = line_event.message.text

        if self.source_type == "room":
            self.roomid = line_event.source.room_id
            self.id = self.roomid
        elif self.source_type == "group":
            self.groupid = line_event.source.group_id
            self.id = self.groupid
        elif self.source_type == "user":
            self.id = self.userid

    def check_item(self, table_name="talkinfo"):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        result = table.get_item(
            Key={"source_id": self.id, "schema_version": 0})
        if (result.get("Item")) and (result["Item"]["source_type"] == self.source_type):
            return True
        else:
            return False

    def register_item(self, table_name="talkinfo"):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        _ts = int(int(self.line_event.timestamp) / 1000)
        fmt = {
            'source_type': self.source_type,
            'source_id': self.id,
            'last_commented_at': Decimal(_ts),
            'schema_version': Decimal('0'),
            'talk_mode': 'default'}
        print("fmt:\n", fmt)
        result = table.put_item(Item=fmt)
        if result["HTTPStatusCode"] == "200":
            return True
        else:
            return False

    def reply(self):
        if self.text == "/info":
            lines = []
            for k, v in vars(self).items():
                if str(k) not in {"line_bot_api", "line_event"}:
                    lines.append("【{}】:\n{}".format(str(k), str(v)))
            msg = "\n\n".join(lines)
        elif self.text == "さよなら！":
            self._leave()
        elif "しりとり" in self.text:
            msg = "実装予定です"
        else:
            msg = random.choice(["へぇ", "すごいですね", "なるほど", "わかります", "いいですね"])

        self.line_bot_api.reply_message(
            self.reply_token, TextSendMessage(text=msg))

    def _leave(self):
        if self.source_type == 'room':
            self.line_bot_api.leave_room(self.roomid)
            sys.exit()
        elif self.source_type == 'group':
            self.line_bot_api.leave_group(self.groupid)
            sys.exit()
        elif self.source_type == 'user':
            sys.exit()

    def greeting(self, msg):
        self.line_bot_api.reply_message(
            self.reply_token, TextSendMessage(text=msg))
