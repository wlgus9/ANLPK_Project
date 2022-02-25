import pandas as pd
import Python.word_extract as word_extract
from konlpy.tag import Mecab
import itertools
import Python.article_preprocess as preprocess


'''##### mecab 사전에 2002-2019 신조어 추가

### 기존 사전 불러오기
with open("C:/mecab/user-dic/nnp.csv", 'r', encoding='utf-8') as f:
  file_data = f.readlines()
# file_data

### 2002-2019 신조어 불러오기
with open("Python/mecab_new_corpus.csv",'r',encoding="cp949") as f:
  new_corpus = f.readlines()
len(new_corpus)

### 신조어를 기존 사전 목록에 추가
for corpus in new_corpus:
  file_data.append(corpus)
len(file_data)

### 신조어 추가한 버전으로 사전 업데이트
with open("C:/mecab/user-dic/nnp.csv", 'w', encoding='utf-8') as f:
  for line in file_data:
    f.write(line)

# 추가한 것 확인
# with open("C:/mecab/user-dic/nnp.csv", 'r', encoding='utf-8') as f:
#   file_new = f.readlines()
# file_new

'''

# 데이터 로드
news_data = pd.read_csv("Python/news_0118~0218.csv", encoding='utf-8')
train_data = news_data.copy()
print(train_data.isnull().sum())

def preprocess_article(train_df, cate, date1, date2):
    file_name = str('Article_Data/preprocessed_article_' + cate + '_' + str(date1) + '_' + str(date2) + '.csv')

    # 데이터 결측치 처리
    train_data = preprocess.set_data(train_df)

    # 카테고리별 기간 별 추출
    train_cate_week = preprocess.split_data_catedate(train_data, cate, date1, date2)

    # 언론사 리스트 추출
    sources = preprocess.source_list(train_cate_week)

    # 기사 전처리 함수
    train_cate_week['article'] = train_cate_week['article'].apply(lambda x : preprocess.preprocessing_text(x, sources))

    # print(new_df['article'][2])

    # 전처리 파일 저장
    preprocess.save_data(train_cate_week, file_name)

    return train_cate_week



def extract_word_list(train_df, cate, date1, date2):

    # 입력 파일 전처리
    train_preprocessed = preprocess_article(train_df, cate, date1, date2)

    print('-------------------------------')
    print(cate, '분야')
    print('기간:', date1, '~', date2)
    print('전체 기사 수 :', len(train_preprocessed))
    print('-------------------------------')

    #########################################################
    ################# 고유명사 리스트 추출 ######################
    proper_nouns = preprocess.extract_proper_nouns(train_preprocessed['article'], 10)

    # soynlp로 추출
    soy_nouns = word_extract.extract_nouns_soy(train_preprocessed)
    print('=> 1차 soynlp 추출 명사 수:', len(soy_nouns))

    ## mecab으로 태깅 후 숫자 제거
    mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
    soy_pos = {i: mecab.pos(noun) for i, noun in enumerate(soy_nouns)}

    # 숫자 태깅 찾아낼 단어인덱스 :  flag 딕셔너리 생성
    # flag = 1 이면 숫자나 단위 있는 단어를 의미
    pos_str_dict = {}
    for i, pos_list in soy_pos.items():
        pos_str = ""
        for p in pos_list:
            pos_str += ' ' + p[1]
        pos_str_dict[i] = pos_str

    isstop_dict = dict()
    stop_pos = ['NNBC', 'NNG XSN', 'SN SL', 'EC'] # SN
    # EC:아닙니다, 그러다, 있었다
    # SN SL : 숫자+영어단위 1m
    for i, pos_str in pos_str_dict.items():
        flag = 0
        for stop in stop_pos:
            if pos_str.find(stop) != -1:
                flag = 1
        isstop_dict[i] = flag


    print('=> 숫자 및 단위 포함 명사 수:', sum(isstop_dict.values()))  # 숫자 및 단위 포함된 단어 : 550

    # 숫자가 아닌 인덱스만 추출
    notnum_ind = [i for i, flag in isstop_dict.items() if flag == 0]

    # 숫자 없는 데이터로 추가
    soy_nouns_result = [soy_nouns[i] for i in notnum_ind]  # 숫자 단위 제외 단어 : 5742
    print('=> 최종 soynlp 추출 명사 수:', len(soy_nouns_result))

    # mecab으로 형태소 분석
    mecab_nouns = word_extract.extract_nouns_mecab(train_preprocessed)

    # 우선 첫주는 전체 mecab 단어목록과 비교해야 하니까 기사 단위로 분리x --> 전체 문서로 합쳐버리기
    mecab_nouns_all = set(list(itertools.chain(*mecab_nouns)))
    print('=> mecab 추출 명사 수:', len(mecab_nouns_all))

    # mecab 결과와 soynlp 결과 비교 후 신조어 후보 추출
    new_word_list = [noun for noun in soy_nouns_result if noun not in mecab_nouns_all]
    print("=> 신조어 후보 개수:", len(new_word_list))
    print('--------------------------------------------------------')

    # 단어 후보 csv저장
    # df_new_words = pd.DataFrame(new_word_list, columns=['new_word'])
    # df_new_words.to_csv(file_path, index=False, encoding='utf-8-sig')

    return new_word_list

cate_list = ['사회', '정치', '국제', '경제']
date_list = [[20220119, 20220125], [20220126, 20220201], [20220202, 20220208], [20220209, 20220216]]
df_new_words = pd.DataFrame(columns = ['new_word', 'category','date1','date2' ])

new_words_cnt = 0
for cate in cate_list:
    for date in date_list:
        new_word_list = extract_word_list(train_data, cate, date[0], date[1])
        for new_word in new_word_list:
            new_word_row = pd.Series([new_word, cate, date[0], date[1]], index=df_new_words.columns)
            df_new_words = df_new_words.append(new_word_row, ignore_index=True)
        new_words_cnt += len(new_word_list)
print(new_words_cnt)
df_new_words.to_csv('new_words_temp_0224_num_ver3.csv', index=False, encoding='utf-8-sig')


'''
a=['감사하다','구체적', '1월31일']
mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
pos = {i: mecab.pos(noun) for i, noun in enumerate(a)}
pos
# 숫자 태깅 찾아낼 단어인덱스 :  flag 딕셔너리 생성
# flag = 1 이면 숫자나 단위 있는 단어를 의미

posdict = {}
for i, pos_list in pos.items():
    pos_str = ""
    for p in pos_list:
        pos_str += ' ' + p[1]
    posdict[i] = pos_str
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
ind = [i for i, flag in isnum.items() if flag == 0]

# 숫자 없는 데이터로 추가
a_result = [a[i] for i in ind]  # 숫자 단위 제외 단어 : 5742
print(a_result)
# print('=> 최종 soynlp 추출 명사 수:', len(soy_nouns_result))
'''