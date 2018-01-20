# Embedded file name: main.py
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
        soup = BeautifulSoup(page, 'lxml')
        table_node = soup.find('table', id='user')
        trs = table_node.find_all('tr')[1:]
        for tr in trs:
            tds = tr.find_all('td')
            ok = tds[3].text == u'\u662f'
            if not ok:
                course_info = {}
                course_info['name'] = tds[0].text + tds[2].text
                infos = filter(lambda x: x.isdigit() or x[0] == 'z', tds[4].find('img')['name'].split('#@'))
                course_info['params'] = infos
                course_infos.append(course_info)

    return course_infos


def get_list(session):
    url = 'http://zhjw.scu.edu.cn/jxpgXsAction.do?oper=listWj'
    page1 = session.get(url).content
    params = {'totalrows': '27',
     'page': '2',
     'pageSize': '20'}
    page2 = session.get('http://zhjw.scu.edu.cn/jxpgXsAction.do', params=params).text
    course_infos = []
    course_infos.extend(parse_course(page1))
    course_infos.extend(parse_course(page2))
    return course_infos


def parse_names(page):
    soup = BeautifulSoup(page, 'lxml')
    node_attrs = {'align': 'left',
     'border': '0',
     'cellspacing': '0',
     'cellpadding': '0'}
    table_node = soup.find_all('table', attrs=node_attrs)[1]
    trs = table_node.find_all('tr')[1::3]
    names = []
    for tr in trs:
        name = tr.find('input')['name']
        print name
        names.append(name)

    return names


def do_evaluate(session, parameters):
    form_data1 = {'wjbm': parameters[0],
     'bpr': parameters[1],
     'pgnr': parameters[2],
     'oper': 'wjShow'}
    url = 'http://zhjw.scu.edu.cn/jxpgXsAction.do'
    page = session.post(url, data=form_data1).text
    names = parse_names(page)
    form_data2 = {'wjbm': parameters[0],
     'bpr': parameters[1],
     'pgnr': parameters[2]}
    for name in names:
        print name
        form_data2[name] = '10_1'

    form_data2['zgpj'] = u'\u5f88\u68d2\u7684\u8001\u5e08!'.encode('gb2312')
    session.post('http://zhjw.scu.edu.cn/jxpgXsAction.do?oper=wjpg', form_data2)


if __name__ == '__main__':
    print u'\u5b66\u53f7:'
    zjh = raw_input()
    print u'\u5bc6\u7801:'
    mm = raw_input()
    form_data = {'zjh': zjh,
     'mm': mm}
    session = get_default_session()
    login(session, form_data)
    try:
        course_list = get_list(session)
        for i in course_list:
            do_evaluate(session, i['params'])
            print i['name'], u'------------------\u8bc4\u4ef7\u5b8c\u6210!!'

    except Exception as e:
        print u'\u51fa\u9519\u4e86'