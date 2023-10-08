# 載入 Flask 函式庫
from flask import Flask, request

# 載入 Linebot 函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, StickerSendMessage, ImageSendMessage, LocationSendMessage, AudioSendMessage

# 載入 Pygsheets 相關模組
import pygsheets

# 載入 Random 模組
import random

# 載入 JSON 資料格式
import json

# 載入 OS
import os

# 用 Pygsheets 操控目標 Google Sheet
gc = pygsheets.authorize(service_file="./english-chatbot-399304-7ef3098a521e.json") 
sht = gc.open_by_url("https://docs.google.com/spreadsheets/d/1fIK49B5EGWfoZ43lUeTotaviTMvUwb1JGmvjj7Si9bA/edit#gid=1039325276")
wks = sht.worksheet_by_title("Vocab")

# 定義選取圖卡連結和音檔網址的 URL 試算表範圍
card_start = 'I2'
card_end = 'I297'
res_card = wks.get_values(card_start, card_end)

audio_start = 'H2'
audio_end = 'H297'
res_audio = wks.get_values(audio_start, audio_end)

# 建立 App 物件
app = Flask(__name__)

# 環境變數帶入
line_user_id=os.getenv('LINE_USER_ID')
channel_access_token=os.getenv('CHANNEL_ACCESS_TOKEN')
channel_secret=os.getenv('CHANNEL_SECRET')

# 建立 / 路由
@app.route("/")
def home():
    return "Welcome to 'Your English Tutor!'"

# 建立 Webhook 路由
@app.route("/webhook", methods=['POST'])
def linebot():
    try:
        body = request.get_data(as_text=True)
        json_data = json.loads(body)                           # json 格式化收到的訊息
        line_bot_api = LineBotApi(channel_access_token)  # 輸入 你的 Channel access token
        handler = WebhookHandler(channel_secret)         # 輸入 你的 Channel secret
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']       # 取得 reply token
        tp = json_data['events'][0]['message']['type']  # 取得 message 的類型

        if tp == 'text':
            # 如果是文字類型的訊息
            msg = reply_msg(json_data['events'][0]['message']['text'])   # 取出文字並對應到 reply_msg 的函式
            if msg[0] == 'text':
                # 如果要回傳的訊息是 text，使用 TextSendMessage 方法
                line_bot_api.reply_message(tk,TextSendMessage(text=msg[1]))
            if msg[0] == 'location':
                # 如果要回傳的訊息是 location，使用 LocationSendMessage 方法
                line_bot_api.reply_message(tk,LocationSendMessage(title=msg[1]['title'],
                                                                address=msg[1]['address'],
                                                                latitude=msg[1]['latitude'],
                                                                longitude=msg[1]['longitude']))
            if msg[0] == 'image':
                # 如果要回傳的訊息是 image，使用 ImageSendMessage 方法
                line_bot_api.reply_message(tk,ImageSendMessage(original_content_url=msg[1],
                                                                preview_image_url=msg[1]))
            if msg[0] == 'audio':
                # 如果要回傳的訊息是 audio，使用 AudioSendMessage 方法
                line_bot_api.reply_message(tk, AudioSendMessage(original_content_url=msg[1]['url'],
                                                                duration=msg[1]['duration']))
            if type(msg) == tuple:
                msg_list = [AudioSendMessage(original_content_url=msg[0][1]['url'],
                                                                duration=msg[0][1]['duration']), ImageSendMessage(original_content_url=msg[1][1],
                                                                preview_image_url=msg[1][1])]
                line_bot_api.reply_message(tk, msg_list)

        if tp == 'sticker':
            # 如果收到的訊息是表情貼圖
            stickerId = json_data['events'][0]['message']['stickerId'] # 取得 stickerId
            packageId = json_data['events'][0]['message']['packageId'] # 取得 packageId
            # 使用 StickerSendMessage 方法回傳同樣的表情貼圖
            line_bot_api.reply_message(tk,StickerSendMessage(sticker_id=stickerId, package_id=packageId))
        if tp == 'location':
            # 如果是收到的訊息是地點資訊
            line_bot_api.reply_message(tk,TextSendMessage(text='在哪裡都要記得學英文！'))
        if tp == 'image':
            # 如果是收到的訊息是圖片
            line_bot_api.reply_message(tk,TextSendMessage(text='什麼圖片都比不上認真學習英文的風景'))
        if tp == 'audio':
            # 如果是收到的訊息是聲音
            line_bot_api.reply_message(tk,TextSendMessage(text='張開口，大聲唸英文！'))
        if tp == 'video':
            # 如果是收到的訊息是影片
            line_bot_api.reply_message(tk,TextSendMessage(text='你看的是英文影片嗎？'))
    except:
        print('error', body)
    return 'OK'

# 定義回覆訊息的函式
def reply_msg(text):
    tips_learn_eng = "1. Set Clear Goals: Determine why you want to learn English. Whether it's for work, travel, or personal interest, having clear goals will help you stay motivated.\n\n2. Create a Study Plan: Set aside dedicated time for learning English. Consistency is key.\n\n3. Stay Patient and Persistent: Learning a language takes time and effort. Don't be discouraged by initial challenges.\n\n4. Celebrate Milestones: Acknowledge your progress, whether it's completing a course, having a successful conversation, or understanding a complex text."

    # 如果出現特定地點，提供特定訊息
    msg_dict = {
        '你好':"Hi! How's your English learning going?",
        '怎麼學英文': tips_learn_eng
    }
    # 如果出現特定地點，提供地點資訊
    loc_dict = {
        '英文補習班':{
            'title':'創勝文教',
            'address':'10491台北市中山區朱崙街60號2樓',
            'latitude':'25.05024873445662',
            'longitude':'121.54436202077275'
        }
    }
    # 如果出現特定文字，提供圖片網址
    i = random.randint(0, 296)
    img_dict = {
        '再學一個單字': res_card[i][0]+'.png'
    }
    # 如果出現特定文字，提供音檔網址和音檔長度
    audio_dict = {
        '再學一個單字': {
            'url': res_audio[i][0],
            'duration': 2000
        }
    }
    # 預設回覆的文字就是收到的訊息
    reply_msg_content = ['text',text]
    if text in msg_dict:
        reply_msg_content = ['text',msg_dict[text.lower()]]
    if text in loc_dict:
        reply_msg_content = ['location',loc_dict[text.lower()]]
    if text in img_dict:
        reply_msg_content = ['image',img_dict[text.lower()]]
    if text in audio_dict:
        reply_msg_content = ['audio',audio_dict[text.lower()]], ['image',img_dict[text.lower()]]
    return reply_msg_content


 # 設定 Autosend 路由，自動發送圖檔和音檔訊息
@app.route("/autosend")
def send():
    line_bot_api = LineBotApi(channel_access_token)
    try:
        # 網址被執行時，等同使用 GET 方法發送 request，觸發 LINE Message API 的 push_message 方法
        msg = reply_msg("再學一個單字") 
        msg_list = [AudioSendMessage(original_content_url=msg[0][1]['url'], duration=msg[0][1]['duration']), ImageSendMessage(original_content_url=msg[1][1], preview_image_url=msg[1][1])]
        line_bot_api.push_message(line_user_id, msg_list)
        return 'OK'
    except:
        print('error')

# 在 5002 埠開啟 App
if __name__ == "__main__":
    app.run(port = 3000)