# -- coding: utf-8 --
import requests
from bs4 import BeautifulSoup
def login(session, form_data):
    login_url = 'http://zhjw.scu.edu.cn/loginAction.do'
    session.post(login_url, data=form_data)
    return session


def get_default_session():
    session = requests.session()
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
     'Referer': 'http://zhjw.scu.edu.cn/loginAction.do'}
    session.headers.update(header)
    return session

def parse_course(page):
    course_infos = []
    if page:
        soup = BeautifulSoup(page,"html.parser")
        node_attrs = {'class': 'titleTop2',
        'border': '0',
        'cellspacing': '0',
        'cellpadding': '0'}
        table_node = soup.find('table',attrs=node_attrs)
        trs = table_node.find_all('tr')[2:-9]
        for tr in trs:
            tds = tr.find_all('td')
            ok = tds[5].text.strip() == u'\u5fc5\u4fee'
            if  ok:
                course_info = {}
                course_info['name'] = tds[2].text.strip() #得到课程名
                print tds[2].text.strip()+':'
                txt=tds[6].find('p')
                infos =txt#得到课序号 教师序号之类的信息
                print txt.text.encode("GBK",'ignore')

def get_list(session):
    url = 'http://zhjw.scu.edu.cn/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=3180'
    page1 = session.get(url).content
    course_infos = []
    parse_course(page1)
if __name__ == '__main__':
    print u'\u5b66\u53f7:'
    zjh = raw_input()
    print u'\u5bc6\u7801:'
    mm = raw_input()
    form_data = {'zjh': zjh,
     'mm': mm}
    session = get_default_session()
    login(session, form_data)
    a=get_list(session)
