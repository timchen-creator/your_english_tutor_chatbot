# 載入 Pygsheets 相關模組
import pygsheets

# 載入 Selenium 相關模組
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# 載入 Time 相關模組
import random
import time

# 用 Pygsheets 操控目標 Google Sheet
gc = pygsheets.authorize(service_file="./english-chatbot-399304-7ef3098a521e.json")
sht = gc.open_by_url("https://docs.google.com/spreadsheets/d/1fIK49B5EGWfoZ43lUeTotaviTMvUwb1JGmvjj7Si9bA/edit#gid=0")
wks = sht.worksheet_by_title("Vocab")

# 定義 Response 抓取英文單字清單的範圍
start = 'A2'
end = 'A944'
response = wks.get_values(start, end)

# 設定 Delay 隨機時間
delay_times = [3, 6, 9, 12, 15, 19]
delay = random.choice(delay_times)

# 設定 Chrome Driver 執行檔路徑
options=Options()
options.chrome_executable_path=("/Users/timchen/Desktop/Project_Chatbot/chromedriver")

# 建立 Driver 物件實體、用程式操作瀏覽器運行
driver=webdriver.Chrome(options=options)

# 建立 While 迴圈開始爬蟲
i = 0
while i < 10:
    try:
        driver.get("https://dictionary.cambridge.org/dictionary/english-chinese-traditional/%s" % response[i][0])

        eng_word = driver.find_element(By.CLASS_NAME, "hw.dhw")
        part_of_speech = driver.find_element(By.CLASS_NAME, "pos.dpos")
        eng_meaning = driver.find_element(By.CLASS_NAME, "def.ddef_d.db")
        chin_tran = driver.find_element(By.CLASS_NAME, "trans.dtrans.dtrans-se.break-cj")
        eng_sent = driver.find_element(By.CLASS_NAME, "eg.deg")
        chin_sent = driver.find_element(By.CLASS_NAME, "trans.dtrans.dtrans-se.hdb.break-cj")
        pron = driver.find_element(By.TAG_NAME, "source")
        ipa = driver.find_element(By.CLASS_NAME, "ipa.dipa.lpr-2.lpl-1")

        wks.update_row(i+2,[eng_word.text, "/"+ipa.text+"/", eng_meaning.text, chin_tran.text, part_of_speech.text, eng_sent.text, chin_sent.text, pron.get_attribute('src')])
        i += 1
        # 每爬取 10 筆英文單字資料會休息 1 次
        if i % 10 == 0:
            time.sleep(delay)

    except NoSuchElementException:
        i += 1
        pass
    
driver.close()