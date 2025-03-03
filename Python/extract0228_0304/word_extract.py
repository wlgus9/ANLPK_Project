from soynlp.noun import NewsNounExtractor
import itertools
from konlpy.tag import Mecab
import pandas as pd
from collections import Counter
import os

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
        df_new_words_temp = extract_nouns_list_week(train_processed_week, cate, week,
                                                           stop_pos=stop_pos,
                                                           comp_corpus=new_word_list_update)

        df_new_words = df_new_words.append(df_new_words_temp, ignore_index=True)

    file_name = str('extract0228_0304/new_words/new_words_temp_' + cate + '_V'+str(version)+'.csv')
    df_new_words.to_csv(file_name, index=False, encoding='utf-8-sig')
    print('extract0228_0304/new_words'+'에 '+cate+'_V' + str(version)+' 신조어 파일 저장 완료')


####### 신조어 추출 함수
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
  soy_words_freq = extract_words_freq_soy(train_preprocessed)
  model_dict['modeling'] = {1 : 'soynlp로 추출한 모든 명사 수 : ' + str(len(soy_words_freq))}
  soy_nouns_freq = del_words_in_stop_pos(soy_words_freq, stop_pos)
  model_dict['modeling'][2] = 'soynlp로 추출한 단어 중 명사가 아닌 단어 제거 후 단어 수: ' + str(len(soy_nouns_freq))

  # mecab으로 명사 추출
  mecab_nouns = extract_nouns_mecab(train_preprocessed)

  # mecab 단어 목록 기사 단위로 분리x --> 전체 문서로 합쳐버리기 -> 빈도 추출
  mecab_nouns_all = list(itertools.chain(*mecab_nouns))
  mecab_nouns_freq = Counter(mecab_nouns_all)
  model_dict['modeling'][3] = 'mecab으로 추출한 모든 단어 중 명사 수: ' + str(len(mecab_nouns_freq))
  print('=> mecab 추출 명사 수:', len(mecab_nouns_freq))

  # mecab 결과와 soynlp 결과 비교 후 신조어 후보 추출
  new_word_list = [soy_noun for soy_noun in soy_nouns_freq.keys() if soy_noun not in mecab_nouns_freq.keys()]
  new_word_dict = { soy_noun : get_soy_freq(train_preprocessed, soy_noun) for soy_noun in new_word_list }
  model_dict['modeling'][4] = 'mecab 결과와 soynlp 결과 비교 후 신조어 후보 수: ' + str(len(new_word_dict))
  print("=> 신조어 후보 개수:", len(new_word_dict))

  # 전체 문서에서 빈도가 높은 고유명사와 빈도수 추출
  proper_nouns_dict = get_proper_nouns_dict(train_preprocessed, min_freq=10)
  proper_nouns_freq = del_words_in_stop_pos(proper_nouns_dict, stop_pos)
  model_dict['modeling'][5] = '기사 본문의 홑따옴표 내 단어로 추출한 고유명사 수: ' + str(len(proper_nouns_freq))
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
  model_dict['modeling'][6] = '이전 추출 신조어와 비교 후 해당 카테고리 및 기간의 총 신조어 수: ' + str(len(df_new_words))
  print('>>>>>>>> 최종 신조어 후보 수:', len(df_new_words), '<<<<<<<<')
  print('--------------------------------------------------------')

  # 기사에 해당되는 단어만 추가
  new_word_list = []
  for word in list(df_new_words['new_word']):
    if article_one['article'][0].find(word) != -1:
      new_word_list.append(word)


  model_dict['new_words'] = new_word_list

  return model_dict






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
  new_word_list = [soy_noun for soy_noun in soy_nouns_freq.keys() if soy_noun not in mecab_nouns_freq.keys()]
  new_word_dict = { soy_noun : get_soy_freq(train_preprocessed, soy_noun) for soy_noun in new_word_list }
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


# soy가 나온 기사 수 구하기
def get_soy_freq(train_preprocessed, soy_noun):
  cnt = 0
  for article in train_preprocessed['article']:
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
      if (pos_str.find(stop) != -1) or pos_str == ' SN': # 숫자만 있는 경우도 제거
        flag = 1
    isstop_dict[word] = flag
  print('=> stop_pos 포함 명사 수:', sum(isstop_dict.values()))

  # stop_pos 없는 데이터로 추가
  nouns_result_dict = {word: words_freq_dict[word] for word, flag in isstop_dict.items() if flag == 0}
  print('=> stop_pos 제거 후 추출 명사 수:', len(nouns_result_dict))

  return nouns_result_dict