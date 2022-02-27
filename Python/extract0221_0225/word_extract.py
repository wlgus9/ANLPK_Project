from soynlp.noun import NewsNounExtractor
import itertools
from konlpy.tag import Mecab
import Python.extract0221_0225.article_preprocess as preprocess
import pandas as pd

# text = "중앙대책본부회의에서는 다음과 같은 결과가 나왔다"

# tagged = tokenizer.pos(text)
# nouns = [s for s, t in tagged if t in ['NNG']]
# print(nouns)

####### 신조어 추출 함수
def extract_word_list(train_preprocessed, cate, date1, date2, stop_pos, comp_corpus):
  # # 입력 파일 전처리
  # train_preprocessed = preprocess_article(train_df, cate, date1, date2)

  print('-------------------------------')
  print(cate, '분야')
  print('기간:', date1, '~', date2)
  print('전체 기사 수 :', len(train_preprocessed))
  print('-------------------------------')

  # soynlp로 유의미한 명사 후보만 추출
  soy_nouns_result = extract_nouns_soy(train_preprocessed, stop_pos)

  # mecab으로 명사 추출
  mecab_nouns = extract_nouns_mecab(train_preprocessed)

  # mecab 단어 목록 기사 단위로 분리x --> 전체 문서로 합쳐버리기
  mecab_nouns_all = set(list(itertools.chain(*mecab_nouns)))
  print('=> mecab 추출 명사 수:', len(mecab_nouns_all))

  # mecab 결과와 soynlp 결과 비교 후 신조어 후보 추출
  new_word_list = [noun for noun in soy_nouns_result if noun not in mecab_nouns_all]
  print("=> 신조어 후보 개수:", len(new_word_list))

  # 고유명사 추가
  proper_nouns = preprocess.extract_proper_nouns(train_preprocessed['article'], 10)
  print("고유명사 수 :", len(proper_nouns))
  new_word_result = new_word_list + proper_nouns

  # 이전의 신조어 후보와 비교 후 포함되지 않은것만 추출
  new_words_cnt = 0
  df_new_words = pd.DataFrame(columns=['new_word', 'category', 'date1', 'date2'])

  for new_word in new_word_result:
    # 이전 신조어 리스트와 비교 후 걸러내기
    if new_word not in comp_corpus:
      # 추출 단어 데이터 프레임화
      new_word_row = pd.Series([new_word, cate, date1, date2], index=df_new_words.columns)
      df_new_words = df_new_words.append(new_word_row, ignore_index=True)
      new_words_cnt += 1
  print('최종 신조어 후보 :', new_words_cnt)

  print('--------------------------------------------------------')

  # 단어 후보 csv저장
  # df_new_words = pd.DataFrame(new_word_list, columns=['new_word'])
  # df_new_words.to_csv(file_path, index=False, encoding='utf-8-sig')

  return df_new_words


# soynlp로 명사 추출 -> 제거할 pos 지정해서 처리 후 반환
def extract_nouns_soy(df, stop_pos):
  """
    soynlp로 명사 추출
    :param df: 전처리 완료된 기사 데이터 프레임
    :return: soynlp 명사 리스트
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
  soy_nouns = list(nouns.keys())
  print('=> 1차 soynlp 추출 명사 수:', len(soy_nouns))

  ## soy추출 명사를 mecab으로 태깅 후 stop_pos에 지정한 조건에 해당하는 단어 제거
  mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
  soy_pos = {i: mecab.pos(noun) for i, noun in enumerate(soy_nouns)}

  # 단어별로 모든 mecab pos결과 연결(복합명사를 위해)
  pos_str_dict = {}
  for i, pos_list in soy_pos.items():
    pos_str = ""
    for p in pos_list:
      pos_str += ' ' + p[1]
    pos_str_dict[i] = pos_str

  # 단어인덱스 :  flag 딕셔너리 생성
  # flag = 1 이면 stop_pos 단어에 해당
  isstop_dict = dict()

  for i, pos_str in pos_str_dict.items():
    flag = 0
    for stop in stop_pos:
      if pos_str.find(stop) != -1:
        flag = 1
    isstop_dict[i] = flag

  print('=> stop_pos 포함 명사 수:', sum(isstop_dict.values()))  # 숫자 및 단위 포함된 단어 : 550

  # stop_pos 없는 인덱스만 추출
  # stop_ind = [i for i, flag in isstop_dict.items() if flag == 0]

  # stop_pos 없는 데이터로 추가
  soy_nouns_result = [soy_nouns[i] for i, flag in isstop_dict.items() if flag == 0]  # 숫자 단위 제외 단어 : 5742
  print('=> 최종 soynlp 추출 명사 수:', len(soy_nouns_result))

  return soy_nouns_result


# def add_mecab_dict(nouns_list):



# mecab으로 명사 추출
def extract_nouns_mecab(df):
  article_list = list(df.article)
  mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
  mecab_nouns_list = [mecab.nouns(article) for article in article_list]
  return mecab_nouns_list


