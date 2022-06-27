import os
import sys
import json

from urllib.parse import urlparse, parse_qs
from linebot.models import *

from utils import reply_message, fetchRichMenuIdByName
from richmenu import switchTo
from queryHandler import *


# Log
import logging
logger = logging.getLogger('')
if   os.environ['Log_level'] == 'DEBUG':
    logger.setLevel(logging.DEBUG)
elif os.environ['Log_level'] == 'INFO':
    logger.setLevel(logging.INFO)

def handleText(event):
	msgText = event.message.text
	reply_token = event.reply_token
	
	userId = event.source.user_id
	switchTo(userId, fetchRichMenuIdByName('richmenu-default')[0])
	
	if msgText == "debug":
		flexMsg = json.load(open('./json/debug.json', 'r', encoding='utf-8'))
		reply_message(reply_token, FlexSendMessage('ops', flexMsg))
	elif msgText[:2] == "q1":
		handleQ1(reply_token, msgText[3:])
	elif msgText[:2] == "q2":
		handleQ2(reply_token, msgText[3:])
	elif msgText[:2] == "q3":
		handleQ3(reply_token, msgText[3:])
	elif msgText[:2] == "q4":
		handleQ4(reply_token, msgText[3:])
	elif msgText[:2] == "q5":
		handleQ5(reply_token, msgText[3:])
	else:
		reply_message(reply_token, TextSendMessage(text=msgText))
		

def handleSticker(event):
	msgStickerId = event.message.stickerId
	msgPackageId = event.message.packageId

def handleImage(event):
	msgId = event.message.id
	usrId = event.source.user_id

def handleVideo(event):
	msgId = event.message.id
	usrId = event.source.user_id
	msgDuration = event.message.duration

def handleAudio(event):
	msgId = event.message.id
	usrId = event.source.user_id
	msgDuration = event.message.duration
	
def handleLocation(event):	
	msgAddress = event.message.address
	msgLatitude = event.message.latitude
	msgLongtitude = event.message.longitude


def handleMessage(event):
	message_type = event.message.type
	
	if message_type == "text":
		handleText(event)	
	elif message_type == "sticker":
		handleSticker(event)
	elif message_type == "image":
		handleImage(event)
	elif message_type == "video":
		handleVideo(event)
	elif message_type == "audio":
		handleAudio(event)
	elif message_type == "location":
		handleLocation(event)


def handlePostback(event):
	data = event.postback.data
	userId = event.source.user_id
	
	data = parse_qs(data)
	logger.info(data)
    
	if 'action' in data and data['action'][0] == 'richmenu-default':
		switchTo(userId, fetchRichMenuIdByName('richmenu-default')[0])