import os
TAG_API = "http://api.aixdzs.com/book-sort?gender={}&type=hot&major={}&minor=&start={}&limit=20"
BOOK_INFO_API = 'https://api.aixdzs.com/book/{}'  # 小说信息接口
BOOK_CATALOGUE = 'http://api.aixdzs.com/content/{}?view=chapter'  # 小说目录接口
GET_TYPE_INFO = 'http://api.aixdzs.com/sort/lv2'
CHAPTER_API = 'http://api.aixdzs.com/chapter/{}'
SEARCH_API = 'http://api.aixdzs.com/book/search?query={}'


def CONFIG_PATH(bookName):
    PATH = os.path.join("config", bookName)
    return PATH

def SAVE_BOOK_PATH(bookName):
    PATH = os.path.join("novel", '{}.txt'.format(bookName))
    return PATH

def CONFIG_TEXT_PATH(bookName, chap_number):
    PATH = os.path.join("config", bookName, '{}.txt'.format(chap_number))
    return PATH

def OS_MKDIR(path):
    if not os.path.exists(path):
        os.mkdir(path)
        
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
            file =  open(PATH, f'{mode}', encoding='UTF-8')
            return file
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            print(e)
            file =  open(PATH, f'{mode}', encoding='gbk')
            return file
