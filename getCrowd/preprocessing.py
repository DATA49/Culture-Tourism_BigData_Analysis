import pandas as pd

# Load 관중 데이터
df = pd.read_csv("./crowd.csv")
df = df.rename(columns=df.loc[1])
df = df.drop(index=[0, 1])
# Load 코로나 확진자수
df_corona = pd.read_csv("./서울시코로나.csv")

# # # # Data Preprocessing # # # #
# 특정 경기장 데이터만 추출
df = df[df['경기장'] == '서울 잠실 야구장']

# 연도, 월, 일 병합
df["날짜"] = df["연도"] + "-" + df["월"] + "-" + df['일']

# 필요없는 컬럼 제거
df = df.loc[:, ['날짜', '요일', '경기장', '날씨', '평균기온', '관중수']]

# 날짜를 기준으로 확진자 수 넣기
df = pd.merge(df, df_corona, on='날짜', how='left')

# columnMD = df.columns[df.isnull().any()] # Missing value가 있는 컬럼 찾기
df = df.fillna(0)  # Nan to Zero
df = df.astype({'확진자 수': 'int'})  # Float to Int

# 날짜 오름차순
df = df.sort_values(by='날짜', ascending=True)
df.reset_index(drop=True, inplace=True)
print(df)

df.to_csv(f'crowd_with_corona.csv', encoding='utf-8-sig', index=None)  # 키워드별로 저장
