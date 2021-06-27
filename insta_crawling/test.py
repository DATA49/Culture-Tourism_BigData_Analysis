import pandas as pd
from selenium import webdriver
import time as time
import getpass
from time import sleep

# 인스타그램 로그인 정보 받기
username = getpass.getpass("Input ID : ")  # User ID
password = getpass.getpass("Input PWD : ")  # User PWD

PATH = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=PATH)
driver.get('https://www.instagram.com/')
sleep(2)

elem = driver.find_element_by_name('username')
elem.send_keys(username)
elem = driver.find_element_by_name('password')
elem.send_keys(password)
sleep(1)

# 로그인 클릭 버튼
driver.find_element_by_css_selector('.sqdOP.L3NKy.y3zKF').click()
sleep(5)

hash_tag = '관광'
driver.get(f'https://www.instagram.com/explore/tags/{hash_tag}/')
sleep(10)

# 데이터를 저장할 Dictionary
insta_dict = {'id': [],
              'date': [],
              'hashtag': []}

# 첫 번째 게시물 클릭
first_post = driver.find_element_by_class_name('eLAPa')
first_post.click()

seq = 0
eon = 10  # 크롤링할 게시물 개수
start = time.time()
while True:
    try:
        if driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow'):
            if seq % 20 == 0:
                print('{}번째 수집 중'.format(seq), time.time() - start, sep='\t')

            # id 정보 수집
            try:
                info_id = driver.find_element_by_css_selector('h2._6lAjh').text
                insta_dict['id'].append(info_id)
            except:
                info_id = driver.find_element_by_css_selector('div.C4VMK').text.split()[0]
                insta_dict['id'].append(info_id)

            # 시간정보 수집
            time_raw = driver.find_element_by_css_selector('time.FH9sR.Nzb55')
            time_info = pd.to_datetime(time_raw.get_attribute('datetime')).normalize()
            insta_dict['date'].append(time_info)

            # hashtag 수집
            raw_tags = driver.find_elements_by_css_selector('a.xil3i')
            hash_tag = []
            for i in range(len(raw_tags)):
                if raw_tags[i].text == '':
                    pass
                else:
                    hash_tag.append(raw_tags[i].text)

            insta_dict['hashtag'].append(hash_tag)

            seq += 1

            if seq == eon:
                break

            driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow').click()
            sleep(1.5)

        else:
            break

    except:
        driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow').click()
        sleep(2)

test = pd.DataFrame.from_dict(insta_dict)
print(test)
