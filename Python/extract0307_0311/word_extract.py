from soynlp.noun import NewsNounExtractor
import itertools
from konlpy.tag import Mecab
import pandas as pd
from collections import Counter
import os
import numpy as np
import re



# 신조어 데이터프레임 / 불용어사전이름/ 오미크사전이름
def filter(new_word_df):
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
            ww_after = list(ww_df.loc[ww_df['before'] == new_word, 'after'])
            new_word_df.loc[new_word_df['new_word'] == new_word, 'new_word'] = ww_after[0]

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


### 카테고리 내 모든 주 신조어 추출 함수
def noun_extract_cate(cate, version):
    """
     카테고리에 따라 신조어 목록 csv 저장하는 함수
     cate : 카테고리(str), version : 전처리 버전 (int), filename : 저장 경로
     return : unique한 카테고리 목록 ( 신조어 추출에 사용 )
    """

    # 전처리 파일 전체 리스트 가져오기
    # path = 'extract0228_0304/Article_preprocessed'
    path = 'extract0307_0311/Article_preprocessed'  # 전처리 파일 저장 경로
    file_list = os.listdir(path)  # 전체 파일 목록

    ##### 카테고리 별 전처리 파일 목록에서 불러오기
    for file in file_list:  # 파일 목록 중에
        if (cate in file) & ("V" + str(version) in file):  # 카테고리 및 버전에 따른 파일 이름 선택해서 불러오기
            train_processed = pd.read_csv(str(path + '/' + file), encoding='utf-8-sig')

    # 고유명사 결측치 처리
    train_processed_c = train_processed.copy()
    train_processed_c['proper_nouns'] = train_processed_c['proper_nouns'].fillna('')
    ## 결측치 처리
    train_processed_c.dropna(inplace=True)

    # week를 리스트로 저장
    week_list = list(train_processed_c.week.unique())

    stop_pos = ['NNBC', 'NNG XSN', 'SN SL', 'EC', 'EF', 'VV', 'SY SN', 'JX', 'MAG', 'JKB']  # XSA- ~한, ETM- ~한,
    # JKB: ~으로
    # SY SN : 음수 제거
    # MAG : 게다가, 가득
    # JX : 까지

    df_new_words = pd.DataFrame(columns=['new_word', 'freq', 'ratio', 'category', 'week', 'date1', 'date2'])

    ## 주별로 신조어 추출 후 비교한 결과를 저장
    for week in week_list:
        new_word_list_update = list(df_new_words.new_word.unique())
        train_processed_week = train_processed_c[train_processed_c.week == week]

        # 주별 신조어 추출 : soynlp 추출 -> 한글자 제외, ~적, ~씨 불용어 처리 -> 빈도수 25% 이상 -> 사전 비교 추출
        df_new_words_temp = extract_nouns_list_week(train_processed_week, cate, week,
                                                           stop_pos=stop_pos,
                                                           comp_corpus=new_word_list_update)

        df_new_words = df_new_words.append(df_new_words_temp, ignore_index=True)
    df_new_words.dropna(inplace=True)
    # file_name = str('extract0307_0311/new_words/new_words_temp_' + cate + '_V5_1.csv')
    # df_new_words.to_csv(file_name, index=False, encoding='utf-8-sig')
    # print('extract0307_0311/new_words'+'에 '+cate+'_V5_1' + '신조어 파일 저장 완료')
    return df_new_words

