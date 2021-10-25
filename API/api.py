import re
import time
import os
from rich import print
from functools import partial
from rich.progress import track
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from API import API_URL, setting, getdict, Epub


class Download:
    def __init__(self):
        self.bookid = ''
        self.bookName = ""
        self.epub = Epub.EpubDownload()
        self.get_ = getdict.get_dict_value
        self.Read = setting.SettingConfig().ReadSetting()
        self.pool = self.Read.get('Thread_Pool')
        self.time = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def intro_info(self):
        """打印小说信息"""
        novel_intros = ''
        novel_intros += '书名:{}\n作者:{}\n'.format(self.bookName, self.authorName)
        novel_intros += '状态:{}\n字数:{}\n'.format(self.isFinish, self.charCount)
        novel_intros += '更新:{}\n标签:{}\n'.format(
            self.lastUpdateTime_chap, self.novel_tag)
        novel_intros += '最后更新章节:{}\n'.format(self.lastUpdateTime)
        write_intros = novel_intros
        write_intros += '简介信息\n{}'.format(self.novel_intro)
        """保存小说信息到配置文件"""
        path = os.path.join("config", self.bookName, "0.txt")
        API_URL.WRITE(path, 'w', f"\n简介信息:\n{write_intros}\n")

        return novel_intros

    def get_bookid(self, bookid):
        self.bookid = bookid
        novel_info = getdict.GET(API_URL.BOOK_INFO_API.format(self.bookid))
        """将接口获取到的小说信息存储在变量中"""
        self.bookName, self.authorName, self.isFinish, self.cover, self.charCount = (
            API_URL.strip(self.get_(novel_info, 'title')), self.get_(
                novel_info, 'author'), self.get_(novel_info, 'zt'),
            self.get_(novel_info,  'cover'),  self.get_(novel_info, 'wordCount'))

        self.lastUpdateTime_chap, self.novel_tag, self.lastUpdateTime = (
            self.get_(novel_info, 'lastChapter'), self.get_(novel_info, 'cat'),
            self.get_(novel_info, 'updated'))
        self.novel_intro = ''.join([re.sub(r'^\s*', "\n", novel_intro)
                                    for novel_intro in self.get_(novel_info, 'longIntro').split("\n") if re.search(r'\S', novel_intro) != None])

        """检查 novel config文件夹是否存在主目录"""
        API_URL.OS_MKDIR("novel")
        API_URL.OS_MKDIR("config")

        """检查config文件夹里是否存在对应小说配置文件"""
        if not os.path.isdir(API_URL.CONFIG_PATH(self.bookName)):
            os.makedirs(API_URL.CONFIG_PATH(self.bookName))
        print(self.intro_info())

    def filedir(self):
        """获取当前文件夹中的文件名称列表"""
        meragefiledir = os.path.join("config", self.bookName)
        filenames = os.listdir(meragefiledir)  # 获取文本名
        filenames.sort(key=lambda x: int(x.split('.')[0]))  # 按照数字顺序排序文本
        file = API_URL.WRITE(API_URL.SAVE_BOOK_PATH(self.bookName), 'a')

        """遍历文件名"""
        for filename in filenames:
            filepath = os.path.join(meragefiledir, filename)  # 合并文本所在的路径
            """遍历单个文件，读取行数"""
            try:
                for line in open(filepath, encoding='UTF-8'):
                    file.writelines(line)
            except (UnicodeEncodeError, UnicodeDecodeError):
                for line in open(filepath, encoding='gbk'):
                    file.writelines(line)
            file.write('\n')
        file.close()

    def os_meragefiledir(self):
        """路径：\config\bookname"""
        meragefiledir = API_URL.CONFIG_PATH(self.bookName)
        """获取当前文件夹中的文件名称列表"""
        self.filenames = os.listdir(meragefiledir)
        return self.filenames

    def download(self, chapterid, len_number):
        """
        下载小说标题和正文
        chapterid ([str]): [章节ID]
        len_number ([int]): [章节ID顺序号]
        """
        chapters = getdict.GET(API_URL.CHAPTER_API.format(chapterid))
        self.title, body = (
            self.get_(chapters, 'chapter.title'),
            self.get_(chapters, 'chapter.body')
        )
        title_body = f"\n\n\n{self.title}\n\n{body}"  # 标题加正文
        """标题和正文信息存储到number.txt并保存\config\bookName中"""
        API_URL.WRITE(API_URL.CONFIG_TEXT_PATH(
            self.bookName, len_number), 'w', title_body)
        time.sleep(0.1)
        return '{}下载成功'.format(self.title)

    def get_type(self):
        self.type_dict = {}
        for number, sort in enumerate(getdict.GET(API_URL.GET_TYPE_INFO)['male']):
            print(sort)
            number += 1
            major = self.get_(sort, 'major')
            self.type_dict[number] = major

        return self.type_dict

    def search_book(self, bookname, Epub):
        """bookname     小说书名"""
        for data in getdict.GET(API_URL.SEARCH_API.format(bookname))['books']:
            bookid = self.get_(data, '_id')
        if Epub:
            self.get_bookid(bookid)
            self.ThreadPool()
        else:
            self.epub.download2epub(bookid)

    def ranking(self, ranking_num):
        bookid_list = []
        Response = getdict.GET('http://api.aixdzs.com/ranking/{}'.format(ranking_num))
        for data in self.get_(Response, 'ranking').get('books'):
            for key, Value in data.items():
                if key == 'title':
                    print('\n\n{}:\t\t\t{}'.format(key, Value))
                    continue
                book_info = '{}:\t\t\t{}'.format(key, Value) if len(
                    key) <= 6 else '{}:\t\t{}'.format(key, Value)
                print(book_info)
            bookid_list.append(self.get_(data, '_id'))
        for BOOKID in bookid_list:
            self.get_bookid(BOOKID)
            self.ThreadPool()
            # bookid, bookName, authorname, intro, cover, tag, followerCount, zt, updated, lastchapter = (
            #         self.get_(data, '_id'), self.get_(data, 'title'), self.get_(data, 'author'), 
            #         self.get_(data, 'shortIntro'), self.get_(data, 'cover'),  self.get_(data, 'cat'), 
            #         self.get_(data, 'followerCount'),  self.get_(data, 'zt'), self.get_(data, 'updated'), 
            #         self.get_(data, 'lastchapter'))

    def download_tags(self, dict_number):
        TagName, page, BookidList = (
            self.Read.get('tag').get(dict_number), 1, [])
        print(f"开始下载 {TagName}分类")
        while True:
            page += 20
            Response = getdict.GET(
                API_URL.TAG_API.format(dict_number, TagName, page))
            if not Response['books']:
                print(BookidList)
                return BookidList
            for data in Response['books']:
                BOOKID = data['_id']
                BookidList.append(BOOKID)
                print("第{}本\n".format(len(BookidList)))
                if self.Read.get('Epub'):
                    self.get_bookid(BOOKID)
                    self.ThreadPool()
                else:
                    self.epub.download2epub(BOOKID)
                # print("第{}本\t书名:{}序号:{}".format(len(BookidList), data['title'],BOOKID))
                # API_URL.WRITE(f"{TagName}分类.txt{self.time}", 'w')
                API_URL.WRITE(f"{TagName}分类.txt{self.time}",
                              'a', f'{BOOKID}\n')

    def ThreadPool(self):
        if self.Read.get('Multithreading'):
            print('开始下载[yellow][多线程]')
            # print('多线程', self.Read.get('Multithreading'))
            executor = ThreadPoolExecutor(max_workers=self.pool)
        elif not self.Read.get('Multithreading'):
            print('开始下载[yellow][多进程]')
            # print('多进程', self.Read.get('Multithreading'))
            executor = ProcessPoolExecutor(max_workers=self.pool)
        task_list = []
        for url in self.continue_chap():
            len_number = url.split('/')[1]
            task = partial(self.download, url, len_number)
            task_list.append(executor.submit(task))
        if task_list:
            [task.result() for task in track(task_list)]
        else:
            print('\n\n提示：[red]文本已是最新内容！')
        # 清除旧文本内容，合并缓存章节并写入
        try:
            open(API_URL.SAVE_BOOK_PATH(self.bookName), 'w')
            self.filedir()
            print(f'\n小说 {self.bookName} 下载完成')
        except FileNotFoundError as e:
            API_URL.WRITE('下载失败.txt', 'a', self.bookName)
            print(e, '文件名不规范，无法创建！')

    def continue_chap(self):
        """通过目录接口获取小说章节ID"""
        Response = getdict.GET(API_URL.BOOK_CATALOGUE.format(self.bookid))
        self.chapters_id_list = [chapters["link"] for chapters in self.get_(
            Response, 'mixToc.chapters')]  # 将小说章节ID存储到列表中
        _list_ = []
        for url in self.chapters_id_list:
            len_number = url.split('/')[1]
            filenames = self.os_meragefiledir()
            if len_number in ''.join(filenames):  # 跳过已经下载的章节
                continue
            _list_.append(url)
        return _list_
