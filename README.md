# Download-aixdzs

## 爱下电子书APP爬虫

---
## 实现功能
<ul>
<li>支持多线程，默认为6线程</li>
<li>支持多进程，默认为6线程</li>
<li>多进程和多线程--mul命令切换</li>
<li>支持命令行操作</li>
<li>通过Bookid下载小说</li>
<li>通过书名下载小说</li>
<li>通过分类序号批量下载小说</li>
<li>通过本地保存的序号文本批量下载小说</li>
<li>支持epub格式下载</li>
<li>邮件推送下载信息，文本附件【暂时只在单线程版本支持】</li>
<li>请分别在189行和216行输入收件邮箱</li>
<li>已提供了一个临时Email用作发送文件，使用者可自行替换发送Email的账号和密码</li>
</ul>

### 环境需求

<ul>

<li>Python3.3或以上</li>

</ul>

### 依赖包

<ul>

<li>random</li>

<li>request</li>

<li>os</li>

<li>EbookLib</li>
  
<li>concurrent.futures</li>
  
<li>pyyaml</li>
  
<li>time</li>

<li>sys</li>

<li>rich</li>
  
<li>concurrent</li>
  
</ul>

### 安装依赖包

`pip install -r requirement.txt`

### 免责声明
<ul>
<li>本项目仅用作开源学习，请勿利用本项目进行任何盈利用途</li>
<ul>