####### 플라스크 신조어 추출 함수
def flask_extract_nouns_list_week(train_preprocessed, article_one, cate, week, stop_pos, comp_corpus):

    """
    지정한 카테고리와 주에 따라 신조어 목록 추출 후 딕셔너리 반환
    train_preprocessed : 전처리 한 데이터 프레임(dataframe), cate : 카테고리(str), week : 주(int),
    stop_pos : 명사 제외할 pos 태깅, comp_corpus : 비교할 이전 기간 신조어 목록
    return : dataframe
    """

    date1 = min(train_preprocessed.date)
    date2 = max(train_preprocessed.date)

    print('-------------------------------')
    print(cate, '분야')
    print('기간:', week, ',', date1, '~', date2)
    print('전체 기사 수 :', len(train_preprocessed))
    print('-------------------------------')

    # 반환할 딕셔너리 지정
    model_dict = {'cate': cate, 'week': week,
                'date1': date1, 'date2': date2,
                'cnt_all_articles': len(train_preprocessed)}

    # soynlp로 모든 단어 추출 -> 명사 가능성 적은 태깅 제거
    soy_words_dict = extract_words_soy(train_preprocessed)
    model_dict['modeling'] = {1: cate+' '+week+' 기사, '+'soynlp로 추출한 모든 명사 수 : ' + str(len(soy_words_dict))}
    soy_nouns_dict = del_words_in_stop_pos(soy_words_dict, stop_pos)
    model_dict['modeling'][2] = 'soynlp로 추출한 단어 중 ~씨, 단위명사, 명사파생 접미사, 숫자+영어, 연결어미, 종결어미, 동사, 기호+숫자, 일반부사, 부사격조사 포함' \
                                '단어 제거 후 단어 수: ' + str(len(soy_nouns_dict))

    # soynlp로 추출한 단어들 중 한글자는 제거
    soy_nouns_list = list(soy_nouns_dict.keys())
    soy_nouns_temp1 = [soy_noun for soy_noun in soy_nouns_list if len(soy_noun) >= 2]
    model_dict['modeling'][3] = 'soynlp로 추출한 단어 중 한글자 단어 제거 후 단어 수: ' + str(len(soy_nouns_temp1))
    print("=> soynlp 추출 명사 개수(한글자제거):", len(soy_nouns_temp1))

    # 사전 단어들과 비교
    no_dict_word_list = compare_dict_words(soy_nouns_temp1)
    model_dict['modeling'][4] = '사전 비교 후 사전에 있는 단어 제거 후 단어 수: ' + str(len(no_dict_word_list))
    print("=> 사전 비교 후 단어 수 :", len(no_dict_word_list))

    # 단어가 등장한 기사수, 전체 전처리 기사수 대비 단어수를 딕셔너리 형태로 저장
    soy_nouns_freq = {soy_noun: get_soy_freq(train_preprocessed, soy_noun) for soy_noun in no_dict_word_list}
    soy_nouns_freq_ratio = {soy_noun: {'freq': freq, 'ratio': freq / len(train_preprocessed)}
                          for soy_noun, freq in soy_nouns_freq.items()}

    # 단어 등장 기사 빈도수가 상위 25%인 것만 추출
    soy_freq_list = [freq_dict['freq'] for freq_dict in soy_nouns_freq_ratio.values()]
    new_word_dict = {soy_noun: freq_dict
                   for soy_noun, freq_dict in soy_nouns_freq_ratio.items()
                   if freq_dict['freq'] >= np.percentile(soy_freq_list, 75)}
    model_dict['modeling'][5] = '신조어 등장 기사수 기준 상위 25% 단어 추출 후 단어 수 : ' + str(len(new_word_dict))
    print("=> 빈도수 기준 추출 개수:", len(new_word_dict))

    # 전체 문서에서 빈도가 높은 고유명사와 빈도수 추출
    train_preprocessed_c = train_preprocessed.copy()
    train_preprocessed_c['proper_nouns'] = train_preprocessed_c['proper_nouns'].fillna('')
    proper_nouns_dict = get_proper_nouns_dict(train_preprocessed_c, min_freq=10)
    proper_nouns_freq = del_words_in_stop_pos(proper_nouns_dict, stop_pos)

    # 고유명사 사전 비교
    no_dict_proper_list = compare_dict_words(list(proper_nouns_freq.keys()))
    proper_nouns_result = {proper: proper_nouns_freq[proper] for proper in no_dict_proper_list}

    new_word_dict.update(proper_nouns_result)
    model_dict['modeling'][6] = '기사 본문의 홑따옴표 내 단어로 추출한 고유명사 추가 후 단어 수: ' + str(len(new_word_dict))


    # 이전의 신조어 후보와 비교 후 포함되지 않은것만 추출
    df_new_words = pd.DataFrame(columns=['new_word', 'freq', 'ratio', 'category', 'week', 'date1', 'date2'])

    for new_word, freq_dict in new_word_dict.items():
        # 이전 신조어 리스트와 비교 후 걸러내기
        if new_word not in comp_corpus:
        # 추출 단어 데이터 프레임화
            new_word_row = pd.Series([new_word, freq_dict['freq'], freq_dict['ratio'], cate, week, date1, date2],
                                 index=df_new_words.columns)
            df_new_words = df_new_words.append(new_word_row, ignore_index=True)

    model_dict['modeling'][7] = '이전 추출 신조어와 비교 후 해당 카테고리 및 기간의 총 신조어 수: ' + str(len(df_new_words))
    print('=> 이전 추출 신조어와 비교 후 단어 수:', len(df_new_words), '<<<<<<<<')

    # 불용어 제거
    df_new_word_filter = filter(df_new_words)
    model_dict['modeling'][8] = '불용어 처리 및 잘못 추출된 단어 적용 완료 후 단어 수 : ' + str(len(df_new_word_filter))
    print(cate + ' 불용어 처리 및 잘못 추출된 단어 적용 완료 후 단어 수 : ' + str(len(df_new_word_filter)))
    print('===> 이전 추출 신조어와 비교 후 해당 카테고리 및 기간의 총 신조어 수:', len(df_new_word_filter), '<<<<<<<<')
    print('--------------------------------------------------------')

    article_one.reset_index(drop=True, inplace=True)
    # 기사에 해당되는 단어만 추가
    new_word_list = []
    for word in list(df_new_word_filter['new_word']):
      if list(article_one['article'])[0].find(word) != -1:
          new_word_list.append(word)
    model_dict['modeling'][9] = '입력 기사에서 추출된 신조어 수 : ' + str(len(new_word_list))


    model_dict['new_words'] = new_word_list

    return model_dict



