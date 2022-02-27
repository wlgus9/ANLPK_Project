import pandas as pd
from konlpy.tag import Mecab
import extract0228_0304.word_extract as word_extract
import extract0228_0304.article_preprocess as preprocess
import time
import datetime


### 우리 수집 데이터
# 데이터 로드
news_data = pd.read_csv("extract0228_0304/news_0118~0218.csv", encoding='utf-8')
train_data = news_data.copy()
print(train_data.isnull().sum())

# 2002-2019 신조어 목록 불러오기
mecab_new_corpus = pd.read_csv("extract0228_0304/mecab_new_corpus.csv",encoding="cp949")
mecab_new_corpus.head()
new_word_list_pre= list(mecab_new_corpus.단어.unique())

# 데이터 결측치 처리
train_data = preprocess.set_data(train_data)
cate_list = ['사회', '정치', '국제', '경제']
date_list = [[20220119, 20220125], [20220126, 20220201], [20220202, 20220208], [20220209, 20220216]]

stop_pos = ['NNBC', 'NNG XSN', 'SN SL', 'EC','EF']

##### 신조어 후보 추출
start = time.time()
for cate in cate_list:
    df_new_words = pd.DataFrame(columns=['new_word', 'freq', 'category', 'date1', 'date2'])
# cate = '사회'
    for date in date_list:
        # date = [20220119, 20220125]
        new_word_list_update = new_word_list_pre + list(df_new_words.new_word.unique())
        # 카테고리별 기간 별 추출
        train_cate_week = preprocess.split_data_catedate(train_data, cate, date[0], date[1])
        # 기사 본문 전처리
        train_processed = preprocess.preprocess_article(train_cate_week, cate, date[0], date[1])
        # 신조어 추출 후 데이터프레임 반환
        df_new_words_temp = word_extract.extract_word_list(train_processed, cate, date[0], date[1],
                                                           stop_pos=stop_pos,
                                                           comp_corpus=new_word_list_update)
        df_new_words = df_new_words.append(df_new_words_temp, ignore_index=True)
    filename = str('extract0228_0304/new_words/new_words_temp_0227_'+cate+'.csv')
    df_new_words.to_csv(filename, index=False, encoding='utf-8-sig')
sec = time.time()-start
times = str(datetime.timedelta(seconds=sec)).split(".")
times = times[0]
print(times)


'''## 수석님이 주신 데이터
news_data2_o = pd.read_csv("Python/articles.csv", encoding='utf-8')
news_data2 = news_data2_o[['article', 'category', 'date', 'source', 'title', 'url']]
train_data2 = news_data2.copy()

# 결측치 처리
train_data2.dropna(inplace=True)
print(train_data2.isnull().sum())
# len(news_data2), len(train_data2)

# category date 확인
sorted(train_data2.category.unique())
sorted(train_data2.date.unique().astype(int))

# cate date 지정
cate_list2 = sorted(train_data2.category.unique())
date_list2 = [[20220101, 20220107], [20220108, 20220114], [20220115, 20220121]]
df_new_words2 = pd.DataFrame(columns = ['new_word', 'category','date1','date2' ])

# path = './Article_Data/'
# file_list = os.listdir(path)
# file_list_py = [file for file in file_list if (file.endswith('.csv'))]  ## 파일명 끝이 .csv인 경우

# ent_df = preprocess.split_data_catedate(train_data2, 'entertainment', 20220115, 20220121)

new_words_cnt = 0
for cate in cate_list2:
    for date in date_list2:
        df_cate_week = preprocess.split_data_catedate(train_data2, cate, date[0], date[1])
        if len(df_cate_week) == 0 : # 분할한 데이터 프레임이 길이가 0인지 확인
            break
        else: # 비어있지 않은 데이터 프레임만 전처리 -> 명사 추출
            train_processed2 = preprocess_article(df_cate_week, cate, date[0], date[1])  # 일단 데이터 분할
            new_word_list = extract_word_list(train_processed2, cate, date[0], date[1])
            for new_word in new_word_list:
                new_word_row = pd.Series([new_word, cate, date[0], date[1]], index=df_new_words2.columns)
                df_new_words2 = df_new_words2.append(new_word_row, ignore_index=True)
            new_words_cnt += len(new_word_list)
print(new_words_cnt)
df_new_words2.to_csv('new_words_temp_0224_num_ver3.csv', index=False, encoding='utf-8-sig')

'''




a={'감사하다':1, '구체적':50, '1월31일':16}
mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
pos = {i: mecab.pos(noun) for i, noun in enumerate(list(a.keys()))}
pos = {noun: mecab.pos(noun) for noun in list(a.keys())}
pos
# 숫자 태깅 찾아낼 단어인덱스 :  flag 딕셔너리 생성
# flag = 1 이면 숫자나 단위 있는 단어를 의미

posdict = {}
for noun, pos_list in pos.items():
    pos_str = ""
    for p in pos_list:
        pos_str += ' ' + p[1]
    posdict[noun] = pos_str
posdict

isnum = dict()
stoppos = ['SN', 'NNBC','XSN']
for i, posstr in posdict.items():
    flag = 0
    for pos in stoppos:
        if posstr.find(pos) != -1:
            flag = 1
    isnum[i] = flag

print('=> 숫자 및 단위 포함 명사 수:', sum(isnum.values()))  # 숫자 및 단위 포함된 단어 : 550

# 숫자가 아닌 인덱스만 추출
# ind = [i for i, flag in isnum.items() if flag == 0]

# 숫자 없는 데이터로 추가
a_result = {noun: a[noun] for noun, flag in isnum.items() if flag == 0}  # 숫자 단위 제외 단어 : 5742
print(a_result)
# print('=> 최종 soynlp 추출 명사 수:', len(soy_nouns_result))

