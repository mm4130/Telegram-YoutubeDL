import sys
import os
import time
import telepot
import requests
import pafy

TOKEN = "364811061:AAF4FpLb9bIYm6kEtUJL_isAYa1n5zkNIAg"

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    flavor = telepot.flavor(msg)
    summary = telepot.glance(msg, flavor=flavor)
    print (flavor, summary)
    
    order = msg['text'].split(' ')
    title = ''
    url = ''
    flag_URL = 0
    flag_VIDEO = 0

    for text in order:
    	if text.startswith('https://') or text.startswith('www.') or text.startswith('youtu'):
    		url = text
    		flag_URL = 1
    	elif text.lower().startswith('video'):
    		flag_VIDEO = 1

    if flag_URL == 0:
    	bot.sendMessage(chat_id, 'Please enter a video link to download.')

    else:
        video = pafy.new(url)
        best = video.getbest()
        message = video.title + '\t(' + video.duration + ')'
        bot.sendMessage(chat_id, message)
        if flag_VIDEO == 1:
            r = requests.get('http://tinyurl.com/api-create.php?url=' + best.url)
            message = 'Download Video: ' + str(r.text)
            bot.sendMessage(chat_id, message)

        else :
            bestaudio = video.getbestaudio(preftype="m4a")
            r = requests.get('http://tinyurl.com/api-create.php?url=' + bestaudio.url)
            message = 'Download Audio: ' + str(r.text)
            bot.sendMessage(chat_id, message)
            message = 'IMPORTANT: After downloading, rename the file to (anyname).m4a.\nNOTE: You could also save in .mp3 extension, but m4a provides better quality!'
            bot.sendMessage(chat_id, message)

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

while 1:
    time.sleep(10)
