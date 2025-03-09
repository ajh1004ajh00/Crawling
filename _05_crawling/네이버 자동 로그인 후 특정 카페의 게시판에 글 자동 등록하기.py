#!/usr/bin/env python
# coding: utf-8

# In[1]:
import pyupbit
import pandas as pd
import time
import subprocess
import requests
from bs4 import BeautifulSoup


#2.Telegram Bot API 설정
bot_token = '5873963259:AAFg1UzWV8uUPRQuJ47s3TOzdjviGbe6cLQ'
base_url = f'https://api.telegram.org/bot{bot_token}'
chatid_s1 = '1111111'  #텔레그램 ID를 찾아서 넣으세요

bot_token_s2='7641435947:AAE-XZ5dvE3-MY4hhhj60xfAcuSAFeSUMp4'  #서진수 선불폰
base_url_s2 = f'https://api.telegram.org/bot{bot_token_s2}'
chatid_s2='111111'  # 텔레그램 ID룰 찾아서 넣으세요

#####################################################################################################
#1. 텔레그램 메시지 보내는 함수
def send_message(chat_id, text):
    send_message_url = f'{base_url}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(send_message_url, data=data)
    return response.json()
####################################################################################################


# def get_bitcoin_news():
#     url = "https://news.google.com/search?q=%EC%95%94%ED%98%B8%ED%99%94%ED%8F%90&hl=ko&gl=KR&ceid=KR:ko"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
    
#     # 뉴스 제목과 링크 추출
#     news_list = []
#     articles = soup.find_all('a', class_='JtKRv')  # 이 클래스는 변경될 수 있음
    
#     for article in articles:
#         title = article.get_text()
#         link = "https://news.google.com" + article['href'][1:]
#         news_list.append((title, link))

#     return news_list
def get_bitcoin_news():
    url = "https://news.google.com/search?q=%EC%95%94%ED%98%B8%ED%99%94%ED%8F%90&hl=ko&gl=KR&ceid=KR:ko"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 뉴스 제목과 링크 추출
    news_list = []
    articles = soup.find_all('a', class_='JtKRv')  # 이 클래스는 변경될 수 있음

    for idx, article in enumerate(articles):
        if idx >= 100:  # 200개의 뉴스만 크롤링
            break
        title = article.get_text()
        link = "https://news.google.com" + article['href'][1:]
        news_list.append((title, link))

    return news_list


# In[59]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import urllib.request
import urllib
import pyautogui

def login_naver_cafe(driver, username, password):
    driver.get('https://nid.naver.com/nidlogin.login')
    time.sleep(2)
    driver.maximize_window()
    driver.find_element(By.XPATH, '//*[@id="loinid"]/span/span').click()
    time.sleep(2)

    # 로그인 폼에 아이디와 비밀번호 입력
    driver.execute_script("document.getElementsByName('id')[0].value=\'"+username+"\'")
    driver.execute_script("document.getElementsByName('pw')[0].value=\'"+password+"\'")
    driver.find_element(By.XPATH,'//*[@id="log.login"]').click()
    time.sleep(2)

def post_to_cafe(driver, cafe_url, title, link):
    driver.get(cafe_url)
    time.sleep(3)

    # 게시판 선택하기 - 가치랩스
    driver.find_element(By.XPATH,'//*[@id="menuLink41"]').click()
    time.sleep(2)
   
    # 글쓰기 버튼 클릭 (XPath는 상황에 맞게 수정)
    driver.switch_to.frame('cafe_main')
    driver.find_element('xpath', '//*[@id="writeFormBtn"]').click()
    time.sleep(3)

    # 현재 열려 있는 모든 창의 핸들 수집
    window_handles = driver.window_handles
    
    # 첫 번째 핸들은 기존 창, 두 번째 핸들은 새로 열린 창이므로 두 번째 창으로 전환
    driver.switch_to.window(window_handles[-1])
    time.sleep(10)
    
    # 제목과 내용 작성
    title_area = driver.find_element('xpath', '//*[@id="app"]/div/div/section/div/div[2]/div[1]/div[1]/div/div[2]/div/textarea')
    title_area.send_keys(title)
    time.sleep(2)
    urlbtn = pyautogui.locateOnScreen('c:\\py_temp\\images\\urlbtn.png')
    center = pyautogui.center(urlbtn)
    pyautogui.click( center )
    time.sleep(3)
    urlbtn2 = pyautogui.locateOnScreen('c:\\py_temp\\images\\urlbtn2.png')
    center2 = pyautogui.center(urlbtn2)
    pyautogui.click( center2 )
    pyautogui.write(link,interval=0.1)
    time.sleep(1)
    pyautogui.press('enter')
    
    time.sleep(2)

    # 등록 버튼 클릭
    driver.find_element('xpath', '//*[@id="app"]/div/div/section/div/div[1]/div/a').click()
    time.sleep(3)


# In[60]:


import schedule

def job():
    driver = webdriver.Chrome()
    login_naver_cafe(driver, "Naver login ID", "로그인 비밀번호")
    
    news = get_bitcoin_news()
    for title, link in news:
        post_to_cafe(driver, "https://cafe.naver.com/gachilabs", title, link)

    driver.quit()

schedule.every().day.at("02:10").do(job)

while True:
    try :
        schedule.run_pending()
        time.sleep(60) 
    except :
        # driver = webdriver.Chrome()
        # driver.quit( )
        # 텔레그램으로 메시지보내기
        message_text = '네이버 카페 뉴스 등록 작업에 오류가 발생했습니다~ 2분 뒤 재 시작합니다!!'
        response = send_message(chatid_s1, message_text)
        response = send_message(chatid_s2, message_text)
        
        time.sleep(120)
        subprocess.run(['python','c:\\py_temp\\naver_cafe.py'])
            
    




