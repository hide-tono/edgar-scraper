from urllib.request import urlopen

import re
from bs4 import BeautifulSoup


def lambda_handler(event, context):
    list_html = urlopen("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&owner=exclude&count=40&hidefilings=0")
    list_bs = BeautifulSoup(list_html)
    interactive_link = []
    for child in list_bs.find_all('a', {'id': 'interactiveDataBtn'}):
        interactive_link.append(child.attrs['href'])
    detail_html = urlopen('https://www.sec.gov' + interactive_link[0])
    detail_bs = BeautifulSoup(detail_html)
    js = detail_bs.find('script', {'language': 'javascript'})
    matcher = re.compile('/Archives/edgar/data/.*.htm')
    link_list = matcher.findall(js.string)

    target = detail_bs.findAll('a', {'class': 'xbrlviewer'}, text=re.compile(r'.*CONSOLIDATED.*'))
    target_idx = [i.attrs['href'][-3] for i in target]

    for i in target_idx:
        data_html = urlopen('https://www.sec.gov' + link_list[int(i) - 1])
        data_trs = BeautifulSoup(data_html).find('table', {'class': 'report'}).findAll('tr')
        data = [{tr.find('a').text: tr.findAll('td').text} for tr in data_trs]
        print(data)
        break

    return target_idx
    # xlsx_link = detail_bs.find('a', href=re.compile('.*.xlsx')).attrs['href']
    # xlsx = urlopen('https://www.sec.gov' + xlsx_link)
    # return xlsx


if __name__ == '__main__':
    print(lambda_handler('', ''))
