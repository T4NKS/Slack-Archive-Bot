import os
import re
import sqlite3
import datetime
from slackclient import SlackClient


# creating the database
conn = sqlite3.connect('tedxuw.sqlite')
cur = conn.cursor()
cur.execute('create table if not exists tedxuw (user VARCHAR, name VARCHAR, message VARCHAR, channel VARCHAR)')
conn.commit()

# slack_token = os.environ[slack_token]
# slack_token_bot = os.environ[slack_token_bot]
slack_token = 'xoxp-533073680406-531491385364-576999913393-eaac0abfe3492d52d6e58834f4a58bf1'
slack_bot_token = 'xoxb-533073680406-577003789457-2DN1q56uEbzbgj1lq1cKJNYX'
sc = SlackClient(slack_token)
scb = SlackClient(slack_bot_token)

# workspace information
slack_info = {
    'user_id': {},
    'channel_id': {},
    'channel_topic': {}
}


# get user list
def get_users():
    users = sc.api_call('users.list')
    slack_info['user_id'] = dict([(i['id'], i['name']) for i in users['members']])


# get channel list
def get_channels():
    channels = sc.api_call('channels.list')['channels']
    slack_info['channel_id'] = dict([(i['id'], i['name']) for i in channels])
    slack_info['channel_topic'] = dict([(i['id'], i['topic']) for i in channels])


#
def messages(event):
    if 'text' in event:
        return
    elif 'subtype' in event and event['subtype'] == 'bot_message':
        return


# changing time format
def timestamp(ts):
    return datetime.datetime.fromtimestamp(int(ts.split('.')[0])).strftime('%Y-%m-%d %H:%M:%S')


# loop
if scb.rtm_connect(auto_reconnect=True):
    get_users()
    get_channels()
    while sc.server.connected:
        try:
            for event in scb.rtm_read():
                if event['type'] == 'message':
                    messages(event)
                    if 'subtype' in event and event['subtype'] in ['group_leave']:
                        get_channels()
                elif event['type'] in ['group_joined', 'member_joined_channel', 'channel_created', 'group_left']:
                    get_channels()
        except WebSocketConnectionClosedException:
            sc.rtm_connect()
else:
    print('Not connecting - perhaps invalid token?')


cur.execute('insert into tedxuw (user, name, message, channel) values ("hi", "my", "name", "is")')
conn.commit()
conn.close()
