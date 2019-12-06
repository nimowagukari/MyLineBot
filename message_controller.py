import datetime
import random
import time

class LineBotTextMassageHandler(object):
    def __init__(self,line_event):
        self.line_event = line_event
        self.text = line_event.message.text
        self.timestamp = str(datetime.datetime.fromtimestamp(time.time()))
        self.source_type = line_event.source.type
        self.userid = line_event.source.user_id

    def parser(self):
        pass
    
    def reply(self):
        if self.text == "/info":
            msg = """\
Event Info:

text: {}
timestamp: {}
sourcetype: {}
userid: {}\
""".format(self.text, self.timestamp, self.source_type, self.userid)
        elif self.text == "さよなら！":
            msg = "ひどい"
        elif "しりとり" in self.text:
            msg = "実装予定です"
        else:
            msg = random.choice(["へぇ","すごいですね","なるほど","わかります","いいですね"])
        return msg