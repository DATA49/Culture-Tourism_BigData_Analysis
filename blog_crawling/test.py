from selenium import webdriver
from konlpy.tag import Okt
from nltk import Text
from matplotlib import font_manager, rc
from wordcloud import WordCloud

import matplotlib.pyplot as plt
import time

path = "chromedriver.exe"  # 웹드라이버 실행

driver = webdriver.Chrome(path)  # 드라이버 경로 설정
url_list = []  # 블로그 url을 저장하기 위한 변수
content_list = ""  # 블로그 content를 누적하기 위한 변수
text = "관광"  # 검색어

for i in range(1, 3):  # 1~2페이지까지의 블로그 내용을 읽어옴
    url = 'https://section.blog.naver.com/Search/Post.nhn?pageNo=' + str(
        i) + '&rangeType=ALL&orderBy=sim&keyword=' + text  # url 값 설정
    driver.get(url)
    time.sleep(0.5)  # 오류 방지 sleep

    for j in range(1, 3):
        titles = driver.find_element_by_xpath(
            '/html/body/ui-view/div/main/div/div/section/div[2]/div[' + str(j) + ']/div/div[1]/div[1]/a[1]')
        title = titles.get_attribute('href')
        url_list.append(title)

print("url 수집 끝, 해당 url 데이터 크롤링")

for url in url_list:  # 저장했던 블로그 하나씩 순회
    driver.get(url)

    driver.switch_to.frame('mainFrame')
    overlays = ".se-component.se-text.se-l-default"  # 내용 크롤링
    contents = driver.find_elements_by_css_selector(overlays)

    for content in contents:
        content_list = content_list + content.text  # 각 블로그의 내용을 변수에 누적함

# 트위터에서 만든 소셜 분석을 위한 형태소 분석기 Okt 사용
okt = Okt()
myList = okt.pos(content_list, norm=True, stem=True)  # 모든 형태소 추출
myList_filter = [x for x, y in myList if y in ['Noun']]

Okt = Text(myList_filter, name="Okt")

# 그래프에서 한글이 출력이 안되는 문제 해결 (ㅁㅁㅁ 처럼 출력됨)
font_location = "c:/Windows/Fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_location).get_name()
rc('font', family=font_name)

# 그래프 x, y 라벨 설정
plt.xlabel("명사")
plt.ylabel("빈도")

# 그래프에서 x, y 값을 설정
wordInfo = dict()
for tags, counts in Okt.vocab().most_common(50):
    if (len(str(tags)) > 1):
        wordInfo[tags] = counts

values = sorted(wordInfo.values(), reverse=True)
keys = sorted(wordInfo, key=wordInfo.get, reverse=True)

# 그래프 값 설정
plt.bar(range(len(wordInfo)), values, align='center')
plt.xticks(range(len(wordInfo)), list(keys), rotation='70')
plt.show()

# wordCloud 출력
wc = WordCloud(width=1000, height=600, background_color="white", font_path=font_location, max_words=50)
plt.imshow(wc.generate_from_frequencies(Okt.vocab()))
plt.axis("off")
plt.show()