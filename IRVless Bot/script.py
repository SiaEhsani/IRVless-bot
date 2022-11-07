import configparser
from telethon import TelegramClient, events
import sqlite3
from datetime import datetime

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

API_ID = config.get('default','api_id') 
API_HASH = config.get('default','api_hash')
BOT_TOKEN = config.get('default','bot_token')
session_name = "sessions/Bot"

client = TelegramClient(session_name, API_ID, API_HASH).start(bot_token=BOT_TOKEN)


@client.on(events.NewMessage(pattern="(?i)/start"))
async def start(event):
    sender = await event.get_sender()
    SENDER = sender.id
    text = "Test Test"
    await client.send_message(SENDER, text, parse_mode='html')

def create_message_select_query(ans):
    text = ""
    for i in ans:
        down = i[0]

        text += "<b>"+str(down) + "</b>\n"
    message = "<b>میزان مصرف :\n\n"+text
    return message



@client.on(events.NewMessage(pattern="(?i)/select"))
async def select(event):
    try:
        sender = await event.get_sender()
        SENDER = sender.id

        list_of_words = event.message.text.split(" ")
        username = list_of_words[1] 
        print (username)

        sql_command = "SELECT down FROM inbounds WHERE remark =?" 
        crsr.execute(sql_command,[username])
        res = crsr.fetchall() 

        if(res):
            testo_messaggio = create_message_select_query(res) 
            await client.send_message(SENDER, testo_messaggio, parse_mode='html')
        else:
            text = "کابر یافت نشد"
            await client.send_message(SENDER, text, parse_mode='html')

    except Exception as e: 
        print(e)
        await client.send_message(SENDER, "<b>پایان سشن✔️</b>", parse_mode='html')
        return


##### MAIN
if __name__ == '__main__':
    try:
        db_name = 'Database/x-ui.db' 
        conn = sqlite3.connect(db_name, check_same_thread=False)
        crsr = conn.cursor() 
        print("Connected")
        client.run_until_disconnected()

    except Exception as error:
        print('Cause: {}'.format(error))