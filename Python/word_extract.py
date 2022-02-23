from soynlp.noun import NewsNounExtractor

from konlpy.tag import Mecab
#
# text = "중앙대책본부회의에서는 다음과 같은 결과가 나왔다"

# tagged = tokenizer.pos(text)
# nouns = [s for s, t in tagged if t in ['NNG']]
# print(nouns)

# 기사 카테고리 기간 별로 분리
def split_data_catedate(df, cate, date1, date2):
  """
    카테고리와 지정 데이터로 데이터 분할
    cate : str, date1&2 : int
  """
  train_cate = df[df['category']==cate]
  train_catedate = train_cate.loc[(train_cate.date >= date1)&(train_cate.date <= date2)]
  # train_cate_n_date = train_cate.loc[(train_cate.date >= date1) & (train_cate.date <= date2)]['article']
  return train_catedate

# soynlp로 명사 추출
def extract_nouns_soy(df):
  """
    soynlp로 명사 추출
    :param data: 전처리 완료된 기사 데이터 프레임
    :return: soynlp 명사 리스트
  """
  article_list = list(df.article)
  noun_extractor = NewsNounExtractor(
    # max_left_length=10,
    # max_right_length=7,
    # predictor_fnames=None,
    # verbose=True
  )
  nouns = noun_extractor.train_extract(article_list)
  soy_nouns_list = list(nouns.keys())
  # soy_nouns_freq = {noun[0]: noun[1].frequency for noun in nouns.items()}
  return soy_nouns_list


# def add_mecab_dict(nouns_list):



# mecab으로 명사 추출
def extract_nouns_mecab(df):
  article_list = list(df.article)
  mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
  mecab_nouns_list = [mecab.nouns(article) for article in article_list]
  return mecab_nouns_list


