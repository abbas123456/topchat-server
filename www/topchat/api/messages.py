import json
import re

class Message(object):
    
    TYPE_BOT_MESSAGE = 1
    TYPE_USER_MESSAGE = 2
    TYPE_USER_JOINED_MESSAGE = 3
    TYPE_USER_LEFT_MESSAGE = 4
    TYPE_PRIVATE_BOT_MESSAGE = 5
    TYPE_PRIVATE_CONVERSATION_SEND_USER_MESSAGE = 6
    TYPE_PRIVATE_CONVERSATION_RECEIVE_USER_MESSAGE = 7
    TYPE_USER_BLOCKED_MESSAGE = 8
    TYPE_USER_UNBLOCKED_MESSAGE = 9
        
    def __init__(self, type, message):
        self.type = type
        self.message = message

class BotMessage(Message):
    def __init__(self, message_text):
        self.username = 'MoBot'
        super(BotMessage, self).__init__(Message.TYPE_BOT_MESSAGE, message_text)
        
class UserMessage(Message):
    def __init__(self, username, colour_rgb, message_text):
        self.username = username
        self.colour_rgb = colour_rgb
        super(UserMessage, self).__init__(Message.TYPE_USER_MESSAGE, self.remove_html_tags(message_text))
    
    def remove_html_tags(self, string):
        regex = re.compile(r'<.*?>')
        return regex.sub('', string)
    
class UserJoinedMessage(Message):
    def __init__(self, user, recipent_user):
        self.username = user.username
        self.colour_rgb = user.colour_rgb
        self.is_administrator = user.is_administrator
        self.is_recipient_administator = recipent_user.is_administrator 
        super(UserJoinedMessage, self).__init__(Message.TYPE_USER_JOINED_MESSAGE, '')

class UserLeftMessage(Message):
    def __init__(self, username):
        self.username = username
        super(UserLeftMessage, self).__init__(Message.TYPE_USER_LEFT_MESSAGE, '')

class PrivateBotMessage(Message):
    def __init__(self, message_text, recipient_username):
        self.username = 'MoBot'
        self.recipient_username = recipient_username
        super(PrivateBotMessage, self).__init__(Message.TYPE_PRIVATE_BOT_MESSAGE, message_text)

class PrivateConversationSendUserMessage(Message):
    def __init__(self, username, colour_rgb, message_text, recipient_username):
        self.username = username
        self.colour_rgb = colour_rgb
        self.recipient_username = recipient_username
        super(PrivateConversationSendUserMessage, self).__init__(
                         Message.TYPE_PRIVATE_CONVERSATION_SEND_USER_MESSAGE, message_text)

class PrivateConversationReceiveUserMessage(Message):
    def __init__(self, username, colour_rgb, message_text):
        self.username = username
        self.colour_rgb = colour_rgb
        super(PrivateConversationReceiveUserMessage, self).__init__(
                        Message.TYPE_PRIVATE_CONVERSATION_RECEIVE_USER_MESSAGE, message_text)

class UserBlockedMessage(Message):
    def __init__(self, username):
        self.username = username
        super(UserBlockedMessage, self).__init__(
                         Message.TYPE_USER_BLOCKED_MESSAGE, '')


class UserUnblockedMessage(Message):
    def __init__(self, username):
        self.username = username
        super(UserUnblockedMessage, self).__init__(
                         Message.TYPE_USER_UNBLOCKED_MESSAGE, '')


class MessageEncoder(json.JSONEncoder):
    
    def default(self, object):
        if not isinstance(object, Message):
            return super(MessageEncoder, self).default(object)

        return object.__dict__
