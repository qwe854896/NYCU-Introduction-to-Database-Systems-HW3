import os
import sys
import json

from urllib.parse import urlparse, parse_qs
from linebot.models import *

from utils import reply_message, replace_json, fetchImageURL
from SQL import Video_Games, fetchSession
from richmenu import switchTo
from queryHandler import *


# Log
import logging
logger = logging.getLogger('')
if   os.environ['Log_level'] == 'DEBUG':
    logger.setLevel(logging.DEBUG)
elif os.environ['Log_level'] == 'INFO':
    logger.setLevel(logging.INFO)


session = fetchSession()

def handleQ1(token, msgText):
	if msgText == "其他":
		reply_message(token, TextSendMessage(text='請輸入: "q1 [遊戲名稱]"'))
	else:
		cnt = 0
		data = {}
		try:
			for instance in session.query(Video_Games).filter(Video_Games.Name==msgText):
				cnt += 1
				data = instance.__dict__
		except Exception as e:
			reply_message(token, TextSendMessage(text='不要 SQL injection 我 ><'))
		
		if cnt == 0:
			reply_message(token, TextSendMessage(text='不存在遊戲: ' + msgText))
		else:
			cnt = 4
			for instance in session.query(Video_Games).\
							filter(Video_Games.Genre==data['Genre'], Video_Games.Global_Sales != None).\
							order_by(Video_Games.Global_Sales)[-3:]:
				cnt -= 1
				name = instance.Name
				data['Name' + str(cnt)] = name
			
			data['Images'] = fetchImageURL(msgText)
			
			flexMsg = replace_json('json/q1_reply.json', data)
			logger.info(flexMsg)
			reply_message(token, FlexSendMessage(msgText, flexMsg))
			
			
def handleQ2(token, msgText):
	header = ''
	orderby = ''
	if msgText == "Sales":
		header = 'Rank by Global Sales'
		orderby = Video_Games.Global_Sales
	elif msgText == "critic":
		header = 'Rank by Critic Score'
		orderby = Video_Games.Critic_Score
	elif msgText == "Users":
		header = 'Rank by User Score'
		orderby = Video_Games.User_Score
	elif msgText == "Year":
		reply_message(token, TextSendMessage(text='請輸入: "q5 [年份]"'))
		return
	else:
		reply_message(token, TextSendMessage(text='沒有這個查詢><'))
		return
		
	cnt = 4
	data = {"Header": header}
	for name in session.query(Video_Games.Name).filter(orderby != None).order_by(orderby)[-3:]:
		cnt -= 1
		name = name[0]
		data['Name' + str(cnt)] = name
		
	flexMsg = replace_json('json/q2_reply.json', data)
	logger.info(flexMsg)
	reply_message(token, FlexSendMessage(header, flexMsg))
		
		
def handleQ3(token, msgText): # Genre
	header = 'Rank of {} Game'.format(msgText)
	data = {"Header": header}
	
	cnt = 4
	for name in session.query(Video_Games.Name).\
							filter(Video_Games.Genre == msgText, Video_Games.Global_Sales != None).\
							order_by(Video_Games.Global_Sales)[-3:]:
		cnt -= 1
		name = name[0]
		data['Name' + str(cnt)] = name
			
	if cnt == 4:
		reply_message(token, TextSendMessage(text='沒有這個查詢><'))
		return
			
	flexMsg = replace_json('json/q2_reply.json', data)
	logger.info(flexMsg)
	reply_message(token, FlexSendMessage(header, flexMsg))
		
		
def handleQ4(token, msgText): # Region Sales
	header = ''
	orderby = ''
	if msgText == "NA":
		header = '北美前三'
		orderby = Video_Games.NA_Sales
	elif msgText == "EU":
		header = '歐洲前三'
		orderby = Video_Games.EU_Sales
	elif msgText == "JP":
		header = '日本前三'
		orderby = Video_Games.JP_Sales
	else:
		reply_message(token, TextSendMessage(text='沒有這個查詢><'))
		return
	
	cnt = 4
	data = {"Header": header}
	for name in session.query(Video_Games.Name).\
							filter(orderby != None).\
							order_by(orderby)[-3:]:
		cnt -= 1
		name = name[0]
		data['Name' + str(cnt)] = name
			
	if cnt == 4:
		reply_message(token, TextSendMessage(text='沒有這個查詢><'))
		return
			
	flexMsg = replace_json('json/q2_reply.json', data)
	logger.info(flexMsg)
	reply_message(token, FlexSendMessage(header, flexMsg))
		
		
def handleQ5(token, msgText):
	year = msgText
	if not year.isdigit():
		reply_message(token, TextSendMessage(text='這不是年份喔><'))
		return
	header = '{} 年後前三'.format(year)
	year = int(year)
	
	cnt = 4
	data = {"Header": header}
	for name in session.query(Video_Games.Name).\
							filter(Video_Games.Year_of_Release >= year, Video_Games.Global_Sales != None).\
							order_by(Video_Games.Global_Sales)[-3:]:
		cnt -= 1
		name = name[0]
		data['Name' + str(cnt)] = name
			
	if cnt == 4:
		reply_message(token, TextSendMessage(text='這之後太少遊戲了><'))
		return
			
	flexMsg = replace_json('json/q2_reply.json', data)
	logger.info(flexMsg)
	reply_message(token, FlexSendMessage(header, flexMsg))