from soynlp.noun import NewsNounExtractor
import itertools
from konlpy.tag import Mecab
import extract0228_0304.article_preprocess as preprocess
import pandas as pd
from collections import Counter


####### 신조어 추출 함수
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
  soy_words_freq = extract_words_freq_soy(train_preprocessed)
  soy_nouns_freq = del_words_in_stop_pos(soy_words_freq, stop_pos)

  # mecab으로 명사 추출
  mecab_nouns = extract_nouns_mecab(train_preprocessed)

  # mecab 단어 목록 기사 단위로 분리x --> 전체 문서로 합쳐버리기 -> 빈도 추출
  mecab_nouns_all = list(itertools.chain(*mecab_nouns))
  mecab_nouns_freq = Counter(mecab_nouns_all)
  print('=> mecab 추출 명사 수:', len(mecab_nouns_all))

  # mecab 결과와 soynlp 결과 비교 후 신조어 후보 추출
  new_word_dict = {soy_noun : freq for soy_noun, freq in soy_nouns_freq.items() if soy_noun not in mecab_nouns_freq.keys()}
  print("=> 신조어 후보 개수:", len(new_word_dict))

  # 전체 문서에서 빈도가 높은 고유명사와 빈도수 추출
  proper_nouns_dict = get_proper_nouns_dict(train_preprocessed, min_freq=10)
  proper_nouns_freq = del_words_in_stop_pos(proper_nouns_dict, stop_pos)
  new_word_dict.update(proper_nouns_freq)

  # 이전의 신조어 후보와 비교 후 포함되지 않은것만 추출
  df_new_words = pd.DataFrame(columns=['new_word', 'freq', 'category', 'week', 'date1', 'date2'])

  for new_word, freq in new_word_dict.items():
    # 이전 신조어 리스트와 비교 후 걸러내기
    if new_word not in comp_corpus:
      # 추출 단어 데이터 프레임화
      new_word_row = pd.Series([new_word, freq, cate, week, date1, date2], index=df_new_words.columns)
      df_new_words = df_new_words.append(new_word_row, ignore_index=True)
      # new_words_cnt += 1
  print('>>>>>>>> 최종 신조어 후보 수:', len(df_new_words), '<<<<<<<<')
  print('--------------------------------------------------------')

  return df_new_words


# soynlp로 명사 추출 -> 제거할 pos 지정해서 처리 후 반환
def extract_words_freq_soy(df):
  """
    soynlp로 명사 추출
    :param df: 전처리 완료된 기사 데이터 프레임
    :return: soynlp 명사 딕셔너리
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
  soy_nouns_freq = {noun[0] : noun[1].frequency for noun in nouns.items()} #list(nouns.keys())
  print('=> 1차 soynlp 추출 명사 수:', len(soy_nouns_freq))

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
  proper_nouns_dict = {proper: freq for proper, freq in proper_nouns_freq.items() if freq >= min_freq}
  print("=> 고유명사 수 :", len(proper_nouns_dict))
  return proper_nouns_dict


# 명사를 mecab으로 태깅 후 stop_pos에 지정한 조건에 해당하는 단어 제거
def del_words_in_stop_pos(words_freq_dict, stop_pos):
  """
   input한 단어 목록을 mecab pos태깅하고, 태깅결과에 지정한 pos가 포함되면 제거하는 함수
   words_freq_dict : 단어-빈도 딕셔너리, stop_pos : 제거할 mecab pos 조건
   return 단어-빈도 딕셔너리
  """
  ## 단어들을 mecab pos 태깅
  mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
  words_pos = {word: mecab.pos(word) for word in list(words_freq_dict.keys())}  # word가 키, mecab 태깅 결과가 값

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
      if pos_str.find(stop) != -1:
        flag = 1
    isstop_dict[word] = flag
  print('=> stop_pos 포함 명사 수:', sum(isstop_dict.values()))

  # stop_pos 없는 데이터로 추가
  nouns_result_dict = {word: words_freq_dict[word] for word, flag in isstop_dict.items() if flag == 0}
  print('=> stop_pos 제거 후 추출 명사 수:', len(nouns_result_dict))

  return nouns_result_dict