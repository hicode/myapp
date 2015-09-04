# -*- coding: utf-8 -*- 
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')  
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
fp = open(r'D:\TDDOWNLOAD\pdfminer-20110515\pdfminer-20110515\samples\simple1.pdf', 'rb')
#用文件对象来创建一个pdf文档分析器
parser = PDFParser(fp)
# 创建一个  PDF 文档 
doc = PDFDocument()
# 连接分析器 与文档对象
parser.set_document(doc)
doc.set_parser(parser)
# 提供初始化密码
# 如果没有密码 就创建一个空的字符串
doc.initialize()
# 检测文档是否提供txt转换，不提供就忽略
if not doc.is_extractable:
    raise PDFTextExtractionNotAllowed
# 创建PDf 资源管理器 来管理共享资源
rsrcmgr = PDFResourceManager()
# 创建一个PDF设备对象
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
# 处理文档对象中每一页的内容
# doc.get_pages() 获取page列表
# 循环遍历列表，每次处理一个page的内容
# 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
for i, page in enumerate(doc.get_pages()):
    interpreter.process_page(page)
    layout = device.get_result()
    for x in layout:
        if(isinstance(x, LTTextBoxHorizontal)):
            if(len(x.text) > 100):
                string = x.text.replace('/n', ' ')
                print string
    print '/n/n/n/n' 
    