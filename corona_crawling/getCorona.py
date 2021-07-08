import requests
import datetime
import pandas as pd

searchStartDate = '2020.01.01'
searchEndDate = '2021.07.08'

# 서울시 코로나 확진자
ROOT_URL = "https://www.seoul.go.kr/coronaV/searchCoronaDayStatus.do?"


def makeCSV(date, decide):
    df = pd.DataFrame(data=list(zip(date, decide)), columns=['날짜', '확진자 수'])
    df['날짜'] = pd.to_datetime(df['날짜'])
    print(df)
    df.to_csv(f'서울시코로나.csv', encoding='utf-8-sig', index=None)  # 키워드별로 저장


def getData():
    REQ_URL = ROOT_URL + 'sdate=' + searchStartDate + '&edate=' + searchEndDate
    # print(REQ_URL)
    response = requests.get(REQ_URL)
    if response.status_code == 200:
        text = response.json()
        # print(text)
        date = []
        decide = []
        for eachDay in text['rVal']:
            eachDate = (datetime.datetime.strptime(eachDay['C_DATE2'], '%Y.%m.%d') - datetime.timedelta(days=1)).date()
            eachGap = eachDay['GAP']
            # print(f'날짜: {eachDate} 확진자 수: {eachGap}')
            date.append(eachDate)
            decide.append(eachGap)
        makeCSV(date, decide)


def main():
    getData()


if __name__ == '__main__':
    main()
