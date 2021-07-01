import csv
import pandas as pd
from selenium import webdriver
import time
from selenium.common.exceptions import WebDriverException

PATH = "../chromedriver.exe"  # 웹드라이버 실행
driver = webdriver.Chrome(PATH)  # 드라이버 경로 설정

url_list = []  # 초기 블로그 url을 저장하기 위한 변수
search_words = ['여행', '축제', '관람', '전시', '뮤지컬', '문화', '공연', '행사']  # 검색어
startDate = ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01', '2020-06-01', '2020-07-01',
             '2020-08-01', '2020-09-01', '2020-10-01', '2020-11-01', '2020-12-01']
endDate = ['2020-01-31', '2020-02-29', '2020-03-31', '2020-04-30', '2020-05-31', '2020-06-30', '2020-07-31',
           '2020-08-31', '2020-09-30', '2020-10-31', '2020-11-30', '2020-12-31']

# https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=PERIOD&orderBy=sim&startDate=2021-06-01&endDate=2021-06-30&keyword=%EC%97%AC%ED%96%89
# 검색어 내에서 월별로 28개씩 정확도 기준
for word in search_words:
    for sDate, eDate in zip(startDate, endDate):
        for page in range(1, 5):  # 1 ~ 4페이지까지의 블로그 내용을 읽어옴 28개
            url = f'https://section.blog.naver.com/Search/Post.nhn?pageNo={page}&rangeType=PERIOD&orderBy=sim&startDate={sDate}&endDate={eDate}&keyword={word}'  # url 값 설정
            driver.get(url)
            time.sleep(0.8)  # 오류 방지 sleep
            try:
                for j in range(1, 8):
                    links = driver.find_element_by_xpath(
                        f'/html/body/ui-view/div/main/div/div/section/div[2]/div[{j}]/div/div[1]/div[1]/a[1]')
                    link = links.get_attribute('href')
                    url_list.append((word, link))
            except WebDriverException as e:
                print(e)
                continue
        print(f"{word}의 {sDate}~{eDate} url 수집 끝")

# 게시글 링크들 저장
with open('test.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(url_list)

# 블로그 게시글 데이터를 저장할 Dictionary
blog_dict = {'title': [],  # 제목
             'date': [],  # 날짜
             'maintext': [],  # 본문
             # 'hashtag': []  # 해시태그
             }

keyword = '여행'
for word, url in url_list:  # 저장했던 블로그 하나씩 순회
    driver.get(url)
    driver.switch_to.frame('mainFrame')
    content_list = ""  # 블로그 content를 누적하기 위한 변수

    try:
        # 제목
        title_object = driver.find_element_by_css_selector('div.se-module.se-module-text.se-title-text').text
        print(title_object)
        blog_dict['title'].append(title_object)  # 제목

        # 날짜
        date_object = driver.find_element_by_css_selector('span.se_publishDate.pcol2').text
        blog_dict['date'].append(date_object)

        overlays = ".se-component.se-text.se-l-default"  # 내용 크롤링
        contents = driver.find_elements_by_css_selector(overlays)
        for content in contents:
            content_list = content_list + content.text  # 각 블로그의 내용을 변수에 누적함
        blog_dict['maintext'].append(content_list)
    except WebDriverException as e:
        print(e)
        continue

    if word != keyword:
        test = pd.DataFrame.from_dict(blog_dict)
        print(test.head)
        test.to_csv(f'{keyword}_blog_crawling.csv', encoding='utf-8-sig')  # 키워드별로 저장
        keyword = word
        blog_dict = {'title': [],  # 제목
                     'date': [],  # 날짜
                     'maintext': [],  # 본문
                     # 'hashtag': []  # 해시태그
                     }

test = pd.DataFrame.from_dict(blog_dict)
print(test.head)
test.to_csv(f'{search_words[-1]}_blog_crawling.csv', encoding='utf-8-sig')  # 키워드별로 저장
