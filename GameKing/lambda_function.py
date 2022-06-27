import os
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, PostbackEvent
)

import eventHandler


# Log
import logging
logger = logging.getLogger('')
if   os.environ['Log_level'] == 'DEBUG':
    logger.setLevel(logging.DEBUG)
elif os.environ['Log_level'] == 'INFO':
    logger.setLevel(logging.INFO)


# LINE
line_bot_api = LineBotApi(os.environ['Channel_access_token'])
handler = WebhookHandler(os.environ['Channel_secret'])


def lambda_handler(event, context):
    # Handle message events
    @handler.add(MessageEvent)
    def handle_message(event):
        eventHandler.handleMessage(event)
            
    # Handle postback events
    @handler.add(PostbackEvent)
    def handle_postback(event):
        eventHandler.handlePostback(event)
    
    logger.info(event)
    
    # get X-Line-Signature header value
    signature = event['headers']['x-line-signature']

    # get request body as text
    body = event['body']

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {
            'statusCode': 502,
            'body': json.dumps("Invalid signature. Please check your channel access token/channel secret.")
            }
    except LineBotApiError:
        return {
            'statusCode': 400,
            'body': json.dumps("LineBotApi errors. Please check your firewall.")
            }
    return {
        'statusCode': 200,
        'body': json.dumps("Hello from Lambda!")
        }