from API import *
Downloader = Download()

def shell_book(inputs):
    if len(inputs) >= 2:
        start = time.time()
        Downloader.get_bookid(inputs[1])
        Downloader.ThreadPool()
        end = time.time()
        print(f'下载耗时:{round(end - start, 2)} 秒')
    else:
        print('未输入Bookid')


def shell_search_book(inputs):
    if len(inputs) >= 2:
        start = time.time()
        Downloader.search_book(inputs[1])
        end = time.time()
        print(f'下载耗时:{round(end - start, 2)} 秒')
    else:
        print('未输入书名')

        
def shell_list_class(inputs):
    if len(inputs) >= 2:
        try:
            dict_number = int(inputs[1])
        except ValueError:
            print('输入不规范，请输入数字')
            return
            
        tag_dict = Downloader.get_type()
        if dict_number not in tag_dict:
            print(f"服务器内不存在{dict_number}这个标签号\n", tag_dict)
        else:
            Downloader.get_book_list(dict_number)
    else:
        print(Downloader.get_type())

def shell():
    loop = True
    print(intro_dict)
    if len(sys.argv) > 1:
        inputs = sys.argv[1:]
    else:
        inputs = re.split('\\s+', get('>').strip())
    while True:
        if inputs[0].startswith('q'):
            print("已退出程序")
            sys.exit()
        elif inputs[0].startswith('h'):
            print(intro_dict, Downloader.get_type())
        elif inputs[0].startswith('t'):
            shell_list_class(inputs)
        elif inputs[0].startswith('d'):
            shell_book(inputs)
        elif inputs[0].startswith('s'):
            shell_search_book(inputs)
        else:
            pass
        if loop is False:
            break
        inputs = re.split('\\s+', get('>').strip())


shell()