####### 카테고리 내 한주 신조어 추출 함수
def extract_nouns_list_week(train_preprocessed, cate, week, stop_pos, comp_corpus):
    """
    지정한 카테고리와 주에 따라 신조어 목록 추출
    train_preprocessed : 전처리 한 데이터 프레임(dataframe), cate : 카테고리(str), week : 주(int),
    stop_pos : 명사 제외할 pos 태깅, comp_corpus : 비교할 이전 기간 신조어 목록
    return : dataframe
    """
    date1 = min(train_preprocessed.date)
    date2 = max(train_preprocessed.date)

    print('-------------------------------')
    print(cate, '분야')
    print('기간:', week, ',', date1, '~', date2)
    print('전체 기사 수 :', len(train_preprocessed))
    print('-------------------------------')

    # soynlp로 모든 단어 추출 -> 명사 가능성 적은 태깅 제거
    soy_words_dict = extract_words_soy(train_preprocessed)
    soy_nouns_dict = del_words_in_stop_pos(soy_words_dict, stop_pos)

    # soynlp로 추출한 단어들 중 한글자는 제거
    soy_nouns_list = list(soy_nouns_dict.keys())
    soy_nouns_temp1 = [ soy_noun for soy_noun in soy_nouns_list if len(soy_noun)>1]
    print("=> soynlp 추출 명사 개수(한글자제거):", len(soy_nouns_temp1))

    # 사전 단어들과 비교
    no_dict_word_list = compare_dict_words(soy_nouns_temp1)
    print("=> 사전 비교 후 단어 수 :", len(no_dict_word_list))

    # 단어가 등장한 기사수, 전체 전처리 기사수 대비 단어수를 딕셔너리 형태로 저장
    soy_nouns_freq = { soy_noun : get_soy_freq(train_preprocessed, soy_noun) for soy_noun in no_dict_word_list}
    soy_nouns_freq_ratio = { soy_noun : {'freq' : freq, 'ratio' : freq/len(train_preprocessed)}
                                                               for soy_noun, freq in soy_nouns_freq.items()}


    # 단어 등장 기사 빈도수가 상위 25%인 것만 추출
    soy_freq_list = [freq_dict['freq'] for freq_dict in soy_nouns_freq_ratio.values()]
    new_word_dict = { soy_noun : freq_dict
                    for soy_noun, freq_dict in soy_nouns_freq_ratio.items()
                    if freq_dict['freq'] >= np.percentile(soy_freq_list, 75)}

    print("=> 빈도수 기준 추출 개수:", len(new_word_dict))

    # 전체 문서에서 빈도가 높은 고유명사와 빈도수 추출
    proper_nouns_dict = get_proper_nouns_dict(train_preprocessed, min_freq=10)
    proper_nouns_freq = del_words_in_stop_pos(proper_nouns_dict, stop_pos)

    # 고유명사 사전 비교
    no_dict_proper_list = compare_dict_words(list(proper_nouns_freq.keys()))
    proper_nouns_result = { proper : proper_nouns_freq[proper] for proper in no_dict_proper_list }
    print("=> 고유명사 사전 비교 후 단어 수 :", len(proper_nouns_result))

    new_word_dict.update(proper_nouns_result)

    # 이전의 신조어 후보와 비교 후 포함되지 않은것만 추출
    df_new_words = pd.DataFrame(columns=['new_word', 'freq', 'ratio', 'category', 'week', 'date1', 'date2'])

    for new_word, freq_dict in new_word_dict.items():
        # 이전 신조어 리스트와 비교 후 걸러내기
        if new_word not in comp_corpus:
            # 추출 단어 데이터 프레임화
            new_word_row = pd.Series([new_word, freq_dict['freq'], freq_dict['ratio'], cate, week, date1, date2], index=df_new_words.columns)
            df_new_words = df_new_words.append(new_word_row, ignore_index=True)

    print('=> 이전 추출 신조어와 비교 후 단어 수:', len(df_new_words), '<<<<<<<<')
    print('--------------------------------------------------------')

    return df_new_words


