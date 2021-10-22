import re
import time
import os
import yaml
from rich import print
from ebooklib import epub
from functools import partial
from rich.progress import track
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from API import API_URL, config_file, getdict


class Download():
    def __init__(self):
        self.bookid = ''
        self.bookName = ""
        self.get_ = getdict.get_dict_value
        self.Read = config_file.SettingConfig().ReadSetting()
        self.pool = self.Read.get('Thread_Pool')
        self.Multithreading = self.Read.get('Multithreading')
        self.time = time.strftime('%Y-%m-%d',time.localtime(time.time()))



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
            self.get_(novel_info, 'title'), self.get_(
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
        API_URL.WRITE(API_URL.CONFIG_TEXT_PATH(self.bookName, len_number), 'w', title_body)
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
            self.download2epub(bookid)

    def download_tags(self, dict_number, Epub):
        TagName, page, BookidList = (self.Read.get('tag').get(dict_number), 1, [])
        print(f"开始下载 {TagName}分类")
        while True:
            page += 20
            Response = getdict.GET(API_URL.TAG_API.format(dict_number, TagName, page))
            if not Response['books']:
                print(BookidList)
                return BookidList
            for data in Response['books']:
                BOOKID = data['_id']
                BookidList.append(BOOKID)
                print("第{}本\n".format(len(BookidList)))
                if Epub:
                    self.get_bookid(BOOKID)
                    self.ThreadPool()
                else:
                    self.download2epub(BOOKID)
                # print("第{}本\t书名:{}序号:{}".format(len(BookidList), data['title'],BOOKID))
                # API_URL.WRITE(f"{TagName}分类.txt{self.time}", 'w')
                API_URL.WRITE(f"{TagName}分类.txt{self.time}", 'a', f'{BOOKID}\n')
                

    def ThreadPool(self):
        if not self.Multithreading:
            print('开始下载[yellow][多进程]')
            executor = ProcessPoolExecutor(max_workers=self.pool)
        else:
            print('开始下载[yellow][多线程]')
            executor = ThreadPoolExecutor(max_workers=self.pool)
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
        
        open(API_URL.SAVE_BOOK_PATH(self.bookName), 'w')
        self.filedir()
        print(f'\n小说 {self.bookName} 下载完成')

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

    def writeEpubPoint(self, downloaded_list):
        save_epub_path = os.path.join(
            "epub", self.bookName, f"{self.bookName}.yaml")
        with open(save_epub_path, "w", encoding="utf-8") as yaml_file:
            yaml.dump(downloaded_list, yaml_file, allow_unicode=True)

    def readEpubPoint(self):
        downloadedList = []
        save_epub_path = os.path.join(
            "epub", self.bookName, f"{self.bookName}.yaml")
        if os.path.exists(save_epub_path):
            with open(save_epub_path, "r", encoding="utf-8") as yaml_file:
                downloadedList = yaml.load(yaml_file.read())
        return downloadedList

    def download2epub(self, bookid):
        self.get_bookid(bookid)
        default_style = '''
            body {font-size:100%;}
            p{
                font-family: Auto;
                text-indent: 2em;
            }
            h1{
                font-style: normal;
                font-size: 20px;
                font-family: Auto;
            }      
            '''
        ic = None
        # TODO: 创建一个EPUB文件
        if not os.path.exists('./epub'):
            os.mkdir('./epub')
        if not os.path.exists('./epub/' + self.bookName):
            os.mkdir('./epub/' + self.bookName)
        downloadedList = self.readEpubPoint()
        C = [None] * len(self.chapters_id_list)
        book = epub.EpubBook()
        book.set_identifier(self.bookid)
        book.set_title(self.bookName)
        book.set_language('zh-CN')
        book.add_author(self.authorName)
        ic = epub.EpubHtml(title='简介', file_name='intro.xhtml', lang='zh-CN')
        ic.content = '<html><head></head><body><h1>简介</h1><p>' + self.novel_intro + \
            '</p>' + '<p>系统标签：' + self.novel_tag + '</p></body></html>'
        book.add_item(ic)

        default_css = epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css",
                                    content=default_style)
        book.add_item(default_css)
        x = 0
        for chapterid in track(self.chapters_id_list):
            """断点下载，跳过已经存在本地的章节id"""
            if chapterid in downloadedList:
                continue
            chapters = getdict.GET(
                f'http://api.aixdzs.com/chapter/{chapterid}')

            c1 = ''
            chapter_title = self.get_(chapters, 'chapter.title')
            print("{}: {}".format(self.bookName, chapter_title))
            text = chapters['chapter']['body']  # 获取正文
            text_list = text.split('\n')
            for t in text_list:
                if chapter_title in t:  # 在正文中移除标题
                    continue
                if '[img' in t[:5]:
                    continue
                t = t.strip()
                c1 += '<p>' + t + '</p>'
            C[x] = epub.EpubHtml(title=chapter_title, file_name='chapter_' +
                                 chapterid + '.xhtml', lang='zh-CN', uid='chapter_' + chapterid)
            # c2 = self.download_insert_pict(book,text = text, chapterid=chapterid)
            C[x].content = '<h1>' + chapter_title + '</h1>' + c1
            C[x].add_item(default_css)
            downloadedList.append(chapterid)
            x += 1

        else:
            print("全本小说已经下载完成")
