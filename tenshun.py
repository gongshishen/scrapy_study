from bs4 import BeautifulSoup
import requests
# from lxml import

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36',

}
position = {}
urls = []
def job_parse(url):
    req = requests.get(url=url, headers=headers)
    response = req.content.decode('utf-8')
    #这里采用lxml无法解析页面
    soup = BeautifulSoup(response, 'html5lib')#这里需要使用utf-8解码, html5lib
    title = soup.select('table .h td')[0].string#这里是一个列表,需要索引
    position['title'] = title
    place = soup.select('table .c.bottomline td ')[0].text
    position['place'] = place
    category = soup.select('table .c.bottomline td ')[1].text
    position['category'] = category
    nums = soup.select('table .c.bottomline td ')[2].text
    position['nums'] = nums
    duty = soup.select('table .squareli')[0].text
    position['duty'] = duty
    require = soup.select('table .squareli')[1].text
    position['require'] = require
    return  position

def main_url(url):
    domin = 'https://hr.tencent.com/'
    req = requests.get(url=url, headers=headers)
    response = req.content.decode('utf-8')
    soup = BeautifulSoup(response, 'html5lib')
    for i in range(10):
        url_all = soup.select('table a')[i].attrs['href']
        urls.append(domin + url_all)
    return urls

def spider():
    base_url = 'https://hr.tencent.com/position.php?keywords=Python&lid=0&tid=0&start={}#a'
    for i in range(1, 54):
        url = base_url.format(i)
        detail_urls = main_url(url)
        for i in urls:
            job_parse(i)
            with open('job.txt', 'a', encoding='utf-8') as jobfile:
                jobfile.write(str(position))
                jobfile.write('\n')



if __name__ == '__main__':
    spider()
