import requests
from bs4 import BeautifulSoup
import os

login = 'your_login' # Write here your login on litres
password = 'your_pass' # Write here your password on litres


base_url = 'https://listen.litres.ru'
data = {'pre_action':'login','login':login,'pwd':password}
s = requests.Session()
s.get('https://listen.litres.ru/pages/login/')
s.post("https://listen.litres.ru/pages/ajax_empty2/",data=data)


def my_session():
    global s
    s.close()
    s.get('https://listen.litres.ru/pages/login/')
    s.post("https://listen.litres.ru/pages/ajax_empty2/", data=data)
    
def download(url,ndir):
    file = url.split('/')[-1]
    r = s.head(base_url+ url)
    if r.headers['Content-Type'] != 'audio/mpeg, audio/mpeg':
        er = s.get(base_url + url).text
        if er.find('Войдите в свой профиль') != -1:
            print('Войдите в свой профиль')
            my_session()
            download(url, ndir)
        if er.find('Невозможно') != -1: print('Нет доступа к книге')
        return False # 'Content-Type': 'audio/mpeg, audio/mpeg'

    r = s.get(base_url+ url).content
    with open(ndir+'//'+file, 'wb') as f:
        f.write(r)
    print('downloded '+ ndir+'//'+file)
    return True

def parse_book(url):
    ndir = url.replace('/','_')
    if os.path.isdir(ndir): return None
    os.mkdir(ndir)
    r = s.get(base_url+ url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = str(soup).split('''audioData = [''')[-1].split('];')[0].replace('\n','').replace('\t','')
    for link in links.split(','):
        if link[:6] == '  mp3:':
            d = download(link.split(' mp3:')[1][1:-3],ndir)
            if not d: break


def main(catalogue):
    '''
    catalogue : Here I put second part url of catalogues what I want to download 
    '''
    boks_links =[]
    for i in range(1,10):
        if i == 1:
            url = catalogue+'?gu_ajax=true&lite=1'
        else:
            url = catalogue+'page-'+str(i)+'/?gu_ajax=true&lite=1'
        r = s.get(base_url+url)
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.find_all('a',class_="art__name__href")
        if len(links) == 0: return boks_links
        for link in  links:
            boks_links.append(link.get('href'))
    return boks_links


# Put in main() second part of URL
if __name__ == '__main__':
    books_list = main('/knigi-fentezi/boevoe/')
    for book in books_list:
        parse_book(book)
    print('End parser!')
