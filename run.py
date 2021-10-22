from API import *



def get(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default
        
def shell_book(inputs):
    """通过小说ID下载单本小说"""
    if len(inputs) >= 2:
        start = time.time()
        if Read.get('Epub'):
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
        Downloader.search_book(inputs[1], Read.get('Epub'))
        end = time.time()
        print(f'下载耗时:{round(end - start, 2)} 秒')
    else:
        print('未输入书名')
        
def shell_Multithreading(inputs):
    if Read.get('Multithreading'):
        Read['Multithreading'] = False
        Setting.WriteSettings(Read)
        print("已设置为多进程")
    else:
        Read['Multithreading'] = True
        Setting.WriteSettings(Read)
        print("已设置为多线程")
        
def shell_epub(inputs):
    """设置布尔值，默认为True"""
    if Read.get('Epub'):
        """将布尔值设置为False"""
        Read['Epub'] = False
        Setting.WriteSettings(Read)
        print("已设置为下载epub")
    else:
        """将布尔值设置为True"""
        Read['Epub'] = True
        Setting.WriteSettings(Read)
        print("已设置为下载TXT")
        
def get_pool(inputs):
    if len(inputs) >= 2:
        if inputs[1].isdigit():
            Downloader.Pool = int(inputs[1])
            Read['Thread_Pool'] = Downloader.Pool
            Setting.WriteSettings(Read)
            print("线程已设置为", Downloader.Pool)

        else:
            print("设置失败，输入信息不是数字")
    else:
        print("默认线程为", Downloader.Pool)
        
def shell_list_class(inputs):
    if len(inputs) >= 2:
        dict_number = inputs[1]
        if not Read.get('tag').get(dict_number):
            print(f"{dict_number} 标签号不存在\n", Read.get('tag'))
        else:
            Downloader.download_tags(dict_number, Read.get('Epub'))
    else:
        print(Read.get('tag'))

def shell_list(inputs):
    start = time.time()
    if len(inputs) >= 2:
        list_file_name = inputs[1] + '.txt'
    else:
        list_file_name = 'list.txt'
    try:
        list_file_input = open(list_file_name, 'r', encoding='utf-8')
    except OSError:
        print(f"{list_file_name}文件不存在")
        return
    list_lines = list_file_input.readlines()
    for line in list_lines:
        if re.match("^\\s*([0-9]{1,7}).*$", line):
            start = time.time()
            bookid = re.sub("^\\s*([0-9]{1,7}).*$\\n?", "\\1", line)
            Downloader.get_bookid(bookid)
            Downloader.ThreadPool()
            end = time.time()
            print(f'下载耗时:{round(end - start, 2)} 秒')
    end = time.time()
    print(f'下载耗时:{round(end - start, 2)} 秒')
            
def shell():
    print(Read.get('help'))
    if len(sys.argv) > 1:
        inputs = sys.argv[1:]
    else:
        inputs = re.split('\\s+', get('>').strip())
    while True:
        if inputs[0].startswith('q') or inputs[0] == '--quit':
            sys.exit("已退出程序")
        if inputs[0] == 'h' or inputs[0] == '--help':
            print(Read.get('help'))
        elif inputs[0] == 't' or inputs[0] == '--tag':
            shell_list_class(inputs)
        elif inputs[0] == 'd' or inputs[0] == '--download':
            shell_book(inputs)
        elif inputs[0] == 'n' or inputs[0] == '--name':
            shell_search_book(inputs)
        elif inputs[0] == 'o' or inputs[0] == '--all':
            shell_list(inputs)
        elif inputs[0] == 'p' or inputs[0] == '--pool':
            get_pool(inputs)
        elif inputs[0] == 'e' or inputs[0] == '--epub':
            shell_epub(inputs)
        elif inputs[0] == 'm' or inputs[0] == '--mul':
            shell_Multithreading(inputs)
        else:
            print(inputs[0], '不是有效命令')
        inputs = re.split('\\s+', get('>').strip())

if __name__ == '__main__':
    Downloader = Download()
    
    Setting = SettingConfig()
    
    Setting.setup_config()
    
    Read = Setting.ReadSetting()
    
    shell()
