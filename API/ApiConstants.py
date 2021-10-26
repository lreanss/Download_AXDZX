import os
import re
TAG_API = "http://api.aixdzs.com/book-sort?gender={}&type=hot&major={}&minor=&start={}&limit=20"
BOOK_INFO_API = 'https://api.aixdzs.com/book/{}'  # 小说信息接口
BOOK_CATALOGUE = 'http://api.aixdzs.com/content/{}?view=chapter'  # 小说目录接口
GET_TYPE_INFO = 'http://api.aixdzs.com/sort/lv2'
CHAPTER_API = 'http://api.aixdzs.com/chapter/{}'
SEARCH_API = 'http://api.aixdzs.com/book/search?query={}'


def strip(path):
    return re.sub(r'[？?\*|“<>:/]', '', str(path))
def CONFIG_PATH(bookName):
    return os.path.join("config", bookName)
def SAVE_BOOK_PATH(bookName):
    return os.path.join("novel", '{}.txt'.format(bookName))
def CONFIG_TEXT_PATH(bookName, chap_number):
    return os.path.join("config", bookName, '{}.txt'.format(chap_number))
# def save_epub_path(bookName):
#     return os.path.join("epub", bookName, f'{bookName}.yaml')

def save_epub_path(bookName):
    return os.path.join("epub", bookName, f'{bookName}.json')
def save_epub_config_path(bookName, chapid):
    return os.path.join("epub", bookName, 'text', f'{chapid}.xhtml')
def OS_MKDIR(path):
    if not os.path.exists(path):
        os.mkdir(path)
def OS_MKEDIRS(path):
    if not os.path.exists(path):
        os.makedirs(path)
def OS_MKNOD(path):
    if not os.path.exists(path):
        os.mknod(path)
def WRITE(PATH, mode, info=None):
    if info is not None:
        try:
            with open(PATH, f'{mode}', encoding='UTF-8', newline='') as file:
                file.writelines(info)
        except (UnicodeEncodeError, UnicodeDecodeError)as e:
            print(e)
            with open(PATH, f'{mode}', encoding='gbk', newline='') as file:
                file.writelines(info)
    else:
        try:
            return open(PATH, f'{mode}', encoding='UTF-8')
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            print(e)
            return open(PATH, f'{mode}', encoding='gbk')
def READ_FILE(PATH):
    try:
        with open(PATH, 'r+', encoding='UTF-8') as file:
            return file.read()
    except (UnicodeEncodeError, UnicodeDecodeError) as e:
        print(e)
        with open(PATH, 'r+', encoding='gbk') as file:
            return file.read()
        
     
