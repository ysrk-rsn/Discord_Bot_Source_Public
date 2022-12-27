import bs4
import requests

#yahoo のトップニュースの一覧を取得
def yahoo_news_checker():
    url = "https://news.yahoo.co.jp"
    html = requests.get(url) #domainからURLを取得する
    soup = bs4.BeautifulSoup(html.text, "lxml")
    elements = soup.select('main > div > div > section > div > div > div > ul > li > a') #「topicsListItem」のクラスであり、かつ"a"の中に入っているものをリストで取得する
    dict_list = []
    for elem in elements:
        news_dict = {'title': elem.getText(), 'link': elem.get('href')} #getText()でタイトル、get()でその属性をもつ要素の中身を取得する
        dict_list.append(news_dict)
    
    return dict_list
#Gigazineのトップニュースの一覧を取得する
def gigazine_news_checker():
    url = "https://gigazine.net"
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text, "lxml")
    elements = soup.select('h2 > a')
    dict_list = []
    for elem in elements:
        news_dict = {'title': elem.getText(), 'link': elem.get('href')} #getText()でタイトル、get()でその属性をもつ要素の中身を取得する
        dict_list.append(news_dict)
    
    return dict_list[:10]

#Gigazineのトップニュースの一覧を取得する
def lovelive_news_checker():
    url = "http://lovelivematocha.com/blog-category-3.html"
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text, "lxml")
    elements = soup.select('h2 > a')
    dict_list = []
    for elem in elements:
        news_dict = {'title': elem.getText(), 'link': elem.get('href')} #getText()でタイトル、get()でその属性をもつ要素の中身を取得する
        dict_list.append(news_dict)
    
    return dict_list[:10]

def vipper_news_checker():
    url = "http://blog.livedoor.jp/news23vip/"
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text, "lxml")
    elements = soup.select('h2 > a')
    dict_list = []
    for elem in elements:
        news_dict = {'title': elem.getText(), 'link': elem.get('href')} #getText()でタイトル、get()でその属性をもつ要素の中身を取得する
        dict_list.append(news_dict)
    
    return dict_list[:10]
    