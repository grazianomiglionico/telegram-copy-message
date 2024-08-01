import configparser
import sys

from telethon import TelegramClient, events

config = configparser.ConfigParser()
config.read("config.ini", encoding='utf-8')

source_channel = config['Telegram']['source_channel']
destination_channel = config['Telegram']['destination_channel']

client = TelegramClient(
    session=config['Telegram']['username'],
    api_id=int(config['Telegram']['api_id']),
    api_hash=str(config['Telegram']['api_hash'])
)


# we fetch the chats until we find the channels we want to listen to/forward to
def fetch_chats():
    source_found = destination_found = False
    print('fetching chats looking for', source_channel, 'and', destination_channel)
    for dialog in client.iter_dialogs():
        # print(f'{dialog.id}:{dialog.title}')
        if dialog.title == source_channel:
            source_found = True
            # print('source channel found')
        elif dialog.title == destination_channel:
            destination_found = True
            # print('destination channel found')
        if source_found and destination_found:
            print('Channels/Chats found! Starting listening')
            return
    print('channel/chat not found, forcing exit')
    sys.exit("STOPPING APPLICATION! Cannot find channels/chats")


@client.on(events.NewMessage(chats=source_channel))
async def on_new_message_received(event):
    message = event.message.message
    print('\nReceived new message')
    await send_message(message)

    if event.message.is_reply:
        print('this is a reply to message')
        print((await event.message.get_reply_message()).message)


async def send_message(message):
    print('sending message')
    await client.send_message(destination_channel, message)


print('\nInitializing connection to Telegram')
client.start(lambda: config['Telegram']['phone'])
print('Connection to Telegram initialized')
fetch_chats()
client.run_until_disconnected()