import smtplib
import requests
import os
import re
import json
import random
import time
from .headers import *
from requests.models import Request, requote_uri
from rich.progress import track
from rich import print
from rich.console import Console
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
import _pickle as pk, datetime
from hashlib import md5
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class Download:
    random_user = None
    USER_AGENT_LIST = None

    def __init__(self):
        self.bookid = ''
        self.bookName = ""
        self.main_path = ""
        self.bookName = ""
        self.charCount = ""
        self.lastUpdateTime = ""
        self.authorName = ""
        self.isFinish = ""
        self.type_dict = type_dict
        self.headers = {'User-Agent' : None}
        self.USER_AGENT_LIST = user_agent_list
            
            
    def user_agent_list(self):
        self.headers['User-Agent'] = random.choice(self.USER_AGENT_LIST)
        return self.headers


    def get_requests(self, api):
        requ = requests.get(url=api, headers=self.headers)
        return requ
    
    
        
        
    def get_bookid(self,bookid):
        self.user_agent_list()
        self.bookid = bookid
        url = f'https://api.aixdzs.com/book/{self.bookid}'
        self.bookName = self.get_requests(url)['title']
        self.authorName = self.get_requests(url)['author']
        self.isFinish = self.get_requests(url)['zt']
        self.charCount = self.get_requests(url)['wordCount']
        self.lastUpdateTime_chap = self.get_requests(url)['lastChapter']
        self.novel_tag = self.get_requests(url)['cat'] 
        self.lastUpdateTime = self.get_requests(url)['updated']  # 最后更新章节
        self.novel_intro = self.get_requests(url)['longIntro']  # 简介
        
            
    def new_file(self):
        if not os.path.exists("config"):
            os.mkdir("config")
            
        if not os.path.exists("novel"):
            os.mkdir("novel")
            
        if not os.path.exists(os.path.join("config", self.bookName + ".json")):
            open(os.path.join("config", self.bookName + ".json"),'w')
    
        
    def write_novel_article(self,write_txt_info):  # 将信息写入TXT文件
        with open(os.path.join('novel', f"{self.bookName}.txt"), 'a', newline='') as fb:
            fb.write(str(write_txt_info))
            
    
    def write_json_article(self,write_json_info):  # 将信息写入json文件
        with open(os.path.join("config", self.bookName + ".json"), 'a', newline='') as fb:
            fb.write(str(write_json_info))
    
    
    def intro_info(self):
        self.new_file()
        self.user_agent_list()
        novel_intros = ''
        novel_intros += '书名:{}\n作者:{}\n'.format(self.bookName, self.authorName)
        novel_intros += '状态:{}\n字数:{}\n'.format(self.isFinish, self.charCount)
        novel_intros += '更新:{}\n标签:{}\n'.format(self.lastUpdateTime_chap,self.novel_tag)
        novel_intros += '最后更新章节:{}\n'.format(self.lastUpdateTime)
        novel_intros += '简介信息\n{}'.format(self.novel_intro)
        self.novel_intros = novel_intros
        print(self.novel_intros)
        
        with open(os.path.join("config", self.bookName + ".json"), 'r', encoding='gbk', newline='') as fb:
            chapId_list = fb.read()
        if "简介信息" not in chapId_list:
            self.write_json_article(f"\n简介信息:\n{novel_intros}\n")
            intro_file = os.path.join('novel', f"{self.bookName}.txt")
            file = open(intro_file, 'a')
            file.close()
            with open(intro_file, 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(f"\n简介信息:\n{novel_intros}\n" + content)


    def download_book(self):
        self.user_agent_list()
        url = f'http://api.aixdzs.com/content/{self.bookid}?view=chapter'
        catalogue = self.get_requests(url)['mixToc']
        number = 0
        self.intro_info()
        self.send_text()
        for chapters in track(catalogue['chapters']):
            chapters_id = str(chapters['link'])
            with open(os.path.join("config", self.bookName + ".json"), 'r', encoding='gbk', newline='') as fb:
                chapId_list = fb.read()
            if chapters_id not in chapId_list:
                self.write_json_article(f"{chapters_id}\n")
                number += 1
                url = f'http://api.aixdzs.com/chapter/{chapters_id}'
                novel_title = self.get_requests(url)['chapter']['title']
                novel_body = self.get_requests(url)['chapter']['body']
                title_body = f"\n\n\n{novel_title}\n{novel_body}"
                self.write_novel_article(title_body)
            else:
                continue
        self.send_file()
        
        
    def search_book(self):
        self.user_agent_list()
        book = input('input book name:')
        while not book:
            book = input("input book name:")
        url = f'http://api.aixdzs.com/book/search?query={book}'
        print(self.get_requests(url))
        

    def get_book_list(self, dict_number):
        self.user_agent_list()
        number = 1
        book_url_ID_list = []
        for i in range(10000):
            number += 20
            url = "http://api.aixdzs.com/book-sort?gender=6&type=hot&major={}&minor=&start={}&limit=20".format(
                  self.type_dict[int(dict_number)], number)
            for data in self.get_requests(url)['books']:
                self.bookid = data['_id']
                book_title = data['title']
            book_url_ID_list.append(self.bookid)
            self.get_bookid(self.bookid)
            start = time.time()
            self.download_book()
            end = time.time()
            print(f'下载耗时:{round(end - start, 2)} 秒')
            with open(os.path.join('novel', f"list.txt"), 'a', newline='') as fb:
                json.dump(self.get_requests(url), fb, ensure_ascii=False, indent=4)
                


    def send_text(self):
        host_server = 'smtp.163.com'
        pwd = 'ha8277'
        sender = 'jiang47475tan87@163.com'
        receiver = 'jiang47475tan87@163.com' # input you email
        mail_content = f"{self.novel_intros}"
        mail_title = f"开始下载小说:{self.bookName}"
        msg = MIMEText(mail_content, 'plain', 'utf-8')
        msg['Subject'] = Header(mail_title, 'utf-8')
        msg['From'] = sender
        msg['To'] = receiver
        try:
            smtp = SMTP_SSL(host_server)
            smtp.ehlo(host_server)
            smtp.set_debuglevel(0)
            smtp.login(sender, pwd)
            smtp.sendmail(sender, receiver, msg.as_string())
            smtp.quit()
        except smtplib.SMTPException as e:
            print('error:',e) #打印错误
 
 
 
    def send_file(self):
        host_server = 'smtp.163.com'
        pwd = 'ha8277'
        sender = 'jiang47475tan87@163.com'
        receiver = 'jiang47475tan87@163.com' # input you email
        txt_file = os.path.join('novel', f"{self.bookName}.txt")
        txtApart = MIMEApplication(open(txt_file, 'rb').read())
        txtApart.add_header('Content-Disposition', 'attachment', filename=f"{self.bookName}.txt")
        upload_file = MIMEMultipart()
        upload_file.attach(txtApart)
        mail_upload_title = f"下载小说文件:{self.bookName}"
        upload_file['Subject'] = mail_upload_title
        try:
            smtp = SMTP_SSL(host_server)
            smtp.ehlo(host_server)
            smtp.set_debuglevel(0)
            smtp.login(sender, pwd)
            smtp.sendmail(sender, receiver, upload_file.as_string())
            print("邮件发送完毕")
            smtp.quit()
        except smtplib.SMTPException as e:
            print('error:',e) #打印错误


    
    def get_type(self):
        self.user_agent_list()
        type_dict = {}
        type_dict_number = 0
        
        url = 'http://api.aixdzs.com/sort/lv2'
        for sort in self.get_requests(url)['male']:
            type_dict_number += 1
            major = sort['major']
            type_dict[type_dict_number] = major
        print(type_dict)
        
        


    

    


                
