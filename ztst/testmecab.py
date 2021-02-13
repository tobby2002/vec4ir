# import MeCab as mecab
from konlpy.tag import Mecab
mecab = Mecab()

morphs_l = mecab.morphs('영등포구청역에 있는 맛집 좀 알려주세요.')
print('morphs_l')
morphs_txt = ' '.join(morphs_l)

print('morphs_txt')
print(morphs_txt)

nouns = mecab.nouns('영등포구청역에 있는 맛집 좀 알려주세요.')
print('nouns')
print(nouns)
# ['영등포구청역', '에', '있', '는', '맛집', '좀', '알려', '주', '세요', '.']