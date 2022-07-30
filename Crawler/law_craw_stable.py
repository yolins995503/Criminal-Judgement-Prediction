# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:38:44 2019

@author: Kai-Yuan
"""
from datetime import date, timedelta, datetime
# Generated by Selenium IDE
import random
import pytest
import time
import re
import requests
import os
import warnings
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

#os.chdir(r'C:\Users\yo\Desktop\123')

USER_AGENT_LIST = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    ] 

class Craw():
  def setup_method(self, method):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless')
    self.driver = webdriver.Chrome(options=options)
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def search_one_day(self, date):
    year = date.year-1911
    month = date.month
    day = date.day
    locator =(By.ID,'dy1')
    self.driver.get("https://law.judicial.gov.tw/FJUD/Default_AD.aspx")
    WebDriverWait(self.driver, 30,0.5).until(EC.presence_of_element_located(locator))
    self.driver.find_element(By.ID, "dy1").click()
    self.driver.find_element(By.ID, "dy1").send_keys(str(year))
    self.driver.find_element(By.ID, "dm1").click()
    self.driver.find_element(By.ID, "dm1").send_keys(str(month))
    self.driver.find_element(By.ID, "dd1").click()
    self.driver.find_element(By.ID, "dd1").send_keys(str(day))
    self.driver.find_element(By.ID, "dy2").click()
    self.driver.find_element(By.ID, "dy2").send_keys(str(year))
    self.driver.find_element(By.ID, "dm2").click()
    self.driver.find_element(By.ID, "dm2").send_keys(str(month))
    self.driver.find_element(By.ID, "dd2").click()
    self.driver.find_element(By.ID, "dd2").send_keys(str(day))
    element = self.driver.find_element(By.ID, "jud_title")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.ID, "jud_title").send_keys("")#搜尋
    self.driver.find_element(By.ID, "vtype_A").click()
    select = Select(self.driver.find_element_by_name('jud_court'))

    select.select_by_value("TPD")
    select.select_by_value("SLD")    
    select.select_by_value("PCD")
    select.select_by_value("ILD")
    select.select_by_value("KLD")
    select.select_by_value("TYD")
    select.select_by_value("SCD")
    select.select_by_value("MLD")
    select.select_by_value("TCD")
    select.select_by_value("CHD")
    select.select_by_value("NTD")
    select.select_by_value("ULD")
    select.select_by_value("CYD")
    select.select_by_value("TND")
    select.select_by_value("KSD")
    select.select_by_value("CTD")
    select.select_by_value("HLD")
    select.select_by_value("TTD")
    select.select_by_value("PTD")
    select.select_by_value("PHD")
    select.select_by_value("KMD")
    select.select_by_value("LCD")
  
    self.driver.find_element(By.ID, "btnQry").click()
    self.driver.switch_to.frame("iframe-data")
    
    html = self.driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(html, 'html5lib')
    form = soup.find('form',attrs={'class':None})
    action = form.attrs['action']
    q_position = action.find("&q=")
    div = form.find('div',attrs={"id":"plPager"})
    title = soup.find('title')
    if title.text.strip()!='查詢結果列表':
        return
    if div:
        span_text = div.find('span').text
        result_amount = eval(re.search(r'\d+', span_text).group())
        if result_amount > 500:
            result_amount = 500 
        
            
    else:
        result_amount = len(form.find_all('tr', attrs={'class':'summary'}))
        
    url_base = "https://law.judicial.gov.tw/FJUD/data.aspx?ro={}&sort=DS&ot=in" + action[q_position:]
    for i in range(result_amount):
        print(f'case{i}')
        random_num = 0
        check = 0
        if random_num<=(500*2/15047) and check == 0:
          USER_AGENT = random.choice(USER_AGENT_LIST)
          headers={'user-agent':USER_AGENT}
          try:
            #print(f'case{i}')
            article_html = requests.get(url_base.format(i),verify=False,headers=headers)
            #print(article_html.encoding)
            article_soup = BeautifulSoup(article_html.text, 'html5lib')
            article_div = article_soup.find('div', attrs={'class':'text-pre text-pre-in'})
            #print(article_div.text)
            random_num=random.uniform(0,1)
          except:
            print('error_occur')
            check= 1
            time.sleep(1)
            #print(random_num)          
            print(f'***case{i}')
            with open(f"law_txts/{date.strftime('%Y %m %d')}-{i}.txt", 'w', encoding='utf-8') as fp:
                fp.write(article_div.text)
        
    

def with_days(days, start_day, reverse):
	# if reverse = true 往後數
	for i in range(days):
		if reverse:
			#起始日期往後
			current = start_day + timedelta(i)
		else:
			#起始日期往前
			current = start_day - timedelta(i)
		print(f"Proccess: Day{current}")
		test = Craw()
		test.setup_method("POST")
		test.search_one_day(current)
		test.teardown_method("POST")



def with_end(start_day, end_day):
  current = start_day
  i = 0
  while current < end_day:
    current = start_day + timedelta(i)
    i += 1
    print(f"Proccess: Day{current}")
    test = Craw()
    test.setup_method("POST")
    test.search_one_day(current)
    test.teardown_method("POST")


if __name__ == '__main__':
	warnings.simplefilter('ignore',requests.urllib3.exceptions.InsecureRequestWarning)

	today = date.today()
	#起始日期
	start_day = datetime.strptime('2018 03 15','%Y %m %d')
	#尋找次數
	days = 22
	#結束日期
	end_day = datetime.strptime('2018 12 31','%Y %m %d')
	#
	reverse = True
	
	if 'law_txts' not in os.listdir():
		os.mkdir('law_txts')
		
	#with_days(days, start_day, reverse)
	with_end(start_day, end_day)


