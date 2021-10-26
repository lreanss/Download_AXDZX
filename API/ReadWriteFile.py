import re
import time
import os

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