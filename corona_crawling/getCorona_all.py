import pandas as pd
import requests
import json
import xmltodict
import datetime
from bs4 import BeautifulSoup

ServiceKey = 'inputKey'
pageNo = '1'
numOfRows = '10'
startCreateDt = '20200101'  # 검색할 생성일 범위의 시작
endCreateDt = '20210707'  # 검색할 생성일 범위의 종료

# 전국 코로나 확진자
ROOT_URL = "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?"


def makeCSV(date, decide):
    df = pd.DataFrame(data=list(zip(date, decide)), columns=['날짜', '확진자 수'])
    df['날짜'] = pd.to_datetime(df['날짜'])
    print(df)
    df.to_csv(f'전국코로나.csv', encoding='utf-8-sig', index=None)  # 키워드별로 저장


def getData():
    REQ_URL = ROOT_URL + 'serviceKey=' + ServiceKey + '&pageNo=' + pageNo + '&numOfRows' + numOfRows + '&startCreateDt=' + startCreateDt + '&endCreateDt=' + endCreateDt
    # print(REQ_URL)
    response = requests.get(REQ_URL)
    if response.status_code == 200:
        xmlString = response.text
        jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)
        jsonString = jsonString.replace('resultCode', '결과코드').replace('resultMsg', '결과메세지').replace('numOfRows',
                                                                                                    '한 페이지 결과 수').replace(
            'pageNo', '페이지 수').replace('totalCount', '전체 결과 수').replace('seq', '게시글번호(감염현황 고유값)').replace('stateDt',
                                                                                                          '기준일').replace(
            'stateTime', '기준시간').replace('decideCnt', '확진자 수').replace('clearCnt', '격리해제 수').replace('examCnt',
                                                                                                     '검사진행 수').replace(
            'deathCnt', '사망자 수').replace('careCnt', '치료중 환자 수').replace('resutlNegCnt', '결과 음성 수').replace('accExamCnt',
                                                                                                           '누적 검사 수').replace(
            'accExamCompCnt', '누적 검사 완료 수').replace('accDefRate', '누적 환진률').replace('createDt', '등록일시분초').replace(
            'updateDt', '수정일시분초')

        data_dict = json.loads(jsonString)
        # print(data_dict)

    date = []
    decide = []
    all_items = data_dict["response"]['body']['items']['item']
    for i in range(1, len(all_items)):
        decide_cnt = int(all_items[i - 1]['확진자 수']) - int(all_items[i]['확진자 수'])
        date.insert(0, all_items[i]['기준일'])
        decide.insert(0, decide_cnt)

    makeCSV(date, decide)


def main():
    getData()
    # test1()


if __name__ == '__main__':
    main()
