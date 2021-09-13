import json
import random
import requests
import sys
import re, time, os
import yaml
from ebooklib import epub
from rich.progress import track
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, as_completed
from time import sleep


class Download():

    def __init__(self):
        self.bookid = ''
        self.bookName = ""
        self.novel_intro = ""
        self.bookName = ""
        self.charCount = ""
        self.lastUpdateTime = ""
        self.authorName = ""
        self.path_config = os.path.join("config", self.bookName)
        self.path_novel = os.path.join("novel", self.bookName)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
        
 


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
        
        print(self.get_requests(novel_api))
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
        self.download2epub()
   
        
    def writeEpubPoint(self,downloaded_list):
        with open("./epub/" + self.bookName +'/' + self.bookName + ".yaml", "w", encoding="utf-8") as yaml_file:
            yaml.dump(downloaded_list, yaml_file, allow_unicode=True)
    def readEpubPoint(self):
        downloadedList = []
        if os.path.exists("./epub/" + self.bookName +'/' + self.bookName + ".yaml"):
            with open("./epub/" + self.bookName +'/' + self.bookName + ".yaml", "r", encoding="utf-8") as yaml_file:
                downloadedList = yaml.load(yaml_file.read())
        return downloadedList


    def download2epub(self):
        # self.get_bookid()
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
            # time.sleep(0.1)
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
            
if __name__ == '__main__':
    Download = Download()
    Download.get_bookid('38804')