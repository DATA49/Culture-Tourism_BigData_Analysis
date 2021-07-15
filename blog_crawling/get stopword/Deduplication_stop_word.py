import pandas as pd

df = pd.read_csv('stop_word_v1.csv', encoding='utf-8-sig')
df_stop_word = df['stop_word']
# print(df_stop_word.head())

stop_word_list = list(set(df_stop_word.values.tolist()))

# 불용어리스트 저장
df = pd.DataFrame({'stop_word': stop_word_list})
df.sort_values(by=['stop_word'], axis=0, inplace=True)
df.to_csv('stop_word_v2.csv', encoding='utf-8-sig', index=None)
