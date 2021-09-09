import json
import requests
import time, os
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED,as_completed
from time import sleep

class axdzs:
    #bookid = ""
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
        self.isFinish = ""
        self.headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36"}
    
    
    # def write_json(self, info):
        
    #     with open('data.json', 'a') as fw:
    #         self.content_dict = {}
    #         self.content_dict['data'] = info
    #         file_write = fw.write(
    #             json.dumps(self.content_dict,indent=4, ensure_ascii=False)
    #         )
    #     return file_write
            

    def get_bookid(self, bookid):
        self.bookid = bookid
        novel_info = requests.get(f'https://api.aixdzs.com/book/{self.bookid}', headers=self.headers).json()
        # print(novel_info)
        self.bookName = novel_info['title']
        self.new_file()


    def new_file(self):
        if not os.path.exists("novel"):
            os.mkdir("novel")
        if not os.path.exists("config"):
            os.mkdir("config")
        # if not os.path.exists(os.path.join("config", self.bookName)):
        #     os.makedirs(os.path.join("config", self.bookName))
    
        if not os.path.isdir(os.path.join("config", self.bookName)):
            os.makedirs(os.path.join("config", self.bookName))
    
    def write_json_article(self,write_json_info):  # 将信息写入json文件
        with open(os.path.join("config", self.bookName + ".txt"), 'a', newline='') as fb:
            fb.write(str(write_json_info))


        
    def filedir(self):
        meragefiledir = os.path.join("config", self.bookName)  # 获取当前文件夹中的文件名称列表  
        filenames = os.listdir(meragefiledir)
        filenames.sort(key=lambda x:int(x.split('.')[0]))
        file = open(os.path.join("novel", f'{self.bookName}.txt'),'a')
        for filename in filenames:  #先遍历文件名
            # if filename == str(item):
            #     continue
            # else:
            filepath = os.path.join(meragefiledir, filename)
            # print(filepath)
            #遍历单个文件，读取行数  
            for line in open(filepath):  
                file.writelines(line)  
            file.write('\n')
        file.close()

    def os_meragefiledir(self):
        meragefiledir = os.path.join("config", self.bookName)  # 获取当前文件夹中的文件名称列表
        filenames = os.listdir(meragefiledir)
        return filenames
    
    def chapte(self):
        url = f'http://api.aixdzs.com/content/{self.bookid}?view=chapter'
        reps = requests.get(url, headers=self.headers).json()
        self.chapters_id_list = []
        for chapters in reps['mixToc']['chapters']:
            self.chapters_id_list.append(chapters['link'])
        # print(self.chapters_id_list)
            

    def download(self, chapterid, len_number):
        req = requests.get(f'http://api.aixdzs.com/chapter/{chapterid}' ,headers=self.headers).json()
        # print(req)
        # dict_ = {}
        self.title = req['chapter']['title']
        body = req['chapter']['body']
        print('正在下载: {}'.format(self.title))
        all = f"\n\n\n{self.title}\n\n{body}"  # 正文内容len_number
        # dict_[len_number] = {
        #     'title': self.title, 
        #     'content': body
        # }
        # print(dict_)
            
        
        # with open('data.json','r') as f:
        #     self.content_dict = {}
        #     data = json.loads(f.read())
        # self.write_json(dict_)

        with open(os.path.join("config", self.bookName,f"{len_number}.txt"), 'a', newline='') as fb:
            fb.write(all)
        sleep(2)
        return '{}下载成功'.format(self.title)
    

    def ThreadPool(self):
        len_number_list = []
        chapters_id_len_list = []
        file_bookid = []
        self.chapte()
        len_number = 0
        for merage in self.os_meragefiledir():
            merage = merage.split('.')
            file_bookid.append(merage[0])
        for chapters_id_len in range(len(self.chapters_id_list)):
            chapters_id_len_list.append(str(chapters_id_len))
        # remain_list = set(chapters_id_len_list)^set(file_bookid)
        # remain_list = list(remain_list)
        # print('remain_list', remain_list)
        # print('self.chapters_id', len(chapters_id_len_list))
        # print('file_bookid', len(file_bookid))
        # print('remain_list', len(remain_list))
        with ThreadPoolExecutor(max_workers=6) as t:
            obj_list = []
            for url in self.chapters_id_list:
                len_number += 1
                # len_number_list.append(len_number)
                obj = t.submit(self.download, url, len_number)
                obj_list.append(obj)
            for future in as_completed(obj_list):
                data = future.result()
        self.filedir()
        print(self.bookName,'下载完成')
        # for item in remain_list:
        #     print(item)
        #     self.filedir(item)
        # print(self.content_dict)
        

        
if __name__ == '__main__':
    dow = axdzs()
    bookid = input('please input bookid:')
    while not bookid:
        bookid = input('please input bookid:')
    dow.get_bookid(bookid)
    dow.ThreadPool()
