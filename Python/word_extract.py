from soynlp.noun import NewsNounExtractor

from konlpy.tag import Mecab
#
# text = "중앙대책본부회의에서는 다음과 같은 결과가 나왔다"

# tagged = tokenizer.pos(text)
# nouns = [s for s, t in tagged if t in ['NNG']]
# print(nouns)



# soynlp로 명사 추출
def extract_nouns_soy(df):
  """
    soynlp로 명사 추출
    :param df: 전처리 완료된 기사 데이터 프레임
    :return: soynlp 명사 리스트
  """
  article_list = list(df.article)
  noun_extractor = NewsNounExtractor(
    # max_left_length=10,
    # max_right_length=7,
    # predictor_fnames=None,
    verbose=False
  )
  nouns = noun_extractor.train_extract(article_list)
  soy_nouns = list(nouns.keys())
  # soy_nouns_freq = {noun[0]: noun[1].frequency for noun in nouns.items()}
  # print('=> 1차 soynlp 추출 명사 수:', len(soy_nouns))
  #
  # ## mecab으로 태깅 후 숫자 제거
  # mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
  # soy_pos = {i: mecab.pos(noun) for i, noun in enumerate(soy_nouns)}
  #
  # # 숫자 태깅 찾아낼 단어인덱스 :  flag 딕셔너리 생성
  # # flag = 1 이면 숫자나 단위 있는 단어를 의미
  # pos_str_dict = {}
  # for i, pos_list in soy_pos.items():
  #   pos_str = ""
  #   for p in pos_list:
  #     pos_str += ' ' + p[1]
  #   pos_str_dict[i] = pos_str
  #
  # isstop_dict = dict()
  # stop_pos = ['NNBC', 'NNG XSN']  # 숫자 : 'SN'
  # for i, pos_str in pos_str_dict.items():
  #   flag = 0
  #   for stop in stop_pos:
  #     if pos_str.find(stop) != -1:
  #       flag = 1
  #   isstop_dict[i] = flag
  #
  # print('=> 숫자 및 단위 포함 명사 수:', sum(isstop_dict.values()))  # 숫자 및 단위 포함된 단어 : 550
  #
  # # 숫자가 아닌 인덱스만 추출
  # notnum_ind = [i for i, flag in isstop_dict.items() if flag == 0]
  #
  # # 숫자 없는 데이터로 추가
  # soy_nouns_result = [soy_nouns[i] for i in notnum_ind]  # 숫자 단위 제외 단어 : 5742
  # print('=> 최종 soynlp 추출 명사 수:', len(soy_nouns_result))


  return soy_nouns


# def add_mecab_dict(nouns_list):



# mecab으로 명사 추출
def extract_nouns_mecab(df):
  article_list = list(df.article)
  mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
  mecab_nouns_list = [mecab.nouns(article) for article in article_list]
  return mecab_nouns_list


