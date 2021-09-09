import json
import random
import requests
import time, os
from .headers import *
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, as_completed
from time import sleep


class Download():
    headers['User-Agent'] = random.choice(USER_AGENT_LIST)
    
    def __init__(self):
        self.bookid = ''
        self.bookName = ""
        self.main_path = ""
        self.bookName = ""
        self.charCount = ""
        self.lastUpdateTime = ""
        self.authorName = ""
        self.path_config = os.path.join("config", self.bookName)
        self.path_novel = os.path.join("novel", self.bookName)
        self.headers = headers
        
        

    # def user_agent_list(self):
    #     self.headers['User-Agent'] = random.choice(self.USER_AGENT_LIST)
    #     return self.headers
    
    
    def get_requests(self, api):
        """get.requests(url, headers)"""
        """api ([str]): [api_url]    """
        return requests.get(url=api, headers=self.headers).json()

    def os_mkdir(self, path_):
        if not os.path.exists(path_):
            os.mkdir(path_)

    def intro_info(self):
        """打印小说信息"""
        novel_intros = ''
        novel_intros += '书名:{}\n作者:{}\n'.format(self.bookName, self.authorName)
        novel_intros += '状态:{}\n字数:{}\n'.format(self.isFinish, self.charCount)
        novel_intros += '更新:{}\n标签:{}\n'.format(
            self.lastUpdateTime_chap, self.novel_tag)
        novel_intros += '最后更新章节:{}\n'.format(self.lastUpdateTime)
        novel_intros += '简介信息\n{}'.format(self.novel_intro)
        
        """保存小说信息到配置文件"""
        with open(os.path.join("config", self.bookName, "0.txt"), 'w') as fb:
            fb.write(f"\n简介信息:\n{novel_intros}\n")

        return novel_intros

    def get_bookid(self, bookid):
        self.bookid = bookid
        novel_api = f'https://api.aixdzs.com/book/{self.bookid}'  # 小说信息接口
        novel_contents_api = f'http://api.aixdzs.com/content/{self.bookid}?view=chapter'  # 小说目录接口
        
        """将接口获取到的小说信息存储在变量中"""
        self.bookName = self.get_requests(novel_api)['title']
        self.authorName = self.get_requests(novel_api)['author']
        self.isFinish = self.get_requests(novel_api)['zt']
        self.charCount = self.get_requests(novel_api)['wordCount']
        self.lastUpdateTime_chap = self.get_requests(novel_api)['lastChapter']
        self.novel_tag = self.get_requests(novel_api)['cat']
        self.lastUpdateTime = self.get_requests(novel_api)['updated']  # 最后更新章节
        self.novel_intro = self.get_requests(novel_api)['longIntro']  # 简介
        
        """检查 novel config文件夹是否存在主目录"""
        self.os_mkdir("novel")
        self.os_mkdir("config")
        
        """检查config文件夹里是否存在对应小说配置文件"""
        if not os.path.isdir(os.path.join("config", self.bookName)):
            os.makedirs(os.path.join("config", self.bookName))
        print(self.intro_info())
        """通过目录接口获取小说章节ID"""
        reps = requests.get(novel_contents_api, headers=self.headers).json()
        self.chapters_id_list = []
        for chapters in reps['mixToc']['chapters']:
            self.chapters_id_list.append(chapters['link'])  # 将小说章节ID存储到列表中

    def filedir(self):
        """获取当前文件夹中的文件名称列表"""
        meragefiledir = os.path.join("config", self.bookName)
        filenames = os.listdir(meragefiledir)  # 获取文本名
        filenames.sort(key=lambda x: int(x.split('.')[0]))  # 按照数字顺序排序文本
        file = open(os.path.join("novel", f'{self.bookName}.txt'), 'a')

        """遍历文件名"""
        for filename in filenames:
            filepath = os.path.join(meragefiledir, filename)  # 合并文本所在的路径
            """遍历单个文件，读取行数"""
            for line in open(filepath):
                file.writelines(line)
            file.write('\n')
        file.close()

    def os_meragefiledir(self):
        """路径：\config\bookname"""
        meragefiledir = os.path.join("config", self.bookName)
        """获取当前文件夹中的文件名称列表"""
        self.filenames = os.listdir(meragefiledir)
        return self.filenames

    def download(self, chapterid, len_number):
        """
        下载小说标题和正文
        chapterid ([str]): [章节ID]
        len_number ([int]): [章节ID顺序号]
        """
        chapter_api = f'http://api.aixdzs.com/chapter/{chapterid}'
        chapters = self.get_requests(chapter_api)
        self.title = chapters['chapter']['title']  # 小说标题
        body = chapters['chapter']['body']  # 小说正文
        title_body = f"\n\n\n{self.title}\n\n{body}"  # 标题加正文
        print('正在下载: {}'.format(self.title))
        
        """标题和正文信息存储到number.txt并保存\config\bookName中"""
        with open(os.path.join("config", self.bookName, f"{len_number}.txt"), 'a', newline='') as fb:
            fb.write(title_body)
        sleep(2)
        return '{}下载成功'.format(self.title)


    def ThreadPool(self):
        self.os_meragefiledir()
        with ThreadPoolExecutor(max_workers=6) as t:
            obj_list = []
            for url in self.chapters_id_list:
                """url          小说完整序号"""
                """len_number   小说单章号码"""
                """filenames    小说单章名字"""
                len_number = url.split('/')[1]
                filenames = self.os_meragefiledir()

                """跳过已经下载的章节"""
                if len_number in ''.join(filenames):
                    print(len_number, '已经下载过')
                    continue
                else:
                    obj = t.submit(self.download, url, len_number)
                    obj_list.append(obj)
            for future in as_completed(obj_list):
                data = future.result()

        with open(os.path.join("novel", self.bookName + '.txt'), 'w') as f:
            self.filedir()
            print(self.bookName, '下载完成')

    def get_type(self):
        self.type_dict = {}
        type_dict_number = 0
        url = 'http://api.aixdzs.com/sort/lv2'
        for sort in self.get_requests(url)['male']:
            type_dict_number += 1
            major = sort['major']
            self.type_dict[type_dict_number] = major
        return self.type_dict
        
    def search_book(self, bookname):
        """bookname     小说书名"""
        search_api = f'http://api.aixdzs.com/book/search?query={bookname}'
        for search_books_data in self.get_requests(search_api)['books']:
            bookid = search_books_data['_id']
        self.get_bookid(bookid)
        self.ThreadPool()
        

    def get_book_list(self, dict_number):
        number, _dict_ = 1, self.get_type()
        tag_id_list = []
        for i in range(10000):
            number += 20
            url = "http://api.aixdzs.com/book-sort?gender=6&type=hot&major={}&minor=&start={}&limit=20".format(
                  _dict_[dict_number], number)
            if self.get_requests(url)['books']:
                for data in self.get_requests(url)['books']:
                    tag_id = data['_id']
                    start = time.time()
                    self.get_bookid(tag_id)
                    self.ThreadPool()
                    end = time.time()
                    print(f'下载耗时:{round(end - start, 2)} 秒')

            else:
                print('此分类小说已经下载完毕'); break