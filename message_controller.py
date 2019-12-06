import random

class LineBotTextMassageHandler(object):
    def __init__(self,line_event):
        self.line_event = line_event
        self.text = line_event.message.text

    def parser(self):
        pass
    
    def reply(self):
        if self.text == "さよなら！":
            msg = "ひどい"
        elif "しりとり" in self.text:
            msg = "実装予定です"
        else:
            msg = random.choice(["へぇ","すごいですね","なるほど","わかります","いいですね"])
        return msg