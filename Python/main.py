# from flask import Flask, render_template, request, jsonify, make_response
import pandas as pd
from konlpy.tag import Mecab
import extract0307_0311.word_extract as word_extract
# import extract0228_0304.article_preprocess as preprocess
import re
import os
import time
import datetime


# 신조어 데이터프레임 / 불용어사전이름/ 오미크사전이름
def filter(new_word_df, stop_words, wrong_words):
    sw_df = pd.read_csv('stop_words.csv',encoding='utf-8')
    ww_df = pd.read_csv('wrong_words.csv',encoding='utf-8')

    sw = list(sw_df['stop_word'])
    ww_before = list(ww_df['before'])

    for new_word in new_word_df['new_word']:
        # ~씨 제거
        if re.sub('[가-힣a-zA-Z ]+?씨', '', new_word) == '':
            new_word_df.drop(new_word_df[new_word_df['new_word'] == new_word].index, inplace=True)
        # 불용어 제거
        if new_word in sw:
            new_word_df.drop(new_word_df[new_word_df['new_word'] == new_word].index, inplace=True)
        # 오미크 처리
        if new_word in ww_before:
            new_word_df['new_word'][new_word_df['new_word'] == new_word] = ww_df['after'][ww_df['before'] == new_word]

    new_word_df.reset_index(drop=True, inplace=True)

    return new_word_df


# 신조어 데이터프레임(불용어, 오미크 처리 후) / 기존에 갖고 있던 신조어 사전이름
def final_dict(new_word_df, dic_df):
    # dic_df = pd.read_csv(dic_name + '.csv', encoding='cp949')
    duplicate_new_words = []
    for new_word in new_word_df['new_word']:
        if new_word in list(dic_df['new_word']):
            duplicate_new_words.append(new_word)

    for new_word in duplicate_new_words:
        dic_ratio = list(dic_df['ratio'].loc[dic_df['new_word'] == new_word])
        new_word_ratio = list(new_word_df['ratio'].loc[new_word_df['new_word'] == new_word])
        if dic_ratio < new_word_ratio:
            # 기존 단어 빈도수 < 새로 업데이트될 단어 빈도수
            dic_df[dic_df['new_word'] == new_word] = new_word_df[new_word_df['new_word'] == new_word]
        else :
            # 기존 단어 빈도수 > 새로 업데이트될 단어 빈도수
            new_word_df.drop(new_word_df[new_word_df['new_word'] == new_word].index, inplace=True)
    dic_df = pd.concat([dic_df, new_word_df])
    dic_df.reset_index(drop=True, inplace=True)

    return dic_df




if __name__ == '__main__':
    # p_df = pd.read_csv("extract0307_0311/Article_preprocessed/preprocessed_사회_V5.csv")
    # df = p_df.copy()
    # df['proper_nouns'] = df['proper_nouns'].fillna('')
    # df_society_week1 = df[df['week'] == '1주차']



    # 명사 제외할 pos 태깅
    # stop_pos = ['NNBC', 'NNG XSN', 'SN SL', 'EC', 'EF', 'VV', 'SY SN', 'JX', 'MAG', 'JKB']  # XSA- ~한, ETM- ~한,
    # JKB: ~으로
    # SY SN : 음수 제거
    # MAG : 게다가, 가득
    # JX : 까지



     #### 카테고리 별 전체 신조어 CSV 파일 생성 작업 - 주별 비교
    # ### 전처리 파일 저장
    start1 = time.time()
    cate_list = ['IT', '경제', '국제', '문화', '보도자료', '사설칼럼', '사회', '스포츠', '연예', '정치']
    # cate_list = ['사회', '스포츠', '연예', '정치']
    # # cate_list = preprocess.create_preprocessed_data("Article/", 4, path = "extract0228_0304/Article_preprocessed")
    end1 = time.time()
    #
    #
    ### 신조어 추출
    start2 = time.time()
    ## 카테고리 여러개 지정해서 여러개 신조어 파일 얻을때
    df_new_words_all = pd.DataFrame(columns=['new_word', 'freq', 'ratio', 'category', 'week', 'date1', 'date2'])
    for cate in cate_list:
        # file_name = str('extract0228_0304/new_words/new_words_temp_' + cate + '_V1_2_proper.csv')
        df_new_words_cate = word_extract.noun_extract_func(cate, "5")
        print(cate+' 전체 신조어 수 : '+str(len(df_new_words_cate)))
        # df_new_word_filter = filter(df_new_words_cate, 'stop_words', 'wrong_words')
        # print(cate + ' 불용어 처리 및 잘못 추출된 단어 적용 완료 후 단어 수 : ' + str(len(df_new_word_filter)))
        # df_new_words_all = final_dict(df_new_word_filter, df_new_words_all)
        df_new_words_cate.dropna(inplace=True)
        df_new_words_all = pd.concat([df_new_words_all, df_new_words_cate])
        df_new_words_all.reset_index(drop=True, inplace=True)
        print('현재 전체 신조어 추출 개수 : ' + str(len(df_new_words_all)))


    ## 카테고리 하나 정해서 신조어 파일 하나 얻을때
    # file_name = str('extract0228_0304/new_words/new_words_temp_0301_경제.csv')
    # noun_extract_func("경제", "1_1", file_name=file_name)
    # word_extract.noun_extract_func('사회', 5)
    end2 = time.time()

    sec = [end1 - start1, end2 - start2]
    times = [str(datetime.timedelta(seconds=s)).split(".") for s in sec ]
    times = [t[0] for t in times]
    print(times) # 실행 시간 출력

    df_new_words_all.to_csv('new_words_all_catogory_V2_1.csv', encoding='utf-8-sig', index=False)

'''
from konlpy.tag import Mecab
mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
a={'감사하다':1, '구체적':50, '14일경과':16}

pos = {i: mecab.pos(noun) for i, noun in enumerate(list(a.keys()))}
pos = {noun: mecab.pos(noun) for noun in list(a.keys())}
pos
# 숫자 태깅 찾아낼 단어인덱스 :  flag 딕셔너리 생성
# flag = 1 이면 숫자나 단위 있는 단어를 의미
{word : p for word, p in pos.items() if ('씨', 'NNB') in p}
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

'''
b = {'안녕' : {'freq': 1},
      '반가워' : {'freq': 4},
      '아아' : {'freq': 6},
      '코로나' : {'freq': 8}}
a = {'안녕' : {'freq': 1, 'ratio' : 0.001},
      '반가워' : {'freq': 4, 'ratio' : 0.004},
      '아아' : {'freq': 6, 'ratio' : 0.006},
      '코로나' : {'freq': 8, 'ratio' : 0.008}
}

{dict['ratio'] = dict['freq']/10 for dict in b.values()}
'''