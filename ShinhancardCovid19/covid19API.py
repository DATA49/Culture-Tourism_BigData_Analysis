# coding: utf-8

# 필요한 라이브러리
import requests
from bs4 import BeautifulSoup as bs
from urllib import parse
import pandas as pd

serviceKey = 'privat key' # 공공데이터포털에서 발급받은 서비스키
params = {'ServiceKey':parse.unquote(serviceKey), # 서비스키(필수)
          'startCreateDt':20200101, # 데이터 생성일 시작범위(선택)
          'endCreateDt':20210601 # 데이터 생성일 종료범위(선택)
          }

# 서비스URL
url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?'
res = requests.get(url, params=params)
soup = bs(res.text, 'lxml')

# 결과 출력
print(soup)

# 필요한 데이터 추출
items = soup.find_all('item')
print(items)

for x in items:
    print(x)
    print()

# xml을 dictionary로 바꿔 리스트 원소로 추가
lst = []
for y in items:
    l = {}
    for x in y:
        l[x.name] = x.text
    lst.append(l)
print(lst)

# list를 dataframe으로 만들기
df = pd.DataFrame(lst)
print(df)

# 만든 dataframe csv파일로 저장
df.to_csv("C:/Users/samsung/Desktop/covid_open_api.csv")
