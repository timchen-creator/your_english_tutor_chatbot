# 載入 Pygsheets 相關模組
import pygsheets

# 載入 Selenium 相關模組
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# 載入 Time 相關模組
import time

# 載入 Json
import json

def edit(str, block):
    actions.move_to_element(block)
    actions.click()
    actions.click()
    actions.key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND) 
    actions.send_keys(str)
    # actions.perform()
    actions.move_by_offset(-300,0).click().perform() # 在空白處點一下
    time.sleep(2)


# 用 Pygsheets 操控目標 Google Sheet
gc = pygsheets.authorize(service_file="./english-chatbot-399304-7ef3098a521e.json") 
sht = gc.open_by_url("https://docs.google.com/spreadsheets/d/1fIK49B5EGWfoZ43lUeTotaviTMvUwb1JGmvjj7Si9bA/edit#gid=1039325276")
wks = sht.worksheet_by_title("Project")

# 定義 Response 抓取範圍
start = 'A2'
end = 'G5999'
res = wks.get_values(start, end)

# 設定 Chrome Driver 執行檔路徑
options=Options()
options.chrome_executable_path=("/Users/timchen/Desktop/Your-english-tutor-chatbot/chromedriver") 


# 建立 Driver 物件實體、用程式操作瀏覽器運行
driver=webdriver.Chrome(options=options)

# 連線到 Canva 登入頁面
driver.get("https://www.canva.com/design/DAFv7Ev_hiQ/5ks0vsXdJUuSSY2v1YNqhA/edit")
driver.maximize_window()

# 載入 Cookie Session 自動登入
file=open('cookie.json','r')
data=json.loads(file.read())
for c in data:
    driver.add_cookie(c)
driver.refresh()

# 建立 actions 物件，準備操作 Canva
actions = ActionChains(driver)
for i in range(296, 501):
    # 複製頁面
    copyBtn = driver.find_element(By.CLASS_NAME, "_1QoxDw.Qkd66A.tYI0Vw.o4TrkA.Eph8Hg.cclg9A.YPTJew.Qkd66A.tYI0Vw.HySjhA.cwOZMg.zQlusQ.uRvRjQ.pgaA2w.ApD3tw.MsUq3g")
    copyBtn.click()
    time.sleep(3)

    # 編輯檔名
    fileName = driver.find_elements(By.CLASS_NAME, "GZPi5g.Yp81Yw")[2]
    edit(res[i][0], fileName)
    
    # 編輯文字方塊
    blocks = driver.find_elements(By.CLASS_NAME, "OYPEnA")
    for j in range(7): # 英文單字 音標 英文解釋 中文解釋 詞性 英文例句 中文例句
        edit(res[i][j], blocks[j+7])

# 關閉瀏覽器
driver.close()