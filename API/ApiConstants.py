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
        
     