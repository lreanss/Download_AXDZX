from API import *
from multiprocessing import Pool, Manager

Downloader = Download()
new_file_settings_json()
settings = read_settings_info()
Epub = settings['info_msg']['Epub']

def shell_book(inputs):
    """通过小说ID下载单本小说"""
    if len(inputs) >= 2:
        start = time.time()
        if Epub:
            Downloader.get_bookid(inputs[1])
            Downloader.ThreadPool()
        else:
            Downloader.download2epub(inputs[1])
        end = time.time()
        print(f'下载耗时:{round(end - start, 2)} 秒')
    else:
        print('未输入Bookid')


def shell_search_book(inputs):
    """搜索书名下载小说"""
    if len(inputs) >= 2:
        start = time.time()
        Downloader.search_book(inputs[1], Epub)
        end = time.time()
        print(f'下载耗时:{round(end - start, 2)} 秒')
    else:
        print('未输入书名')
        
       

def get(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default
            
def get_epub(inputs):
    """设置布尔值，默认为True"""
    if len(inputs) >= 2:
        global Epub
        if inputs[1] == 'f':
            """将布尔值设置为False"""
            Epub = False
            settings['info_msg']['Epub'] = False
            write_settings_info(settings)
            print("已设置为下载epub")
        elif inputs[1] == 't':
            """将布尔值设置为True"""
            settings['info_msg']['Epub'] = True
            settings['info_msg']['Epub'] = True
            write_settings_info(settings)
            print("已设置为下载TXT")
    else:
        print("布尔值为", settings['info_msg']['Epub'])  # 打印布尔值
        
def get_pool(inputs):
    if len(inputs) >= 2:
        if inputs[1].isdigit():
            Downloader.Pool = int(inputs[1])
            settings['info_msg']['Thread_Pool'] = Downloader.Pool
            write_settings_info(settings)
            print("线程已设置为", Downloader.Pool)

        else:
            print("设置失败，输入信息不是数字")
    else:
        print("默认线程为", Downloader.Pool)
        
def shell_list_class(inputs):
    if len(inputs) >= 2:
        try:
            dict_number = int(inputs[1])
        except ValueError:
            print('输入不规范，请输入数字')
            return
        tag_dict = settings['help_msg']['tag']
        if inputs[1] not in tag_dict:
            print(f"{dict_number} 标签号不存在\n", tag_dict)
        else:
            Downloader.download_tags(dict_number, Epub)
    else:
        print(settings['help_msg']['tag'])

def shell():
    print(settings['help_msg']['help'])
    if len(sys.argv) > 1:
        inputs = sys.argv[1:]
    else:
        inputs = re.split('\\s+', get('>').strip())
    while True:
        if inputs[0].startswith('q'):
            print("已退出程序")
            sys.exit()
        elif inputs[0] == 'h':
            print(settings['help_msg']['help'])
        elif inputs[0] == 't':
            shell_list_class(inputs)
        elif inputs[0] == 'd':
            shell_book(inputs)
        elif inputs[0] == 's':
            shell_search_book(inputs)
        elif inputs[0] == 'p':
            get_pool(inputs)
        elif inputs[0] == 'e':
            get_epub(inputs)
        else:
            print(inputs[0], '不是有效命令')
        inputs = re.split('\\s+', get('>').strip())


shell()
