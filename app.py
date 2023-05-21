#鸚鵡機器人
from flask import Flask, request, abort

#載入linebot模組中的LineBotApi(Line Token), Webhookhandler(Line Secret)
from linebot import(
    LineBotApi, WebhookHandler
)

from linebot.exceptions import(
    InvalidSignatureError
)

from linebot.models import(
    MessageEvent, TextMessage, TextSendMessage
)

import json

#建立application物件
app = Flask(__name__)
#放入自己的LINE BOT-Channel Access Token
line_bot_api = LineBotApi("qiuquf2apa19G8a2mxZcGJmCOIPfckibPCF1BqbQm/BwTjb02/KqYtNA8yMR6qUsmOcSXGZ2BcH7t04lc1lM5tUNMh9qYM73Bh+b4UbOlIi4KlAqX7is7cCeBjRWvHT3wao95nkLPsVqb7LJhM1XAgdB04t89/1O/w1cDnyilFU=")
#放入自己的LINE BOT-Channel Secret
handler = WebhookHandler("e40a4cead4570c4a22d1205b04060bf2")


#監聽所有來自 /callback的Post Request
@app.route("/callback", methods = ['POST'])
def callback():
    #確保由LINE傳過來的
    signature = request.headers['X-Line-Signature']
    #將接收到的請求轉換為文字
    body = request.get_data(as_text = True)
    #文字轉為JSON格式
    json_data = json.loads(body)
    #格式化json_data讓輸出結果增加可讀性
    json_str = json.dumps(json_data, indent=4)
    print(json_str)
    
    try:
        #如果Channel Access Token或 Channel Secret發生錯誤
        #會進入到except InvalidSignatureError區塊
        handler.handle(body, signature)
    except InvalidSignatureError:
        #如果有錯誤代表Channel Access Token與Channel Secret可能輸入錯誤或失效
        abort(400)
    
    #返回OK，LINE Developers收到OK後代表Webhook執行沒問題
    #'OK'必須大寫，200回應成功
    return 'OK'

#LineBot訊息接收處
@handler.add(MessageEvent, message = TextMessage)
def handle_message(event):
    #將接收資訊轉為JSON格式
    json_data = json.loads(str(event))
    #格式化json_data讓輸出結果增加可讀性
    json_str = json.dumps(json_data, indent=4)
    print(json_str)
    #獲得使用者傳來的訊息
    msg = event.message.text
    #回傳訊息，傳送msg
    line_bot_api.reply_message(event.reply_token,TextSendMessage(msg))

#確保不是別的檔案引入，因為別的程式也有主程式，確保執行的是目前的程式
if __name__ == "__main__":
    app.run(port=4000)
