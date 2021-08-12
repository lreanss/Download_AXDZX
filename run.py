from API import *
Downloader = API.Download()


intro = """bookid可在  https://m.aixdzs.com/  获取
d | 加上bookid下载单本小说
c | 批量爱下电子书下载分类小说
\n"""
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
    if len(inputs) >= 1:
        Downloader.get_book_list()
        

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
            print(intro)
        elif inputs[0].startswith('c'):
            shell_list_class(inputs)
        elif inputs[0].startswith('d'):
            shell_book(inputs)
        else:
            pass
        if loop is False:
            break
        inputs = re.split('\\s+', get('>').strip())
        

shell()


