"""
更新时间：2021年2月15日
"""

from API import *
Downloader = API.Download()

intro = """爱下电子书爬虫
网站地址:https://m.aixdzs.com/
输入序号
d | +bookid下载单本小说
t | +分类号批量下载分类小说
h | 获取使用程序帮助
q | 退出运行的程序

"""

tpye_intro = """1: '玄幻', 2: '奇幻', 3: '武侠', 4: '仙侠', 5: '都市',
6: '职场', 7: '历史', 8: '军事', 9: '游戏', 10: '竞技', 
11: '科幻', 12: '灵异', 13: '同人', 14: '轻小说'"""


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
    save = False
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
        # elif inputs[0].startswith('t'):
            # shell_get_type(inputs)
        else:
            pass
        if loop is False:
            break
        inputs = re.split('\\s+', get('>').strip())
        

shell()


