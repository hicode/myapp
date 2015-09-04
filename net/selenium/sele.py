from selenium import webdriver

browser = webdriver.Chrome()
browser.get("http://www.yahoo.com")
assert "Yahoo!" in browser.title

browser.close()


#coding=gbk
from selenium import selenium

def selenium_init(browser,url,para):
    sel = selenium('localhost', 4444, browser, url)
    sel.start()
    sel.open(para)
    sel.set_timeout(60000)
    sel.window_focus()
    sel.window_maximize()    
    return sel

def selenium_capture_screenshot(sel):
    sel.capture_screenshot("d:\\singlescreen.png")

def selenium_get_value(sel):
    innertext=sel.get_eval("this.browserbot.getCurrentWindow().document.getElementById('urla').innerHTML")
    url=sel.get_eval("this.browserbot.getCurrentWindow().document.getElementById('urla').href")
    print("The innerHTML is :"+innertext+"\n")
    print("The url is :"+url+"\n")

def selenium_capture_entire_page_screenshot(sel):
    sel.capture_entire_page_screenshot("d:\\entirepage.png", "background=#CCFFDD")

if __name__ =="__main__" :
    sel1=selenium_init('*firefox3','http://202.108.23.172','/m?word=mp3,http://www.slyizu.com/mymusic/VnV5WXtqXHxiV3ZrWnpnXXdrWHhrW3h9VnRkWXZtXHp1V3loWnlrXXZlMw$$.mp3,,[%B1%A7%BD%F4%C4%E3+%CF%F4%D1%C7%D0%F9]&ct=134217728&tn=baidusg,%B1%A7%BD%F4%C4%E3%20%20&si=%B1%A7%BD%F4%C4%E3;;%CF%F4%D1%C7%D0%F9;;0;;0&lm=16777216&sgid=1')
    selenium_get_value(sel1)
    selenium_capture_screenshot(sel1)
    sel1.stop()
    sel2=selenium_init('*firefox3','http://www.sina.com.cn','/')
    selenium_capture_entire_page_screenshot(sel2)
    sel2.stop()

