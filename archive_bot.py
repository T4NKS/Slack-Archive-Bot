import os
import time
import re
from slackclient import SlackClient


# slack_token = os.environ[slack_bot_tocken]
slack_token = ''
sc = SlackClient(slack_token)

# workspace information
slack_info = {
    'user_id': {},
    'channel_id': {},
    'channel_info': {}
}


# update user list
def update_users():
    pass


# update channel list
def update_channels():
    pass


