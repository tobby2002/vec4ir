import MeCab as mecab
mecab = mecab.MeCab()

mecab.morphs('영등포구청역에 있는 맛집 좀 알려주세요.')
# ['영등포구청역', '에', '있', '는', '맛집', '좀', '알려', '주', '세요', '.']