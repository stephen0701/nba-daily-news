import requests
from bs4 import BeautifulSoup

def get_nba_headline(url):
    resp = requests.get(url)
    if resp.status_code is 200:
        resp.encoding = "utf-8"

        soup = BeautifulSoup(resp.text, "html.parser")
        news = soup.select("#news_body")
        headlines = news[0].find_all('h3')
        highlights = news[0].find_all('p')

        result = list()
        for headline in headlines:
            result.append(headline.text)
        return result
    else:
        print("Unable to crawl the website.")
        return None
    
def get_latest_news(date):

    nba_lines = get_nba_headline("https://nba.udn.com/nba/index")
    
    all_lines = "你好!歡迎收聽{}年{}月{}日NBA即時新聞!\n".format(date[:4], date[4:6], date[6:8])
    for idx, line in enumerate(nba_lines):
        all_lines += "第{}則新聞:{}\n".format(idx+1, line)
    return all_lines