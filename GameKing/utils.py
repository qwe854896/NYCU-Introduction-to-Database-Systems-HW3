import os
import sys
import json
import jinja2
import logging
import requests

from linebot import LineBotApi
from linebot.models import *

line_bot_api = LineBotApi(os.environ['Channel_access_token'])

def reply_message(token, msg):
	line_bot_api.reply_message(token, msg)


def textMsg(Text='Hello, world'):
	return TextSendMessage(text=Text)

def stickerMsg(pid='1', sid='1'):
	return StickerSendMessage(
		package_id=pid,
		sticker_id=sid
	)

def imageMsg(content_url, preview_url):
	return ImageSendMessage(
		original_content_url=content_url,
		preview_image_url=preview_url
	)

def videoMsg(content_url, preview_url):
	return VideoSendMessage(
		original_content_url=content_url,
		preview_image_url=preview_url
	)

def audioMsg(content_url, Duration=30):
	return AudioSendMessage(
		original_content_url=content_url,
		duration=Duration
	)
	

def replace_json(jin,dic):
    template=""
    with open(jin,"r") as read:
        template=json.load(read)
        template=json.dumps(template)

    result = jinja2.Template(template)
    return json.loads(result.render(dic))


def fetchImageURL(keyword):
	req = requests.request('GET', 'https://serpapi.com/search?q=' + keyword + '&tbm=isch&ijn=0&api_key=' + os.environ['Serp_api_key'])
	req = json.loads(req.text)
	logging.info(req['images_results'][0]['original'])
	return req['images_results'][0]['original']

def fetchRichMenuIdByName(name):
    headers = {
        "Authorization":"Bearer " + os.environ['Channel_access_token']
    }
    req = requests.request('GET', 'https://api.line.me/v2/bot/richmenu/list', 
                           headers=headers)
    req = json.loads(req.text)
    ids = []

    for richmenu in req["richmenus"]:
        if richmenu['name'] == name:
            ids.append(richmenu['richMenuId'])

    return ids