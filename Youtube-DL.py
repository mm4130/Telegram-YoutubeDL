import sys
import os
import time
import telepot
import requests
from bs4 import BeautifulSoup as BS

TOKEN = "322697558:AAHvhQKphdRMQ8bPnkAY9aAOcu_Vn4tgptQ"
#comment for fun

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    flavor = telepot.flavor(msg)
    summary = telepot.glance(msg, flavor=flavor)
    print (flavor, summary)
    
    order = msg['text'].split(' ')
    title = ''
    flag_URL = 0
    flag_AUDIO = 0

    for text in order:
    	if text.startswith('https://') or text.startswith('www.') or text.startswith('youtu'):
    		url = text
    		r = requests.get(url)
    		soup = BS(r.text, "html.parser")
    		title = soup.title.string
    		title = title.split(' - YouTube')[0]
    		title = title.split('|')[0].split('(')[0].split('.')[0].strip()
    		title = title.replace(' ', '_')
    		print title
    		flag_URL = 1
    	elif text.lower().startswith('audio'):
    		flag_AUDIO = 1

    if flag_URL == 0:
    	bot.sendMessage(chat_id, 'Please enter a video link to download.')

    elif flag_AUDIO == 0:
    	cmd = 'youtube-dl -f \'bestvideo[ext=mp4]+bestaudio[ext=mp3]/best[ext=mp4]/best\' --output \"' + title + '.mp4\" ' + url
    	os.system(cmd)
    	bot.sendMessage(chat_id, 'Please wait while we fetch the file for you. Video files can be heavy, we get the best for you. Hold tight!')
    	sendVideo(chat_id, title+'.mp4')
    	os.system('rm '+title+'.mp4')

    elif flag_AUDIO == 1 :
    	cmd = 'youtube-dl -f \'bestaudio/best\' --extract-audio --audio-format mp3 --output \"' + title + '.mp3\" ' + url
    	os.system(cmd)
    	bot.sendMessage(chat_id, 'Please wait while we fetch the audio file for you.')
    	sendAudio(chat_id, title+'.mp3')
    	os.system('rm '+title+'.mp3')

def sendVideo(chat_id, file_name):
	url = "https://api.telegram.org/bot%s/sendVideo"%(TOKEN)
	try:
		files = {'video': open(file_name, 'rb')}
	except:
		bot.sendMessage(chat_id, 'There seems to be an error with your message. Please check the URL again!')
		return
	data = {'chat_id' : chat_id}
	r = requests.post(url, files=files, data=data)
	print(r.status_code, r.reason, r.content)

def sendAudio(chat_id, file_name):
	url = "https://api.telegram.org/bot%s/sendAudio"%(TOKEN)
	try:
		files = {'audio': open(file_name, 'rb')}
	except:
		bot.sendMessage(chat_id, 'There seems to be an error with your message. Please check the URL again!')
		return
	data = {'chat_id' : chat_id}
	r = requests.post(url, files=files, data=data)
	print(r.status_code, r.reason, r.content)

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

while 1:
    time.sleep(10)
