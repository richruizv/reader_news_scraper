import requests as req
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.sopitas.com/'

X_PATH_LINK_TO_ARTICLE = '//h2[@class="post-title-ticker"]//a/@href'
X_PATH_TITLE= '//div[contains(@class,"thumbnail")]/following-sibling::h1[1]/text()'
#X_PATH_SUMMARY = '//header[@class="col s12"]/h2/p/text()'
X_PATH_BODY = '//div[contains(@class,"content")]/p/text()'

def parse_link( link , today ):
    try:
        response = req.get(link)
        if response.status_code== 200:
            notice = response.content.decode('UTF-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(X_PATH_TITLE)[0]
                #summary = parsed.xpath(X_PATH_SUMMARY)[0]
                body = parsed.xpath(X_PATH_BODY)
            except IndexError:
                print(IndexError)
            
            with open('news/{}/{}.txt'.format(today,title),'w' , encoding = 'utf-8' ) as f:
                f.write(title)
                #f.write('\n\n')
                #f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')



        else:
            raise ValueError(response.status_code)
    except ValueError as e:
        print(e)

def parse_home():
    try:
        response = req.get(HOME_URL)
        if response.status_code== 200:
            home = response.content.decode('UTF-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(X_PATH_LINK_TO_ARTICLE)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir('news/'+today):
                os.mkdir('news/'+today)
            links_to_notices = list(set(links_to_notices))
            for link in links_to_notices:
                print(link)

                parse_link(link,today)
        else: 
            raise ValueError(response.status_code)
    except ValueError as e:
        print(e)

def run():
    parse_home()

if __name__ == "__main__":
    run()