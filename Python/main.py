import pandas as pd
from konlpy.tag import Mecab
import extract0228_0304.word_extract as word_extract
import extract0228_0304.article_preprocess as preprocess
import time
import datetime
import os


# p_df = pd.read_csv("extract0228_0304/Article_preprocessed/전처리테스트V3.csv", encoding="utf-8")
# p_df.drop(['Unnamed: 0'], axis=1, inplace=True)
# p_df['proper_nouns'] = p_df['proper_nouns'].fillna('')
# p_df.dropna(inplace=True)
# p_df.groupby(['category']).count()
# preprocess.split_data_cate(p_df,3,"extract0228_0304/Article_preprocessed")



######## 전처리 데이터 준비 #######

def create_preprocessed_data(raw_data_file, ver, path = "extract0228_0304/Article_preprocessed"):
    """
     전처리 데이터를 생성하여 지정한 경로에 저장하는 함수
     raw_data_file : 원본데이터 파일, path : 저장 위치
    """
    # 데이터 로드
    df=pd.read_csv(raw_data_file, encoding='utf-8')

    # 결측치 처리
    df.dropna(inplace=True)

    # 카테고리 목록
    cate_list = preprocess.category_list(df)

    # 전처리 후 전처리 파일을 카테고리 별로 저장 (※기사별 고유명사 컬럼이 추가됌)
    train_preprocessed = preprocess.preprocess_article(df)

    # 전처리 된 데이터 카테고리 별로 분리하여 저장
    preprocess.split_data_cate(train_preprocessed,ver,path)


    # return cate_list


def noun_extract_func(cate, version):
    """
     카테고리에 따라 신조어 목록 csv 저장하는 함수
     cate : 카테고리(str), version : 전처리 버전 (int), filename : 저장 경로
     return : unique한 카테고리 목록 ( 신조어 추출에 사용 )
    """

    # 전처리 파일 전체 리스트 가져오기
    # path = 'extract0228_0304/Article_preprocessed'
    path = 'extract0228_0304/Article_preprocessed'  # 전처리 파일 저장 경로
    file_list = os.listdir(path)  # 전체 파일 목록

    ##### 카테고리 별 전처리 파일 목록에서 불러오기
    for file in file_list:  # 파일 목록 중에
        if (cate in file) & ("V" + str(version) in file):  # 카테고리 및 버전에 따른 파일 이름 선택해서 불러오기
            train_processed = pd.read_csv(str(path + '/' + file), encoding='utf-8-sig')
    ## 결측치 처리
    train_processed.dropna(inplace=True)

    # week를 리스트로 저장
    week_list = list(train_processed.week.unique())

    # 2002-2019 신조어 목록 불러오기
    mecab_new_corpus = pd.read_csv("mecab_new_corpus.csv",encoding="cp949")
    new_word_list_pre= list(mecab_new_corpus.단어.unique())

    # 명사 제외할 pos 태깅
    stop_pos = ['NNBC', 'NNG XSN', 'SN SL', 'EC','EF','VV', 'SY SN', 'JX', 'MAG','JKB'] # XSA- ~한, ETM- ~한,
    # JKB: ~으로
    # SY SN : 음수 제거
    # MAG : 게다가, 가득
    # JX : 까지

    df_new_words = pd.DataFrame(columns=['new_word', 'freq', 'category', 'week', 'date1', 'date2'])

    ## 주별로 신조어 추출 후 비교한 결과를 저장
    for week in week_list:
        new_word_list_update = new_word_list_pre + list(df_new_words.new_word.unique())
        train_processed_week = train_processed[train_processed.week == week]
        # 주별 신조어 추출
        df_new_words_temp = word_extract.extract_nouns_list_week(train_processed_week, cate, week,
                                                           stop_pos=stop_pos,
                                                           comp_corpus=new_word_list_update)

        df_new_words = df_new_words.append(df_new_words_temp, ignore_index=True)

    file_name = str('extract0228_0304/new_words/new_words_temp_' + cate + '_V'+str(version)+'.csv')
    df_new_words.to_csv(file_name, index=False, encoding='utf-8-sig')
    print('extract0228_0304/new_words'+'에 '+cate+'_V' + str(version)+' 신조어 파일 저장 완료')


if __name__ == '__main__':

    ### 전처리 파일 저장
    start1 = time.time()
    cate_list = ['사회', '정치', '경제', '국제', '문화', '연예', '스포츠', 'IT', '사설칼럼', '보도자료']
    # cate_list = \
    # create_preprocessed_data("Article/2022년1월다음뉴스_주차별정리.csv", "1_3")
    end1 = time.time()


    ### 신조어 추출
    start2 = time.time()
    ## 카테고리 여러개 지정해서 여러개 신조어 파일 얻을때
    for cate in cate_list:
        # file_name = str('extract0228_0304/new_words/new_words_temp_' + cate + '_V1_2_proper.csv')
        noun_extract_func(cate, "3")

    ## 카테고리 하나 정해서 신조어 파일 하나 얻을때
    # file_name = str('extract0228_0304/new_words/new_words_temp_0301_경제.csv')
    # noun_extract_func("경제", "1_1", file_name=file_name)
    end2 = time.time()

    sec = [end1 - start1, end2 - start2]
    times = [str(datetime.timedelta(seconds=s)).split(".") for s in sec ]
    times = [t[0] for t in times]
    print(times) # 실행 시간 출력

'''
import pandas as pd
import itertools
from collections import Counter
a=pd.read_csv('extract0228_0304/Article_preprocessed/preprocessed_경제_V1_1.csv', encoding='utf-8')
a['prop'] = a['proper_nouns']
a['prop'] = a['prop'].apply(lambda x : x.replace("[","").replace("]","").replace("'","").replace(",",""))

tt=a['prop']
tt = [t.split(' ')for t in tt if t != '']

proper_nouns_all = list(itertools.chain(*tt))

proper_nouns_freq = Counter(proper_nouns_all)
proper_nouns_dict = { proper : freq for proper, freq in proper_nouns_freq.items() if freq >= 10 }
print("=> 고유명사 수 :", len(proper_nouns_dict))

'''



'''
from konlpy.tag import Mecab
mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
a={'감사하다':1, '구체적':50, '14일경과':16}

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

'''

