import json
import os
from .ReadWriteFile import *


class SettingConfig():
    path = None
    config_path = None
    
    def __init__(self):
        self.path = os.getcwd()
        self.config_path = os.path.join(self.path, 'settings.json')
        
    def WriteSettings(self, info):
        """更新settings.json文件"""
        file = WRITE(self.config_path, 'w')
        return file.write(json.dumps(info))

    def ReadSetting(self):
        if not os.path.isfile(self.config_path):
            open(self.config_path, 'w').write("{}")
        """读取settings.json文件"""
        read_file = WRITE(self.config_path, 'r')
        return json.loads(read_file.read())

    def setup_config(self):
        Read = self.ReadSetting()
        if type(Read.get('Epub')) is not bool or Read.get('Epub') == "":
            Read['Epub'] = True

        if type(Read.get('Multithreading')) is not bool or Read.get('Multithreading') == "":
            Read['Multithreading'] = True

        if type(Read.get('Thread_Pool')) is not int or Read.get('Thread_Pool') == "":
            Read['Thread_Pool'] = 12

        if type(Read.get('agreed_to_readme')) is not str or Read.get('agreed_to_readme') == "":
            Read['agreed_to_readme'] = 'No'

        if type(Read.get('agree_terms')) is not str or Read.get('agree_terms') == "":
            Read['agree_terms'] = '是否以仔细阅读且同意LICENSE中叙述免责声明\n如果同意声明，请输入英文 \"yes\" 或者中文 \"同意\" 后按Enter建，如果不同意请关闭此程式'

        if type(Read.get('help')) is not str or Read.get('help') == "":
            Read['help'] = 'https://m.aixdzs.com/\nd | bookid\t\t\t\t\t———输入书籍序号下载单本小说\nt | tagid\t\t\t\t\t———输入分类号批量下载分类小说\n' + \
                'n | bookname\t\t\t\t\t———下载单本小说\nh | help\t\t\t\t\t———获取使用程序帮助\nq | quit\t\t\t\t\t———退出运行的程序\n' + \
                'm | method\t\t\t\t\t———切换多线程和多进程\np | pool\t\t\t\t\t———改变线程数目\nu | updata\t\t\t\t\t———下载指定文本中的bookid'

        if type(Read.get('tag')) is not dict or Read.get('tag') == "":
            Read['tag'] = {1: '玄幻', 2: '奇幻', 3: '武侠', 4: '仙侠', 5: '都市', 6: '职场', 7: '历史',
                           8: '军事', 9: '游戏', 10: '竞技', 11: '科幻', 12: '灵异', 13: '同人', 14: '轻小说'}

        if type(Read.get('USER_AGENT_LIST')) is not list or Read.get('USER_AGENT_LIST') == "":
            Read['USER_AGENT_LIST'] = [
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
                "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
                "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
            ]
        self.WriteSettings(Read)
