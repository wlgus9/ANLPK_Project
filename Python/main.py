import pandas as pd
import Python.word_extract as word_extract

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
news_data = pd.read_csv("Python/preprocessed_data_0222.csv", encoding='cp949')
train_data = news_data.copy()
print(train_data.isnull().sum())
# 결측치 제거
train_data = train_data.drop(['url'], axis=1)
train_data.dropna(inplace=True)

# 카테고리('사회', '정치', '국제', '경제'), 기간 별 데이터 분할
# 사회
train_society_w1 = word_extract.split_data_catedate(train_data, '사회', 20220119, 20220125) # 1371
train_society_w2 = word_extract.split_data_catedate(train_data, '사회', 20220126, 20220201)
train_society_w3 = word_extract.split_data_catedate(train_data, '사회', 20220202, 20220208)
train_society_w4 = word_extract.split_data_catedate(train_data, '사회', 20220209, 20220216)


# len(train_society_w1)

# soynlp로 명사 추출
soynouns_society_w1 = word_extract.extract_nouns_soy(train_society_w1) # soynlp로 추출한 단어 : 6292
# len(soynouns_society_w1)


# 추출한 명사 사전에 추가

## 숫자 제거
from konlpy.tag import Mecab
mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
soynouns_pos = {i : mecab.pos(noun) for i, noun in enumerate(soynouns_society_w1)}
soynouns_pos

# 숫자 태깅 찾아낼 단어인덱스 :  flag 딕셔너리 생성
# flag = 1 이면 숫자나 단위 있는 단어를 의미
soyflagdict = dict()
for i, pos_list in soynouns_pos.items():
    flag = 0
    for pos in pos_list:
        if pos[1] in ['SN', 'NNBC']:
            flag = 1
    soyflagdict[i] = flag

sum(soyflagdict.values()) # 숫자 및 단위 포함된 단어 : 550

# 숫자가 아닌 인덱스만 추출
nounind = [i for i, flag in soyflagdict.items() if flag == 0]


# 숫자 없는 데이터로 추가
soydictnouns=[soynouns_society_w1[i] for i in nounind] # 숫자 단위 제외 단어 : 5742
# len(soydictnouns)


# mecab으로 형태소 분석
mecabnouns_society_w1 = word_extract.extract_nouns_mecab(train_society_w1)
# len(mecabnouns_society_w1)

# 우선 첫주는 전체 mecab 단어목록과 비교해야 하니까 기사 단위로 분리x --> 전체 문서로 합쳐버리기
import itertools
mecabnouns_society_w1_all = set(list(itertools.chain(*mecabnouns_society_w1)))

# mecab 결과와 soynlp 결과 비교 후 신조어 후보 추출
new_word_temp = [new_word for new_word in soydictnouns if new_word not in mecabnouns_society_w1_all]
len(new_word_temp)

# 단어 후보 csv저장
df_new_word = pd.DataFrame(new_word_temp, columns=['new_word'])
df_new_word.to_csv('new_word_temp_society_week1_ver2.csv', index=False, encoding='utf-8-sig')


mecab.pos('기술적')