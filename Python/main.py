# from flask import Flask, render_template, request, jsonify, make_response
import pandas as pd
from konlpy.tag import Mecab
import extract0307_0311.word_extract as word_extract
# import extract0228_0304.article_preprocess as preprocess
import re
import os
import time
import datetime



if __name__ == '__main__':
    p_df = pd.read_csv("extract0307_0311/Article_preprocessed/preprocessed_사회_V5.csv")
    df = p_df.copy()
    df['proper_nouns'] = df['proper_nouns'].fillna('')
    df_society_week1 = df[df['week'] == '1주차']

    # 비교사전 로드
    mecab_new_corpus = pd.read_csv("mecab_new_corpus.csv", encoding="cp949")
    new_word_list_pre = list(mecab_new_corpus.단어.unique())
    nia_dic = pd.read_csv('NIADic.csv', encoding='cp949')
    nia_term_list = list(nia_dic.term.unique())
    comp_corpus = list(set(new_word_list_pre + nia_term_list))

    # 명사 제외할 pos 태깅
    stop_pos = ['NNBC', 'NNG XSN', 'SN SL', 'EC', 'EF', 'VV', 'SY SN', 'JX', 'MAG', 'JKB']  # XSA- ~한, ETM- ~한,
    # JKB: ~으로
    # SY SN : 음수 제거
    # MAG : 게다가, 가득
    # JX : 까지

    # 사회 1주차만 soynlp 추출 -> 한글자 제외, ~적, ~씨 불용어 처리 -> 빈도수 25% 이상 -> 사전 비교 추출
    df_new_words = word_extract.extract_nouns_list_week(df_society_week1,
                                                        '사회', '1주차', stop_pos=stop_pos, comp_corpus=comp_corpus)

    # 파일에 저장
    df_new_words.to_csv('extract0307_0311/new_words/new_words_사회_1주차_V6_2.csv', encoding='utf-8-sig', index=False)



     #### 카테고리 별 전체 신조어 CSV 파일 생성 작업 - 주별 비교
    # ### 전처리 파일 저장
    # start1 = time.time()
    # cate_list = ['IT', '경제', '국제', '문화', '보도자료', '사설칼럼', '사회', '스포츠', '연예', '정치']
    # # cate_list = preprocess.create_preprocessed_data("Article/", 4, path = "extract0228_0304/Article_preprocessed")
    # end1 = time.time()
    #
    #
    # ### 신조어 추출
    # start2 = time.time()
    # ## 카테고리 여러개 지정해서 여러개 신조어 파일 얻을때
    # for cate in cate_list:
    #     # file_name = str('extract0228_0304/new_words/new_words_temp_' + cate + '_V1_2_proper.csv')
    #     word_extract.noun_extract_func(cate, "5")
    #
    # ## 카테고리 하나 정해서 신조어 파일 하나 얻을때
    # # file_name = str('extract0228_0304/new_words/new_words_temp_0301_경제.csv')
    # # noun_extract_func("경제", "1_1", file_name=file_name)
    # end2 = time.time()
    #
    # sec = [end1 - start1, end2 - start2]
    # times = [str(datetime.timedelta(seconds=s)).split(".") for s in sec ]
    # times = [t[0] for t in times]
    # print(times) # 실행 시간 출력


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

