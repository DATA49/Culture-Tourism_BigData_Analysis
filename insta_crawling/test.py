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
insta_dict = {'id': [],  # UserId
              'date': [],  # 날짜
              'maintext': [],  # 본문
              'hashtag': []}  # 해시태그

# 첫 번째 게시물 클릭
first_post = driver.find_element_by_class_name('eLAPa')
first_post.click()

count_extract = 0
wish_num = 10  # 크롤링할 게시물 개수
start = time.time()

insta_obj_next_btn = 'a._65Bje.coreSpriteRightPaginationArrow'  # 다음 사진 버튼
insta_obj_user_id = 'h2._6lAjh'  # 유저 아이디
insta_obj_date = 'time.FH9sR.Nzb55'  # 날짜
insta_obj_main_text = 'div.C4VMK'  # 본문
insta_obj_main_tag = 'a.xil3i'  # 본문 해시태그
# insta_obj_comment_id = 'h2_6lAjh'  # 댓글 아이디
# insta_obj_comment_text = 'a.xil3i'

while True:
    try:
        if driver.find_element_by_css_selector(insta_obj_next_btn):
            # if count_extract % 20 == 0:
            print('{}번째 수집 중'.format(count_extract), time.time() - start, sep='\t')

            # id 정보 수집
            try:
                user_id = driver.find_element_by_css_selector(insta_obj_user_id).text
                insta_dict['id'].append(user_id)
            except:
                user_id = driver.find_element_by_css_selector('div.C4VMK').text.split()[0]
                insta_dict['id'].append(user_id)

            # 날짜정보 수집
            try:
                date_object = driver.find_element_by_css_selector(insta_obj_date)
                date = date_object.get_attribute("title")
                insta_dict['date'].append(date)
            except:
                date = None
                insta_dict['date'].append(date)

            # 본문
            try:
                raw_info = driver.find_element_by_css_selector(insta_obj_main_text).text.split()
                text = []
                for i in range(len(raw_info)):
                    # 첫번째 text는 아이디니까 제외
                    if i == 0:
                        pass
                    # 두번째부터 시작
                    else:
                        if '#' in raw_info[i]:
                            pass
                        else:
                            text.append(raw_info[i])
                clean_text = ' '.join(text)
                insta_dict['maintext'].append(clean_text)
            except:
                main_text = None
                insta_dict['maintext'].append(main_text)

            # hashtag 수집
            try:
                main_tags = driver.find_elements_by_css_selector(insta_obj_main_tag)
                hash_tag = []
                for i in range(len(main_tags)):
                    if main_tags[i].text == '':
                        pass
                    else:
                        # print(main_tags[i].text.replace("#", ""))
                        hash_tag.append(main_tags[i].text.replace("#", ""))

                insta_dict['hashtag'].append(hash_tag)
            except:
                hash_tag = None
                insta_dict['hashtag'].append(hash_tag)
            # # 댓글
            # ## 더보기 버튼 클릭
            # try:
            #     while True:
            #         try:
            #             more_btn = driver.find_element_by_css_selector(comment_more_btn)
            #             more_btn.click()
            #         except:
            #             break
            # except:
            #     print("----------------------fail to click more btn----------------------------")
            #     continue
            #
            # ## 댓글 데이터
            # try:
            #     comment_data = {}
            #     comment_ids_objects = driver.find_elements_by_css_selector(comment_ids_objects_css)
            #     comment_texts_objects = driver.find_elements_by_css_selector(comment_texts_objects_css)

            count_extract += 1
            if count_extract == wish_num:
                break

            driver.find_element_by_css_selector(insta_obj_next_btn).click()
            sleep(1.5)

        else:
            break

    except:
        driver.find_element_by_css_selector(insta_obj_next_btn).click()
        sleep(2)

test = pd.DataFrame.from_dict(insta_dict)
print(test.head)
test.to_csv('insta.csv', encoding='utf-8-sig')