# 사전이랑 비교하는 함수
def compare_dict_words(nouns_list):
    # 비교사전 로드
    mecab_new_corpus = pd.read_csv("mecab_new_corpus.csv", encoding="cp949")
    new_word_list_pre = list(mecab_new_corpus.단어.unique())
    nia_dic = pd.read_csv('NIADic.csv', encoding='cp949')
    nia_term_list = list(nia_dic.term.unique())
    corpus_dic = list(set(new_word_list_pre + nia_term_list))

    # 사전 단어들과 비교
    corpus_dic_new = [x for x in corpus_dic if pd.isnull(x) == False]
    comp_str = ', '+', '.join(corpus_dic_new)
    no_dict_word_list = []
    for noun in nouns_list:
        if comp_str.find(', '+noun+', ') == -1: # 사전에 없으면
            no_dict_word_list.append(noun)  # 신조어 후보로 추가
    return no_dict_word_list




# soy가 나온 기사 수 구하기
def get_soy_freq(df, soy_noun):
    cnt = 0
    for article in df['article']:
        if article.find(soy_noun) != -1 :
            cnt += 1
    return cnt


# 매개변수 최종전처리된 데이터프레임 / 신조어후보군 데이터프레임의 단어리스트
### 신조어후보군 데이터프레임에서 컬렴명 다시 확인해서 수정할것! ###
def find_word_in_article(df, word_df, url):
  new_df = df[df['url'] == url].reset_index(drop=True)
  word_list = []
  for word in list(word_df['new_word']):
    if new_df['article'][0].find(word) != -1:
      word_list.append(word)

  return word_list



