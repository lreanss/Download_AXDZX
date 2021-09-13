import random
import requests
import sys, json
import re, time, os
import yaml
from ebooklib import epub
from .config_file import *
from rich.progress import track
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, as_completed
from time import sleep

new_file_settings_json()

settings = read_settings_info()
headers = settings['headers'] 
USER_AGENT_LIST = random.choice(settings['info_msg']['USER_AGENT_LIST'])

class Download():

    headers['User-Agent'] = USER_AGENT_LIST
    def __init__(self):
        self.bookid = ''
        self.bookName = ""
        self.novel_intro = ""
        self.bookName = ""
        self.charCount = ""
        self.Pool = settings['info_msg']['Thread_Pool']
        self.lastUpdateTime = ""
        self.authorName = ""
        self.path_config = os.path.join("config", self.bookName)
        self.path_novel = os.path.join("novel", self.bookName)
        self.headers = headers
        
 


    def get_requests(self, api):
        """get.requests(url, headers)"""
        """api ([str]): [api_url]    """
        return requests.get(url=api, headers=self.headers).json()

    def os_mkdir(self, path_):
        if not os.path.exists(path_):
            os.mkdir(path_)

    def intro_info(self):
        """打印小说信息"""
        novel_intros = ''
        novel_intros += '书名:{}\n作者:{}\n'.format(self.bookName, self.authorName)
        novel_intros += '状态:{}\n字数:{}\n'.format(self.isFinish, self.charCount)
        novel_intros += '更新:{}\n标签:{}\n'.format(
            self.lastUpdateTime_chap, self.novel_tag)
        novel_intros += '最后更新章节:{}\n'.format(self.lastUpdateTime)
        novel_intros += '简介信息\n{}'.format(self.novel_intro)
        
        """保存小说信息到配置文件"""
        with open(os.path.join("config", self.bookName, "0.txt"), 'w') as fb:
            fb.write(f"\n简介信息:\n{novel_intros}\n")

        return novel_intros

    def get_bookid(self, bookid):
        self.bookid = bookid
        novel_api = f'https://api.aixdzs.com/book/{self.bookid}'  # 小说信息接口
        novel_contents_api = f'http://api.aixdzs.com/content/{self.bookid}?view=chapter'  # 小说目录接口
        
        # print(self.get_requests(novel_api))
        """将接口获取到的小说信息存储在变量中"""
        self.bookName = self.get_requests(novel_api)['title']
        self.authorName = self.get_requests(novel_api)['author']
        self.isFinish = self.get_requests(novel_api)['zt']
        self.cover = self.get_requests(novel_api)['cover']
        self.charCount = self.get_requests(novel_api)['wordCount']
        self.lastUpdateTime_chap = self.get_requests(novel_api)['lastChapter']
        self.novel_tag = self.get_requests(novel_api)['cat']
        self.lastUpdateTime = self.get_requests(novel_api)['updated']  # 最后更新章节
        for novel_intro in self.get_requests(novel_api)['longIntro'].split("\n"):
            novel_intro = re.sub(r'^\s*', "\n", novel_intro)
            if re.search(r'\S', novel_intro) != None:
                self.novel_intro += novel_intro
        """检查 novel config文件夹是否存在主目录"""
        self.os_mkdir("novel")
        self.os_mkdir("config")
        
        """检查config文件夹里是否存在对应小说配置文件"""
        if not os.path.isdir(os.path.join("config", self.bookName)):
            os.makedirs(os.path.join("config", self.bookName))
        print(self.intro_info())
        """通过目录接口获取小说章节ID"""
        reps = requests.get(novel_contents_api, headers=self.headers).json()
        self.chapters_id_list = []
        for chapters in reps['mixToc']['chapters']:
            self.chapters_id_list.append(chapters['link'])  # 将小说章节ID存储到列表中

    def filedir(self):
        """获取当前文件夹中的文件名称列表"""
        meragefiledir = os.path.join("config", self.bookName)
        filenames = os.listdir(meragefiledir)  # 获取文本名
        filenames.sort(key=lambda x: int(x.split('.')[0]))  # 按照数字顺序排序文本
        file = open(os.path.join("novel", f'{self.bookName}.txt'), 'a')

        """遍历文件名"""
        for filename in filenames:
            filepath = os.path.join(meragefiledir, filename)  # 合并文本所在的路径
            """遍历单个文件，读取行数"""
            for line in open(filepath):
                file.writelines(line)
            file.write('\n')
        file.close()

    def os_meragefiledir(self):
        """路径：\config\bookname"""
        meragefiledir = os.path.join("config", self.bookName)
        """获取当前文件夹中的文件名称列表"""
        self.filenames = os.listdir(meragefiledir)
        return self.filenames

    def download(self, chapterid, len_number):
        """
        下载小说标题和正文
        chapterid ([str]): [章节ID]
        len_number ([int]): [章节ID顺序号]
        """
        chapter_api = f'http://api.aixdzs.com/chapter/{chapterid}'
        chapters = self.get_requests(chapter_api)
        self.title = chapters['chapter']['title']  # 小说标题
        body = chapters['chapter']['body']  # 小说正文
        title_body = f"\n\n\n{self.title}\n\n{body}"  # 标题加正文
        # print('正在下载: {}'.format(self.title))
        sys.stdout.write('\n{}/{}\t{}'.format(
                int(len_number) -1, len(self.chapters_id_list), self.title))
        sys.stdout.flush()
        """标题和正文信息存储到number.txt并保存\config\bookName中"""
        with open(os.path.join("config", self.bookName, f"{len_number}.txt"), 'a', newline='') as fb:
            fb.write(title_body)
        sleep(0.1)
        return '{}下载成功'.format(self.title)

    def get_type(self):
        self.type_dict = {}
        type_dict_number = 0
        url = 'http://api.aixdzs.com/sort/lv2'
        for sort in self.get_requests(url)['male']:
            type_dict_number += 1
            major = sort['major']
            self.type_dict[type_dict_number] = major
        return self.type_dict
        
    def search_book(self, bookname, Epub):
        """bookname     小说书名"""
        search_api = f'http://api.aixdzs.com/book/search?query={bookname}'
        for search_books_data in self.get_requests(search_api)['books']:
            bookid = search_books_data['_id']
        if Epub:
            self.get_bookid(bookid)
            self.ThreadPool()
        else:
            self.download2epub(bookid)

    def download_tags(self, dict_number, Epub):
        dict_data, tag_id_list, number = self.get_type(), [], 1
        for i in range(10000):
            number += 20
            print("开始下载", dict_data[dict_number], "分类")
            url = "http://api.aixdzs.com/book-sort?gender={}&type=hot&major={}&minor=&start={}&limit=20".format(
                  dict_number, dict_data[dict_number], number)
            if self.get_requests(url)['books']:
                for data in self.get_requests(url)['books']:
                    tag_id = data['_id']
                    start = time.time()
                    if Epub:
                        self.get_bookid(tag_id)
                        self.ThreadPool()
                    else:
                        self.download2epub(tag_id)
                    end = time.time()
                    print(f'下载耗时:{round(end - start, 2)} 秒')

            else:
                print('此分类小说已经下载完毕'); break
                
    def ThreadPool(self):
        self.os_meragefiledir()
        with ThreadPoolExecutor(max_workers=self.Pool) as t:
            obj_list = []
            for url in track(self.chapters_id_list):
                """url          小说完整序号"""
                """len_number   小说单章号码"""
                """filenames    小说单章名字"""
                len_number = url.split('/')[1]
                filenames = self.os_meragefiledir()
                """跳过已经下载的章节"""
                # print("开始检查本地缓存文件")
                if len_number in ''.join(filenames):
                    # print(len_number, '已经下载过')
                    continue
                else:
                    
                    obj = t.submit(self.download, url, len_number)
                    
                    obj_list.append(obj)
            for future in as_completed(obj_list):
                data = future.result()

        with open(os.path.join("novel", self.bookName + '.txt'), 'w') as f:
            self.filedir()
            print(f'\n小说 {self.bookName} 下载完成')
            

    def writeEpubPoint(self,downloaded_list):
        with open("./epub/" + self.bookName +'/' + self.bookName + ".yaml", "w", encoding="utf-8") as yaml_file:
            yaml.dump(downloaded_list, yaml_file, allow_unicode=True)
            
            
    def readEpubPoint(self):
        downloadedList = []
        if os.path.exists("./epub/" + self.bookName +'/' + self.bookName + ".yaml"):
            with open("./epub/" + self.bookName +'/' + self.bookName + ".yaml", "r", encoding="utf-8") as yaml_file:
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

        print(self.bookName)
        # if len(downloadedList) == 0:
        #     coverimg = requests.get(f"http://img22.aixdzs.com/{self.cover}", self.headers)
        #     if not os.path.exists('.//JPG//' + self.bookName + '.jpg'):
        #         with open(os.path.join('JPG', self.bookName + '.jpg'),'wb') as img:
        #             img.write(coverimg.content)

        book = epub.EpubBook()
        book.set_identifier(self.bookid)
        book.set_title(self.bookName)
        book.set_language('zh-CN')
        book.add_author(self.authorName)
        # book.set_cover(self.bookName + '.png', open('.//JPG//' + self.bookName + '.jpg','rb').read())

        # intro chapter
        ic = epub.EpubHtml(title='简介', file_name='intro.xhtml', lang='zh-CN')
        ic.content = '<html><head></head><body><h1>简介</h1><p>' + self.novel_intro + '</p>' + '<p>系统标签：' + self.novel_tag +'</p></body></html>'
        book.add_item(ic)

        default_css = epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css",
                                    content=default_style)
        book.add_item(default_css)
        # else:
        #     book = epub.read_epub('./epub/' + self.bookName + '/' + self.bookName + '.epub')
        #     default_css = epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css",
        #                                 content=default_style)

        x = 0
        for chapterid in self.chapters_id_list:
            
            # 断点下载
            if chapterid in downloadedList:
                continue
            chapters = self.get_requests(f'http://api.aixdzs.com/chapter/{chapterid}')
            
            c1 = ''
            chapter_title = chapters['chapter']['title']
            print("{}: {}".format(self.bookName, chapter_title))
            text = chapters['chapter']['body']  # 获取正文
            text_list = text.split('\n')
            for t in text_list:
                if chapter_title in t:
                    # 在正文中移除标题
                    continue
                if '[img' in t[:5]:
                    continue
                t = t.strip()
                c1 += '<p>' + t + '</p>'
            C[x] = epub.EpubHtml(title=chapter_title, file_name='chapter_' + chapterid +'.xhtml',lang = 'zh-CN',uid='chapter_' + chapterid)
            # c2 = self.download_insert_pict(book,text = text, chapterid=chapterid)
            C[x].content = '<h1>' + chapter_title + '</h1>' + c1
            C[x].add_item(default_css)
            # print("\t\t",j[-1],':已完成下载')
            downloadedList.append(chapterid)
            x += 1

        else:
            print("全本小说已经下载完成")
        u = []
        if C[0] is None:
            return 1
        for c in C:
            if c is None:
                break
            book.add_item(c)
            u.append(c)
        if ic is None:
            c_f = tuple(u)
            book.toc.extend(c_f)
            book.spine.extend(u)
            book.items.remove(book.get_item_with_id('ncx'))
            book.items.remove(book.get_item_with_id('nav'))
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())
            epub.write_epub('./epub/' + self.bookName + '/' + self.bookName + '.epub', book, {})
            #print(downloadedList)
            self.writeEpubPoint(downloadedList)
        else:
            c_f = tuple([ic] + u)
            
            book.toc = c_f
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())
            style = '''
            body {
                font-family: Auto;
            }
            h2 {
                 text-align: left;
                 text-transform: uppercase;
                 font-weight: 200;     
            }
            ol {
                    list-style-type: none;
            }
            ol > li:first-child {
                    margin-top: 0.3em;
            }
            nav[epub|type~='toc'] > ol > li > ol  {
                list-style-type:square;
            }
            nav[epub|type~='toc'] > ol > li > ol > li {
                    margin-top: 0.3em;
            }
            '''
            nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
            book.add_item(nav_css)
            book.spine = ['nav',ic]
            book.spine.extend(u)
            epub.write_epub('./epub/' + self.bookName + '/' + self.bookName + '.epub', book, {})
            self.writeEpubPoint(downloadedList)
            