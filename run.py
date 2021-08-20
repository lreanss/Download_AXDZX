import time
import os
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, as_completed
from time import sleep
from API import *
from API.headers import *
Downloader = API.Download()


intro = intro_dict
tpye_intro = tpye_intro_dict


def ThreadPool(self):  # 定义线程
    with ThreadPoolExecutor(max_workers=6) as t:
        obj_list = []
        for _url_ in self.chapters_id_list:
            obj = t.submit(self.download, _url_)
            obj_list.append(obj)
        for future in as_completed(obj_list):
            data = future.result()
    print('全部下载完成！！！')
        
def get_bookid(inputs):
    if len(inputs) >= 2:
        
        start = time.time()
        url = 'http://api.aixdzs.com/content/{}?view=chapter'.format(inputs[1])
        Downloader.get_requests(url)
        Downloader.download_book()
        end = time.time()
        print(f'下载耗时:{round(end - start, 2)} 秒')
        
        
def get(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default



def shell_book(inputs):
    if len(inputs) >= 2:
        bookid = inputs[1]
    Downloader.get_bookid(bookid)
    start = time.time()
    Downloader.download_book()
    end = time.time()
    print(f'下载耗时:{round(end - start, 2)} 秒')



def shell_list_class(inputs):
    if len(inputs) >= 2:
        dict_number = inputs[1]
        Downloader.get_book_list(dict_number)
    else:
        print(tpye_intro)
    
            


def shell():
    loop = True
    print(intro)
    if len(sys.argv) > 1:
        inputs = sys.argv[1:]
    else:
        inputs = re.split('\\s+', get('>').strip())
    while True:
        if inputs[0].startswith('q'):
            print("已退出程序");sys.exit()
        elif inputs[0].startswith('h'):
            print(intro, tpye_intro)
        elif inputs[0].startswith('t'):
            shell_list_class(inputs)
        elif inputs[0].startswith('d'):
            shell_book(inputs)
        else:
            pass
        if loop is False:
            break
        inputs = re.split('\\s+', get('>').strip())
        

shell()