# soynlp로 단어  추출
def extract_words_soy(df):
  """
    soynlp로 명사 추출
    :param df: 전처리 완료된 기사 데이터 프레임
    :return: soynlp 명사 딕셔너리 => 명사 리스트로 수정
  """
  # stop_pos = ['NNBC', 'NNG XSN', 'SN SL', 'EC','EF']  # SN
  # EC:아닙니다, 그러다, 있었다
  # SN SL : 숫자+영어단위 1m

  article_list = list(df.article)
  noun_extractor = NewsNounExtractor(
    # max_left_length=10,
    # max_right_length=7,
    # predictor_fnames=None,
    verbose=False
  )
  nouns = noun_extractor.train_extract(article_list)
  # soy_nouns = list(nouns.keys())
  soy_nouns_freq = {noun[0] : noun[1].frequency for noun in nouns.items()}
  print('=> 전체 soynlp 추출 명사 수:', len(soy_nouns_freq))

  return soy_nouns_freq


# mecab으로 명사 추출
def extract_nouns_mecab(df):
  article_list = list(df.article)
  mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
  mecab_nouns_list = [mecab.nouns(article) for article in article_list]
  return mecab_nouns_list


# 고유명사-빈도수 딕셔너리
def get_proper_nouns_dict(df, min_freq):
  """
   고유명사-빈도수 딕셔너리 얻는 함수
   df : proper_nouns 컬럼 데이터프레임
   return 고유명사-빈도수 딕셔너리
  """
  prop_nouns_list = [prop_str.split(' ') for prop_str in df['proper_nouns'] if prop_str != '']
  proper_nouns_all = list(itertools.chain(*prop_nouns_list))
  proper_nouns_freq = Counter(proper_nouns_all)
  proper_nouns_dict = {proper: {'freq' : freq, 'ratio':freq/len(df)} for proper, freq in proper_nouns_freq.items() if freq >= min_freq}
  print("=> 고유명사 수 :", len(proper_nouns_dict))
  return proper_nouns_dict


# 명사를 mecab으로 태깅 후 stop_pos에 지정한 조건에 해당하는 단어 제거
def del_words_in_stop_pos(words_freq_dict, stop_pos=['NNBC', 'NNG XSN', 'SN SL', 'EC','EF','VV', 'SY SN', 'JX', 'MAG','JKB']):
  """
   input한 단어 목록을 mecab pos태깅하고, 태깅결과에 지정한 pos가 포함되면 제거하는 함수
   words_freq_dict : 단어-빈도 딕셔너리, stop_pos : 제거할 mecab pos 조건
   return 단어-빈도 딕셔너리
  """
  ## 단어들을 mecab pos 태깅
  mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
  words_pos_temp = {word: mecab.pos(word) for word in words_freq_dict.keys()}  # word가 키, mecab 태깅 결과가 값
  words_pos = {word : pos for word, pos in words_pos_temp.items() if ('씨', 'NNB') not in pos}
  print("=> 의존명사 ~'씨' 포함 단어 제거 후 단어 수 : ", len(words_pos))

  # 단어별로 모든 mecab pos결과 연결 (복합명사를 위해)
  pos_str_dict = dict()
  for word, pos_list in words_pos.items():
    pos_str = ""
    for p in pos_list:
      pos_str += ' ' + p[1]
    pos_str_dict[word] = pos_str

  # 단어인덱스 :  flag 딕셔너리 생성
  # flag = 1 이면 stop_pos 단어에 해당
  isstop_dict = dict()
  for word, pos_str in pos_str_dict.items():
    flag = 0
    for stop in stop_pos:
      if (pos_str.find(stop) != -1) or pos_str == ' SN' or pos_str == ' SY NNG':
        # 숫자만 있는 경우, -오프라인 이런 단어도 제거
        flag = 1
    isstop_dict[word] = flag
  print('stop_pos : 단위명사, 명사파생 접미사, 숫자+영어, 연결어미, 종결어미, 동사, 기호+숫자, 일반부사, 부사격조사')
  print('=> stop_pos 포함 명사 수:', sum(isstop_dict.values()))

  # stop_pos 없는 데이터로 추가
  nouns_result_list = {word : words_freq_dict[word] for word, flag in isstop_dict.items() if flag == 0}
  print('=> stop_pos 제거 후 추출 명사 수:', len(nouns_result_list))

  return nouns_result_list