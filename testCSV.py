import requests
from bs4 import BeautifulSoup
import csv
import pprint

BASE_URL = 'http://www.pythonscraping.com'


def create_list_from_table(table_tag):

    # CSV 파일로 만들기 위해서 2중 리스트 생성
    gifts = []

    # 헤더에 해당하는 1번째 로우 작성
    headers = []
    headers_tag = table_tag.find('tr')
    for th_tag in headers_tag.find_all('th'):
        headers.append(th_tag.text.strip())
    gifts.append(headers)

    #print(gifts)

    # 선물 레코드 작성
    for tr_tag in table_tag.find_all('tr'):
        gift = []
        idx = 0;
        for td_tag in tr_tag.find_all('td'):
            idx+=1;
            if td_tag.text.strip() != '':
                # 좌우 공백을 제거하고 텍스트 속에 \n문자를 공백으로 변경
                if(idx==2):
                    gift.append(td_tag.text[0:6].strip().replace('\n', ' '))
                else:
                    gift.append(td_tag.text.strip().replace('\n', ' '))
            else:
                gift.append(BASE_URL + td_tag.find('img').get('src')[2:])

        if not gift:
            continue

        gifts.append(gift)
    pprint.pprint(gifts)

    return gifts


def create_csv_file(lol, filename):
    # 이중 리스트의 내용을 CSV 파일로 저장
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for l in lol:
            writer.writerow(l)


def main():
    res = requests.get(BASE_URL + '/pages/page3.html')
    soup = BeautifulSoup(res.text, 'lxml')

    table_tag = soup.find(id='giftList')

    #print(table_tag)
    gifts = create_list_from_table(table_tag)
    create_csv_file(gifts, 'gifts.csv')

    print('finished job!')


if __name__ == '__main__' :
    main()
