from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('i3gEO5iMJLy8ggIN2wFCJQohbONv3/OOg9509TmkL7TfyGULbB2uxHim87MQQfPVM8k9witGyllPAWlsmyfJu5BQQuzo2nMw5O6cbENwGNXn2/D+c+8VrGR7x5FWLVxywLsK0Ea7vF1lFNJ2PvuBBQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b121f45158b19004b8cb30c2a65446fa')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()