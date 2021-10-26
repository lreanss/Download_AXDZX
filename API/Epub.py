import re
import os
from ebooklib import epub
from rich.progress import track
from API import ApiConstants, HttpRequest, setting


class EpubDownload():
    def __init__(self):
        self.bookid = ''
        self.bookName = ''
        self.get_ = HttpRequest.get_dict_value
        self.request = HttpRequest.GET
        self.Read = setting.SettingConfig().ReadSetting()

    def get_bookid(self):
        novel_info = self.request(ApiConstants.BOOK_INFO_API.format(self.bookid))
        """将接口获取到的小说信息存储在变量中"""
        self.bookName, self.authorName, self.isFinish, self.cover, self.charCount = (
            ApiConstants.strip(self.get_(novel_info, 'title')), self.get_(
                novel_info, 'author'), self.get_(novel_info, 'zt'),
            self.get_(novel_info,  'cover'),  self.get_(novel_info, 'wordCount'))

        self.lastUpdateTime_chap, self.novel_tag, self.lastUpdateTime = (
            self.get_(novel_info, 'lastChapter'), self.get_(novel_info, 'cat'),
            self.get_(novel_info, 'updated'))
        self.novel_intro = ''.join([re.sub(r'^\s*', "\n", novel_intro)
                for novel_intro in self.get_(novel_info, 'longIntro').split("\n") if re.search(r'\S', novel_intro) != None])


    # def writeEpubPoint(self, chapid, chap_id):
    #     ApiConstants.WRITE(ApiConstants.save_epub_config_path(self.bookName, chap_id), 'a', f"{chapid}、")
                      
    def readEpubPoint(self):
        return ''.join(os.listdir(os.path.join("epub", self.bookName, 'text')))

    def download2epub(self, bookid):
        self.bookid = bookid
        self.get_bookid()
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
        Response = self.request(ApiConstants.BOOK_CATALOGUE.format(self.bookid))
        self.chapters_id_list = [chapters["link"] for chapters in self.get_(
            Response, 'mixToc.chapters')]
        ApiConstants.OS_MKDIR('epub')
        ApiConstants.OS_MKEDIRS(os.path.join('epub', self.bookName))
        ApiConstants.OS_MKEDIRS(os.path.join('epub', self.bookName, 'text'))
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
        num = 0
        x = 0
        for chapterid in track(self.chapters_id_list):
            num += 1
            """断点下载，跳过已经存在本地的章节id"""
            chap_id = chapterid.split('/')[1]
            if chap_id in self.readEpubPoint():
                continue
            chapters = self.request(ApiConstants.CHAPTER_API.format(chapterid))

            c1 = ''
            chapter_title = self.get_(chapters, 'chapter.title')
            print("{}: {}".format(self.bookName, chapter_title))
            try:
                text = self.get_(chapters, 'chapter.body')  # 获取正文
            except TypeError:
                # 意外报错重试
                text = self.get_(chapters, 'chapter.body')
            text_list = text.split('\n')
            for title in text_list:
                if chapter_title in title:  # 在正文中移除标题
                    continue
                if '[img' in title[:5]:
                    continue
                title = title.strip()
                c1 += '<p>' + title + '</p>'
                
                ApiConstants.WRITE(ApiConstants.save_epub_config_path(self.bookName, chap_id), 'w', c1)
            C[x] = epub.EpubHtml(title=chapter_title, file_name='chapter_' +
                                 chapterid + '.xhtml', lang='zh-CN', uid='chapter_' + chapterid)
            print(C[x])
            # c2 = self.download_insert_pict(book,text = text, chapterid=chapterid)
            C[x].content = '<h1>' + chapter_title + '</h1>' + c1
            C[x].add_item(default_css)
            # self.writeEpubPoint(chapterid)
            epub.write_epub(ApiConstants.save_epub_path(self.bookName), book)
            # downloadedList.append(chapterid)
            x += 1

        else:
            print("全本小说已经下载完成")
if __name__ == '__main__':
    pass
    